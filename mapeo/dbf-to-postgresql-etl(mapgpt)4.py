import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import psycopg2
from datetime import datetime
import dbf
import re
from typing import Dict, List
import os

class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL DBF a PostgreSQL")
        self.root.geometry("1200x800")

        # Variables
        self.files_selected: List[str] = []
        self.mappings: Dict[str, Dict] = {}
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'sexo',
            'fecha_nacimiento', 'lugar_nacimiento', 'direccion',
            'id_barrio', 'id_distrito', 'id_dpto', 'zona',
            'fecha_defuncion', 'email'
        ]

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Archivos
        files_frame = ttk.LabelFrame(main_frame, text="Archivos DBF")
        files_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(files_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5)
        self.files_listbox = tk.Listbox(files_frame, width=100, height=5)
        self.files_listbox.pack(pady=5)

        # Mapeo
        self.mapping_frame = ttk.LabelFrame(main_frame, text="Mapeo de columnas")
        self.mapping_frame.pack(fill="x", padx=10, pady=5)

        # Barra de progreso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill="x", padx=10, pady=5)

        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(pady=5)
        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack()

        # Botón procesar
        ttk.Button(main_frame, text="Procesar", command=self.process_files).pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("DBF files", "*.dbf")])
        if not files:
            return

        self.files_selected = list(files)
        self.files_listbox.delete(0, tk.END)

        for file_path in self.files_selected:
            file_name = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, file_name)

            # Crear mapeo por archivo
            dbf_columns = self.get_dbf_columns(file_path)
            file_frame = ttk.LabelFrame(self.mapping_frame, text=file_name)
            file_frame.pack(fill="x", padx=5, pady=5)
            self.mappings[file_path] = {}

            for pg_col in self.pg_columns:
                frame = ttk.Frame(file_frame)
                frame.pack(fill="x", padx=5, pady=2)

                ttk.Label(frame, text=f"{pg_col}:", width=20, anchor="w").pack(side="left")
                combo = ttk.Combobox(frame, values=[''] + dbf_columns, width=30)
                combo.pack(side="left", padx=5)

                for dbf_col in dbf_columns:
                    if pg_col in dbf_col.lower():
                        combo.set(dbf_col)
                        break

                self.mappings[file_path][pg_col] = combo

    def get_dbf_columns(self, file_path):
        try:
            table = dbf.Table(file_path)
            table.open()
            columns = table.field_names
            table.close()
            return columns
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer {file_path}: {e}")
            return []

    def validate_mappings(self):
        for file_path, mapping in self.mappings.items():
            for pg_col in self.pg_columns:
                if not mapping[pg_col].get():
                    return False, f"Falta mapear la columna PostgreSQL '{pg_col}' en el archivo {os.path.basename(file_path)}."
        return True, ""

    def process_files(self):
        if not self.files_selected:
            messagebox.showerror("Error", "No se seleccionaron archivos")
            return

        valid, message = self.validate_mappings()
        if not valid:
            messagebox.showerror("Error de mapeo", message)
            return

        try:
            conn = psycopg2.connect(
                dbname="Gabriela_Fragancias",
                user="postgres",
                password="salmos23",
                host="localhost"
            )
            cursor = conn.cursor()

            for file_path in self.files_selected:
                table = dbf.Table(file_path)
                table.open()
                df = pd.DataFrame(list(table))
                table.close()

                mapping = self.mappings[file_path]
                records = []
                for _, row in df.iterrows():
                    record = {}
                    for pg_col, combo in mapping.items():
                        dbf_col = combo.get()
                        value = row.get(dbf_col)
                        record[pg_col] = value
                    records.append(record)

                if records:
                    columns = records[0].keys()
                    values_template = ', '.join(['%s'] * len(columns))
                    insert_query = f"""
                        INSERT INTO gf.cedulas ({', '.join(columns)})
                        VALUES ({values_template})
                        ON CONFLICT (numero_cedula) DO NOTHING;
                    """
                    cursor.executemany(insert_query, [tuple(r.values()) for r in records])

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Éxito", "Todos los archivos se procesaron correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error procesando archivos: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
