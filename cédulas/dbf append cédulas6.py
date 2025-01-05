import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import psycopg2
from datetime import datetime
import dbf
import threading
import re
from typing import Dict, List, Optional
import os


class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL DBF a PostgreSQL")
        self.root.geometry("1200x800")
        
        # Variables
        self.files_selected: List[str] = []
        self.mappings: Dict[str, Dict] = {}  # Mapeo por archivo
        self.total_records = 0
        
        # Columnas destino PostgreSQL
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
            'direccion', 'barrio', 'distrito', 'dpto', 'lugar_nacimiento',
            'fecha_defuncion', 'zona'  # Añadido "zona"
        ]

        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal con scrollbar
        main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame para archivos
        files_frame = ttk.LabelFrame(scrollable_frame, text="Archivos DBF", padding="5")
        files_frame.pack(fill="x", padx=5, pady=5)

        # Botón selección de archivos
        ttk.Button(files_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5)

        # Lista de archivos
        self.files_listbox = tk.Listbox(files_frame, width=100, height=5)
        self.files_listbox.pack(pady=5)

        # Frame para mapeo
        self.mapping_frame = ttk.LabelFrame(scrollable_frame, text="Mapeo de columnas", padding="5")
        self.mapping_frame.pack(fill="x", padx=5, pady=5)

        # Barra de progreso
        progress_frame = ttk.Frame(scrollable_frame)
        progress_frame.pack(fill="x", padx=5, pady=5)

        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(pady=5)

        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack(pady=5)

        self.total_label = ttk.Label(progress_frame, text="Total registros procesados: 0")
        self.total_label.pack(pady=5)

        # Botón procesar
        ttk.Button(scrollable_frame, text="Procesar", command=self.process_files).pack(pady=10)

        # Configurar el layout del scroll
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_files(self):
        """Seleccionar archivos DBF y mostrar opciones de mapeo."""
        files = filedialog.askopenfilenames(filetypes=[("DBF files", "*.dbf")])
        if not files:
            return

        self.files_selected = list(files)
        self.files_listbox.delete(0, tk.END)

        # Limpiar frame de mapeo
        for widget in self.mapping_frame.winfo_children():
            widget.destroy()

        # Mostrar archivos seleccionados y crear mapeo para cada uno
        for file_path in self.files_selected:
            file_name = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, file_path)

            # Crear frame para el archivo
            file_frame = ttk.LabelFrame(self.mapping_frame, text=file_name, padding="5")
            file_frame.pack(fill="x", padx=5, pady=5)

            # Obtener columnas del archivo DBF
            dbf_columns = self.get_dbf_columns(file_path)

            # Crear mapeo para cada columna PostgreSQL
            self.mappings[file_path] = {}

            # Grid para organizar los combobox
            for i, pg_col in enumerate(self.pg_columns):
                row = i // 3
                col = i % 3

                # Frame para cada mapeo
                mapping_pair = ttk.Frame(file_frame)
                mapping_pair.grid(row=row, column=col, padx=5, pady=2)

                ttk.Label(mapping_pair, text=f"{pg_col}:").pack(side="left")
                combo = ttk.Combobox(mapping_pair, values=[''] + dbf_columns, width=20)
                combo.pack(side="left", padx=2)

                # Autoseleccionar si hay coincidencia exacta o similar
                for dbf_col in dbf_columns:
                    if dbf_col.lower() in pg_col.lower() or pg_col.lower() in dbf_col.lower():
                        combo.set(dbf_col)
                        break

                self.mappings[file_path][pg_col] = combo

    def get_dbf_columns(self, file_path: str) -> List[str]:
        """Obtener las columnas de un archivo DBF."""
        try:
            table = dbf.Table(file_path)
            table.open()
            columns = table.field_names
            table.close()
            return columns
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo {os.path.basename(file_path)}: {str(e)}")
            return []
def _process_files_worker(self):
    """Lógica principal del procesamiento de archivos."""
    try:
        conn = psycopg2.connect(
            dbname="Gabriela_Fragancias",
            user="postgres",
            password="salmos23",
            host="localhost"
        )
        cursor = conn.cursor()

        total_files = len(self.files_selected)
        self.progress['maximum'] = total_files
        records_processed = 0

        def update_progress():
            self.progress['value'] = i + 1

        for i, file_path in enumerate(self.files_selected):
            file_name = os.path.basename(file_path)
            self.root.after(0, lambda: self.progress_label.config(text=f"Procesando {file_name}..."))

            # Leer archivo DBF
            table = dbf.Table(file_path)
            table.open()
            df = pd.DataFrame(list(table))
            table.close()

            # Transformar y cargar los datos
            transformed_data = self.transform_data(df, file_path)
            if transformed_data:
                self.load_to_postgresql(cursor, transformed_data)

            conn.commit()
            records_processed += len(transformed_data)
            self.root.after(0, update_progress)

        cursor.close()
        conn.close()

        self.root.after(0, lambda: self.progress_label.config(text="¡Proceso completado!"))
        self.root.after(0, lambda: self.total_label.config(text=f"Total registros procesados: {records_processed}"))
        messagebox.showinfo("Éxito", f"ETL completado exitosamente\nRegistros procesados: {records_processed}")
    except Exception as e:
        self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}"))
