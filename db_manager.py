import mysql.connector
from mysql.connector import Error

def crear_conexion():
    """Create a connection to the MySQL database."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='sistema_deteccion_placas',
            user='root',
            password=''
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def verificar_placa(numero_placa):
    """Verify if the plate number exists in the database."""
    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT * FROM placas WHERE numero_placa = %s"
            cursor.execute(query, (numero_placa,))
            resultado = cursor.fetchone()
            return resultado is not None
        except Error as e:
            print(f"Error al consultar la base de datos: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    return False
