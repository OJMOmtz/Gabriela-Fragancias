import os
import pandas as pd
import dbfread
import psycopg2
from psycopg2.extras import execute_batch
from time import time
from tqdm import tqdm
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'dbname': 'Gabriela_Fragancias',
    'user': 'postgres',
    'password': 'salmos23',
    'host': 'localhost',
    'port': 5432
}

def obtener_columnas_existentes(cursor, tabla):
    """Obtiene las columnas existentes en la tabla destino."""
    cursor.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'gf' AND table_name = '{tabla}'
    """)
    return [row[0] for row in cursor.fetchall()]

def procesar_archivo_csv(filepath, estructura):
    """Procesa un archivo CSV y retorna un DataFrame listo para insertar."""
    columnas_necesarias = list(estructura['mapeo_columnas'].keys())
    df = pd.read_csv(
        filepath,
        encoding='iso-8859-1',
        usecols=columnas_necesarias,
        on_bad_lines='skip',
        dtype=str,
        low_memory=False
    )
    df.rename(columns=estructura['mapeo_columnas'], inplace=True)
    return df

def procesar_archivo_dbf(filepath, estructura):
    """Procesa un archivo DBF y retorna un DataFrame listo para insertar."""
    registros = []
    columnas_necesarias = estructura['mapeo_columnas'].keys()
    for record in dbfread.DBF(filepath, lowernames=True):
        registros.append({col: record.get(col, None) for col in columnas_necesarias})
    return pd.DataFrame(registros).rename(columns=estructura['mapeo_columnas'])

def cargar_datos_a_postgresql(dataframes, tabla_destino, batch_size=1000):
    """Carga datos desde múltiples DataFrames a una tabla PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Obtener columnas existentes en la tabla
        columnas_existentes = obtener_columnas_existentes(cursor, tabla_destino)

        # Desactivar índices temporalmente
        cursor.execute(f"ALTER TABLE {tabla_destino} DISABLE TRIGGER ALL;")
        conn.commit()

        for idx, df in enumerate(dataframes, 1):
            print(f"\n[{idx}/{len(dataframes)}] Procesando conjunto de datos...")
            
            # Mantener solo columnas existentes
            columnas_a_insertar = [col for col in columnas_existentes if col in df.columns]
            df = df[columnas_a_insertar]

            # Reemplazar valores nulos con None
            df = df.where(pd.notnull(df), None)

            # Construir la consulta INSERT
            insert_query = f"""
                INSERT INTO {tabla_destino} ({', '.join(columnas_a_insertar)}) 
                VALUES ({', '.join(['%s'] * len(columnas_a_insertar))}) 
                ON CONFLICT (numero_cedula) DO UPDATE SET 
                {', '.join([f"{col} = EXCLUDED.{col}" for col in columnas_a_insertar if col != 'numero_cedula'])}
            """

            # Insertar en lotes con barra de progreso
            with tqdm(total=len(df), desc="Insertando registros", unit="reg") as pbar:
                for i in range(0, len(df), batch_size):
                    batch = df.iloc[i:i + batch_size].values.tolist()
                    execute_batch(cursor, insert_query, batch)
                    conn.commit()
                    pbar.update(len(batch))

        # Reactivar índices
        cursor.execute(f"ALTER TABLE {tabla_destino} ENABLE TRIGGER ALL;")
        conn.commit()
        cursor.close()
        conn.close()
        print("\nProceso completado exitosamente.")

    except Exception as e:
        print(f"Error durante la carga de datos: {str(e)}")

class CargadorCedulasApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cargador de Cédulas")
        self.window.geometry("600x400")
        self.dataframes = []

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(main_frame, text="Seleccionar archivos", command=self.seleccionar_archivos).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Cargar datos", command=self.cargar_datos).pack(pady=5, fill=tk.X)

        self.log_text = tk.Text(main_frame, height=10, width=50)
        self.log_text.pack(pady=5, fill=tk.BOTH, expand=True)

        self.files_listbox = tk.Listbox(main_frame, height=5)
        self.files_listbox.pack(pady=5, fill=tk.X)

        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress_bar.pack(pady=5, fill=tk.X)

    def log_to_ui(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.window.update()

    def seleccionar_archivos(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Archivos CSV y DBF", "*.csv *.dbf")])
        self.files_listbox.delete(0, tk.END)
        for file_path in file_paths:
            self.files_listbox.insert(tk.END, file_path)

    def cargar_datos(self):
        detalle_archivos = {
            file_path: {
                "tipo": "csv" if file_path.endswith('.csv') else "dbf",
                "mapeo_columnas": {
                    "numero_cedula": "numero_cedula",
                    "nombre": "nombre",
                    "apellido": "apellido",
                    "fecha_nacimiento": "fecha_nacimiento",
                    "sexo": "sexo"
                } if file_path.endswith('.csv') else {
                    "cedula": "numero_cedula",
                    "nombre": "nombre",
                    "apellido": "apellido",
                    "fec_nac": "fecha_nacimiento",
                    "sexo": "sexo"
                }
            } for file_path in self.files_listbox.get(0, tk.END)
        }

        self.dataframes = []
        for filepath, estructura in detalle_archivos.items():
            self.log_to_ui(f"Procesando archivo: {os.path.basename(filepath)}")
            if estructura['tipo'] == 'csv':
                df = procesar_archivo_csv(filepath, estructura)
            elif estructura['tipo'] == 'dbf':
                df = procesar_archivo_dbf(filepath, estructura)
            else:
                self.log_to_ui(f"Tipo de archivo desconocido para {filepath}, omitiendo...")
                continue
            self.dataframes.append(df)

        cargar_datos_a_postgresql(self.dataframes, "gf.cedulas")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CargadorCedulasApp()
    app.run()
