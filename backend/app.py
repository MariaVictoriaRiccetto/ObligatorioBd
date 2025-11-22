
from flask import Flask, jsonify, request
from flask_cors import CORS
from bd import get_connection
import mysql.connector
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
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
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
#----------------------------------------------PARTICIPANTES--------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------
@app.route('/participantes', methods=['GET'])#checked
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


    contraseña=data.get("contraseña")

    ci = data.get("ci")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO participante (ci, nombre, apellido, email)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (ci, nombre, apellido, email))
        conn.commit()

        cursor.execute("INSERT INTO login (correo, contraseña) "
                       "values (%s, %s) ", (email, contraseña))
        conn.commit()

        return jsonify({"status": "Participante creado correctamente"}), 201

    except mysql.connector.IntegrityError:
        return jsonify({"error": "La CI ya está registrada"}), 400

    finally:
        cursor.close()
        conn.close()

@app.route('/participantes/delete/<ci>', methods=['DELETE'])#checked
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

    cursor.close()
    conn.close()

    return jsonify({"status": "Participante modificado correctamente"})

# --------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------SALAS--------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

#cosas que faltan: Obtener todas las salas, obtener todas las reservas
@app.route('/sala/crear', methods=['POST'])#checked
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

@app.route("/salas/obtener", methods=["GET"])
def obtenerSalas():

    conn = get_connection()
    cursor=conn.cursor()
    cursor.execute("Select * From sala")
    salas = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"Estado": "Se obtuvieron todas las salas", "Datos": salas})




# --------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------RESERVAS--------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------


@app.route("/reservas/obtener", methods=["GET"])
def obtenerReservas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("Select * from reserva ")
    reservas=cursor.fetchall()


    cursor.close()
    conn.close()

    return jsonify({"Estado":"Reservas obtenidos con éxito ", "Data":reservas})

@app.route("/reservas/crear", methods=["POST"])  #Checked
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

@app.route("/reservas/eliminar/<int:id_reserva>", methods=["DELETE"]) #Checked
def eliminarReserva(id_reserva):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM reserva WHERE id_reserva=%s ", (id_reserva,) )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status": " Reserva eliminada correctamente "})

@app.route("/reservas/modificar/<int:id_reserva>", methods=["PUT"]) #checked
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
# --------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------SANCIONES--------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

#cada vez que el admin llama a este endpoint, el endpoint genera automaticamente las sanciones y las añade a las tablas, la logica de las sanciones
# es que si el usuario tiene la asistencia en 0~ no asistio, y la fecha actual es sueriro a a la fecha de la reserva, ala usuario se
# le sanciona, en el caso de que sea 0 pero no haya ocurrido , no pasa nada, o en el caso de que ocurrio y sea 1, tampoco el usuairo va a s er sancionado
@app.route("/sanciones/generar", methods=["POST"]) #checked
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
        WHERE r.fecha < CURRENT_DATE
          AND rp.asistencia = 0
          AND rp.ci_participante NOT IN (
                SELECT ci_participante
                FROM sancion_participante
                WHERE fecha_fin >= CURRENT_DATE
          );
    """)

    filas = cursor.rowcount  # cuantos sanciono

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "status": "ok",
        "sanciones_creadas": filas
    }), 200

@app.route("/sanciones/crear/<ci_participante>", methods=["POST"]) #checked
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

    return jsonify({"Estado":" La sancion fue removida con exite "})

#obtengo los datos de un participante en especifico, esto es para ver sus sanciones, el vencimiento de la misma, etc

@app.route("/sanciones/<ci_participante>", methods=["GET"])#checked
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

    cursor.execute("")

    cursor.close()
    conn.close()

    return jsonify({})
#Cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado)

@app.route("/reportes/reservas/asistencias-prof-alumnos",methods=["GET"])
def cantidadReservasAsistencias():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""select ppa.rol , count(rp.id_reserva) as total_reservas, sum(rp.asistencia= TRUE) as total_asistencias,sum(rp.asistencia= FALSE) as inasistencias
        from participante_programa_academico ppa
        join reserva_participante rp on ppa.ci_participante = rp.ci_participante -- FUNCIONA NO TOCAR
        group by ppa.rol """)

    resultado=cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"estado":"consulta realizada con exito", "data":resultado})

#• Cantidad de sanciones para profesores y alumnos (grado y posgrado)
@app.route("/reportes/sanciones/prof-alum", methods=["GET"])
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





# Levantar el server todo el codigo debe estar arriba para que le programa lo tome

if __name__ == '__main__':
    app.run(debug=True)
