import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from psycopg2.extras import execute_batch
import dbfread
from datetime import datetime
import os

class DBFToPostgres:
    def __init__(self, root):
        self.root = root
        self.root.title("Cargar Cédulas a PostgreSQL")
        self.files_selected = []
        self.pg_columns = [
            'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
            'direccion', 'id_barrio', 'id_distrito', 'id_dpto', 'zona',
            'lugar_nacimiento', 'fecha_defuncion'
        ]
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self.root, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5)
        self.files_listbox = tk.Listbox(self.root, width=80, height=5)
        self.files_listbox.pack(pady=5)
        ttk.Button(self.root, text="Procesar Archivos", command=self.process_files).pack(pady=10)
        self.progress_label = ttk.Label(self.root, text="")
        self.progress_label.pack(pady=5)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Archivos DBF", "*.dbf")])
        if files:
            self.files_selected = list(files)
            self.files_listbox.delete(0, tk.END)
            for file in files:
                self.files_listbox.insert(tk.END, os.path.basename(file))

    def process_files(self):
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos.")
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
                self.progress_label.config(text=f"Procesando {os.path.basename(file_path)}...")
                records = self.read_and_transform(file_path, cursor)
                if records:
                    self.insert_data(cursor, records)
                    conn.commit()

            cursor.close()
            conn.close()
            self.progress_label.config(text="¡Proceso completado con éxito!")
            messagebox.showinfo("Éxito", "Todos los archivos fueron procesados correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Error procesando archivos: {str(e)}")

    def read_and_transform(self, file_path, cursor):
        try:
            table = dbfread.DBF(file_path, lowernames=True)
            records = []
            for record in table:
                transformed = self.process_record(record, cursor)
                if transformed:
                    records.append(transformed)
            return records
        except Exception as e:
            messagebox.showerror("Error", f"Error leyendo archivo {os.path.basename(file_path)}: {str(e)}")
            return None

    def process_record(self, record, cursor):
        try:
            # Mapear automáticamente las columnas del archivo a las columnas de la tabla
            mapped_record = {col: record.get(col.lower()) for col in self.pg_columns}
            # Llenar valores faltantes desde otra tabla origen
            for col, value in mapped_record.items():
                if not value:
                    mapped_record[col] = self.fetch_from_other_source(col, record.get('numero_cedula'), cursor)

            return tuple(mapped_record[col] for col in self.pg_columns)
        except Exception as e:
            print(f"Error transformando registro {record}: {str(e)}")
            return None

    def fetch_from_other_source(self, column, numero_cedula, cursor):
        """Buscar datos faltantes en otra tabla."""
        if not numero_cedula:
            return None
        try:
            query = f"SELECT {column} FROM otra_tabla_origen WHERE numero_cedula = %s"
            cursor.execute(query, (numero_cedula,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error buscando dato en otra tabla: {str(e)}")
            return None

    def transform_date(self, date_value):
        if not date_value:
            return None
        try:
            if isinstance(date_value, datetime):
                return date_value.strftime('%Y-%m-%d')
            if isinstance(date_value, str):
                for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%Y%m%d'):
                    try:
                        return datetime.strptime(date_value, fmt).strftime('%Y-%m-%d')
                    except ValueError:
                        continue
        except Exception:
            pass
        return None

    def insert_data(self, cursor, data):
        query = """
            INSERT INTO gf.cedulas (
                numero_cedula, nombre, apellido, fecha_nacimiento, sexo,
                direccion, id_barrio, id_distrito, id_dpto, zona,
                lugar_nacimiento, fecha_defuncion
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (numero_cedula)
            DO UPDATE SET
                nombre = EXCLUDED.nombre,
                apellido = EXCLUDED.apellido,
                fecha_nacimiento = COALESCE(EXCLUDED.fecha_nacimiento, gf.cedulas.fecha_nacimiento),
                direccion = COALESCE(EXCLUDED.direccion, gf.cedulas.direccion),
                updated_at = CURRENT_TIMESTAMP;
        """
        execute_batch(cursor, query, data)

if __name__ == "__main__":
    root = tk.Tk()
    app = DBFToPostgres(root)
    root.mainloop()
