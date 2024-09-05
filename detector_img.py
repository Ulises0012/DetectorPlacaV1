import cv2
import pytesseract
import numpy as np
from PIL import Image, ImageTk
import time
import re
import tkinter as tk
from tkinter import ttk
import subprocess
from db_manager import verificar_placa

# Configure Tesseract-OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize video capture
cap = cv2.VideoCapture(0)

def update_frame(window, label_img):
    """Update the frame in the Tkinter window."""
    global texto_placa, ultimo_tiempo, tiempo_minimo, placas_reconocidas

    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar el fotograma.")
        return

    altura, ancho, _ = frame.shape

    # Define regions of interest (ROI) for license plate recognition
    x1 = int(ancho / 3)
    x2 = int(x1 * 2)
    y1 = int(altura / 3)
    y2 = int(y1 * 2)

    # Draw rectangles and text on the frame
    cv2.rectangle(frame, (185, 80), (500, 130), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, 'Procesando Placa', (x1 - 10, y1 - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)

    cv2.rectangle(frame, (185, 340), (500, 420), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, texto_placa[0:8], (240, 400),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Perform detection only if the minimum time has passed
    if time.time() - ultimo_tiempo >= tiempo_minimo:
        recorte = frame[y1:y2, x1:x2]
        cv2.imshow('RECORTE', recorte)

        Gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
        cv2.imshow('GRIS', Gris)

        Gris = cv2.bilateralFilter(Gris, 15, 17, 17)
        bordes = cv2.Canny(Gris, 150, 250)
        cv2.imshow('UMBRAL', bordes)

        contornos, _ = cv2.findContours(bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:4]

        contorno_placa = None
        for contorno in contornos:
            peri = cv2.arcLength(contorno, True)
            aprox_contorno = cv2.approxPolyDP(contorno, 0.017 * peri, True)
            if len(aprox_contorno) == 4:
                contorno_placa = aprox_contorno
                break

        if contorno_placa is not None:
            cv2.drawContours(frame, [contorno_placa], -1, (255, 255, 0), 2)
            x, y, ancho, alto = cv2.boundingRect(contorno_placa)

            x_I_placa = x + x1
            y_I_placa = y + y1
            x_F_placa = x + ancho + x1
            y_F_placa = y + alto + y1

            placa = frame[y_I_placa:y_F_placa, x_I_placa:x_F_placa]

            matriz_valores = 255 - np.maximum.reduce([placa[:, :, 0], placa[:, :, 1], placa[:, :, 2]])
            _, binarizada = cv2.threshold(matriz_valores, 80, 255, cv2.THRESH_BINARY)

            binarizada = Image.fromarray(binarizada)
            texto_placa = pytesseract.image_to_string(binarizada, config='--psm 7')
            texto_placa = texto_placa.upper()

            if len(texto_placa) >= 5:
                placas_reconocidas.append(texto_placa)
                print("Letras de la placa:", texto_placa)

                placa_limpia = re.sub(r'[^a-zA-Z0-9]', '', texto_placa)
                placa_en_registro = verificar_placa(placa_limpia)

                if placa_en_registro:
                    print(f"La placa {texto_placa} está en la base de datos.")
                else:
                    print(f"La placa {texto_placa} no está en la base de datos.")

                ultimo_tiempo = time.time()

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    img_tk = ImageTk.PhotoImage(image=img)
    label_img.config(image=img_tk)
    label_img.image = img_tk

    window.after(10, update_frame, window, label_img)

def open_database_view():
    """Open a new file to display the database."""
    subprocess.Popen(['python', 'ver_datos.py'])

def start_detector():
    global texto_placa, placas_reconocidas, ultimo_tiempo, tiempo_minimo

    texto_placa = ''
    placas_reconocidas = []
    tiempo_minimo = 1
    ultimo_tiempo = time.time()

    window = tk.Tk()
    window.title("Detector503")
    window.geometry("800x600")

    header = tk.Label(window, text="Detector503", font=("Impact", 30), fg="#0B636B", pady=20)
    header.pack()

    frame_img = tk.Label(window)
    frame_img.pack(fill=tk.BOTH, expand=True)

    btn_db = tk.Button(window, text="Ver BD", command=open_database_view)
    btn_db.pack(side=tk.RIGHT, padx=10, pady=10)

    btn_logout = tk.Button(window, text="Cerrar Sesión", command=window.quit)
    btn_logout.pack(side=tk.BOTTOM, padx=10, pady=10)

    update_frame(window, frame_img)
    window.mainloop()

if __name__ == "__main__":
    start_detector()
