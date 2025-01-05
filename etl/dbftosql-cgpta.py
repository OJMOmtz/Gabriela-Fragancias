import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from psycopg2.extras import execute_batch
import pandas as pd
import dbfread
import threading
from datetime import datetime
import os
from typing import List, Dict, Any, Optional

class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL DBF a PostgreSQL")
        self.root.geometry("800x600")
        
        # Variables
        self.files_selected: List[str] = []
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
            'direccion', 'barrio', 'distrito', 'dpto', 'lugar_nacimiento',
            'fecha_defuncion', 'zona'
        ]
        
        # Crear interfaz
        self.create_widgets()
    
    def create_widgets(self):
        """Crear interfaz gráfica."""
        # Selección de archivos
        ttk.Button(self.root, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5)
        self.files_listbox = tk.Listbox(self.root, width=100, height=5)
        self.files_listbox.pack(pady=5)
        
        # Barra de progreso
        self.progress_label = ttk.Label(self.root, text="")
        self.progress_label.pack(pady=5)
        self.progress_bar = ttk.Progressbar(self.root, mode='determinate', length=400)
        self.progress_bar.pack(pady=5)

        # Botón de procesamiento
        ttk.Button(self.root, text="Procesar", command=self.process_files).pack(pady=10)
    
    def select_files(self):
        """Seleccionar archivos DBF."""
        files = filedialog.askopenfilenames(filetypes=[("Archivos DBF", "*.dbf")])
        if files:
            self.files_selected = list(files)
            self.files_listbox.delete(0, tk.END)
            for file in files:
                self.files_listbox.insert(tk.END, os.path.basename(file))
    
    def process_files(self):
        """Procesar archivos en un hilo separado."""
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return
        
        thread = threading.Thread(target=self._process_files_worker)
        thread.start()
    
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

            for i, file_path in enumerate(self.files_selected):
                file_name = os.path.basename(file_path)
                self.root.after(0, lambda: self.progress_label.config(text=f"Procesando {file_name}..."))
                self.logger.info(f"Procesando archivo: {file_name}")

                # Leer y transformar datos
                try:
                    table = dbfread.DBF(file_path, lowernames=True)
                    transformed_data = self.transform_data(table)
                    if transformed_data:
                        self.insert_data(cursor, transformed_data)
                        conn.commit()
                        records_processed += len(transformed_data)

                except Exception as ex:
                    self.logger.error(f"Error procesando archivo {file_path}: {str(ex)}")
                    self.root.after(0, lambda ex=ex: messagebox.showerror("Error", f"Ocurrió un error: {str(ex)}"))
                    continue

                # Actualización correcta de la barra de progreso
                self.root.after(0, lambda i=i: self.progress.config(value=i + 1))

            cursor.close()
            conn.close()

            self.root.after(0, lambda: self.progress_label.config(text="¡Proceso completado!"))
            self.root.after(0, lambda: self.total_label.config(text=f"Total registros procesados: {records_processed}"))
            messagebox.showinfo("Éxito", f"ETL completado exitosamente\nRegistros procesados: {records_processed}")
        except Exception as ex:
            self.logger.error(f"Error general en el procesamiento: {str(ex)}")
            self.root.after(0, lambda ex=ex: messagebox.showerror("Error", f"Error durante el procesamiento: {str(ex)}"))

    
    def process_record(self, record: Dict[str, Any]) -> Optional[tuple]:
        """Procesar un registro del archivo DBF."""
        try:
            return (
                record.get('cedula', None),
                record.get('nombre', '').strip(),
                record.get('apellido', '').strip(),
                self.standardize_date(record.get('fecha_nac')),
                record.get('sexo', '').upper(),
                record.get('direccion', '').strip(),
                record.get('barrio', '').strip(),
                record.get('distrito', '').strip(),
                record.get('dpto', '').strip(),
                record.get('lugar_nacimiento', '').strip(),
                self.standardize_date(record.get('fecha_defuncion')),
                record.get('zona', '').strip()
            )
        except Exception as e:
            print(f"Error en registro: {record}, {e}")
            return None

    def standardize_date(self, date_value: Any) -> Optional[str]:
        """Estándar para fechas."""
        try:
            if isinstance(date_value, datetime):
                return date_value.strftime('%Y-%m-%d')
            elif isinstance(date_value, str):
                for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%Y%m%d'):
                    try:
                        return datetime.strptime(date_value, fmt).strftime('%Y-%m-%d')
                    except ValueError:
                        continue
        except Exception:
            return None
        return None
    
    def insert_records(self, cursor, records: List[tuple]):
        """Insertar registros en PostgreSQL."""
        query = """
        INSERT INTO Cedulas (numero_cedula, nombre, apellido, fecha_nacimiento, sexo, direccion, 
                             barrio, distrito, dpto, lugar_nacimiento, fecha_defuncion, zona)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (numero_cedula) DO UPDATE 
        SET nombre = EXCLUDED.nombre,
            apellido = EXCLUDED.apellido,
            fecha_nacimiento = EXCLUDED.fecha_nacimiento,
            sexo = EXCLUDED.sexo,
            direccion = EXCLUDED.direccion,
            barrio = EXCLUDED.barrio,
            distrito = EXCLUDED.distrito,
            dpto = EXCLUDED.dpto,
            lugar_nacimiento = EXCLUDED.lugar_nacimiento,
            fecha_defuncion = EXCLUDED.fecha_defuncion,
            zona = EXCLUDED.zona
        """
        execute_batch(cursor, query, records)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    app.run()
