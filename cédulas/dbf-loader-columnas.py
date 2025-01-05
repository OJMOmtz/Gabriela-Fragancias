import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
from typing import Optional, Any, Dict
import os
from psycopg2.extras import execute_batch
import configparser
import time

class DBFLoader:
    def __init__(self):
        self.tables = []
        self.config = self.load_config()
        self.setup_logging()
        self.setup_ui()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read('database.ini')
        return config['postgresql']

    def setup_logging(self):
        logging.basicConfig(
            filename='dbf_loader.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_ui(self):
        self.window = tk.Tk()
        self.window.title("Cargador de tablas DBF")
        self.window.geometry("600x400")

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(main_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Cargar datos", command=self.load_data).pack(pady=5, fill=tk.X)

        self.log_text = tk.Text(main_frame, height=10, width=50)
        self.log_text.pack(pady=5, fill=tk.BOTH, expand=True)

        self.files_listbox = tk.Listbox(main_frame, height=5)
        self.files_listbox.pack(pady=5, fill=tk.X)

        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress_bar.pack(pady=5, fill=tk.X)

    def log_to_ui(self, message: str):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.window.update()

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['dbname'],
                user=self.config['user'],
                password=self.config['password']
            )
            cur = conn.cursor()
            cur.execute("SET search_path TO gf;")
            self.logger.info("Conexión establecida con la base de datos")
            return conn, cur
        except psycopg2.Error as e:
            self.logger.error(f"Error conectándose a la base de datos: {e}")
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            raise

    def standardize_date(self, date_value: Any) -> Optional[datetime.date]:
        if date_value is None or (isinstance(date_value, str) and not date_value.strip()):
            return None

        try:
            if isinstance(date_value, datetime.date):
                return date_value

            if isinstance(date_value, datetime):
                return date_value.date()

            if isinstance(date_value, str):
                formats_to_try = [
                    '%d/%m/%Y', '%Y%m%d', '%Y-%m-%d', '%d-%m-%Y', '%d.%m.%Y', '%m/%d/%Y'
                ]

                for date_format in formats_to_try:
                    try:
                        return datetime.strptime(date_value.strip(), date_format).date()
                    except ValueError:
                        continue

            if isinstance(date_value, (int, float)):
                date_str = str(int(date_value))
                if len(date_str) == 8:
                    try:
                        return datetime.strptime(date_str, '%Y%m%d').date()
                    except ValueError:
                        pass

            self.logger.warning(f"Formato de fecha no reconocido: {date_value} ({type(date_value)})")
            return None
        except Exception as e:
            self.logger.error(f"Error procesando fecha {date_value}: {e}")
            return None

    def clean_address(self, address: Optional[str]) -> Optional[str]:
        if address is None:
            return None

        if not isinstance(address, str):
            address = str(address)

        address = address.strip()
        address = ''.join(char for char in address if char.isprintable())
        address = ' '.join(address.split())

        if len(address) < 2:
            return None

        return address

    def get_value_with_alternatives(self, record: Dict, field_alternatives: list, default: Any = None) -> Any:
        for field in field_alternatives:
            if field in record:
                return record[field]
        return default

    def process_record(self, record: Dict) -> Optional[tuple]:
        try:
            self.logger.debug(f"Procesando registro: {record}")

            cedula = record.get('cedula', '').strip()
            if not cedula or not cedula.isdigit():
                self.logger.warning(f"Cédula inválida: {cedula}")
                return None

            nombre = record.get('nombre', '').strip()
            apellido = record.get('apellido', '').strip()
            fecha_nac = self.standardize_date(record.get('fecha_nacimiento'))
            sexo = record.get('sexo', '').strip().upper()[:1]
            direccion = self.clean_address(record.get('direccion'))

            id_distrito = record.get('id_distrito', '').strip()
            id_dpto = record.get('id_dpto', '').strip()
            zona = record.get('zona', '').strip()
            lugar_nacimiento = record.get('lugar_nacimiento', '').strip()
            fecha_defuncion = self.standardize_date(record.get('fecha_defuncion'))

            return (
                cedula, nombre, apellido, fecha_nac, sexo, direccion,
                id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
            )
        except Exception as e:
            self.logger.error(f"Error procesando registro: {e}")
            return None

    def load_data(self):
        if not self.tables:
            messagebox.showwarning("Advertencia", "Por favor seleccione archivos DBF primero")
            return

        try:
            conn, cur = self.get_db_connection()
            total_records = 0
            processed_records = 0
            start_time = time.time()

            for table_path in self.tables:
                table = dbfread.DBF(table_path, lowernames=True)
                total_records += len(table)

            self.progress_bar['maximum'] = total_records

            for table_path in self.tables:
                table = dbfread.DBF(table_path, lowernames=True)
                records_to_insert = []

                for record in table:
                    processed_record = self.process_record(record)
                    if processed_record:
                        records_to_insert.append(processed_record)
                    processed_records += 1

                    if len(records_to_insert) >= 1000:
                        execute_batch(cur, """
                            INSERT INTO gf.cedulas (
                                numero_cedula, nombre, apellido, fecha_nacimiento, sexo, direccion,
                                id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, records_to_insert, page_size=1000)
                        conn.commit()
                        records_to_insert = []

                    self.update_progress(processed_records, total_records, start_time)

                if records_to_insert:
                    execute_batch(cur, """
                        INSERT INTO gf.cedulas (
                            numero_cedula, nombre, apellido, fecha_nacimiento, sexo, direccion,
                            id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, records_to_insert, page_size=1000)
                    conn.commit()

                self.update_progress(processed_records, total_records, start_time)

            messagebox.showinfo("Éxito", f"Datos cargados exitosamente. Total registros: {processed_records}")
        except Exception as e:
            self.logger.error(f"Error general: {e}")
            messagebox.showerror("Error", "Ocurrió un error durante la carga")
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()

    def update_progress(self, processed_records, total_records, start_time):
        self.progress_bar['value'] = processed_records
        self.window.update()

        elapsed_time = time.time() - start_time
        remaining_time = (elapsed_time / processed_records) * (total_records - processed_records)
        minutes, seconds = divmod(int(remaining_time), 60)

        self.progress_label['text'] = f"Progreso: {processed_records}/{total_records} - Tiempo restante: {minutes}m {seconds}s"
        self.window.update()
           
    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Archivos DBF", "*.dbf")])
        self.tables = list(file_paths)
        self.files_listbox.delete(0, tk.END)
        for file_path in file_paths:
            self.files_listbox.insert(tk.END, file_path)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = DBFLoader()
    app.run()            
