import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import psycopg2
from datetime import datetime
import dbf
import re
from typing import Dict, List
import os
import time
import threading

class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL DBF a PostgreSQL")
        self.root.geometry("1200x800")

        # Variables
        self.files_selected: List[str] = []
        self.mappings: Dict[str, Dict] = {}  # Mapeo por archivo
        self.dbf_tables = {}  # Guardar referencia a las tablas DBF

        # Columnas destino PostgreSQL
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'sexo',
            'fecha_nacimiento', 'lugar_nacimiento', 'direccion',
            'id_barrio', 'id_distrito', 'id_dpto', 'zona',
            'fecha_defuncion',
        ]

        self.create_widgets()

    def create_widgets(self):
        # Frame principal con scrollbar
        main_canvas = tk.Canvas(self.root)
        scrollbar_y = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollbar_x = ttk.Scrollbar(self.root, orient="horizontal", command=main_canvas.xview)
        scrollable_frame = ttk.Frame(main_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Frame para archivos
        files_frame = ttk.LabelFrame(scrollable_frame, text="Archivos DBF", padding="5")
        files_frame.pack(fill="x", padx=5, pady=5)

        # Botón selección de archivos
        ttk.Button(files_frame, text="Seleccionar archivos DBF", 
                  command=self.select_files).pack(pady=5)

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

        self.detail_label = ttk.Label(progress_frame, text="Detalles: 0 registros procesados, tiempo estimado: --")
        self.detail_label.pack(pady=5)

        # Botón procesar
        ttk.Button(scrollable_frame, text="Procesar", 
                  command=self.start_processing).pack(pady=10)

        # Configurar el layout del scroll
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

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

    def transform_date(self, date_value):
        """Transformar diferentes formatos de fecha a fecha PostgreSQL."""
        if pd.isna(date_value):
            return None
            
        try:
            if isinstance(date_value, (int, float)):
                # Convertir fecha numérica (YYYYMMDD)
                date_str = str(int(date_value))
                if len(date_str) == 8:
                    return datetime.strptime(date_str, '%Y%m%d').date()
            elif isinstance(date_value, str):
                # Intentar varios formatos comunes
                for fmt in ('%Y%m%d', '%d/%m/%Y', '%Y-%m-%d'):
                    try:
                        return datetime.strptime(date_value, fmt).date()
                    except ValueError:
                        continue
            elif isinstance(date_value, datetime):
                return date_value.date()
                
        except Exception as e:
            print(f"Error transformando fecha {date_value}: {str(e)}")
        return None

    def clean_text(self, text):
        """Limpiar y normalizar texto."""
        if pd.isna(text):
            return None
        text = str(text).strip()
        text = re.sub(r'\s+', ' ', text)
        text = text.upper()  # Normalizar a mayúsculas
        return text if text else None

    def transform_sex(self, sex_value):
        """Normalizar valor de sexo a M/F."""
        if pd.isna(sex_value):
            return None
        sex_value = str(sex_value).upper().strip()
        if sex_value in ['M', '1', 'MASCULINO']:
            return 'M'
        elif sex_value in ['F', '2', 'FEMENINO']:
            return 'F'
        return None

    def start_processing(self):
        """Iniciar el procesamiento en un hilo separado."""
        threading.Thread(target=self.process_files).start()

    def process_files(self):
        """Procesar los archivos DBF seleccionados y cargar a PostgreSQL."""
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return

        try:
            # Configuración de conexión PostgreSQL
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
            start_time = time.time()

            for i, file_path in enumerate(self.files_selected):
                file_name = os.path.basename(file_path)
                self.progress_label['text'] = f"Procesando {file_name}..."

                # Leer archivo DBF
                try:
                    table = dbf.Table(file_path)
                    table.open()
                    
                    # Convertir a DataFrame para proceso más eficiente
                    df = pd.DataFrame(list(table))
                    table.close()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al procesar {file_name}: {e}")
                    continue

                # Obtener mapeo para este archivo
                file_mapping = self.mappings[file_path]

                # Aplicar transformaciones
                transformed_data = []
                for _, row in df.iterrows():
                    record = {}
                    for pg_col, combo in file_mapping.items():
                        dbf_col = combo.get()
                        value = row.get(dbf_col, None)

                        if pg_col == 'fecha_nacimiento' or pg_col == 'fecha_defuncion':
                            record[pg_col] = self.transform_date(value)
                        elif pg_col == 'sexo':
                            record[pg_col] = self.transform_sex(value)
                        elif isinstance(value, str):
                            record[pg_col] = self.clean_text(value)
                        else:
                            record[pg_col] = value

                    transformed_data.append(record)

                # Insertar datos en PostgreSQL
                columns = ', '.join(file_mapping.keys())
                placeholders = ', '.join(['%s'] * len(file_mapping))
                query = f"INSERT INTO destino ({columns}) VALUES ({placeholders})"

                try:
                    cursor.executemany(query, [tuple(record.values()) for record in transformed_data])
                    conn.commit()
                    records_processed += len(transformed_data)
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("Error", f"Error al insertar datos de {file_name}: {e}")

                # Actualizar barra de progreso y detalles
                self.progress['value'] = i + 1
                elapsed_time = time.time() - start_time
                estimated_time = (elapsed_time / (i + 1)) * (total_files - (i + 1))
                self.detail_label['text'] = f"Detalles: {records_processed} registros procesados, tiempo estimado: {int(estimated_time)}s"

            self.progress_label['text'] = "Procesamiento completado"
            messagebox.showinfo("Éxito", "Todos los archivos han sido procesados correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error general: {e}")

        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
