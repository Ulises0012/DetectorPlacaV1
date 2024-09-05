import tkinter as tk
import login
import detector

def on_login_success():
    print("Login successful, starting detector...")
    detector.start_detector()
if __name__ == "__main__":
    print("Starting application...")
    root = tk.Tk()
    
    # Elimina la línea que oculta la ventana principal
    # root.withdraw()

    login.Login_page(root, on_login_success)
    print("Login page opened")
    root.mainloop()
