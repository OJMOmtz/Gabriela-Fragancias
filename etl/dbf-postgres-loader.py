import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from psycopg2.extras import execute_batch
from psycopg2.extensions import register_adapter, AsIs
import dbfread
from datetime import datetime
import os
import numpy as np
import pandas as pd

# Adaptador para manejar tipos numpy en psycopg2
def adapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(np.int64, adapt_numpy_int64)

class DBFToPostgres:
    def __init__(self, root):
        self.root = root
        self.root.title("Cargar Cédulas a PostgreSQL")
        self.files_selected = []
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
            'direccion', 'id_barrio', 'id_distrito', 'id_dpto', 'zona',
            'lugar_nacimiento', 'fecha_defuncion'
        ]
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self.root, text="Seleccionar archivos DBF/CSV", command=self.select_files).pack(pady=5)
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

        try:
            conn = psycopg2.connect(
                dbname="Gabriela_Fragancias",
                user="postgres",
                password="salmos23",
                host="localhost"
            )
            
            # Deshabilitar autocommit para mejorar el rendimiento
            conn.autocommit = False
            
            with conn.cursor() as cursor:
                all_records = []
                
                for file_path in self.files_selected:
                    self.progress_label.config(text=f"Procesando {os.path.basename(file_path)}...")
                    
                    if file_path.endswith('.dbf'):
                        records = self.read_dbf(file_path)
                    elif file_path.endswith('.csv'):
                        records = self.read_csv(file_path)
                    
                    all_records.extend(records)
                
                # Actualizar la barra de progreso
                self.progress_bar["maximum"] = len(all_records)
                
                # Inserción por lotes más grande
                batch_size = 5000
                for i in range(0, len(all_records), batch_size):
                    batch = all_records[i:i+batch_size]
                    self.insert_data(cursor, batch)
                    conn.commit()
                    
                    # Actualizar barra de progreso
                    self.progress_bar["value"] = min(i + batch_size, len(all_records))
                    self.root.update_idletasks()
            
            self.progress_label.config(text="¡Proceso completado con éxito!")
            messagebox.showinfo("Éxito", f"Se procesaron {len(all_records)} registros.")

        except Exception as e:
            messagebox.showerror("Error", f"Error procesando archivos: {str(e)}")
        finally:
            conn.close()
            self.progress_bar["value"] = 0

    def read_dbf(self, file_path):
        table = dbfread.DBF(file_path, lowernames=True)
        return [self.transform_record(record) for record in table if self.is_valid_record(record)]

    def read_csv(self, file_path):
        df = pd.read_csv(file_path, encoding='latin1', dtype=str)
        return [self.transform_record(record) for _, record in df.iterrows() if self.is_valid_record(record.to_dict())]

    def is_valid_record(self, record):
        # Verificar que al menos tenga cédula, nombre y apellido
        return (record.get('numero_cedula') or record.get('cedula') or 
                record.get('num_cedula')) is not None

    def transform_record(self, record):
        def safe_get(keys, default=None):
            for key in keys:
                value = record.get(key.lower())
                if value not in (None, ''):
                    return str(value).strip()
            return default

        def transform_date(date_str):
            if not date_str:
                return None
            try:
                # Formatos de fecha más comunes
                for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%Y%m%d', '%m/%d/%Y']:
                    try:
                        return datetime.strptime(str(date_str), fmt).strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            except Exception:
                pass
            return None

        record_data = {
            'numero_cedula': safe_get(['numero_cedula', 'cedula', 'num_cedula']),
            'nombre': safe_get(['nombre', 'first_name']),
            'apellido': safe_get(['apellido', 'last_name', 'surname']),
            'fecha_nacimiento': transform_date(safe_get(['fecha_nacimiento', 'birth_date', 'birthdate'])),
            'sexo': safe_get(['sexo', 'sex', 'genero']),
            'direccion': safe_get(['direccion', 'address']),
            'id_barrio': safe_get(['id_barrio', 'barrio', 'neighborhood']),
            'id_distrito': safe_get(['id_distrito', 'distrito', 'district']),
            'id_dpto': safe_get(['id_dpto', 'departamento', 'department']),
            'zona': safe_get(['zona', 'zone']),
            'lugar_nacimiento': safe_get(['lugar_nacimiento', 'birth_place', 'birthplace']),
            'fecha_defuncion': transform_date(safe_get(['fecha_defuncion', 'death_date', 'deathdate']))
        }
        
        return tuple(record_data.get(col) for col in self.pg_columns)

    def insert_data(self, cursor, data):
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
                apellido = COALESCE(EXCLUDED.apellido, gf.cedulas.apellido),
                fecha_nacimiento = COALESCE(EXCLUDED.fecha_nacimiento, gf.cedulas.fecha_nacimiento),
                sexo = COALESCE(EXCLUDED.sexo, gf.cedulas.sexo),
                direccion = COALESCE(EXCLUDED.direccion, gf.cedulas.direccion),
                id_barrio = COALESCE(EXCLUDED.id_barrio, gf.cedulas.id_barrio),
                id_distrito = COALESCE(EXCLUDED.id_distrito, gf.cedulas.id_distrito),
                id_dpto = COALESCE(EXCLUDED.id_dpto, gf.cedulas.id_dpto),
                zona = COALESCE(EXCLUDED.zona, gf.cedulas.zona),
                lugar_nacimiento = COALESCE(EXCLUDED.lugar_nacimiento, gf.cedulas.lugar_nacimiento),
                fecha_defuncion = COALESCE(EXCLUDED.fecha_defuncion, gf.cedulas.fecha_defuncion),
                updated_at = CURRENT_TIMESTAMP;
        """
        execute_batch(cursor, query, data)

if __name__ == "__main__":
    root = tk.Tk()
    app = DBFToPostgres(root)
    root.mainloop()
