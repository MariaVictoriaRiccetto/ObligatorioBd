
from flask import Flask, jsonify, request
from flask_cors import CORS
from bd import get_connection
import jwt
from datetime import datetime, timedelta, timezone
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import logging
from  funciones import  (
    esta_sancionado,
    sala_existe,
    turnos_validos,
    validar_capacidad,
    validar_tipo_sala,
    validar_limite_diario,
    validar_limite_semanal,
    hay_solapamiento,
    participante_existe
)

SECRET_KEY = "llaveNatu"

# ------------------------
# MIDDLEWARES
# ------------------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        try:
            token = auth_header.replace("Bearer ", "")
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        request.user = data
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token requerido"}), 401

        try:
            token = auth_header.replace("Bearer ", "")
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        if data.get("rol") != "admin":
            return jsonify({"error": "Acceso denegado: Se requiere rol ADMIN"}), 403

        request.user = data
        return f(*args, **kwargs)
    return wrapper

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
#testeo de la conexion

@app.route('/test-db')
def test_db():
    conn = get_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a MySQL"}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({"conexion_exitosa": True, "servidor_hora": str(resultado[0])})

# --------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------PARTICIPANTESSS--------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------
@app.route('/participantes', methods=['GET'])#checked
@admin_required
def listar_participantes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM participante;")
    participantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(participantes)


@app.route('/participantes/crear', methods=['POST'])#checked


def crear_participante():
    data = request.get_json()

    contraseña = data.get("contraseña")
    password_hash = generate_password_hash(contraseña) if contraseña else None

    ci = data.get("ci")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Insert participante
        query = """
        INSERT INTO participante (ci, nombre, apellido, email)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (ci, nombre, apellido, email))

        # Detecto dinámicamente el nombre de la columna de contraseña en la tabla login
        try:
            cursor.execute("SHOW COLUMNS FROM login")
            cols = cursor.fetchall()
            col_names = set()
            for c in cols:
                if isinstance(c, dict):
                    col_names.add(c.get('Field'))
                else:
                    col_names.add(c[0])
        except Exception as e:
            conn.rollback()
            return jsonify({"error": "Error interno comprobando esquema de login"}), 500

        # Detectar columna de password/contraseña automáticamente
        password_col = None
        # buscar coincidencias por substrings comunes (inglés/español)
        for col in col_names:
            lname = col.lower()
            if any(sub in lname for sub in ("pass", "pwd", "contr", "hash")):
                password_col = col
                break

        # Si no detectamos por substrings, intentar nombres comunes explícitos
        if password_col is None:
            candidates = ["password_hash", "password", "pwd_hash", "passwordHash", "contraseña"]
            for c in candidates:
                if c in col_names:
                    password_col = c
                    break
        if password_col is None:
            conn.rollback()
            return jsonify({"error": "Esquema inesperado: no se encontró columna de contraseña en tabla login"}), 500

        # Construyo la inserción sólo con las columnas que existan (rol puede no existir)
        lower_cols = {c.lower() for c in col_names}
        cols_to_insert = ['correo', password_col]
        params = [email, password_hash]
        if 'rol' in lower_cols:
            cols_to_insert.append('rol')
            params.append('estudiante')

        cols_quoted = ', '.join(f'`{c}`' for c in cols_to_insert)
        placeholders = ', '.join(['%s'] * len(params))
        insert_login_sql = f"INSERT INTO login ({cols_quoted}) VALUES ({placeholders})"
        try:
            cursor.execute(insert_login_sql, tuple(params))
        except Exception as e:
            conn.rollback()
            return jsonify({"error": "Error al crear credenciales de login"}), 500

        # Ambas inserciones OK -> confirmamos
        conn.commit()
        return jsonify({"status": "Participante creado correctamente"}), 201

    except mysql.connector.IntegrityError as ie:
        # Posible duplicado en participante (CI) u otra violación de integridad
        conn.rollback()
        return jsonify({"error": "La CI ya está registrada o violación de integridad"}), 400

    except Exception as e:
        # Error inesperado
        conn.rollback()
        return jsonify({"error": "Error interno al crear participante"}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/participantes/delete/<ci>', methods=['DELETE'])#checked
@admin_required

def eliminar_participante(ci):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM participante WHERE ci=%s;"
    cursor.execute(query, (ci,))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"status": "Participante eliminado correctamente"})


@app.route('/participantes/modificar/<int:ci>', methods=['PUT'])#checked
@admin_required

def modificar_participante(ci):
    data = request.get_json()

    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE participante
        SET nombre=%s, apellido=%s, email=%s
        WHERE ci=%s;
    """
    cursor.execute(query, (nombre, apellido, email, ci))  
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "No se encontró participante con ese CI"}), 404

    cursor.close()
    conn.close()
    return jsonify({"status": "Participante modificado correctamente"})

        
