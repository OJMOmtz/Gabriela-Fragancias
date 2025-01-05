import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import psycopg2
from datetime import datetime
import dbfread
import os
import re
import logging
from psycopg2.extras import execute_batch
from configparser import ConfigParser
from typing import Dict, List, Optional, Any
import chardet

class DatabaseConfig:
    def __init__(self, config_file: str = 'database.ini'):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, str]:
        if not os.path.exists(self.config_file):
            self._create_default_config()

        parser = ConfigParser()
        parser.read(self.config_file)

        return {
            'dbname': parser.get('postgresql', 'dbname', fallback='Gabriela_Fragancias'),
            'user': parser.get('postgresql', 'user', fallback='postgres'),
            'password': parser.get('postgresql', 'password', fallback='salmos23'),
            'host': parser.get('postgresql', 'host', fallback='localhost'),
            'port': parser.get('postgresql', 'port', fallback='5432')
        }

    def _create_default_config(self):
        parser = ConfigParser()
        parser.add_section('postgresql')
        parser.set('postgresql', 'dbname', 'Gabriela_Fragancias')
        parser.set('postgresql', 'user', 'postgres')
        parser.set('postgresql', 'password', 'salmos23')
        parser.set('postgresql', 'host', 'localhost')
        parser.set('postgresql', 'port', '5432')

        with open(self.config_file, 'w') as f:
            parser.write(f)

class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL CSV y DBF a PostgreSQL")
        self.root.geometry("1200x800")

        self.db_config = DatabaseConfig()
        self.files_selected: List[str] = []
        self.mappings: Dict[str, Dict] = {}

        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'sexo',
            'fecha_nacimiento', 'lugar_nacimiento', 'direccion',
            'id_barrio', 'id_distrito', 'id_dpto', 'zona',
            'fecha_defuncion', 'email'
        ]

        self._setup_logging()
        self.create_widgets()
        self.verify_database_connection()

    def _setup_logging(self):
        logging.basicConfig(
            filename='etl_process.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def verify_database_connection(self):
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE SCHEMA IF NOT EXISTS gf;
                        CREATE TABLE IF NOT EXISTS gf.cedulas (
                            numero_cedula VARCHAR(20) PRIMARY KEY,
                            nombre VARCHAR(100),
                            apellido VARCHAR(100),
                            sexo CHAR(1),
                            fecha_nacimiento DATE,
                            lugar_nacimiento VARCHAR(100),
                            direccion VARCHAR(200),
                            id_barrio VARCHAR(3),
                            id_distrito VARCHAR(2),
                            id_dpto VARCHAR(2),
                            zona VARCHAR(50),
                            fecha_defuncion DATE,
                            email VARCHAR(100),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                conn.commit()
            messagebox.showinfo("Conexión exitosa", "Conexión a la base de datos verificada correctamente")
        except Exception as e:
            logging.error(f"Error de conexión a la base de datos: {str(e)}")
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {str(e)}")

    def get_db_connection(self):
        return psycopg2.connect(**self.db_config.config)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        files_frame = ttk.LabelFrame(self.scrollable_frame, text="Archivos", padding="5")
        files_frame.pack(fill="x", padx=5, pady=5)

        button_frame = ttk.Frame(files_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="Seleccionar archivos", command=self.select_files).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpiar selección", command=self.clear_selection).pack(side="left", padx=5)

        list_frame = ttk.Frame(files_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.files_listbox = tk.Listbox(list_frame, height=5)
        list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_listbox.yview)

        self.files_listbox.configure(yscrollcommand=list_scrollbar.set)
        self.files_listbox.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")

        progress_frame = ttk.LabelFrame(self.scrollable_frame, text="Progreso", padding="5")
        progress_frame.pack(fill="x", padx=5, pady=5)

        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(pady=5)

        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack(pady=5)

        process_frame = ttk.Frame(self.scrollable_frame)
        process_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(process_frame, text="Procesar archivos", command=self.process_files).pack(side="left", padx=5)
        ttk.Button(process_frame, text="Cancelar", command=self.cancel_process).pack(side="left", padx=5)

    def clear_selection(self):
        self.files_selected.clear()
        self.files_listbox.delete(0, tk.END)
        self.progress['value'] = 0
        self.progress_label['text'] = ""

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos",
            filetypes=[("Archivos soportados", "*.csv *.dbf")]
        )

        if not files:
            return

        self.files_selected = list(files)
        self.files_listbox.delete(0, tk.END)
        for file in self.files_selected:
            self.files_listbox.insert(tk.END, file)

    def process_files(self):
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return

        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()

                for i, file_path in enumerate(self.files_selected):
                    ext = os.path.splitext(file_path)[-1].lower()
                    if ext == '.csv':
                        self.process_csv(file_path, cursor)
                    elif ext == '.dbf':
                        self.process_dbf(file_path, cursor)

                    self.progress['value'] = i + 1
                    self.progress_label['text'] = f"Procesando... {i + 1}/{len(self.files_selected)}"
                    self.root.update_idletasks()

                conn.commit()
                messagebox.showinfo("Éxito", "Archivos procesados correctamente")

        except Exception as e:
            logging.error(f"Error durante el procesamiento: {str(e)}")
            messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")

    def detect_csv_encoding(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read(10000))
        return result['encoding']

    def process_csv(self, file_path: str, cursor):
        encoding = self.detect_csv_encoding(file_path)
        df = pd.read_csv(file_path, encoding=encoding)
        self.insert_data(df, cursor)

    def process_dbf(self, file_path: str, cursor):
        table = dbfread.DBF(file_path)
        for chunk in self.iter_dbf_in_chunks(table, chunk_size=1000):
            df = pd.DataFrame(chunk)
            self.insert_data(df, cursor)

    def iter_dbf_in_chunks(self, table, chunk_size=1000):
        chunk = []
        for record in table:
            chunk.append(record)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    def insert_data(self, df: pd.DataFrame, cursor):
        batch_data = []

        for _, row in df.iterrows():
            record = {col: self.clean_data(row.get(col)) for col in self.pg_columns}
            if record['numero_cedula']:
                batch_data.append(record)

        if batch_data:
            columns = batch_data[0].keys()
            values = [[rec[col] for col in columns] for rec in batch_data]

            insert_query = f"""
                INSERT INTO gf.cedulas ({', '.join(columns)})
                VALUES ({', '.join(['%s'] * len(columns))})
                ON CONFLICT (numero_cedula) DO UPDATE
                SET {', '.join(f"{col} = EXCLUDED.{col}" for col in columns if col != 'numero_cedula')}
            """

            execute_batch(cursor, insert_query, values, page_size=1000)

    def clean_data(self, value: Any) -> Optional[str]:
        if pd.isna(value):
            return None
        if isinstance(value, str):
            return re.sub(r"\s+", " ", value.strip()).upper()
        return str(value).strip()

    def cancel_process(self):
        self.files_selected.clear()
        self.progress['value'] = 0
        self.progress_label['text'] = "Proceso cancelado"

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
