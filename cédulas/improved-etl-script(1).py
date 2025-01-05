import tkinter as tk 
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import psycopg2
from datetime import datetime
import dbfread
import csv
from typing import Dict, List, Optional, Any, Union
import os
import re
import logging
from psycopg2.extras import execute_batch
from configparser import ConfigParser

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
        self.root.title("ETL CSV a PostgreSQL")
        self.root.geometry("1200x800")
        
        # Configurar logging
        self._setup_logging()
        
        # Cargar configuración de base de datos
        self.db_config = DatabaseConfig()
        
        # Variables
        self.files_selected: List[str] = []
        self.mappings: Dict[str, Dict] = {}
        
        # Columnas destino PostgreSQL según la estructura proporcionada
        self.pg_columns = [
            'numero_cedula',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'sexo',
            'direccion',
            'id_barrio',
            'id_distrito',
            'id_dpto',
            'zona',
            'id_via',
            'lugar_nacimiento',
            'fecha_defuncion',
            'email'
        ]
        
        self.create_widgets()
        
        # Verificar conexión a la base de datos al inicio
        self.verify_database_connection()
    
    def _setup_logging(self):
        """Configurar el sistema de logging."""
        logging.basicConfig(
            filename='etl_process.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def verify_database_connection(self):
        """Verificar la conexión a la base de datos y la existencia de la tabla."""
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # Verificar si existe el schema
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT 1 FROM information_schema.schemata 
                            WHERE schema_name = 'gf'
                        );
                    """)
                    schema_exists = cursor.fetchone()[0]
                    
                    if not schema_exists:
                        cursor.execute("CREATE SCHEMA gf;")
                        conn.commit()
                    
                    # Verificar si existe la tabla
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT 1 FROM information_schema.tables 
                            WHERE table_schema = 'gf' 
                            AND table_name = 'cedulas'
                        );
                    """)
                    table_exists = cursor.fetchone()[0]
                    
                    if not table_exists:
                        self.create_table(cursor)
                        conn.commit()
                        
            messagebox.showinfo("Conexión exitosa", 
                              "Conexión a la base de datos verificada correctamente")
        except Exception as e:
            logging.error(f"Error de conexión a la base de datos: {str(e)}")
            messagebox.showerror("Error de conexión", 
                               f"No se pudo conectar a la base de datos: {str(e)}")
    
    def create_table(self, cursor):
        """Crear la tabla si no existe con la estructura exacta proporcionada."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gf.cedulas (
                numero_cedula character varying(20) NOT NULL,
                nombre character varying(100) NOT NULL,
                apellido character varying(100) NOT NULL,
                fecha_nacimiento date,
                sexo character(1),
                direccion text,
                id_barrio character varying(3),
                id_distrito character varying(2),
                id_dpto character varying(2),
                zona character varying(2),
                id_via character varying(50),
                lugar_nacimiento character varying(100),
                fecha_defuncion date,
                email character varying(100),
                created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
                updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
            );
        """)

    def get_db_connection(self):
        """Obtener conexión a la base de datos usando la configuración."""
        return psycopg2.connect(**self.db_config.config)

    def create_widgets(self):
        # Frame principal con scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        # Crear canvas con scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configuración del grid
        main_frame.grid_columnconfigure(0, weight=1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para archivos
        files_frame = ttk.LabelFrame(self.scrollable_frame, text="Archivos DBF", padding="5")
        files_frame.pack(fill="x", padx=5, pady=5)
        
        # Botones de acción
        button_frame = ttk.Frame(files_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Seleccionar archivos", 
                  command=self.select_files).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpiar selección", 
                  command=self.clear_selection).pack(side="left", padx=5)
        
        # Lista de archivos con scrollbar
        list_frame = ttk.Frame(files_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.files_listbox = tk.Listbox(list_frame, height=5)
        list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                     command=self.files_listbox.yview)
        
        self.files_listbox.configure(yscrollcommand=list_scrollbar.set)
        self.files_listbox.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")
        
        # Frame para mapeo
        self.mapping_frame = ttk.LabelFrame(self.scrollable_frame, 
                                          text="Mapeo de columnas", padding="5")
        self.mapping_frame.pack(fill="x", padx=5, pady=5)
        
        # Frame para progreso
        progress_frame = ttk.LabelFrame(self.scrollable_frame, 
                                      text="Progreso", padding="5")
        progress_frame.pack(fill="x", padx=5, pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, length=400, 
                                      mode='determinate')
        self.progress.pack(pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack(pady=5)
        
        # Botones de proceso
        process_frame = ttk.Frame(self.scrollable_frame)
        process_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(process_frame, text="Procesar archivos", 
                  command=self.process_files).pack(side="left", padx=5)
        ttk.Button(process_frame, text="Cancelar", 
                  command=self.cancel_process).pack(side="left", padx=5)

    def clear_selection(self):
        """Limpiar la selección de archivos y el mapeo."""
        self.files_selected.clear()
        self.files_listbox.delete(0, tk.END)
        self.mappings.clear()
        
        for widget in self.mapping_frame.winfo_children():
            widget.destroy()
        
        self.progress['value'] = 0
        self.progress_label['text'] = ""

    def cancel_process(self):
        """Cancelar el proceso de ETL."""
        self.processing_cancelled = True
        logging.info("Proceso cancelado por el usuario")
        self.progress_label['text'] = "Proceso cancelado"

    def select_files(self):
        """Seleccionar archivos CSV."""
        try:
            files = filedialog.askopenfilenames(
                title="Seleccionar archivos",
                filetypes=[("CSV files", "*.csv")]
            )
            
            if not files:
                return
                
            self.files_selected = list(files)
            self.files_listbox.delete(0, tk.END)
            
            # Limpiar frame de mapeo
            for widget in self.mapping_frame.winfo_children():
                widget.destroy()
                
            # Procesar cada archivo seleccionado
            for file_path in self.files_selected:
                self._process_file_selection(file_path)
                
        except Exception as e:
            logging.error(f"Error en la selección de archivos: {str(e)}")
            messagebox.showerror("Error", f"Error al seleccionar archivos: {str(e)}")

    def get_csv_columns(self, file_path: str) -> List[str]:
        """Obtener las columnas de un archivo CSV."""
        try:
            # Intentar diferentes encodings
            encodings = ['utf-8', 'latin1', 'iso-8859-1']
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, nrows=1, encoding=encoding)
                    return list(df.columns)
                except UnicodeDecodeError:
                    continue
            raise Exception("No se pudo determinar la codificación del archivo")
        except Exception as e:
            logging.error(f"Error leyendo columnas de {file_path}: {str(e)}")
            messagebox.showerror("Error", 
                               f"Error al leer el archivo {os.path.basename(file_path)}: {str(e)}")
            return []

    def transform_date(self, date_value: Any) -> Optional[datetime.date]:
        """Transformar diferentes formatos de fecha identificados en los archivos."""
        if pd.isna(date_value):
            return None
            
        try:
            if isinstance(date_value, (int, float)):
                date_str = str(int(date_value))
                if len(date_str) == 8:
                    return datetime.strptime(date_str, '%Y%m%d').date()
            elif isinstance(date_value, str):
                for fmt in ('%Y%m%d', '%d/%m/%Y', '%Y-%m-%d'):
                    try:
                        return datetime.strptime(date_value, fmt).date()
                    except ValueError:
                        continue
                        
            elif isinstance(date_value, (int, float)):
                # Manejar fechas numéricas (YYYYMMDD)
                date_str = str(int(date_value))
                if len(date_str) == 8:
                    return datetime.strptime(date_str, '%Y%m%d').date()
                    
        except Exception as e:
            logging.error(f"Error transformando fecha {date_value}: {str(e)}")
        return None

    def clean_text(self, text: Any) -> Optional[str]:
        """Limpiar y normalizar texto."""
        if pd.isna(text):
            return None
        text = str(text).strip()
        text = re.sub(r'\s+', ' ', text)
        text = text.upper()
        return text if text else None

    def transform_sex(self, sex_value: Any) -> Optional[str]:
        """Normalizar valor de sexo a M/F."""
        if pd.isna(sex_value):
            return None
        sex_value = str(sex_value).upper().strip()
        if sex_value in ['M', '1', 'MASCULINO']:
            return 'M'
        elif sex_value in ['F', '2', 'FEMENINO']:
            return 'F'
        return None

    def process_files(self):
        """Procesar archivos CSV y cargar a PostgreSQL."""
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return

        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                
                total_files = len(self.files_selected)
                self.progress['maximum'] = total_files
                records_processed = 0
                duplicates_found = 0
                self.processing_cancelled = False

                for i, file_path in enumerate(self.files_selected):
                    if self.processing_cancelled:
                        break
                        
                    try:
                        # Detectar encoding
                        encoding = self._detect_file_encoding(file_path)
                        
                        # Leer archivo CSV con pandas
                        df = pd.read_csv(file_path, encoding=encoding, low_memory=False)
                        
                        # Obtener mapeo para este archivo
                        file_mapping = self.mappings[file_path]
                        
                        # Procesar registros
                        batch_data = []
                        for _, row in df.iterrows():
                            if self.processing_cancelled:
                                break
                                
                            transformed_record = self._transform_record(row, file_mapping)
                            
                            # Mapear y transformar cada columna
                            for pg_col, combo in file_mapping.items():
                                dbf_col = combo.get()
                                if not dbf_col:
                                    continue

                                value = record.get(dbf_col)

                                # Aplicar transformaciones específicas
                                if pg_col == 'fecha_nacimiento':
                                    value = self.transform_date(value)
                                elif pg_col in ['nombre', 'apellido', 'lugar_nacimiento']:
                                    value = self.clean_text(value)
                                elif pg_col == 'sexo':
                                    value = self.transform_sex(value)
                                elif pg_col == 'numero_cedula':
                                    value = str(value).strip() if value else None

                                transformed_record[pg_col] = value

                            if transformed_record.get('numero_cedula'):
                                batch_data.append(transformed_record)
                                records_processed += 1

                            # Procesar en lotes de 1000 registros
                            if len(batch_data) >= 1000:
                                duplicates = self._insert_batch(cursor, batch_data)
                                duplicates_found += duplicates
                                batch_data = []

                        # Insertar registros restantes
                        if batch_data:
                            duplicates = self._insert_batch(cursor, batch_data)
                            duplicates_found += duplicates

                        conn.commit()
                        self.progress['value'] = i + 1
                        self.progress_label['text'] = f"Procesando... {i+1}/{total_files}"
                        self.root.update_idletasks()
                        
                    except Exception as e:
                        logging.error(f"Error procesando archivo {file_path}: {str(e)}")
                        messagebox.showerror("Error", 
                                           f"Error procesando archivo {os.path.basename(file_path)}: {str(e)}")

                if not self.processing_cancelled:
                    self.progress_label['text'] = (f"¡Proceso completado! {records_processed} registros procesados, "
                                                 f"{duplicates_found} duplicados actualizados")
                    messagebox.showinfo("Éxito", 
                                      f"ETL completado exitosamente\n"
                                      f"Archivos procesados: {total_files}\n"
                                      f"Registros procesados: {records_processed}\n"
                                      f"Duplicados actualizados: {duplicates_found}")

        except Exception as e:
            logging.error(f"Error durante el procesamiento: {str(e)}")
            messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")

    def _detect_file_encoding(self, file_path: str) -> str:
        """Detectar la codificación del archivo."""
        encodings = ['utf-8', 'latin1', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except UnicodeDecodeError:
                continue
        return 'latin1'  # Default fallback

    def _transform_record(self, row: pd.Series, file_mapping: Dict) -> Dict:
        """Transformar un registro según el mapeo y reglas de negocio."""
        transformed_record = {}
        
        for pg_col, combo in file_mapping.items():
            csv_col = combo.get()
            if not csv_col:
                continue

            value = row.get(csv_col)

            # Aplicar transformaciones específicas
            if pg_col == 'numero_cedula':
                value = str(value).strip() if pd.notna(value) else None
            elif pg_col in ['nombre', 'apellido']:
                value = self.clean_text(value)
                if not value:  # Campos obligatorios
                    continue
            elif pg_col == 'fecha_nacimiento':
                value = self.transform_date(value)
            elif pg_col == 'sexo':
                value = self.transform_sex(value)
            elif pg_col in ['id_barrio', 'id_distrito', 'id_dpto']:
                value = str(value).strip() if pd.notna(value) else None
            elif pg_col == 'direccion':
                value = self.clean_text(value)
            elif pg_col == 'fecha_defuncion':
                value = self.transform_date(value)
            else:
                value = str(value).strip() if pd.notna(value) else None

            transformed_record[pg_col] = value
            
        return transformed_record

    def _insert_batch(self, cursor, batch_data: List[Dict]) -> int:
        """Insertar un lote de registros en la base de datos."""
        if not batch_data:
            return 0
            
        columns = batch_data[0].keys()
        values = [[record.get(col) for col in columns] for record in batch_data]
        
        # Consulta con ON CONFLICT para manejar duplicados
        insert_query = f"""
            INSERT INTO gf.cedulas ({', '.join(columns)})
            VALUES ({', '.join(['%s'] * len(columns))})
            ON CONFLICT (numero_cedula) 
            DO UPDATE SET 
                nombre = EXCLUDED.nombre,
                apellido = EXCLUDED.apellido,
                fecha_nacimiento = COALESCE(EXCLUDED.fecha_nacimiento, gf.cedulas.fecha_nacimiento),
                sexo = COALESCE(EXCLUDED.sexo, gf.cedulas.sexo),
                direccion = COALESCE(EXCLUDED.direccion, gf.cedulas.direccion),
                id_barrio = COALESCE(EXCLUDED.id_barrio, gf.cedulas.id_barrio),
                id_distrito = COALESCE(EXCLUDED.id_distrito, gf.cedulas.id_distrito),
                id_dpto = COALESCE(EXCLUDED.id_dpto, gf.cedulas.id_dpto),
                zona = COALESCE(EXCLUDED.zona, gf.cedulas.zona),
                id_via = COALESCE(EXCLUDED.id_via, gf.cedulas.id_via),
                lugar_nacimiento = COALESCE(EXCLUDED.lugar_nacimiento, gf.cedulas.lugar_nacimiento),
                fecha_defuncion = COALESCE(EXCLUDED.fecha_defuncion, gf.cedulas.fecha_defuncion),
                email = COALESCE(EXCLUDED.email, gf.cedulas.email),
                updated_at = CURRENT_TIMESTAMP
            RETURNING (xmax = 0) AS inserted;
        """
        
        duplicate_count = 0
        for value in values:
            cursor.execute(insert_query, value)
            if not cursor.fetchone()[0]:  # False means it was an update
                duplicate_count += 1
                
        return duplicate_count
        execute_batch(cursor, insert_query, values, page_size=1000)
    # ... [resto del código permanece igual]

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
