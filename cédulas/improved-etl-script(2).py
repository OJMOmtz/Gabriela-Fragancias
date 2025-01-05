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
        self.root.title("ETL DBF a PostgreSQL")
        self.root.geometry("1200x800")

        self.db_config = DatabaseConfig()
        self.files_selected: List[str] = []
        self.mappings: Dict[str, Dict] = {}
        self.processing = False

        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'sexo',
            'fecha_nacimiento', 'lugar_nacimiento', 'direccion',
            'id_barrio', 'id_distrito', 'id_dpto', 'zona',
            'fecha_defuncion', 'email'
        ]

        self.setup_logging()
        self.create_widgets()
        self.verify_database_connection()

    def setup_logging(self):
        """Configura el sistema de logging para la aplicación."""
        log_filename = f'etl_process_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Iniciando aplicación ETL")
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

        files_frame = ttk.LabelFrame(self.scrollable_frame, text="Archivos DBF", padding="5")
        files_frame.pack(fill="x", padx=5, pady=5)

        button_frame = ttk.Frame(files_frame)
        button_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(button_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(side="left", padx=5)
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

        self.status_label = ttk.Label(progress_frame, text="Estado: Esperando archivos", font=('Arial', 10, 'bold'))
        self.status_label.pack(pady=5)

        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack(pady=5)

        self.records_label = ttk.Label(progress_frame, text="Registros procesados: 0", font=('Arial', 10))
        self.records_label.pack(pady=5)

        process_frame = ttk.Frame(self.scrollable_frame)
        process_frame.pack(fill="x", padx=5, pady=5)

        self.process_button = ttk.Button(process_frame, text="Procesar archivos", command=self.process_files)
        self.process_button.pack(side="left", padx=5)
        
        self.cancel_button = ttk.Button(process_frame, text="Cancelar", command=self.cancel_process, state="disabled")
        self.cancel_button.pack(side="left", padx=5)

    def clear_selection(self):
        self.files_selected.clear()
        self.files_listbox.delete(0, tk.END)
        self.progress['value'] = 0
        self.progress_label['text'] = ""
        self.status_label['text'] = "Estado: Esperando archivos"
        self.records_label['text'] = "Registros procesados: 0"
        self.processing = False
        self.process_button['state'] = 'normal'
        self.cancel_button['state'] = 'disabled'

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos DBF",
            filetypes=[("Archivos DBF", "*.dbf")]
        )

        if not files:
            return

        self.files_selected = list(files)
        self.files_listbox.delete(0, tk.END)
        for file in self.files_selected:
            self.files_listbox.insert(tk.END, os.path.basename(file))
        
        self.status_label['text'] = "Estado: Archivos seleccionados"

    def process_files(self):
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos DBF")
            return

        self.processing = True
        self.process_button['state'] = 'disabled'
        self.cancel_button['state'] = 'normal'
        total_records = 0

        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                for i, file_path in enumerate(self.files_selected):
                    if not self.processing:
                        break
                        
                    self.status_label['text'] = f"Estado: Procesando {os.path.basename(file_path)}"
                    records_processed = self.process_dbf(file_path, cursor)
                    total_records += records_processed
                    
                    self.progress['value'] = ((i + 1) / len(self.files_selected)) * 100
                    self.progress_label['text'] = f"Archivo {i + 1} de {len(self.files_selected)}"
                    self.records_label['text'] = f"Registros procesados: {total_records}"
                    self.root.update_idletasks()

                if self.processing:
                    conn.commit()
                    self.status_label['text'] = "Estado: Proceso completado"
                    messagebox.showinfo("Éxito", f"Archivos procesados correctamente\nTotal registros: {total_records}")
                else:
                    conn.rollback()
                    self.status_label['text'] = "Estado: Proceso cancelado"

        except Exception as e:
            logging.error(f"Error durante el procesamiento: {str(e)}")
            self.status_label['text'] = "Estado: Error en el proceso"
            messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")
        
        finally:
            self.processing = False
            self.process_button['state'] = 'normal'
            self.cancel_button['state'] = 'disabled'

    def process_dbf(self, file_path: str, cursor) -> int:
        records_processed = 0
        try:
            table = dbfread.DBF(file_path)
            total_records = len(table)
            
            for chunk in self.iter_dbf_in_chunks(table):
                if not self.processing:
                    return records_processed
                    
                df = pd.DataFrame(chunk)
                records_inserted = self.insert_data(df, cursor)
                records_processed += records_inserted
                
                self.records_label['text'] = f"Registros procesados: {records_processed}"
                self.root.update_idletasks()
                
            return records_processed
            
        except Exception as e:
            logging.error(f"Error procesando archivo DBF {file_path}: {str(e)}")
            raise

    def iter_dbf_in_chunks(self, table, chunk_size=1000):
        chunk = []
        for record in table:
            if not self.processing:
                break
            chunk.append(record)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk and self.processing:
            yield chunk

    def insert_data(self, df: pd.DataFrame, cursor) -> int:
        batch_data = []

        for _, row in df.iterrows():
            if not self.processing:
                return 0
                
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
            return len(batch_data)
        return 0

    def clean_data(self, value: Any) -> Optional[str]:
        if pd.isna(value):
            return None
        if isinstance(value, str):
            return re.sub(r"\s+", " ", value.strip()).upper()
        return str(value).strip()

    def cancel_process(self):
        self.processing = False
        self.status_label['text'] = "Estado: Cancelando proceso..."
        self.cancel_button['state'] = 'disabled'

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
