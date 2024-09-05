import tkinter as tk
import login
from selection_page import create_selection_page

def on_login_success():
    print("Login successful, opening selection page...")
    create_selection_page()  # Abre la página de selección en lugar de iniciar el detector

if __name__ == "__main__":
    print("Starting application...")
    root = tk.Tk()

    # Elimina la línea que oculta la ventana principal
    # root.withdraw()

    login.Login_page(root, on_login_success)
    print("Login page opened")
    root.mainloop()
