import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootpassword",
            database="segunda"
        )
        return conn
    except mysql.connector.Error as e:
        print("Error al conectar a MySQL:", e)
        return None
