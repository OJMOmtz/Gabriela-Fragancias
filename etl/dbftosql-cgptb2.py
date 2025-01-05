import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import threading
import logging
from psycopg2.extras import execute_batch
import os


class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL DBF a PostgreSQL")
        self.root.geometry("1200x800")

        # Configuración de logging
        logging.basicConfig(
            filename='etl_process.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Variables
        self.files_selected = []
        self.total_records = 0
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
            'direccion', 'barrio', 'distrito', 'dpto', 'lugar_nacimiento',
            'fecha_defuncion', 'zona'
        ]

        self.create_widgets()

    def create_widgets(self):
        """Crea los elementos de la interfaz gráfica."""
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

        ttk.Button(files_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5)

        self.files_listbox = tk.Listbox(files_frame, width=100, height=5)
        self.files_listbox.pack(pady=5)

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

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def select_files(self):
        """Selecciona los archivos DBF."""
        files = filedialog.askopenfilenames(filetypes=[("DBF files", "*.dbf")])
        if not files:
            return

        self.files_selected = list(files)
        self.files_listbox.delete(0, tk.END)
        for file_path in self.files_selected:
            self.files_listbox.insert(tk.END, file_path)

    def process_files(self):
        """Inicia el procesamiento en un hilo separado."""
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return

        processing_thread = threading.Thread(target=self._process_files_worker)
        processing_thread.start()

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

                except Exception as e:
                    self.logger.error(f"Error procesando archivo {file_path}: {str(e)}")
                    continue

                # Actualización correcta de la barra de progreso
                self.root.after(0, lambda i=i: self.progress.config(value=i + 1))
                
            cursor.close()
            conn.close()

            self.root.after(0, lambda: self.progress_label.config(text="¡Proceso completado!"))
            self.root.after(0, lambda: self.total_label.config(text=f"Total registros procesados: {records_processed}"))
            messagebox.showinfo("Éxito", f"ETL completado exitosamente\nRegistros procesados: {records_processed}")
        except Exception as e:
            self.logger.error(f"Error general en el procesamiento: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}"))

    def transform_data(self, table):
        """Transforma los datos del archivo DBF."""
        transformed = []
        for record in table:
            try:
                transformed.append((
                    record.get('numero_cedula'),
                    record.get('nombre'),
                    record.get('apellido'),
                    self.standardize_date(record.get('fecha_nacimiento')),
                    record.get('sexo'),
                    record.get('direccion'),
                    record.get('barrio'),
                    record.get('distrito'),
                    record.get('dpto'),
                    record.get('lugar_nacimiento'),
                    self.standardize_date(record.get('fecha_defuncion')),
                    record.get('zona')
                ))
            except Exception as e:
                self.logger.warning(f"Error transformando registro: {str(e)}")
        return transformed

def insert_data(self, cursor, data):
    """Inserta datos en PostgreSQL."""
    query = """
        INSERT INTO gf.cedulas (numero_cedula, nombre, apellido, fecha_nacimiento, sexo, direccion, barrio, distrito, dpto, lugar_nacimiento, fecha_defuncion, zona)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (numero_cedula)
        DO UPDATE SET
            nombre = EXCLUDED.nombre,
            apellido = EXCLUDED.apellido,
            fecha_nacimiento = COALESCE(EXCLUDED.fecha_nacimiento, gf.cedulas.fecha_nacimiento),
            direccion = COALESCE(EXCLUDED.direccion, gf.cedulas.direccion);
    """
    if not data:
        self.logger.warning("No hay datos para insertar.")
        return

    try:
        self.logger.debug(f"Datos a insertar: {data[:5]}")
        print(f"Datos a insertar: {data[:5]}")  # Muestra los primeros 5 registros
        execute_batch(cursor, query, data)
    except Exception as e:
        self.logger.error(f"Error durante la inserción: {str(e)}")


    def standardize_date(self, date_value):
        """Estandariza diferentes formatos de fecha."""
        if not date_value:
            return None
        try:
            if isinstance(date_value, datetime):
                return date_value.date()
            if isinstance(date_value, str):
                return datetime.strptime(date_value, '%Y-%m-%d').date()
        except ValueError:
            self.logger.warning(f"Formato de fecha no válido: {date_value}")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
