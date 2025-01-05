import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from psycopg2.extras import execute_batch
import dbfread
import pandas as pd
import os
from datetime import datetime
import multiprocessing as mp
import itertools

def process_single_file(file_path):
    """Función global para procesamiento de archivos"""
    try:
        if file_path.endswith('.dbf'):
            return process_dbf(file_path)
        elif file_path.endswith('.csv'):
            return process_csv(file_path)
        else:
            print(f"Formato no soportado: {file_path}")
            return 0
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return 0

def process_dbf(file_path, chunk_size=1000):
    total_processed = 0
    try:
        conn = psycopg2.connect(
            dbname="Gabriela_Fragancias",
            user="postgres",
            password="salmos23",
            host="localhost"
        )
        conn.autocommit = False
        cursor = conn.cursor()

        # Generador de registros DBF
        dbf_table = dbfread.DBF(file_path, lowernames=True)
        
        def record_generator():
            nonlocal total_processed
            for record in dbf_table:
                if is_valid_record(record):
                    transformed = transform_record(record)
                    if transformed:
                        total_processed += 1
                        yield transformed

        # Procesamiento por chunks
        chunk = list(itertools.islice(record_generator(), chunk_size))
        while chunk:
            insert_data(cursor, chunk)
            conn.commit()
            chunk = list(itertools.islice(record_generator(), chunk_size))

        cursor.close()
        conn.close()
        return total_processed

    except Exception as e:
        print(f"Error en DBF {file_path}: {e}")
        return total_processed

def process_csv(file_path, chunk_size=5000):
    total_processed = 0
    try:
        conn = psycopg2.connect(
            dbname="Gabriela_Fragancias",
            user="postgres",
            password="salmos23",
            host="localhost"
        )
        conn.autocommit = False
        cursor = conn.cursor()

        # Lectura de CSV por chunks
        for chunk in pd.read_csv(file_path, chunksize=chunk_size, encoding='latin1', dtype=str):
            valid_records = []
            for _, record in chunk.iterrows():
                record_dict = record.to_dict()
                if is_valid_record(record_dict):
                    transformed = transform_record(record_dict)
                    if transformed:
                        valid_records.append(transformed)
                        total_processed += 1

            if valid_records:
                insert_data(cursor, valid_records)
                conn.commit()

        cursor.close()
        conn.close()
        return total_processed

    except Exception as e:
        print(f"Error en CSV {file_path}: {e}")
        return total_processed

def is_valid_record(record):
    # Verificar que al menos tenga cédula, nombre y apellido
    return (record.get('numero_cedula') or record.get('cedula') or 
            record.get('num_cedula')) is not None

def transform_record(record):
    # Lógica de transformación
    pg_columns = [
        'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
        'direccion', 'id_barrio', 'id_distrito', 'id_dpto', 'zona',
        'lugar_nacimiento', 'fecha_defuncion'
    ]
    
    def safe_get(keys, default=None):
        for key in keys:
            value = record.get(key.lower())
            if value not in (None, ''):
                return str(value).strip()
        return default

    record_data = {
        'numero_cedula': safe_get(['numero_cedula', 'cedula', 'num_cedula']),
        'nombre': safe_get(['nombre', 'first_name']),
        'apellido': safe_get(['apellido', 'last_name', 'surname']),
        'fecha_nacimiento': safe_get(['fecha_nacimiento', 'birth_date']),
        'sexo': safe_get(['sexo', 'sex']),
        'direccion': safe_get(['direccion', 'address']),
        'id_barrio': safe_get(['id_barrio', 'barrio']),
        'id_distrito': safe_get(['id_distrito', 'distrito']),
        'id_dpto': safe_get(['id_dpto', 'departamento']),
        'zona': safe_get(['zona']),
        'lugar_nacimiento': safe_get(['lugar_nacimiento', 'birth_place']),
        'fecha_defuncion': safe_get(['fecha_defuncion', 'death_date'])
    }
    
    return tuple(record_data.get(col) for col in pg_columns)

def insert_data(cursor, data):
    query = """
        INSERT INTO gf.cedulas (
            numero_cedula, nombre, apellido, fecha_nacimiento, sexo,
            direccion, id_barrio, id_distrito, id_dpto, zona,
            lugar_nacimiento, fecha_defuncion
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (numero_cedula)
        DO UPDATE SET
            nombre = COALESCE(EXCLUDED.nombre, gf.cedulas.nombre),
            updated_at = CURRENT_TIMESTAMP;
    """
    execute_batch(cursor, query, data)

class EfficientDBFLoader:
    def __init__(self, root):
        self.root = root
        self.root.title("Carga Eficiente de Cédulas")
        self.files_selected = []
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self.root, text="Seleccionar archivos", command=self.select_files).pack(pady=5)
        self.files_listbox = tk.Listbox(self.root, width=80, height=5)
        self.files_listbox.pack(pady=5)
        ttk.Button(self.root, text="Procesar Archivos", command=self.process_files).pack(pady=10)
        self.progress_label = ttk.Label(self.root, text="")
        self.progress_label.pack(pady=5)
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=5)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[
            ("Archivos DBF", "*.dbf"), 
            ("Archivos CSV", "*.csv")
        ])
        if files:
            self.files_selected = list(files)
            self.files_listbox.delete(0, tk.END)
            for file in files:
                self.files_listbox.insert(tk.END, os.path.basename(file))

    def process_files(self):
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos.")
            return

        # Usar Pool de procesos
        with mp.Pool(processes=max(1, mp.cpu_count() - 1)) as pool:
            results = pool.map(process_single_file, self.files_selected)

        # Consolidar resultados
        total_processed = sum(results)
        messagebox.showinfo("Completado", f"Se procesaron {total_processed} registros.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EfficientDBFLoader(root)
    root.mainloop()
