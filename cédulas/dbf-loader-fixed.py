import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
from logging.handlers import RotatingFileHandler
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
        self.stats = {
            'processed': 0,
            'successful': 0,
            'failed': 0
        }

    def load_config(self):
        config = configparser.ConfigParser()
        config.read('database.ini')
        return config['postgresql']

    def setup_logging(self):
        # Configurar el rotating file handler (10MB por archivo, máximo 5 archivos)
        handler = RotatingFileHandler(
            'dbf_loader.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Configurar el logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)  # Cambiado a INFO para reducir verbosidad
        
        # Remover handlers existentes y agregar el nuevo
        self.logger.handlers = []
        self.logger.addHandler(handler)

    def process_record(self, record: Dict) -> Optional[tuple]:
        try:
            # Obtener cédula y convertir a string si es necesario
            cedula = self.get_value_with_alternatives(record, ['CEDULA', 'NUMERO_CED'], '')
            if isinstance(cedula, (int, float)):
                cedula = str(int(cedula))
            else:
                cedula = str(cedula).strip()
            
            # Limpieza básica de la cédula
            cedula = ''.join(filter(str.isdigit, cedula))
            if not cedula:
                self.stats['failed'] += 1
                return None

            # Campos obligatorios
            nombre = str(self.get_value_with_alternatives(record, ['NOMBRE'], '')).strip()
            apellido = str(self.get_value_with_alternatives(record, ['APELLIDO'], '')).strip()
            
            # Campos opcionales
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

    def load_data(self):
        if not self.tables:
            messagebox.showwarning("Advertencia", "Por favor seleccione archivos DBF primero")
            return

        try:
            conn, cur = self.get_db_connection()
            total_records = 0
            processed_records = 0
            start_time = time.time()
            self.stats = {'processed': 0, 'successful': 0, 'failed': 0}

            # Contar registros totales
            for table_path in self.tables:
                table = dbfread.DBF(table_path, lowernames=True)
                total_records += len(table)

            self.progress_bar['maximum'] = total_records
            
            for table_path in self.tables:
                table = dbfread.DBF(table_path, lowernames=True, encoding='cp1252')
                records_to_insert = []
                
                for record in table:
                    self.stats['processed'] += 1
                    processed_record = self.process_record(record)
                    
                    if processed_record:
                        records_to_insert.append(processed_record)
                    processed_records += 1

                    # Actualizar cada 10000 registros para no sobrecargar el log
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

    # [El resto de los métodos permanecen igual]
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
