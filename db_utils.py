import mysql.connector
from mysql.connector import Error
import bcrypt  # Asegúrate de tener bcrypt instalado

def conectar_db():
    """Establece una conexión con la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia esto si es necesario
            password="",  # Cambia esto si es necesario
            database="sistema_deteccion_placas"
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
