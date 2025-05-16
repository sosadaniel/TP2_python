import mysql.connector
import sys

print("Iniciando prueba de conexión...")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="root",
        database="trabajo2",
        connection_timeout=5 
    )
    print("✅ Conexión exitosa a la base de datos.")
    conn.close()
except mysql.connector.Error as err:
    print(f"❌ Error de MySQL: {err.errno} - {err.msg}", file=sys.stderr)
except Exception as e:
    print(f"Otro error: {e}", file=sys.stderr)

print("Fin del script.")
