import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
from typing import Optional, Any, Dict
import os
from psycopg2.extras import execute_batch
         
class DBFLoader:
    def __init__(self):
        self.tables = []
        self.setup_logging()
        self.setup_ui()
        
    def setup_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            filename='dbf_loader.log',
            level=logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.window = tk.Tk()
        self.window.title("Cargador de tablas DBF")
        self.window.geometry("400x300")
        
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(main_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Cargar datos", command=self.load_data).pack(pady=5, fill=tk.X)
        
        self.files_listbox = tk.Listbox(main_frame, height=8)
        self.files_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress_bar.pack(pady=5, fill=tk.X)

    def get_db_connection(self) -> tuple:
        """Establece la conexión con la base de datos"""
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="Gabriela_Fragancias",
                user="postgres",
                password="salmos23",
                connect_timeout=3
            )
            cur = conn.cursor()
            return conn, cur
        except psycopg2.Error as e:
            self.logger.error(f"Error de conexión a la base de datos: {str(e)}")
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            raise

    def safe_str(self, value: Any) -> str:
        """Convierte de manera segura cualquier valor a string"""
        if value is None:
            return ''
        return str(value).strip()

    def standardize_date(self, date_value: Any) -> Optional[datetime.date]:
        """Estandariza diferentes formatos de fecha"""
        try:
            if date_value is None:
                return None

            if isinstance(date_value, str):
                date_str = date_value.strip()
                if not date_str:
                    return None

                # Intentar diferentes formatos de fecha
                for fmt in ['%Y%m%d', '%d/%m/%Y']:
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except ValueError:
                        continue

            elif isinstance(date_value, (int, float)):
                # Convertir número a cadena y probar formato YYYYMMDD
                date_str = str(int(date_value))
                if len(date_str) == 8:
                    try:
                        return datetime.strptime(date_str, '%Y%m%d').date()
                    except ValueError:
                        pass

            self.logger.warning(f"Formato de fecha no reconocido: {date_value} ({type(date_value)})")
            return None

        except Exception as e:
            self.logger.warning(f"Error al procesar fecha {date_value}: {str(e)}")
            return None

    def process_record(self, record: Dict) -> tuple:
        """Procesa y valida un registro individual"""
        try:
            # Debug logging para ver los campos raw
            self.logger.debug(f"Registro raw: {record}")
            
            # Procesar campos básicos
            cedula = self.safe_str(record.get('cedula'))
            nombre = self.safe_str(record.get('nombre'))
            apellido = self.safe_str(record.get('apellido'))
            sexo = self.safe_str(record.get('sexo'))
            
            # Procesar dirección - verificar diferentes posibles nombres de campo
            direcc = None
            for field in ['direcc', 'direccion', 'direc', 'dir']:
                if field in record:
                    direcc = self.safe_str(record[field])
                    if direcc:
                        break
                        
            # Procesar fecha de nacimiento - verificar diferentes posibles nombres de campo
            fec_nac = None
            for field in ['fec_nac', 'fecha_nac', 'fechanac', 'fnac']:
                if field in record:
                    fec_nac = self.standardize_date(record[field])
                    if fec_nac:
                        break
            
            # Log detallado de los campos procesados
            self.logger.debug(f"""
                Campos procesados:
                Cédula: {cedula}
                Nombre: {nombre}
                Apellido: {apellido}
                Sexo: {sexo}
                Fecha Nacimiento: {fec_nac}
                Dirección: {direcc}
            """)
            
            # Validaciones básicas
            if not cedula or cedula.isspace():
                raise ValueError("Cédula es obligatoria")
            
            if not cedula.isdigit():
                raise ValueError(f"Cédula debe ser numérica: {cedula}")
            
            return (cedula, nombre, apellido, sexo, fec_nac, direcc)
            
        except Exception as e:
            self.logger.warning(f"Error procesando registro {record}: {str(e)}")
            raise

    def load_data(self):
        """Carga los datos de los archivos DBF a PostgreSQL"""
        if not self.tables:
            messagebox.showwarning("Advertencia", "Por favor seleccione archivos DBF primero")
            return

        try:
            conn, cur = self.get_db_connection()
            total_records = 0
            processed_records = 0
            error_records = 0
            
            # Activar logging detallado temporalmente
            self.logger.setLevel(logging.DEBUG)
            
            # Primer archivo para verificar estructura
            if self.tables:
                first_table = dbfread.DBF(self.tables[0], lowernames=True)
                self.logger.info(f"Estructura del primer archivo: {first_table.field_names}")
            
            # Contar registros totales
            for table_path in self.tables:
                table = dbfread.DBF(table_path, lowernames=True)
                total_records += len(table)
            
            self.progress_bar['maximum'] = total_records
            
            # Procesar los archivos
            for table_path in self.tables:
                try:
                    table = dbfread.DBF(table_path, lowernames=True)
                    self.logger.info(f"Procesando archivo: {table_path}")
                    self.logger.info(f"Campos disponibles: {table.field_names}")
                    
                    records_to_insert = []
                    
                    for record in table:
                        try:
                            processed_record = self.process_record(record)
                            records_to_insert.append(processed_record)
                            processed_records += 1
                            
                            if processed_records % 100 == 0:
                                self.progress_bar['value'] = processed_records
                                self.progress_label.config(
                                    text=f"Procesando: {processed_records}/{total_records} registros"
                                )
                                self.window.update()
                            
                            if len(records_to_insert) >= 1000:
                                execute_batch(cur, """
                                    INSERT INTO Cedulas 
                                    (numero_cedula, nombre, apellido, sexo, fecha_nacimiento, direccion)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (numero_cedula) DO UPDATE 
                                    SET nombre = EXCLUDED.nombre,
                                        apellido = EXCLUDED.apellido,
                                        sexo = EXCLUDED.sexo,
                                        fecha_nacimiento = COALESCE(EXCLUDED.fecha_nacimiento, Cedulas.fecha_nacimiento),
                                        direccion = COALESCE(EXCLUDED.direccion, Cedulas.direccion)
                                """, records_to_insert, page_size=1000)
                                records_to_insert = []
                                conn.commit()
                            
                        except Exception as e:
                            error_records += 1
                            self.logger.warning(f"Error en registro: {str(e)}")
                            continue
                    
                    if records_to_insert:
                        execute_batch(cur, """
                            INSERT INTO Cedulas 
                            (numero_cedula, nombre, apellido, sexo, fecha_nacimiento, direccion)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (numero_cedula) DO UPDATE 
                            SET nombre = EXCLUDED.nombre,
                                apellido = EXCLUDED.apellido,
                                sexo = EXCLUDED.sexo,
                                fecha_nacimiento = COALESCE(EXCLUDED.fecha_nacimiento, Cedulas.fecha_nacimiento),
                                direccion = COALESCE(EXCLUDED.direccion, Cedulas.direccion)
                        """, records_to_insert, page_size=1000)
                        conn.commit()
                    
                except Exception as e:
                    self.logger.error(f"Error procesando archivo {table_path}: {str(e)}")
                    messagebox.showerror("Error", f"Error al procesar {os.path.basename(table_path)}")
                    continue
            
            # Restaurar nivel de logging
            self.logger.setLevel(logging.INFO)
            
            summary = f"""
            Proceso completado:
            - Total registros procesados: {processed_records}
            - Registros con error: {error_records}
            - Tasa de éxito: {((processed_records - error_records) / processed_records * 100):.2f}%
            """
            
            self.logger.info(summary)
            messagebox.showinfo("Éxito", summary)
            
        except Exception as e:
            self.logger.error(f"Error general: {str(e)}")
            messagebox.showerror("Error", "Ocurrió un error durante la carga")
            
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
            self.progress_label.config(text="Proceso completado")

    def select_files(self):
        """Abre un diálogo para seleccionar archivos DBF y los agrega a la lista"""
        file_paths = filedialog.askopenfilenames(filetypes=[("DBF Files", "*.dbf")])
        for file_path in file_paths:
            self.files_listbox.insert(tk.END, file_path)
            self.tables.append(file_path)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = DBFLoader()
    app.run()