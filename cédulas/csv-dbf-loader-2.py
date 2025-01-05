import os
import pandas as pd
import dbfread
import psycopg2
from psycopg2.extras import execute_batch
from time import time
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

class CargadorCedulasApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cargador de Cédulas")
        self.window.geometry("800x600")
        self.dataframes = []
        self.files_selected = []
        self.mappings = {}

        # Columnas destino PostgreSQL
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
            'direccion', 'id_distrito', 'id_dpto', 'zona', 'lugar_nacimiento', 'fecha_defuncion'
        ]

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
        if not file_paths:
            return

        self.files_selected = list(file_paths)
        self.files_listbox.delete(0, tk.END)

        for file_path in self.files_selected:
            self.files_listbox.insert(tk.END, file_path)

        self.mappings = {}
        for file_path in self.files_selected:
            file_name = os.path.basename(file_path)
            dbf_columns = self.get_columns(file_path)
            self.mappings[file_path] = {pg_col: dbf_columns[0] if dbf_columns else '' for pg_col in self.pg_columns}

    def get_columns(self, file_path):
        if file_path.endswith('.dbf'):
            table = dbfread.DBF(file_path, lowernames=True)
            return table.field_names
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, nrows=0)
            return list(df.columns)
        return []

    def cargar_datos(self):
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return

        dataframes = []
        for file_path in self.files_selected:
            if file_path.endswith('.dbf'):
                df = self.procesar_archivo_dbf(file_path, self.mappings[file_path])
            elif file_path.endswith('.csv'):
                df = self.procesar_archivo_csv(file_path, self.mappings[file_path])
            else:
                continue
            dataframes.append(df)

        self.insertar_datos(dataframes, "gf.cedulas")

    def procesar_archivo_csv(self, file_path, mapping):
        columnas_necesarias = [col for col in mapping.values() if col]
        df = pd.read_csv(
            file_path,
            encoding='iso-8859-1',
            usecols=columnas_necesarias,
            on_bad_lines='skip',
            dtype=str,
            low_memory=False
        )
        df.rename(columns={v: k for k, v in mapping.items() if v}, inplace=True)
        return df

    def procesar_archivo_dbf(self, file_path, mapping):
        registros = []
        columnas_necesarias = [col for col in mapping.values() if col]
        for record in dbfread.DBF(file_path, lowernames=True):
            registros.append({col: record.get(col) for col in columnas_necesarias})
        df = pd.DataFrame(registros)
        df.rename(columns={v: k for k, v in mapping.items() if v}, inplace=True)
        return df

    def insertar_datos(self, dataframes, tabla_destino):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            for idx, df in enumerate(dataframes):
                self.log_to_ui(f"[{idx + 1}/{len(dataframes)}] Procesando {self.files_selected[idx]}...")
                columnas = df.columns
                valores = ', '.join(['%s'] * len(columnas))
                insert_query = f"""
                    INSERT INTO {tabla_destino} ({', '.join(columnas)}) 
                    VALUES ({valores}) 
                    ON CONFLICT (numero_cedula) DO UPDATE SET 
                    {', '.join([f"{col} = EXCLUDED.{col}" for col in columnas if col != 'numero_cedula'])}
                """
                execute_batch(cursor, insert_query, df.values.tolist())
                conn.commit()

            cursor.close()
            conn.close()
            self.log_to_ui("Proceso completado exitosamente.")
        except Exception as e:
            self.log_to_ui(f"Error durante la carga de datos: {str(e)}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CargadorCedulasApp()
    app.run()
