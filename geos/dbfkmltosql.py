import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import geopandas as gpd
from dbfread import DBF
import psycopg2

# Función para seleccionar archivo
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos DBF", "*.dbf"), ("Archivos SHP", "*.shp"), 
                                                    ("Archivos KML", "*.kml"), ("Archivos GeoJSON", "*.geojson"),
                                                    ("Archivos JSON", "*.json")])
    ruta_archivo.set(archivo)

# Función para cargar archivo y mostrar columnas
def cargar_archivo():
    archivo = ruta_archivo.get()
    if archivo.endswith(".dbf"):
        table = DBF(archivo)
        df = pd.DataFrame(iter(table))
    elif archivo.endswith(".shp") or archivo.endswith(".kml") or archivo.endswith(".geojson") or archivo.endswith(".json"):
        df = gpd.read_file(archivo)
    else:
        messagebox.showerror("Error", "Formato de archivo no soportado")
        return

    # Mostrar las columnas del archivo cargado
    columnas.set(df.columns.tolist())
    messagebox.showinfo("Éxito", "Archivo cargado exitosamente. Selecciona las columnas a importar.")

# Función para importar datos seleccionados a PostgreSQL
def importar_datos():
    columnas_seleccionadas = [lb_columnas.get(i) for i in lb_columnas.curselection()]
    archivo = ruta_archivo.get()

    if archivo.endswith(".dbf"):
        df = pd.DataFrame(iter(DBF(archivo)))
    elif archivo.endswith(".shp") or archivo.endswith(".kml") or archivo.endswith(".geojson") or archivo.endswith(".json"):
        df = gpd.read_file(archivo)
    else:
        messagebox.showerror("Error", "Formato de archivo no soportado")
        return

    # Filtrar las columnas seleccionadas
    df = df[columnas_seleccionadas]

    # Conectar a PostgreSQL
    conn = psycopg2.connect(host="localhost", database="Gabriela_Fragancias", user="postgres", password="salmos23")
    cur = conn.cursor()

    # Insertar datos en la base de datos
    for _, row in df.iterrows():
        # Aquí ajustas la tabla y columnas de destino en PostgreSQL
        cur.execute(
            "INSERT INTO tabla_destino (columna1, columna2) VALUES (%s, %s)",
            (row[columnas_seleccionadas[0]], row[columnas_seleccionadas[1]])  # Ajusta según las columnas seleccionadas
        )

    conn.commit()
    cur.close()
    conn.close()
    messagebox.showinfo("Éxito", "Datos importados exitosamente.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Importador de Datos DBF/Geoespaciales")

# Variables
ruta_archivo = tk.StringVar()
columnas = tk.StringVar(value=[])

# Interfaz
tk.Label(root, text="Selecciona el archivo:").pack(pady=5)
tk.Entry(root, textvariable=ruta_archivo, width=50).pack(pady=5)
tk.Button(root, text="Seleccionar archivo", command=seleccionar_archivo).pack(pady=5)

tk.Button(root, text="Cargar archivo", command=cargar_archivo).pack(pady=5)

tk.Label(root, text="Selecciona las columnas a importar:").pack(pady=5)
lb_columnas = tk.Listbox(root, listvariable=columnas, selectmode="multiple", width=50, height=10)
lb_columnas.pack(pady=5)

tk.Button(root, text="Importar datos", command=importar_datos).pack(pady=10)

# Ejecutar la aplicación
root.mainloop()