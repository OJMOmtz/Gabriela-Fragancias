import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
from typing import Optional, Any, Dict
import os
from psycopg2.extras import execute_batch

# Asegúrate de ajustar estos según tus necesidades
DB_HOST = "localhost"
DB_NAME = "Gabriela_Fragancias"
DB_USER = "postgres"
DB_PASSWORD = "salmos23"

def normalize_column_name(column_name: str) -> str:
    """Normaliza los nombres de las columnas de los archivos DBF a un conjunto estándar"""
    column_name = column_name.lower()
    if 'direc' in column_name:
        return 'direccion'
    elif 'distri' in column_name:
        return 'id_distrito'
    elif 'depar' in column_name:
        return 'id_dpto'
    elif 'zona' in column_name:
        return 'zona'
    elif 'lug_nac' in column_name:
        return 'lugar_nacimiento'
    else:
        return column_name

class DBFLoader:
    def __init__(self):
        self.tables = []
        self.new_columns = set()  # Conjunto para almacenar nombres de columnas nuevas
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
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
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
        processed_record = {
            'numero_cedula': str(record.get('cedula', '')).strip(),
            'nombre': str(record.get('nombre', '')).strip(),
            'apellido': str(record.get('apellido', '')).strip(),
            'sexo': str(record.get('sexo', '')).strip(),
            'fecha_nacimiento': self.standardize_date(record.get('fec_nac')),
            'direccion': str(record.get('direccion', '')).strip(),
            'id_distrito': str(record.get('id_distrito', '')).strip(),
            'id_dpto': str(record.get('id_dpto', '')).strip(),
            'zona': str(record.get('zona', '')).strip(),
            'lugar_nacimiento': str(record.get('lugar_nac', '')).strip(),
            'fecha_defuncion': self.standardize_date(record.get('fec_def'))
        }
        
        # Detectar columnas nuevas
        for column in record.keys():
            normalized_column = normalize_column_name(column)
            if normalized_column not in processed_record:
                self.new_columns.add(normalized_column)
                processed_record[normalized_column] = str(record[column])
                
        # Normalizar nombres de columnas
        processed_record = {normalize_column_name(k): v for k, v in processed_record.items()}
        
        return tuple(processed_record.values())

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
            
            # Agregar columnas nuevas a la tabla
            for column in self.new_columns:
                cur.execute(f"ALTER TABLE gf.cedulas ADD COLUMN {column} text;")
            conn.commit()
            
            # Construir la consulta SQL de inserción dinámicamente
            insert_query = """
                INSERT INTO gf.cedulas 
                ({})
                VALUES ({})
                ON CONFLICT (numero_cedula) DO NOTHING
            """
            columns = ['numero_cedula', 'nombre', 'apellido', 'sexo', 'fecha_nacimiento', 'direccion', 'id_distrito', 'id_dpto', 'zona', 'lugar_nacimiento', 'fecha_defuncion'] + list(self.new_columns)
            placeholders = ['%s'] * len(columns)
            insert_query = insert_query.format(','.join(columns), ','.join(placeholders))
            
            total_records = 0
            processed_records = 0
            
            # Primer pasada para contar registros totales
            for table_path in self.tables:
                table = dbfread.DBF(table_path, lowernames=True, encoding='latin1')
                total_records += len(table)
            
            self.progress_bar['maximum'] = total_records
            
            # Procesar los archivos
            for table_path in self.tables:
                try:
                    table = dbfread.DBF(table_path, lowernames=True, encoding='latin1')
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
                    execute_batch(cur, insert_query, records_to_insert, page_size=1000)
                    
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
