import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import pandas as pd
import dbfread
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional, Any, Dict, Tuple
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
        self.stats = {
            'processed': 0,
            'successful': 0,
            'failed': 0
        }

    def load_config(self):
        try:
            config = configparser.ConfigParser()
            config.read('database.ini')
            return config['postgresql']
        except KeyError as e:
            self.logger.error("Error en el archivo de configuración: sección 'postgresql' no encontrada.")
            raise

    def setup_logging(self):
        handler = RotatingFileHandler(
            'dbf_loader.log',
            maxBytes=10*1024*1024,
            backupCount=5
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.logger.handlers = []
        self.logger.addHandler(handler)

    def setup_ui(self):
        self.window = tk.Tk()
        self.window.title("Cargador de tablas DBF y CSV")
        self.window.geometry("800x600")

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(button_frame, text="Seleccionar archivos", command=self.select_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cargar datos", command=self.load_data).pack(side=tk.LEFT, padx=5)

        files_frame = ttk.LabelFrame(main_frame, text="Archivos seleccionados", padding="5")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.files_listbox = tk.Listbox(files_frame, height=5)
        self.files_listbox.pack(fill=tk.BOTH, expand=True)

        log_frame = ttk.LabelFrame(main_frame, text="Log de eventos", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.log_text = tk.Text(log_frame, height=10, width=50)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 5))

        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack(fill=tk.X)

        self.progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        self.progress_bar.pack(fill=tk.X)

        self.stats_label = ttk.Label(main_frame, text="")
        self.stats_label.pack(fill=tk.X)

    def get_db_connection(self) -> Tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
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

    def get_value_with_alternatives(self, record: Dict, field_alternatives: list, default: Any = None) -> Any:
        for field in field_alternatives:
            if field in record:
                return record[field]
        return default

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
                    '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y%m%d', '%d-%m-%Y', '%d.%m.%Y'
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

        return address if len(address) >= 2 else None

    def process_record(self, record: Dict) -> Optional[tuple]:
        try:
            cedula = self.get_value_with_alternatives(record, ['CEDULA', 'NUMERO_CED'], '')
            if isinstance(cedula, (int, float)):
                cedula = str(int(cedula))
            else:
                cedula = str(cedula).strip()

            cedula = ''.join(filter(str.isdigit, cedula))
            if not cedula:
                self.stats['failed'] += 1
                return None

            nombre = str(self.get_value_with_alternatives(record, ['NOMBRE'], '')).strip()
            apellido = str(self.get_value_with_alternatives(record, ['APELLIDO'], '')).strip()

            fecha_nac = self.standardize_date(self.get_value_with_alternatives(record, ['FEC_NAC', 'FECHA_NACI', 'FEC_NACI'], None))

            sexo = self.get_value_with_alternatives(record, ['SEXO', 'CODIGO_SEX'], '')
            sexo = str(sexo).strip().upper()[:1] if sexo else None

            direccion = self.clean_address(self.get_value_with_alternatives(record, ['DIRECCION', 'DIRECC'], None))

            id_distrito = self.get_value_with_alternatives(record, ['COD_DIST', 'DISTRITO'], None)
            id_distrito = str(id_distrito).strip() if id_distrito is not None else None

            id_dpto = self.get_value_with_alternatives(record, ['COD_DPTO', 'DEPART'], None)
            id_dpto = str(id_dpto).strip() if id_dpto is not None else None

            zona = self.get_value_with_alternatives(record, ['ZONA'], None)
            zona = str(zona).strip() if zona is not None else None

            lugar_nacimiento = self.get_value_with_alternatives(record, ['LUGAR_NACIMIENTO', 'LUG_NAC', 'LUGNAC'], None)
            lugar_nacimiento = str(lugar_nacimiento).strip() if lugar_nacimiento is not None else None

            fecha_defuncion = self.standardize_date(self.get_value_with_alternatives(record, 
                ['FECHA_DEFUNCION', 'FEC_DEFUNC', 'FEC_DEF'], None))

            self.stats['successful'] += 1
            return (
                cedula, nombre, apellido, fecha_nac, sexo, direccion,
                id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
            )
        except Exception as e:
            self.stats['failed'] += 1
            self.logger.error(f"Error en registro con cédula {cedula if 'cedula' in locals() else 'desconocida'}: {str(e)}")
            return None

    def read_csv(self, file_path: str):
        try:
            data = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')
            return data.to_dict(orient='records')
        except Exception as e:
            self.logger.error(f"Error leyendo CSV {file_path}: {e}")
            return []

    def read_dbf(self, file_path: str):
        try:
            table = dbfread.DBF(file_path, lowernames=True, encoding='cp1252')
            return [record for record in table]
        except Exception as e:
            self.logger.error(f"Error leyendo DBF {file_path}: {e}")
            return []

    def load_data(self):
        if not self.tables:
            messagebox.showwarning("Advertencia", "Por favor seleccione archivos primero")
            return

        try:
            conn, cur = self.get_db_connection()
            total_records = 0
            processed_records = 0
            start_time = time.time()
            self.stats = {'processed': 0, 'successful': 0, 'failed': 0}

            for table_path in self.tables:
                if table_path.endswith('.csv'):
                    records = self.read_csv(table_path)
                elif table_path.endswith('.dbf'):
                    records = self.read_dbf(table_path)
                else:
                    self.logger.warning(f"Formato no soportado: {table_path}")
                    continue

                total_records += len(records)
                self.progress_bar['maximum'] = total_records

                records_to_insert = []

                for record in records:
                    self.stats['processed'] += 1
                    processed_record = self.process_record(record)

                    if processed_record:
                        records_to_insert.append(processed_record)
                    processed_records += 1

                    if self.stats['processed'] % 10000 == 0:
                        self.logger.info(
                            f"Progreso: {self.stats['processed']}/{total_records} "
                            f"(Exitosos: {self.stats['successful']}, "
                            f"Fallidos: {self.stats['failed']})"
                        )

                    if len(records_to_insert) >= 1000:
                        try:
                            execute_batch(cur, """
                                INSERT INTO gf.cedulas (
                                    numero_cedula, nombre, apellido, fecha_nacimiento, sexo, direccion,
                                    id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
                                )
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, records_to_insert, page_size=1000)
                            conn.commit()
                            records_to_insert = []
                        except Exception as e:
                            self.logger.error(f"Error en batch insert: {str(e)}")
                            conn.rollback()

                    self.update_progress(processed_records, total_records, start_time)

                if records_to_insert:
                    try:
                        execute_batch(cur, """
                            INSERT INTO gf.cedulas (
                                numero_cedula, nombre, apellido, fecha_nacimiento, sexo, direccion,
                                id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, records_to_insert, page_size=1000)
                        conn.commit()
                    except Exception as e:
                        self.logger.error(f"Error en batch insert final: {str(e)}")
                        conn.rollback()

            self.logger.info(f"""
                Proceso completado:
                Total procesados: {self.stats['processed']}
                Exitosos: {self.stats['successful']}
                Fallidos: {self.stats['failed']}
                Tiempo total: {time.time() - start_time:.2f} segundos
            """)

            messagebox.showinfo("Éxito", 
                f"Proceso completado:\n"
                f"Total procesados: {self.stats['processed']}\n"
                f"Exitosos: {self.stats['successful']}\n"
                f"Fallidos: {self.stats['failed']}"
            )

        except Exception as e:
            self.logger.error(f"Error general: {str(e)}")
            messagebox.showerror("Error", f"Error durante la carga: {str(e)}")
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()

    def update_progress(self, processed_records, total_records, start_time):
        self.progress_bar['value'] = processed_records

        elapsed_time = time.time() - start_time
        if processed_records > 0:
            records_per_second = processed_records / elapsed_time
            remaining_records = total_records - processed_records
            estimated_remaining_time = remaining_records / records_per_second if records_per_second > 0 else 0

            minutes, seconds = divmod(int(estimated_remaining_time), 60)
            hours, minutes = divmod(minutes, 60)

            progress_text = (
                f"Progreso: {processed_records:,}/{total_records:,} "
                f"({processed_records/total_records*100:.1f}%)\n"
                f"Velocidad: {records_per_second:.0f} registros/seg\n"
                f"Tiempo restante estimado: {hours:02d}:{minutes:02d}:{seconds:02d}"
            )

            self.progress_label['text'] = progress_text

            stats_text = (
                f"Procesados: {self.stats['processed']:,} | "
                f"Exitosos: {self.stats['successful']:,} | "
                f"Fallidos: {self.stats['failed']:,}"
            )
            self.stats_label['text'] = stats_text

        self.window.update()

    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Archivos soportados", "*.dbf;*.csv")])
        self.tables = list(file_paths)
        self.files_listbox.delete(0, tk.END)
        for file_path in file_paths:
            self.files_listbox.insert(tk.END, file_path)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = DBFLoader()
    app.run()