#----------------------------------------------SALAS--------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

#cosas que faltan: Obtener todas las salas, obtener todas las reservas
@app.route('/sala/crear', methods=['POST'])#checked
@admin_required

def crearSala():
    data=request.get_json()#transforma lo que le enviamos en un diccionario
    nombre_sala=data.get("nombre")
    id_edificio=data.get("id_edificio")
    capacidad=data.get("capacidad")
    tipo_sala=data.get("tipo")

    conn = get_connection()
    cursor = conn.cursor()

    query=(" INSERT into sala( nombre_sala, id_edificio, capacidad, tipo_sala) "
           "VALUES (%s,%s,%s,%s)")

    cursor.execute(query,(nombre_sala,id_edificio,capacidad,tipo_sala))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status": "Sala creada correctamente"})

@app.route('/sala/delete/<int:id_sala>',methods=['DELETE']) #checked
@admin_required

def eliminarSala(id_sala):

    conn=get_connection()
    cursor=conn.cursor()

    query="DELETE FROM sala WHERE id_sala = %s"

    cursor.execute(query,(id_sala,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status":"Sala borrada correctamente"})

@app.route('/sala/modificar/<id_sala>', methods=['PUT'])#checked
@admin_required

def modificarSala(id_sala):
    data=request.get_json()
    nombre=data.get("nombre")
    id_edificio=data.get("id_edificio")
    capacidad=data.get("capacidad")
    tipo=data.get("tipo")

    conn=get_connection()
    cursor=conn.cursor()

    query=("UPDATE sala "
           "SET nombre_sala=%s, id_edificio=%s, capacidad=%s, tipo_sala=%s "
           "WHERE id_sala=%s;")

    cursor.execute(query,(nombre,id_edificio,capacidad,tipo,id_sala))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"status": "Sala modificada correctamente"})

@app.route("/salas/obtenerAdmin", methods=["GET"])#checked
@admin_required

def obtenerSalas():

    conn = get_connection()
    cursor=conn.cursor()
    cursor.execute("Select * From sala")
    salas = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado": "Se obtuvieron todas las salas", "Datos": salas})

@app.route("/salas/obtenerTodos", methods=["GET"])
@login_required

def obtenerSalasId():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("Select s.id_sala, s.nombre_sala, e.nombre_edificio From sala s "
                   "join edificio e on s.id_edificio= e.id_edificio")
    salas = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado": "Se obtuvieron todas las salas", "Datos": salas})




# --------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------RESERVASS--------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------


@app.route("/reservas/obtener", methods=["GET"])
@admin_required

def obtenerReservas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("Select * from reserva ")
    reservas=cursor.fetchall()


    cursor.close()
    conn.close()

    return jsonify({"Estado":"Reservas obtenidos con éxito ", "Data":reservas})



@app.route("/reservas/obtener/usuario/<int:ci_participante>", methods=["GET"])
@login_required
def obtenerReservasCi(ci_participante):

    conn = get_connection()

    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)

    correo_token = request.user["correo"]

    cursor.execute("SELECT ci FROM participante WHERE email = %s", (correo_token,))
    row = cursor.fetchone()

    if not row:
        return jsonify({"error": "Usuario del token no encontrado"}), 404

    ci_token = row["ci"]

    if ci_token != ci_participante:
        return jsonify({"error": "Acceso denegado: no puede ver reservas de otros usuarios"}), 403

    cursor.execute("""
        SELECT rp.ci_participante, rp.fecha_solicitud_reserva, r.fecha, r.estado,
               s.nombre_sala, e.nombre_edificio
        FROM reserva_participante rp
        JOIN reserva r ON rp.id_reserva = r.id_reserva
        JOIN sala s ON r.id_sala = s.id_sala
        JOIN edificio e ON s.id_edificio = e.id_edificio
        WHERE rp.ci_participante = %s
    """, (ci_participante,))

    reservas = cursor.fetchall()

    cursor.close()
    conn.close()

    if not reservas:
        return jsonify({"mensaje": "El usuario no tiene reservas registradas"}), 200

    return jsonify({"reservas": reservas}), 200


