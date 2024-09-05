import tkinter as tk
from tkinter import messagebox
from db_utils import conectar_db
import mysql.connector

def Login_page(window, on_login_success):
    def login_user():
        username = username_entry.get()
        password = password_entry.get()

        print(f"Attempting login for user: {username}")

        try:
            # Conectar a la base de datos
            db = conectar_db()
            if db is None:
                raise Exception("No se pudo conectar a la base de datos")

            with db.cursor() as cursor:
                cursor.execute("SELECT contrasena FROM usuarios WHERE username = %s", (username,))
                result = cursor.fetchone()

                if result and result[0] == password:
                    print("Login successful")
                    window.destroy()  # Cerrar la ventana de inicio de sesión
                    on_login_success()  # Llamar al callback para abrir la página de selección
                else:
                    messagebox.showerror("Error", "Invalid username or password!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Database error: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if 'db' in locals() and db.is_connected():
                db.close()

    # Configuración de la ventana
    window.geometry("320x500")

    header = tk.Label(
        window,
        text="Detector",
        font=("Impact", 30),
        fg="#0B636B",
        pady=20
    )
    header.pack()

    username_label = tk.Label(window, text="Username", pady=10)
    username_label.pack()

    username_entry = tk.Entry(window, width=30)
    username_entry.pack()

    password_label = tk.Label(window, text="Password", pady=10)
    password_label.pack()

    password_entry = tk.Entry(window, show="*", width=30)
    password_entry.pack()

    login_button = tk.Button(
        window,
        text="Login",
        command=login_user,
        width=20
    )
    login_button.pack(pady=20)

    # Mostrar la ventana de inicio de sesión
    window.deiconify()
    print("Login page displayed")
