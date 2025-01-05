import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import psycopg2
from datetime import datetime
import dbfread
import csv
from typing import Dict, List
import os
import re

class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL DBF a PostgreSQL")
        self.root.geometry("1200x800")
        
        # Variables
        self.files_selected: List[str] = []
        self.mappings: Dict[str, Dict] = {}  # Mapeo por archivo
        
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

        # Botón procesar
        ttk.Button(scrollable_frame, text="Procesar", 
                  command=self.process_files).pack(pady=10)

        # Configurar el layout del scroll
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


    def get_dbf_columns(self, file_path: str) -> List[str]:
        """Obtener las columnas de un archivo DBF."""
        try:
            table = dbfread.DBF(file_path)
            columns = table.field_names
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

    def dbf_to_csv(self, file_path: str, output_path: str):
        """Convertir archivo DBF a CSV."""
        with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            table = dbfread.DBF(file_path)
            
            writer.writerow(table.field_names)
            
            for record in table:
                writer.writerow([record[field] for field in table.field_names])

    def process_files(self):
        """Convertir archivos DBF a CSV, transformar datos y cargar a PostgreSQL."""
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

            for i, file_path in enumerate(self.files_selected):
                file_name = os.path.basename(file_path)
                csv_path = file_path.replace('.dbf', '.csv')
                
                # Convertir DBF a CSV
                self.dbf_to_csv(file_path, csv_path)
                
                # Leer CSV con pandas
                df = pd.read_csv(csv_path)
                
                # Obtener mapeo para este archivo
                file_mapping = self.mappings[file_path]

                # Aplicar transformaciones
                transformed_data = []
                for _, row in df.iterrows():
                    record = {}

                    # Mapear y transformar cada columna
                    for pg_col, combo in file_mapping.items():
                        dbf_col = combo.get()
                        if not dbf_col:
                            continue

                        value = row[dbf_col]  # <-- Corregido aquí

                        # Aplicar transformaciones específicas
                        if pg_col == 'fecha_nacimiento':
                            value = self.transform_date(value)
                        elif pg_col in ['nombre', 'apellido', 'lugar_nacimiento']:
                            value = self.clean_text(value)
                        elif pg_col == 'sexo':
                            value = self.transform_sex(value)
                        elif pg_col == 'numero_cedula':
                            value = str(value).strip() if value else None

                        record[pg_col] = value

                    if record.get('numero_cedula'):  # Solo insertar si hay número de cédula
                        transformed_data.append(record)
                        records_processed += 1

                # Insertar datos transformados usando COPY
                if transformed_data:
                    columns = transformed_data[0].keys()
                    
                    # Crear CSV temporal con los datos transformados
                    temp_csv_path = f"temp_{os.path.basename(csv_path)}"
                    with open(temp_csv_path, 'w', newline='', encoding='utf-8') as temp_csv_file:
                        writer = csv.writer(temp_csv_file)
                        writer.writerows([tuple(record.values()) for record in transformed_data])
                    
                    # Usar COPY para insertar desde el CSV temporal
                    with open(temp_csv_path, 'r', encoding='utf-8') as temp_csv_file:
                        cursor.copy_from(temp_csv_file, 'gf.cedulas', sep=',', columns=columns)
                    
                    os.remove(temp_csv_path)  # Eliminar CSV temporal

                conn.commit()
                self.progress['value'] = i + 1
                self.root.update_idletasks()

            cursor.close()
            conn.close()

            self.progress_label['text'] = f"¡Proceso completado! {records_processed} registros procesados"
            messagebox.showinfo("Éxito", 
                              f"ETL completado exitosamente\nArchivos procesados: {total_files}\n"
                              f"Registros procesados: {records_processed}")

        except Exception as e:
            messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