@app.route("/reservas/obtener/activas", methods=["GET"]) #checked
@admin_required

def obtenerReservasActivas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("Select * from reserva where estado=%s", ("activa",))
    reservas=cursor.fetchall()


    cursor.close()
    conn.close()

    return jsonify({"Estado":"Reservas obtenidos con éxito ", "Data":reservas})

@app.route("/reservas/obtener/inactivas", methods=["GET"])#checked
@admin_required

def obtenerReservasInactiva():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("Select * from reserva where estado=%s",("cancelada",))
    reservas=cursor.fetchall()


    cursor.close()
    conn.close()

    return jsonify({"Estado":"Reservas obtenidos con éxito ", "Data":reservas})

@app.route("/reservas/crear", methods=["POST"])  #Checked
@login_required


def crearReservas():
    data = request.get_json()

    ci = data.get("ci")
    id_sala = data.get("id_sala")
    fecha = data.get("fecha")
    id_turnos = data.get("id_turnos")
    participantes = data.get("participantes")

    if not participante_existe(ci):
        return jsonify({"error":" el participante no existe "}), 400

    if esta_sancionado(ci):
        return jsonify({"error": "El usuario está sancionado y no puede reservar"}), 403

    if not sala_existe(id_sala):
        return jsonify({"error": "La sala no existe"}), 400

    if not turnos_validos(id_turnos):
        return jsonify({"error": "Uno o más turnos no existen"}), 400

    if not validar_capacidad(id_sala, participantes):
        return jsonify({"error": "Excede la capacidad de la sala"}), 400

    if not validar_tipo_sala(participantes, id_sala):
        return jsonify({"error": "Tipo de sala no permitido"}), 400

    if not validar_limite_diario(ci, fecha, id_turnos):
        return jsonify({"error": "Límite de 2 horas diarias excedido"}), 400

    if not validar_limite_semanal(ci, fecha):
        return jsonify({"error": "Límite de 3 reservas semanales excedido"}), 400

    if hay_solapamiento(id_sala, fecha, id_turnos):
        return jsonify({"error": "Ya existe una reserva en esos horarios"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    id_reservas_creadas = []
    for turno in id_turnos:
        cursor.execute(
            "INSERT INTO reserva (id_sala, fecha, id_turno, estado) "
            "VALUES (%s, %s, %s, 'activa')",
            (id_sala, fecha, turno)
        )
        conn.commit()

        id_reserva = cursor.lastrowid
        id_reservas_creadas.append(id_reserva)

        for ci_p in participantes:
            cursor.execute(
                "INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) "
                "VALUES (%s, %s, NOW(), FALSE)",
                (ci_p, id_reserva)
            )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "Reserva creada correctamente",
        "reservas": id_reservas_creadas
    }), 201

@app.route("/reservas/eliminar/<int:id_reserva>", methods=["PUT"]) #Checked
@login_required


def eliminarReserva(id_reserva):

    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("select estado from reserva where id_reserva=%s ",(id_reserva, ))
    resultado= cursor.fetchone()

    if not resultado:
        cursor.close()
        conn.close()
        return jsonify({"error": "La reserva no existe"}), 404

    if resultado[0] == 'finalizada':
        cursor.close()
        conn.close()
        return jsonify({"error": "No se puede cancelar una reserva finalizada"}), 400

    cursor.execute("Update reserva set estado=%s where id_reserva=%s ", ("cancelada",id_reserva) )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status": " Reserva eliminada correctamente "})

@app.route("/reservas/modificar/<int:id_reserva>", methods=["PUT"]) #checked
@login_required

