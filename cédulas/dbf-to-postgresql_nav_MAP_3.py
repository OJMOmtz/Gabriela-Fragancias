import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import psycopg2
from datetime import datetime
import dbf
import re
import os
from typing import Dict, List, Optional

class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL DBF a PostgreSQL")
        self.root.geometry("1200x800")

        # Variables
        self.files_selected: List[str] = []
        self.mappings: Dict[str, Dict] = {}

        # Columnas destino PostgreSQL
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
            'direccion', 'id_distrito', 'id_dpto', 'zona', 'lugar_nacimiento', 'fecha_defuncion'
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

        ttk.Button(files_frame, text="Seleccionar archivos DBF", 
                  command=self.select_files).pack(pady=5)

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

        ttk.Button(scrollable_frame, text="Procesar", 
                  command=self.process_files).pack(pady=10)

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_dbf_columns(self, file_path: str) -> List[str]:
        try:
            table = dbf.Table(file_path)
            table.open()
            columns = table.field_names
            table.close()
            return columns
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo {file_path}: {str(e)}")
            return []

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("DBF files", "*.dbf")])
        if not files:
            return

        self.files_selected = list(files)
        self.files_listbox.delete(0, tk.END)

        for widget in self.mapping_frame.winfo_children():
            widget.destroy()

        for file_path in self.files_selected:
            file_name = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, file_path)

            file_frame = ttk.LabelFrame(self.mapping_frame, text=file_name, padding="5")
            file_frame.pack(fill="x", padx=5, pady=5)

            dbf_columns = self.get_dbf_columns(file_path)

            self.mappings[file_path] = {}

            for i, pg_col in enumerate(self.pg_columns):
                row = i // 3
                col = i % 3

                mapping_pair = ttk.Frame(file_frame)
                mapping_pair.grid(row=row, column=col, padx=5, pady=2)

                ttk.Label(mapping_pair, text=f"{pg_col}:").pack(side="left")
                combo = ttk.Combobox(mapping_pair, values=[''] + dbf_columns, width=20)
                combo.pack(side="left", padx=2)

                for dbf_col in dbf_columns:
                    if dbf_col.lower() in pg_col.lower():
                        combo.set(dbf_col)
                        break

                self.mappings[file_path][pg_col] = combo

    def transform_date(self, date_value):
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
            elif isinstance(date_value, datetime):
                return date_value.date()
        except Exception as e:
            print(f"Error transformando fecha {date_value}: {str(e)}")
        return None

    def process_files(self):
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return

        try:
            conn = psycopg2.connect(
                dbname="Gabriela_Fragancias",
                user="postgres",
                password="salmos23",
                host="localhost"
            )
            cursor = conn.cursor()

            total_records = 0

            for file_path in self.files_selected:
                file_name = os.path.basename(file_path)
                self.progress_label['text'] = f"Procesando {file_name}..."

                table = dbf.Table(file_path)
                table.open()
                df = pd.DataFrame(list(table))
                table.close()

                file_mapping = self.mappings[file_path]
                transformed_data = []

                for _, row in df.iterrows():
                    record = {}

                    for pg_col, combo in file_mapping.items():
                        dbf_col = combo.get()
                        if not dbf_col:
                            continue

                        value = row.get(dbf_col)
                        if pg_col == 'fecha_nacimiento' or pg_col == 'fecha_defuncion':
                            value = self.transform_date(value)
                        elif pg_col == 'sexo':
                            value = str(value).upper() if value else None

                        record[pg_col] = value

                    if record.get('numero_cedula'):
                        transformed_data.append(record)
                        total_records += 1

                if transformed_data:
                    columns = transformed_data[0].keys()
                    values_template = ', '.join(['%s'] * len(columns))
                    insert_query = f"""
                    INSERT INTO gf.cedulas ({', '.join(columns)})
                    VALUES ({values_template})
                    ON CONFLICT (numero_cedula) DO UPDATE SET
                    {', '.join(f"{col} = EXCLUDED.{col}" for col in columns if col != 'numero_cedula')}
                    """
                    cursor.executemany(insert_query, 
                                       [tuple(record.values()) for record in transformed_data])

            conn.commit()
            cursor.close()
            conn.close()

            self.progress_label['text'] = f"Proceso completado: {total_records} registros procesados"
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
