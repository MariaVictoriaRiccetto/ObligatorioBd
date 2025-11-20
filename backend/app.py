from flask import Flask, jsonify, request
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
    hay_solapamiento
)

app = Flask(__name__)


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

#Participantes ABM
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

#Salas ABM
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

#Reservas
@app.route("/reservas/crear", methods=["POST"])  #Checked
def crearReservas():
    data = request.get_json()

    ci = data.get("ci")
    id_sala = data.get("id_sala")
    fecha = data.get("fecha")
    id_turnos = data.get("id_turnos")
    participantes = data.get("participantes")

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

@app.route("/reservas/modificar/<int:id_reserva>", methods=["PUT"])
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

    # 1. Eliminar la reserva vieja (y sus participantes por cascada)
    cursor.execute("DELETE FROM reserva WHERE id_reserva = %s", (id_reserva,))
    conn.commit()

    # 2. Crear las nuevas reservas según turnos
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


# Levantar el server todo el codigo debe estar arriba para que le programa lo tome

if __name__ == '__main__':
    app.run(debug=True)