def modificarReserva(id_reserva):
    data = request.get_json()

    ci = data.get("ci")
    id_sala = data.get("id_sala")
    fecha = data.get("fecha")
    id_turnos = data.get("id_turnos")
    participantes = data.get("participantes")

    # Validaciones
    if esta_sancionado(ci):
        return jsonify({"error": "El usuario está sancionado y no puede reservar"}), 403

    if not sala_existe(id_sala):
        return jsonify({"error": "La sala no existe"}), 400

    if not turnos_validos(id_turnos):
        return jsonify({"error": "Uno o más turnos no existen"}), 400

    if not validar_capacidad(id_sala, participantes):
        return jsonify({"error": "Excede la capacidad de la sala"}), 400

    if not validar_tipo_sala(participantes, id_sala):
        return jsonify({"error": "Tipo de sala no permitido"}), 400

    if not validar_limite_diario(ci, fecha, id_turnos):
        return jsonify({"error": "Límite de 2 horas diarias excedido"}), 400

    if not validar_limite_semanal(ci, fecha):
        return jsonify({"error": "Límite de 3 reservas semanales excedido"}), 400

    if hay_solapamiento(id_sala, fecha, id_turnos):
        return jsonify({"error": "Ya existe una reserva en esos horarios"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reserva WHERE id_reserva = %s", (id_reserva,))
    conn.commit()

    id_reservas_creadas = []
    for turno in id_turnos:
        cursor.execute(
            "INSERT INTO reserva (id_sala, fecha, id_turno, estado) "
            "VALUES (%s, %s, %s, 'activa')",
            (id_sala, fecha, turno)
        )
        conn.commit()

        nueva_id = cursor.lastrowid
        id_reservas_creadas.append(nueva_id)

        for ci_p in participantes:
            cursor.execute(
                "INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) "
                "VALUES (%s, %s, NOW(), FALSE)",
                (ci_p, nueva_id)
            )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "status": "Reserva modificada correctamente",
        "reservas": id_reservas_creadas
    }), 200

#metodo de admin para marcar asistencia
#este metodo es para marcar la asistencia a la reserva de las salitas, todo esto va de las manos de las sanciones
@app.route("/reservas/asistencia/<int:id_reserva>", methods=["PUT"]) #checked
@admin_required
def marcar_asistencia(id_reserva):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reserva_participante
        SET asistencia = 1
        WHERE id_reserva = %s
    """, (id_reserva,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "Asistencia registrada"}), 200

from datetime import datetime, date

@app.route("/reservas/finalizar_automatico", methods=["PUT"])
@admin_required
def finalizar_reservas_automatico():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    hora_actual = datetime.now().time()
    fecha_hoy = date.today()

    # Seleccionar reservas "activas" cuyo turno ya terminó
    cursor.execute("""
        SELECT r.id_reserva, r.fecha, t.hora_fin
        FROM reserva r
        JOIN turno t ON t.id_turno = r.id_turno
        WHERE r.estado = 'activa'
          AND (
                r.fecha < %s
                OR (r.fecha = %s AND t.hora_fin < %s)
              )
    """, (fecha_hoy, fecha_hoy, hora_actual))

    reservas_finalizables = cursor.fetchall()

    ids = [res["id_reserva"] for res in reservas_finalizables]

    if not ids:
        cursor.close()
        conn.close()
        return jsonify({"status": "No hay reservas para finalizar"}), 200

    # Actualizar estado a FINALIZADA
    cursor.execute("""
        UPDATE reserva
        SET estado = 'finalizada'
        WHERE id_reserva IN (%s)
    """ % ",".join(["%s"] * len(ids)), ids)

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "Reservas finalizadas correctamente",
        "reservas_finalizadas": ids
    }), 200

# --------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------SANCIONESS--------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

#cada vez que el admin llama a este endpoint, el endpoint genera automaticamente las sanciones y las añade a las tablas, la logica de las sanciones
# es que si el usuario tiene la asistencia en 0~ no asistio, y la fecha actual es sueriro a a la fecha de la reserva, ala usuario se
# le sanciona, en el caso de que sea 0 pero no haya ocurrido , no pasa nada, o en el caso de que ocurrio y sea 1, tampoco el usuairo va a s er sancionado
@app.route("/sanciones/generar", methods=["POST"])
@admin_required
def generar_sanciones():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
        SELECT rp.ci_participante,
               CURRENT_DATE,
               DATE_ADD(CURRENT_DATE, INTERVAL 2 MONTH)
        FROM reserva_participante rp
        JOIN reserva r ON r.id_reserva = rp.id_reserva
        WHERE r.estado = 'finalizada'
          AND rp.asistencia = 0
          AND rp.ci_participante NOT IN (
              SELECT ci_participante
              FROM sancion_participante
              WHERE fecha_fin >= CURRENT_DATE
          );
    """)

    sancionadas = cursor.rowcount
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "ok",
        "sanciones_creadas": sancionadas
    }), 200


