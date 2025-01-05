import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog

def seleccionar_archivo():
    """Abre un explorador de archivos para seleccionar el archivo CSV."""
    global archivo_seleccionado
    archivo_seleccionado = filedialog.askopenfilename(initialdir="/", title="Seleccionar archivo CSV", filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
    lbl_archivo.config(text="Archivo seleccionado: " + archivo_seleccionado)

def limpiar_y_guardar_datos(archivo_csv, nuevo_archivo_csv):
    """
    Limpia y guarda los datos de un archivo CSV en un nuevo archivo.

    Args:
        archivo_csv: Ruta del archivo CSV original.
        nuevo_archivo_csv: Ruta del nuevo archivo CSV a crear.
    """

    try:
        # Verificar si el archivo existe antes de intentar leerlo
        if not os.path.exists(archivo_csv):
            raise FileNotFoundError(f"El archivo no existe: {archivo_csv}")

        # Leer el archivo CSV, saltando la primera fila si está duplicada
        df = pd.read_csv(archivo_csv, sep=';', skiprows=1)

        # Limpieza de datos (personaliza según tus necesidades)
        df.drop_duplicates(inplace=True)  # Eliminar filas duplicadas
        df['Peso (Ml)'] = pd.to_numeric(df['Peso (Ml)'], errors='coerce')  # Convertir a numérico
        df.dropna(subset=['Peso (Ml)'], inplace=True)  # Eliminar filas con NaN en 'Peso (Ml)'

        # Seleccionar columnas de interés
        columnas_a_guardar = ['Código De Barras', 'Marca', 'Producto', 'Peso (Ml)', 'Precio']
        df_final = df[columnas_a_guardar]

        # Crear un nuevo DataFrame con cálculos adicionales (ejemplo)
        df_final['Margen_de_ganancia'] = df_final['Precio'] - df_final['Costo']  # Suponiendo que 'Costo' existe

        # Guardar el nuevo DataFrame en un archivo CSV
        df_final.to_csv(nuevo_archivo_csv, index=False)
        print(f"Archivo guardado exitosamente: {nuevo_archivo_csv}")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Analizador de Archivos CSV")

# Botón para seleccionar el archivo
btn_seleccionar = tk.Button(ventana, text="Seleccionar Archivo", command=seleccionar_archivo)
btn_seleccionar.pack(pady=10)

# Label para mostrar el archivo seleccionado
lbl_archivo = tk.Label(ventana, text="Archivo no seleccionado")
lbl_archivo.pack()

# Botón para procesar el archivo
btn_procesar = tk.Button(ventana, text="Procesar Archivo", command=lambda: limpiar_y_guardar_datos(archivo_seleccionado, "datos_procesados.csv"))
btn_procesar.pack(pady=10)

ventana.mainloop()

import pandas as pd

# ... (resto del código)

# Limpieza de datos
df.drop_duplicates(inplace=True)

# Convertir a numérico, ignorando errores y eliminando filas con NaN
df['Peso (Ml)'] = pd.to_numeric(df['Peso (Ml)'], errors='coerce')
df.dropna(subset=['Peso (Ml)'], inplace=True)

# Verificar si hay algún valor no numérico restante
print(df['Peso (Ml)'].dtype)
if df['Peso (Ml)'].dtype != 'float64':
    print("Aún hay valores no numéricos en la columna 'Peso (Ml)'")
