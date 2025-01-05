import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext

def procesar_pagina():
    url = entrada_url.get()
    
    try:
        respuesta = requests.get(url)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        
        texto = soup.get_text()
        lineas = [linea.strip() for linea in texto.splitlines()]
        lineas_sin_vacias = [linea for linea in lineas if linea]
        
        resultado.delete("1.0", tk.END)
        resultado.insert(tk.END, "\n".join(lineas_sin_vacias))
    except requests.exceptions.RequestException as e:
        resultado.delete("1.0", tk.END)
        resultado.insert(tk.END, "Error al obtener la página web.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Procesador de Páginas Web")

# Crear la etiqueta y entrada para la URL
etiqueta_url = tk.Label(ventana, text="URL:")
etiqueta_url.pack()
entrada_url = tk.Entry(ventana, width=50)
entrada_url.pack()

# Crear el botón para procesar la página
boton_procesar = tk.Button(ventana, text="Procesar", command=procesar_pagina)
boton_procesar.pack()

# Crear el área de texto para mostrar el resultado
resultado = scrolledtext.ScrolledText(ventana, width=80, height=20)
resultado.pack()

# Ejecutar la aplicación
ventana.mainloop()