@app.route("/sanciones/crear/<ci_participante>", methods=["POST"]) #checked
@admin_required
def sancionarAProposito(ci_participante):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
            SELECT 1 FROM sancion_participante
            WHERE ci_participante = %s AND fecha_fin >= CURRENT_DATE
        """, (ci_participante,))

    existe = cursor.fetchone()
    if existe:
        cursor.close()
        conn.close()
        return jsonify({"error": "El participante ya tiene una sanción activa"}), 400

    cursor.execute(" Insert into sancion_participante (ci_participante, fecha_inicio, fecha_fin) "
                   "values (%s, CURRENT_DATE, DATE_ADD(CURRENT_DATE, INTERVAL 2 MONTH)) ", (ci_participante,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "sancionado correctamente "})

#le paso la cedula del participante, chequeo si el participante existe o tiene sanciones, en el caos de que no exsite devuelve un mensaje, en el caso de que si exista su sancion la elimina
@app.route("/sanciones/eliminar/<ci_participante>",methods=["DELETE"])#checked
@admin_required
def eliminarSanciones(ci_participante):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("select ci_participante from sancion_participante "
                   "where ci_participante=%s", (ci_participante, ))
    existe=cursor.fetchone()

    if not existe:
        cursor.close()
        conn.close()
        return jsonify({"Estado":"El participante no existe o no tiene sanciones "})

    cursor.execute("Delete FROM sancion_participante where ci_participante=%s ",(ci_participante, ))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"Estado":" La sancion fue removida con éxito"})

#obtengo los datos de un participante en especifico, esto es para ver sus sanciones, el vencimiento de la misma, etc

@app.route("/sanciones/<ci_participante>", methods=["GET"])#checked
@admin_required
def listarSanciones(ci_participante):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "Select * "
        "from sancion_participante "
        "where ci_participante=%s",
        (ci_participante, )
    )
    sanciones = cursor.fetchall()

    cursor.close()
    conn.close()

    if not sanciones:
        return jsonify({"Estado": "El participante no tiene sanciones"})

    return jsonify({"Sanciones": sanciones})

#Este endpoint es para borrar las sanciones en automatico, lo que hace es chequear si la fecha de
# finalizacion de la sancion es mayor a la fecha actual, en el caso de que la fecha la supere, esa sancion sera removida
@app.route("/sanciones/limpiar", methods=["DELETE"])#checked
@admin_required
def limpiarSancionesVencidas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "Select ci_participante "
        "from sancion_participante "
        "where fecha_fin < CURRENT_DATE"
    )
    vencidas = cursor.fetchall()

    if not vencidas:
        cursor.close()
        conn.close()
        return jsonify({"Estado": "No hay sanciones vencidas para limpiar"})

    cursor.execute(
        "Delete from sancion_participante "
        "where fecha_fin < CURRENT_DATE"
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"Estado": "Sanciones vencidas eliminadas correctamente"})

#Este endpoint es para poder modificar las sanciones, lo que hace es permitirme modificar la fehca de incio y la fecha final de una sancion, la verdadera utilidad seria modificar la fecha final para poder extender una sancion
@app.route("/sanciones/modificar/<ci_participante>", methods=["PUT"])#checked
@admin_required
def modificarSancion(ci_participante):
    datos = request.json
    nueva_fecha_inicio = datos.get("fecha_inicio")
    nueva_fecha_fin = datos.get("fecha_fin")

    if not nueva_fecha_inicio or not nueva_fecha_fin:
        return jsonify({"error": "Faltan fechas para modificar la sanción"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "Select ci_participante "
        "from sancion_participante "
        "where ci_participante=%s",
        (ci_participante,)
    )
    existe = cursor.fetchone()

    if not existe:
        cursor.close()
        conn.close()
        return jsonify({"error": "El participante no tiene sanciones registradas"}), 404

    cursor.execute(
        "Update sancion_participante "
        "set fecha_inicio=%s, fecha_fin=%s "
        "where ci_participante=%s",
        (nueva_fecha_inicio, nueva_fecha_fin, ci_participante)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"estado": "Sanción modificada correctamente"})


#aca obtenemos todas las sanciones, mas los nombres de los participantes por un tema de practicidad, para que en el
# dia a dia cuadno un tenga que buscar las sanciones tenga una referencia mas clara que la cedula, debido a que es mas sencillo recordar
#nombres que numeros.

@app.route("/sanciones/obtener", methods=["get"])#checked
@admin_required
def listarObtener():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("select sp.ci_participante, p.nombre, p.apellido, sp.fecha_inicio, sp.fecha_fin From sancion_participante sp "
                   "join participante p on sp.ci_participante=p.ci")
    sanciones=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado ": "Consulta hecha con éxito", "datos ": sanciones})



# --------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------Sistema de reportes --------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

#EndPoint para obtener salas más reservadas
@app.route("/reportes/salasMaxReserva", methods=["GET"])
@admin_required
def obtenerMaxReserva():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""select s.nombre_sala, count(*) as cantidad_reservas
        from reserva r
        join sala s on r.id_sala = s.id_sala    
        group by s.nombre_sala
        order by cantidad_reservas desc;""")

    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"estado": "consulta realizada con exito", "data": resultado})

