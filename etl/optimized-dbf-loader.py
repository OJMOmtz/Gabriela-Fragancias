import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
import csv
import os
from psycopg2.extras import execute_batch
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
import io
import time

class DBFLoader:
    def __init__(self):
        self.tables = []
        self.setup_logging()
        self.setup_ui()
        self.batch_size = 5000  # Aumentado para mejor rendimiento
        self.queue = queue.Queue(maxsize=10000)  # Cola para procesamiento
        self.processing = False
        
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

    def setup_logging(self):
        """Configura el sistema de logging con rotación de archivos"""
        from logging.handlers import RotatingFileHandler
        
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_file = 'dbf_loader.log'
        
        handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        handler.setFormatter(log_formatter)
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)
        self.logger.addHandler(handler)

    def get_db_connection(self) -> tuple:
        """Establece una conexión optimizada a PostgreSQL"""
        try:
            conn = psycopg2.connect(**self.db_config)
            
            # Configurar la conexión para bulk loading
            conn.set_session(autocommit=False)
            cur = conn.cursor()
            
            # Desactivar temporalmente índices y triggers
            cur.execute("""
                ALTER TABLE Cedulas SET (autovacuum_enabled = false);
                ALTER TABLE Cedulas DISABLE TRIGGER ALL;
            """)
            
            return conn, cur
        except psycopg2.Error as e:
            self.logger.error(f"Error de conexión a la base de datos: {str(e)}")
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            raise

    def process_chunk(self, records):
        """Procesa un grupo de registros en memoria"""
        processed_records = []
        for record in records:
            try:
                # Procesar campos básicos con validación mínima para velocidad
                cedula = str(record.get('cedula', record.get('Nroced', ''))).replace('.', '').strip()
                if not cedula or not cedula.isdigit():
                    continue

                nombre = str(record.get('nombre', '')).strip()
                apellido = str(record.get('apellido', record.get('Apelli', ''))).strip()
                
                # Procesamiento rápido de fecha
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

                # Obtener dirección de múltiples campos posibles
                direcc = next((str(record.get(field, '')).strip() 
                             for field in ['direcc', 'direccion', 'direc', 'dir', 'domicilio'] 
                             if record.get(field)), '')

                processed_records.append((cedula, nombre, apellido, None, fec_nac, direcc))
                
            except Exception as e:
                self.logger.warning(f"Error procesando registro: {str(e)}")
                continue
                
        return processed_records

    def process_file_worker(self, file_path):
        """Worker para procesar archivos en un hilo separado"""
        try:
            file_size = os.path.getsize(file_path)
            processed_size = 0
            chunk = []
            
            # Determinar el tipo de archivo
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.dbf':
                table = dbfread.DBF(file_path, lowernames=True)
                records = table
            else:  # CSV o TXT
                with open(file_path, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file, delimiter=';')
                    records = [
                        {k.lower(): v for k, v in row.items()}
                        for row in csv_reader
                    ]

            for record in records:
                chunk.append(record)
                if len(chunk) >= 1000:  # Procesar en chunks para mejor memoria
                    processed_records = self.process_chunk(chunk)
                    self.queue.put(processed_records)
                    chunk = []
                    
                    # Actualizar progreso
                    if file_extension != '.dbf':
                        processed_size = file.tell()
                        progress = (processed_size / file_size) * 100
                        self.update_progress(progress)

            # Procesar el último chunk
            if chunk:
                processed_records = self.process_chunk(chunk)
                self.queue.put(processed_records)

        except Exception as e:
            self.logger.error(f"Error procesando archivo {file_path}: {str(e)}")
            messagebox.showerror("Error", f"Error al procesar {os.path.basename(file_path)}")

    def db_worker(self):
        """Worker para insertar datos en la base de datos"""
        try:
            conn, cur = self.get_db_connection()
            records_to_insert = []
            total_inserted = 0
            
            while self.processing or not self.queue.empty():
                try:
                    # Obtener registros de la cola con timeout
                    records = self.queue.get(timeout=1)
                    records_to_insert.extend(records)
                    
                    if len(records_to_insert) >= self.batch_size:
                        self._insert_batch(cur, records_to_insert)
                        conn.commit()
                        total_inserted += len(records_to_insert)
                        records_to_insert = []
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    self.logger.error(f"Error en inserción: {str(e)}")
                    continue
            
            # Insertar registros restantes
            if records_to_insert:
                self._insert_batch(cur, records_to_insert)
                conn.commit()
            
            # Reactivar índices y triggers
            cur.execute("""
                ALTER TABLE Cedulas SET (autovacuum_enabled = true);
                ALTER TABLE Cedulas ENABLE TRIGGER ALL;
                ANALYZE Cedulas;
            """)
            conn.commit()
            
        except Exception as e:
            self.logger.error(f"Error en db_worker: {str(e)}")
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()

    def _insert_batch(self, cur, records):
        """Inserta un batch de registros usando execute_batch"""
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
        """, records, page_size=self.batch_size)

    def update_progress(self, value):
        """Actualiza la barra de progreso de manera segura desde cualquier hilo"""
        if self.window:
            self.window.after(0, self._update_progress_ui, value)

    def _update_progress_ui(self, value):
        """Actualiza los elementos de la UI con el progreso"""
        self.progress_bar['value'] = value
        self.progress_label.config(text=f"Procesando: {value:.1f}%")
        self.window.update_idletasks()

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
            
            messagebox.showinfo("Éxito", "Proceso completado exitosamente")
            
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
        self.window.mainloop()

if __name__ == "__main__":
    app = DBFLoader()
    app.run()
