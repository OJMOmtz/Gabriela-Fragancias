import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import psycopg2
from datetime import datetime
import dbfread
import csv
from typing import Dict, List, Optional, Any
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
        self.root.title("ETL DBF a PostgreSQL")
        self.root.geometry("1200x800")
        
        # Configurar logging
        self._setup_logging()
        
        # Cargar configuración de base de datos
        self.db_config = DatabaseConfig()
        
        # Variables
        self.files_selected: List[str] = []
        self.mappings: Dict[str, Dict] = {}
        self.processing_cancelled = False
        
        # Columnas destino PostgreSQL
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'sexo',
            'fecha_nacimiento', 'lugar_nacimiento', 'direccion',
            'id_barrio', 'id_distrito', 'id_dpto', 'zona',
            'fecha_defuncion',
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
        """Crear la tabla si no existe."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gf.cedulas (
                numero_cedula VARCHAR(20) PRIMARY KEY,
                nombre VARCHAR(100),
                apellido VARCHAR(100),
                sexo CHAR(1),
                fecha_nacimiento DATE,
                lugar_nacimiento VARCHAR(100),
                direccion VARCHAR(200),
                id_barrio INTEGER,
                id_distrito INTEGER,
                id_dpto INTEGER,
                zona VARCHAR(50),
                fecha_defuncion DATE,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear índices si no existen
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_cedulas_nombre') THEN
                    CREATE INDEX idx_cedulas_nombre ON gf.cedulas(nombre);
                END IF;
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_cedulas_apellido') THEN
                    CREATE INDEX idx_cedulas_apellido ON gf.cedulas(apellido);
                END IF;
            END$$;
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
        """Seleccionar archivos DBF y mostrar opciones de mapeo."""
        try:
            files = filedialog.askopenfilenames(
                title="Seleccionar archivos DBF",
                filetypes=[("DBF files", "*.dbf")]
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

    def _process_file_selection(self, file_path: str):
        """Procesar la selección de un archivo individual."""
        try:
            file_name = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, file_path)
            
            # Crear frame para el archivo
            file_frame = ttk.LabelFrame(self.mapping_frame, text=file_name, padding="5")
            file_frame.pack(fill="x", padx=5, pady=5)
            
            # Obtener columnas del archivo DBF
            dbf_columns = self.get_dbf_columns(file_path)
            if not dbf_columns:
                return
                
            # Inicializar mapeo para este archivo
            self.mappings[file_path] = {}
            
            # Crear grid para los combobox
            self._create_mapping_grid(file_frame, dbf_columns, file_path)
            
        except Exception as e:
            logging.error(f"Error procesando archivo {file_path}: {str(e)}")
            messagebox.showerror("Error", 
                               f"Error procesando archivo {file_name}: {str(e)}")

    def _create_mapping_grid(self, frame: ttk.Frame, dbf_columns: List[str], 
                           file_path: str):
        """Crear grid de mapeo para un archivo."""
        for i, pg_col in enumerate(self.pg_columns):
            row = i // 3
            col = i % 3
            
            # Frame para cada mapeo
            mapping_pair = ttk.Frame(frame)
            mapping_pair.grid(row=row, column=col, padx=5, pady=2)
            
            ttk.Label(mapping_pair, text=f"{pg_col}:").pack(side="left")
            combo = ttk.Combobox(mapping_pair, values=[''] + dbf_columns, width=20)
            combo.pack(side="left", padx=2)
            
            # Autoseleccionar columna si hay coincidencia
            self._auto_select_column(combo, pg_col, dbf_columns)
            
            self.mappings[file_path][pg_col] = combo

    def _auto_select_column(self, combo: ttk.Combobox, pg_col: str, 
                          dbf_columns: List[str]):
        """Autoseleccionar columna basado en coincidencia de nombres."""
        pg_col_clean = pg_col.lower().replace('_', '')
        best_match = None
        best_ratio = 0
        
        for dbf_col in dbf_columns:
            dbf_col_clean = dbf_col.lower().replace('_', '')
            
            # Coincidencia exacta
            if dbf_col_clean == pg_col_clean:
                combo.set(dbf_col)
                return
            
            # Coincidencia parcial
            if (dbf_col_clean in pg_col_clean or 
                pg_col_clean in dbf_col_clean):
                ratio = len(set(dbf_col_clean) & set(pg_col_clean)) / \
                       len(set(dbf_col_clean) | set(pg_col_clean))
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = dbf_col
        
        if best_match and best_ratio > 0.5:
            combo.set(best_match)

    def get_dbf_columns(self, file_path: str) -> List[str]:
        """Obtener las columnas de un archivo DBF."""
        try:
            table = dbfread.DBF(file_path)
            return table.field_names
        except Exception as e