#Obtener turnos mas demandados
@app.route("/reportes/turnosMax", methods=["GET"])
@admin_required
def obtenerTurnosMasDemandados():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""select t.id_turno, count(*) as veces_reservado
        from reserva r
        join turno t on t.id_turno = r.id_turno 
        group by t.id_turno
        order by veces_reservado desc
        limit 1;""")

    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado": "Se realizo la consulta correctamente ", "Los turnos mas demandados son ": resultado})

@app.route("/reportes/sala/promedio", methods=["GET"])
@admin_required
def obtenerPromedioSala():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""select s.nombre_sala, ROUND(avg(pr.cantidad_participante),1) as promedio_participantes
        from sala s
        join reserva r on r.id_sala=s.id_sala
        left join (select id_reserva,count(ci_participante) as cantidad_participante                       
                   from reserva_participante
                   group by id_reserva)
        pr on pr.id_reserva=r.id_reserva -- Unimos cada reserva con la cantidad de participantes que tiene (por id_reserva)
        group by s.nombre_sala ;""")
    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado": "Se realizo la consulta correctamente ", "El promedio de la sala es  ": resultado})

@app.route("/reportes/reservas/facultad-carrera")
@admin_required
def obtenerCantidadReservasFacultadCarrera():
    conn = get_connection()
    cursor = conn.cursor()

    #Cantidad de reservas por carrera y facultad
    cursor.execute("""select f.nombre as facultad,
                   pa.nombre_programa as carrera,
                   count(distinct rp.id_reserva) as cantidad_reservas
            from reserva_participante rp
            join participante_programa_academico ppa
              on rp.ci_participante = ppa.ci_participante
            join programa_academico pa
              on ppa.id_programa_academico = pa.id_programa_academico
            join facultad f
              on pa.id_facultad = f.id_facultad
            group by f.nombre, pa.nombre_programa
            order by f.nombre, pa.nombre_programa;

                   """)

    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado": "Se realizo la consulta correctamente ", "El promedio de la sala es  ": resultado})

#Porcentaje de ocupación de salas por edificio
@app.route("/reportes/salas/porcentaje-ocupacion-edificio",methods=["GET"])
def porcentajeDeOcupacion():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""select s.nombre_sala, ROUND(avg(pr.cantidad_participante),1) as promedio_participantes
from sala s
join reserva r on r.id_sala=s.id_sala
left join (select id_reserva,count(ci_participante) as cantidad_participante                        -- FUNCIONA NO TOCAR
           from reserva_participante
           group by id_reserva)
pr on pr.id_reserva=r.id_reserva -- Unimos cada reserva con la cantidad de participantes que tiene (por id_reserva)
group by s.nombre_sala ;""")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "estado": "consulta realizada con exito",
        "data": resultado
    }), 200


#Cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado)

@app.route("/reportes/reservas/asistencias-prof-alumnos",methods=["GET"])
@admin_required
def cantidadReservasAsistencias():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            ppa.rol,
            COUNT(rp.id_reserva) AS total_reservas,
            SUM(rp.asistencia = TRUE) AS total_asistencias,
            SUM(rp.asistencia = FALSE) AS total_inasistencias
        FROM participante_programa_academico ppa
        JOIN reserva_participante rp 
            ON ppa.ci_participante = rp.ci_participante
        GROUP BY ppa.rol;
    """)

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        "estado": "consulta realizada con exito",
        "data": resultado
    }), 200


