import tkinter as tk
from tkinter import ttk

def open_detector_page():
    """Open the detector page."""
    import detector  # Import the detector module
    detector.start_detector()

def open_ver_datos_page():
    """Open the view data page."""
    import ver_datos  # Import the ver_datos module
    ver_datos.open_database_view()  # Cambiado a open_database_view

def create_selection_page():
    """Create the selection page with buttons to choose actions."""
    window = tk.Tk()
    window.title("Selection Page")
    window.geometry("400x300")
    window.configure(bg="#f0f0f0")

    header = tk.Label(window, text="Seleccione una opción", font=("Impact", 24), fg="#0B636B", bg="#f0f0f0", pady=20)
    header.pack()

    btn_detectar = tk.Button(window, text="Detectar", command=open_detector_page, font=("Arial", 16), bg="#4CAF50", fg="white")
    btn_detectar.pack(pady=10, fill=tk.X, padx=50)

    btn_ver_datos = tk.Button(window, text="Ver Datos", command=open_ver_datos_page, font=("Arial", 16), bg="#2196F3", fg="white")
    btn_ver_datos.pack(pady=10, fill=tk.X, padx=50)

    window.mainloop()
