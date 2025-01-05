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
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.window = tk.Tk()
        self.window.title("Cargador de tablas DBF")
        self.window.geometry("400x300")
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        ttk.Button(main_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Cargar datos", command=self.load_data).pack(pady=5, fill=tk.X)
        
        # Lista de archivos seleccionados
        self.files_listbox = tk.Listbox(main_frame, height=8)
        self.files_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Etiqueta y barra de progreso
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
                # Añadir timeout para evitar bloqueos indefinidos
                connect_timeout=3
            )
            cur = conn.cursor()
            return conn, cur
        except psycopg2.Error as e:
            self.logger.error(f"Error de conexión a la base de datos: {str(e)}")
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            raise

    def standardize_date(self, date_value: Any) -> Optional[datetime.date]:
        """Estandariza diferentes formatos de fecha"""
        try:
            if isinstance(date_value, str):
                if '/' in date_value:
                    return datetime.strptime(date_value, '%d/%m/%Y').date()
                return datetime.strptime(date_value, '%Y%m%d').date()
            elif isinstance(date_value, datetime):
                return date_value.date()
            return None
        except ValueError as e:
            self.logger.warning(f"Error al procesar fecha {date_value}: {str(e)}")
            return None

    def process_record(self, record: Dict) -> tuple:
        """Procesa y valida un registro individual"""
        cedula = record.get('cedula', '').strip()
        nombre = record.get('nombre', '').strip()
        apellido = record.get('apellido', '').strip()
        sexo = record.get('sexo', '').strip()
        fec_nac = self.standardize_date(record.get('fec_nac'))
        direcc = record.get('direcc', '').strip()
        
        # Validaciones básicas
        if not cedula:
            raise ValueError("Cédula es obligatoria")
        
        return (cedula, nombre, apellido, sexo, fec_nac, direcc)

    def select_files(self):
        """Permite al usuario seleccionar archivos DBF"""
        file_paths = filedialog.askopenfilenames(
            title="Seleccionar archivos DBF",
            filetypes=[("DBF Files", "*.dbf")]
        )
        
        self.tables = list(file_paths)
        self.files_listbox.delete(0, tk.END)
        
        for file_path in self.tables:
            self.files_listbox.insert(tk.END, os.path.basename(file_path))

    def load_data(self):
        """Carga los datos de los archivos DBF a PostgreSQL"""
        if not self.tables:
            messagebox.showwarning("Advertencia", "Por favor seleccione archivos DBF primero")
            return

        try:
            conn, cur = self.get_db_connection()
            total_records = 0
            processed_records = 0
            
            # Primer pasada para contar registros totales
            for table_path in self.tables:
                table = dbfread.DBF(table_path, lowernames=True)
                total_records += len(table)
            
            self.progress_bar['maximum'] = total_records
            
            # Procesar los archivos
            for table_path in self.tables:
                try:
                    table = dbfread.DBF(table_path, lowernames=True)
                    records_to_insert = []
                    
                    for record in table:
                        try:
                            processed_record = self.process_record(record)
                            records_to_insert.append(processed_record)
                            processed_records += 1
                            
                            # Actualizar progreso cada 100 registros
                            if processed_records % 100 == 0:
                                self.progress_bar['value'] = processed_records
                                self.progress_label.config(
                                    text=f"Procesando: {processed_records}/{total_records} registros"
                                )
                                self.window.update()
                            
                        except ValueError as e:
                            self.logger.warning(f"Error en registro: {str(e)}")
                            continue
                    
                    # Inserción por lotes
                    execute_batch(cur, """
                        INSERT INTO Cedulas 
                        (numero_cedula, nombre, apellido, sexo, fecha_nacimiento, direccion)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (numero_cedula) DO NOTHING
                    """, records_to_insert, page_size=1000)
                    
                except Exception as e:
                    self.logger.error(f"Error procesando archivo {table_path}: {str(e)}")
                    messagebox.showerror("Error", f"Error al procesar {os.path.basename(table_path)}")
                    continue
            
            conn.commit()
            self.logger.info(f"Proceso completado. {processed_records} registros procesados.")
            messagebox.showinfo("Éxito", "Datos cargados correctamente")
            
        except Exception as e:
            self.logger.error(f"Error general: {str(e)}")
            messagebox.showerror("Error", "Ocurrió un error durante la carga")
            
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
            self.progress_label.config(text="Proceso completado")

    def run(self):
        """Inicia la aplicación"""
        self.window.mainloop()

if __name__ == "__main__":
    app = DBFLoader()
    app.run()