#• Cantidad de sanciones para profesores y alumnos (grado y posgrado)
@app.route("/reportes/sanciones/prof-alum", methods=["GET"])
@admin_required
def sancinesProfAlum():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT ppa.rol,
    COUNT(*) AS cantidad_sanciones
    FROM participante_programa_academico ppa
    JOIN sancion_participante sp 
    ON ppa.ci_participante = sp.ci_participante
    GROUP BY ppa.rol
    ORDER BY ppa.rol;
""")
    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado":"", "data":resultado})

#orcentaje de reservas efectivamente utilizadas vs. canceladas/no asistidas
@app.route("/reportes/reservas/efectivasNo", methods=["GET"])
@admin_required
def obtenerReservasEfectivas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""select ppa.rol  , count(rp.id_reserva) as total_reservas, round(avg(rp.asistencia= TRUE),1) as porcentaje_asistencias,round(avg(rp.asistencia= FALSE),1) as porcentaje_inasistencias
from participante_programa_academico ppa
join reserva_participante rp on ppa.ci_participante = rp.ci_participante -- FUNCIONA NO TOCAR
group by ppa.rol ;""")
    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado":"", "data":resultado})


#-- Participante con mas inasistencias (extra 1)
@app.route("/reportes/participante/masInasistencia", methods=["GET"])
@admin_required
def obtenerParticipanteMasInasistencia():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""select ppa.rol, rp.ci_participante, sum(rp.asistencia= FALSE) as inasistencias
    from participante_programa_academico ppa
    join reserva_participante rp on ppa.ci_participante = rp.ci_participante
    group by ppa.rol, rp.ci_participante
    order by inasistencias desc
    limit 1;""")

    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado":"", "data":resultado})


#-- Ranking top 3 de participantes con mas reservas activas (extra 2)
@app.route("/reportes/participante/reservaActiva", methods=["GET"])
@admin_required
def obtenerParticipantesMasReservasActivas():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""select rp.ci_participante,ppa.rol,COUNT(*) AS total_reservas
from reserva_participante rp
join participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
group by rp.ci_participante, ppa.rol
order by total_reservas DESC
limit 3;""")

    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado":"", "data":resultado})


#-- cantidad de salas por edificio (extra 3)


@app.route("/reportes/sala/cantidadXEdificio", methods=["GET"])
@admin_required
def obtenerCantidadSalaPorEdificio():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""select  e.nombre_edificio,COUNT(*) AS cantidad_salas
from sala s
join edificio e ON s.id_edificio = e.id_edificio
group by e.nombre_edificio;""")

    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado":"", "data":resultado})

# --------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------LOGINNNN --------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar usuario en tabla login
    cursor.execute("SELECT correo, contraseña FROM login WHERE correo = %s", (correo,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Validar contraseña
    if not check_password_hash(user["contraseña"], password):
        cursor.close()
        conn.close()
        return jsonify({"error": "Contraseña incorrecta"}), 401

    # Buscar CI en participante
    cursor.execute("SELECT ci FROM participante WHERE email = %s", (correo,))
    participante = cursor.fetchone()
    if not participante:
        cursor.close()
        conn.close()
        return jsonify({"error": "Participante no encontrado"}), 404

    ci = participante["ci"]

    # Buscar rol en participante_programa_academico
    cursor.execute("SELECT rol FROM participante_programa_academico WHERE ci_participante = %s", (ci,))
    programa = cursor.fetchone()
    rol = programa["rol"] if programa else "estudiante"

    # Generar token con rol correcto
    token = jwt.encode({
        "correo": correo,
        "rol": rol,
        "exp": datetime.now(timezone.utc) + timedelta(hours=12)
    }, SECRET_KEY, algorithm="HS256")

    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Login exitoso",
        "token": token,
        "rol": rol
    }), 200


@app.route("/auth/me", methods=["GET"])
@login_required
def auth_me():

    correo = request.user["correo"]
    rol = request.user["rol"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("SELECT ci, nombre, apellido FROM participante WHERE email = %s", (correo,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user_data:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "correo": correo,
        "rol": rol,
        "ci": user_data["ci"],
        "nombre": user_data["nombre"],
        "apellido": user_data["apellido"]
    }), 200










# Levantar el server todo el codigo debe estar arriba para que le programa lo tome

if __name__ == '__main__':
    app.run(debug=True)
