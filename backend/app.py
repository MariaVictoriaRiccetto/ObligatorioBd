from flask import Flask, jsonify, request
from bd import get_connection
import mysql.connector

app = Flask(__name__)

# -------------------------
# TEST CONEXION
# -------------------------
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

# -------------------------
# LISTAR PARTICIPANTES
# -------------------------
@app.route('/participantes', methods=['GET'])#checked
def listar_participantes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM participante;")
    participantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(participantes)

# -------------------------
# CREAR PARTICIPANTE
# -------------------------
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

# -------------------------
# ELIMINAR PARTICIPANTE
# -------------------------
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

# -------------------------
# MODIFICAR PARTICIPANTE
# -------------------------
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







# Levantar el server todo el codigo debe estar arriba para que le programa lo tome

if __name__ == '__main__':
    app.run(debug=True)
