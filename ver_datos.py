import tkinter as tk
from tkinter import ttk
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

def open_database_view():
    """Open a new window to display the database."""
    new_window = tk.Toplevel()
    new_window.title("Base de Datos")
    new_window.geometry("800x600")

    tab_control = ttk.Notebook(new_window)

    # Create tabs for each table
    tab_placas = ttk.Frame(tab_control)
    tab_propietarios = ttk.Frame(tab_control)
    tab_vehiculos = ttk.Frame(tab_control)

    tab_control.add(tab_placas, text='Placas')
    tab_control.add(tab_propietarios, text='Propietarios')
    tab_control.add(tab_vehiculos, text='Vehículos')
    tab_control.pack(expand=1, fill='both')

    # Placas Tab
    tree_placas = ttk.Treeview(tab_placas, columns=("ID", "Número de Placa"), show="headings")
    tree_placas.heading("ID", text="ID")
    tree_placas.heading("Número de Placa", text="Número de Placa")

    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT id, numero_placa FROM placas"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                tree_placas.insert("", "end", values=row)
        except Error as e:
            print(f"Error al consultar la base de datos: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    tree_placas.pack(fill=tk.BOTH, expand=True)

    # Propietarios Tab
    tree_propietarios = ttk.Treeview(tab_propietarios, columns=("ID", "Nombre", "Apellido", "Dirección", "Teléfono"), show="headings")
    tree_propietarios.heading("ID", text="ID")
    tree_propietarios.heading("Nombre", text="Nombre")
    tree_propietarios.heading("Apellido", text="Apellido")
    tree_propietarios.heading("Dirección", text="Dirección")
    tree_propietarios.heading("Teléfono", text="Teléfono")

    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT id, nombre, apellido, direccion, telefono FROM propietarios"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                tree_propietarios.insert("", "end", values=row)
        except Error as e:
            print(f"Error al consultar la base de datos: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    tree_propietarios.pack(fill=tk.BOTH, expand=True)

    # Vehículos Tab
    tree_vehiculos = ttk.Treeview(tab_vehiculos, columns=("Modelo", "Marca", "Año", "ID Placa", "ID Propietario"), show="headings")
    tree_vehiculos.heading("Modelo", text="Modelo")
    tree_vehiculos.heading("Marca", text="Marca")
    tree_vehiculos.heading("Año", text="Año")
    tree_vehiculos.heading("ID Placa", text="ID Placa")
    tree_vehiculos.heading("ID Propietario", text="ID Propietario")

    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT modelo, marca, año, id_placa, id_propietario FROM vehiculos"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                tree_vehiculos.insert("", "end", values=row)
        except Error as e:
            print(f"Error al consultar la base de datos: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    tree_vehiculos.pack(fill=tk.BOTH, expand=True)

def main():
    """Create a Tkinter window to start the database view."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    open_database_view()
    root.mainloop()

if __name__ == "__main__":
    main()
