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
@app.route('/participantes', methods=['GET'])
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
@app.route('/participantes', methods=['POST'])
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
@app.route('/participantes/<ci>', methods=['DELETE'])
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
@app.route('/participantes/<ci>', methods=['PUT'])
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

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
