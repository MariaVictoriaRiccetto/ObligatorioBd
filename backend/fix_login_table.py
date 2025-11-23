#!/usr/bin/env python3
"""
Script para verificar y reparar el tamaño de la columna contraseña en la tabla login.
Ejecuta: python fix_login_table.py
"""

import mysql.connector
from mysql.connector import Error

# Configuración de conexión (ajusta según tu entorno)
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rootpassword', 
    'database': 'segunda'  
}

def conectar():
    """Conecta a la base de datos."""
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print("✓ Conexión exitosa a la base de datos")
            return conn
    except Error as e:
        print(f"✗ Error de conexión: {e}")
        return None

def verificar_tabla(conn):
    """Verifica la definición actual de la tabla login."""
    try:
        cursor = conn.cursor()
        cursor.execute("DESCRIBE login;")
        print("\n📋 Definición actual de la tabla 'login':")
        print("-" * 80)
        for row in cursor.fetchall():
            print(row)
        cursor.close()
    except Error as e:
        print(f"✗ Error verificando tabla: {e}")

def obtener_tipo_columna_contrasena(conn):
    """Obtiene el tipo de dato actual de la columna contraseña."""
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT COLUMN_TYPE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'login' AND COLUMN_NAME = 'contraseña'
            AND TABLE_SCHEMA = %s
        """, (config['database'],))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Error as e:
        print(f"✗ Error obteniendo tipo de columna: {e}")
        return None

def limpiar_datos_invalidos(conn):
    """Limpia filas con contraseña vacía o NULL antes del ALTER."""
    try:
        cursor = conn.cursor()
        
        # Contar filas con contraseña vacía o NULL
        cursor.execute("SELECT COUNT(*) FROM login WHERE contraseña IS NULL OR contraseña = '';")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"\n🧹 Encontradas {count} filas con contraseña vacía/NULL")
            print("   Eliminando filas inválidas...")
            cursor.execute("DELETE FROM login WHERE contraseña IS NULL OR contraseña = '';")
            conn.commit()
            print(f"✓ {cursor.rowcount} filas eliminadas")
        else:
            print("\n✓ No hay filas con contraseña vacía/NULL")
        
        cursor.close()
        return True
    except Error as e:
        print(f"✗ Error limpiando datos: {e}")
        conn.rollback()
        return False

def reparar_tabla(conn):
    """Aumenta el tamaño de la columna contraseña a VARCHAR(255)."""
    try:
        cursor = conn.cursor()
        
        # Obtener información actual
        info = obtener_tipo_columna_contrasena(conn)
        if not info:
            print("✗ No se pudo encontrar información de la columna 'contraseña'")
            return False
        
        print(f"\n📊 Tipo actual: {info['COLUMN_TYPE']}, Longitud máxima: {info['CHARACTER_MAXIMUM_LENGTH']}")
        
        # Limpiar datos inválidos antes del ALTER
        if not limpiar_datos_invalidos(conn):
            return False
        
        # Ejecutar ALTER TABLE
        alter_sql = "ALTER TABLE `login` MODIFY COLUMN `contraseña` VARCHAR(255) NOT NULL;"
        print(f"\n🔧 Ejecutando: {alter_sql}")
        cursor.execute(alter_sql)
        conn.commit()
        print("✓ ALTER TABLE ejecutado exitosamente")
        
        # Verificar cambio
        info_nueva = obtener_tipo_columna_contrasena(conn)
        if info_nueva:
            print(f"✓ Nuevo tipo: {info_nueva['COLUMN_TYPE']}, Longitud máxima: {info_nueva['CHARACTER_MAXIMUM_LENGTH']}")
        
        cursor.close()
        return True
    except Error as e:
        print(f"✗ Error durante ALTER TABLE: {e}")
        conn.rollback()
        return False

def main():
    """Función principal."""
    print("=" * 80)
    print("Script de reparación: Tabla 'login' - Columna 'contraseña'")
    print("=" * 80)
    
    # Conectar
    conn = conectar()
    if not conn:
        print("\n✗ No se pudo conectar. Ajusta las credenciales en el script.")
        return
    
    try:
        # Verificar estado actual
        print("\n1️⃣  Verificando estado actual...")
        verificar_tabla(conn)
        
        # Reparar
        print("\n2️⃣  Reparando tabla...")
        if reparar_tabla(conn):
            print("\n3️⃣  Verificando cambios...")
            verificar_tabla(conn)
            print("\n" + "=" * 80)
            print("✓ Reparación completada exitosamente")
            print("=" * 80)
            print("\n📝 Próximos pasos:")
            print("  1. Reinicia el servidor Flask (python -u app.py)")
            print("  2. Intenta hacer sign-up nuevamente desde la UI")
            print("  3. Si el error persiste, pega los nuevos logs aquí")
        else:
            print("\n✗ La reparación no se pudo completar")
    finally:
        conn.close()
        print("\n✓ Conexión cerrada")

if __name__ == '__main__':
    main()
