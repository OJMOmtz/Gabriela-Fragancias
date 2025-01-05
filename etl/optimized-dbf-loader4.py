import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
import csv
import json
import os
from psycopg2.extras import execute_batch
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
import io
import time
from collections import defaultdict

class DBFLoader:
    def __init__(self):
        self.tables = []
        self.setup_logging()
        self.setup_ui()
        self.batch_size = 5000
        self.queue = queue.Queue(maxsize=10000)
        self.processing = False
        self.duplicate_counter = defaultdict(int)
        self.duplicate_log = []
        self.processed_cedulas = set()
        self.duplicates_file = 'duplicados.csv'

        # Configuración de la base de datos con parámetros optimizados
        self.db_config = {
            "host": "localhost",
            "database": "Gabriela_Fragancias",
            "user": "postgres",
            "password": "salmos23",
            "port": 5432,
            "connect_timeout": 3,
            "application_name": "bulk_loader",
            # Parámetros de rendimiento de PostgreSQL
            "options": "-c synchronous_commit=off -c work_mem=64MB -c maintenance_work_mem=512MB"
        }
        with open('config.json') as config_file:
            self.db_config = json.load(config_file)

        
        with open('config.json') as config_file:
            self.db_config = json.load(config_file)

    def db_worker(self):
        """Worker thread for database operations."""
    try:
        with psycopg2.connect(**self.db_config) as conn:
            with conn.cursor() as cur:
                while self.processing or not self.queue.empty():
                    records = self.queue.get()
                    if records:
                        self._insert_batch(cur, records)
                        self.queue.task_done()
    except Exception as e:
        self.logger.error(f"Error in db_worker: {str(e)}")

    def setup_logging(self):
        """Configura el logging"""
        self.logger = logging.getLogger('DBFLoader')
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler('dbf_loader.log')
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def log_duplicate(self, cedula, record_actual, record_anterior):
        """Registra información sobre cédulas duplicadas"""
        self.duplicate_counter[cedula] += 1
        log_entry = {
            'cedula': cedula,
            'nombre_actual': record_actual[1],
            'apellido_actual': record_actual[2],
            'nombre_anterior': record_anterior[1] if record_anterior else 'N/A',
            'apellido_anterior': record_anterior[2] if record_anterior else 'N/A',
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.duplicate_log.append(log_entry)

    def save_duplicates_report(self):
        """Guarda un reporte de duplicados en CSV"""
        if self.duplicate_log:
            with open(self.duplicates_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'cedula', 'nombre_actual', 'apellido_actual', 
                    'nombre_anterior', 'apellido_anterior', 'fecha'
                ])
                writer.writeheader()
                writer.writerows(self.duplicate_log)

    def process_file_worker(self, table_path):
        """Worker para procesar un archivo DBF o CSV"""
        try:
            # Determinar el tipo de archivo
            file_extension = os.path.splitext(table_path)[1].lower()
            
            records = []
            if file_extension == '.dbf':
                # Procesar archivo DBF
                for record in dbfread.DBF(table_path, encoding='latin-1'):
                    records.append(record)
            elif file_extension == '.csv':
                # Procesar archivo CSV
                with open(table_path, 'r', encoding='latin-1') as f:
                    reader = csv.DictReader(f, delimiter=';')
                    for row in reader:
                        # Asegurar que los nombres de campo sean consistentes
                        record = {
                            'numero_cedula': row['CEDULA'].replace('.', ''),  # Eliminar separadores de miles
                            'nombre': row['NOMBRE'],
                            'apellido': row['APELLIDO'],
                            'fecha_nacimiento': row['FEC_NAC'],
                            'direccion': row['DIRECC'],
                            'id_barrio': row['BARRIO'],
                            'id_distrito': row['DISTRITO'],
                            'id_dpto': row['DEPART'],
                            'lugar_nacimiento': row['LUGNAC'],
                            'cedula': row['CEDULA'].replace('.', ''),  # Eliminar separadores de miles
                            'nombre': row['NOMBRE'],
                            'apellido': row['APELLIDO'],
                            'fec_nac': row['FEC_NAC'],
                            'direcc': row['DIRECC'],
                            'id_barrio': rpw['BARRIO'],
                            'id_distrito': row['COD_DIST'],
                            'id_dpto': row['COD_DPTO'],
                            'zona': row['ZONA']
                            
                        }
                        record = {
    # Completa los demás campos requeridos en la tabla cedulas
}
                        # Verificar si el registro ya existe antes de agregarlo
                        if record not in records:
                            records.append(record)
                        
            # Procesar registros en chunks
            for i in range(0, len(records), self.batch_size):
                chunk = records[i:i + self.batch_size]
                processed_chunk, chunk_duplicates = self.process_chunk(chunk)
                
                # Enviar chunk procesado a la cola para inserción en BD
                self.queue.put(processed_chunk)
                
                # Actualizar barra de progreso
                self.progress_bar['value'] += len(processed_chunk)
                
                # Procesar duplicados encontrados en el chunk
                for cedula, dup_records in chunk_duplicates.items():
                    for dup_record in dup_records:
                        self.log_duplicate(cedula, dup_record, None)
                
            self.logger.info(f"Procesamiento de {table_path} completado")
            
        except Exception as e:
            self.logger.error(f"Error procesando {table_path}: {str(e)}")
            
    def process_chunk(self, records):
        """Procesa un grupo de registros en memoria con validación de duplicados"""
        processed_records = []
        chunk_duplicates = defaultdict(list)
        
        for record in records:
            try:
                # Procesar campos básicos con validación mínima para velocidad
                cedula = str(record.get('cedula', record.get('Nroced', ''))).replace('.', '').strip()
                
                # Validación básica de cédula
                if not cedula or not cedula.isdigit():
                    continue
                
                # Si la cédula ya fue procesada en este archivo, la registramos como duplicada
                if cedula in self.processed_cedulas:
                    chunk_duplicates[cedula].append(record)
                    continue
                
                self.processed_cedulas.add(cedula)
                
                nombre = str(record.get('nombre', '')).strip()
                apellido = str(record.get('apellido', record.get('Apelli', ''))).strip()
                
                # Procesamiento de fecha
                fec_nac = None
                fecha_raw = record.get('fec_nac', record.get('fecha_nac', record.get('fechanac', '')))
                if fecha_raw:
                    try:
                        if isinstance(fecha_raw, str):
                            if '/' in fecha_raw:
                                dia, mes, anio = fecha_raw.split('/')
                                fec_nac = datetime(int(anio), int(mes), int(dia)).date()
                            else:
                                fec_nac = datetime.strptime(fecha_raw, '%Y%m%d').date()
                    except (ValueError, TypeError):
                        pass

                direcc = next((str(record.get(field, '')).strip() 
                             for field in ['direcc', 'direccion', 'direc', 'dir', 'domicilio'] 
                             if record.get(field)), '')

                processed_records.append((cedula, nombre, apellido, None, fec_nac, direcc))
                
            except Exception as e:
                self.logger.warning(f"Error procesando registro: {str(e)}")
                continue
                
        return processed_records, chunk_duplicates

    def _insert_batch(self, cur, records):
        """Inserta un batch de registros usando execute_batch con manejo de duplicados"""
        try:
            # Primero, verificamos qué registros ya existen
            cedulas = [record[0] for record in records]
            cur.execute("""
                SELECT numero_cedula, nombre, apellido, fecha_nacimiento, direccion 
                FROM Cedulas 
                WHERE numero_cedula = ANY(%s)
            """, (cedulas,))
            
            existing_records = {row[0]: row for row in cur.fetchall()}
            
            # Separar registros en nuevos y actualizaciones
            new_records = []
            update_records = []
            
            for record in records:
                cedula = record[0]
                if cedula in existing_records:
                    # Registrar el duplicado
                    self.log_duplicate(cedula, record, existing_records[cedula])
                    # Decidir si actualizar basado en la completitud de los datos
                    existing = existing_records[cedula]
                    if self.should_update_record(record, existing):
                        update_records.append(record)
                else:
                    new_records.append(record)
            
            # Insertar nuevos registros
            if new_records:
                execute_batch(cur, """
                    INSERT INTO Cedulas 
                    (numero_cedula, nombre, apellido, sexo, fecha_nacimiento, direccion, distrito, depart, zona)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, new_records, page_size=self.batch_size)
            
            # Actualizar registros existentes si es necesario
            if update_records:
                execute_batch(cur, """
                    UPDATE Cedulas 
                    SET nombre = CASE WHEN COALESCE(TRIM(%s), '') != '' THEN %s ELSE nombre END,
                        apellido = CASE WHEN COALESCE(TRIM(%s), '') != '' THEN %s ELSE apellido END,
                        sexo = CASE WHEN %s IS NOT NULL THEN %s ELSE sexo END,
                        fecha_nacimiento = CASE WHEN %s IS NOT NULL THEN %s ELSE fecha_nacimiento END,
                        direccion = CASE WHEN COALESCE(TRIM(%s), '') != '' THEN %s ELSE direccion END,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE numero_cedula = %s
                """, [(r[1], r[1], r[2], r[2], r[3], r[3], r[4], r[4], r[5], r[5], r[0]) 
                      for r in update_records], 
                    page_size=self.batch_size)
            
        except Exception as e:
            self.logger.error(f"Error en inserción batch: {str(e)}")
            raise

    def should_update_record(self, new_record, existing_record):
        """
        Decide si un registro existente debe ser actualizado basado en la completitud de los datos
        """
        # Desempaquetar registros
        _, new_nombre, new_apellido, _, new_fecha, new_direccion = new_record
        _, exist_nombre, exist_apellido, exist_fecha, exist_direccion = existing_record
        
        # Verificar si los nuevos datos son más completos
        update_needed = False
        
        # Comparar nombre y apellido
        if new_nombre and not exist_nombre:
            update_needed = True
        if new_apellido and not exist_apellido:
            update_needed = True
            
        # Comparar fecha
        if new_fecha and not exist_fecha:
            update_needed = True
            
        # Comparar dirección
        if new_direccion and not exist_direccion:
            update_needed = True
            
        return update_needed

    def load_data(self):
        """Inicia el proceso de carga de datos"""
        if not self.tables:
            messagebox.showwarning("Advertencia", "Por favor seleccione archivos primero")
            return

        try:
            self.processing = True
            self.progress_bar['value'] = 0
            
            # Iniciar worker de base de datos
            db_thread = threading.Thread(target=self.db_worker)
            db_thread.start()
            
            # Procesar archivos en parallel
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [
                    executor.submit(self.process_file_worker, table_path)
                    for table_path in self.tables
                ]
                
                # Esperar a que terminen todos los procesamientos
                for future in futures:
                    future.result()
            
            self.processing = False
            db_thread.join()
            
            # Al finalizar, guardar el reporte de duplicados
            self.save_duplicates_report()
            
            # Mostrar resumen de duplicados
            duplicates_summary = f"""
            Proceso completado:
            - Total registros procesados: {len(self.processed_cedulas)}
            - Duplicados encontrados: {len(self.duplicate_log)}
            - Reporte de duplicados guardado en: {self.duplicates_file}
            """
            
            messagebox.showinfo("Éxito", duplicates_summary)
            
        except Exception as e:
            self.logger.error(f"Error en load_data: {str(e)}")
            messagebox.showerror("Error", "Ocurrió un error durante la carga")
        finally:
            self.progress_label.config(text="Proceso completado")

    def select_files(self):
        """Permite al usuario seleccionar los archivos"""
        file_paths = filedialog.askopenfilenames(
            filetypes=[
                ("Archivos soportados", "*.dbf;*.csv;*.txt"),
                ("Archivos DBF", "*.dbf"),
                ("Archivos CSV", "*.csv"),
                ("Archivos TXT", "*.txt")
            ]
        )
        if file_paths:
            self.tables.clear()
            self.files_listbox.delete(0, tk.END)
            for file_path in file_paths:
                self.tables.append(file_path)
                self.files_listbox.insert(tk.END, os.path.basename(file_path))
    def is_valid_record(self, record):
        """Verifica si un registro tiene los campos requeridos"""
        required_fields = ['cedula', 'nombre', 'apellido']
        for field in required_fields:
            if not record.get(field):
                return False
        return True

    def process_csv_file(self, file_path):
        """Procesa un archivo CSV"""
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if self.is_valid_record(row):
                    self.queue.put(row)

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.window = tk.Tk()
        self.window.title("Cargador de Datos Masivos")
        self.window.geometry("500x400")

        # Crear frame principal con padding
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Estilo para los botones
        style = ttk.Style()
        style.configure('Action.TButton', padding=5)

        # Botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="Seleccionar Archivos", 
            command=self.select_files,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Iniciar Carga", 
            command=self.load_data,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)

        # Lista de archivos con scroll
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED
        )
        self.files_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)

        # Etiqueta y barra de progreso
        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.pack(pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(
            main_frame,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X)

    def run(self):
        """Inicia la aplicación"""
        self.window.mainloop()    # ... (Las demás funciones aquí) ...

if __name__ == "__main__":
    app = DBFLoader()
    app.run()
