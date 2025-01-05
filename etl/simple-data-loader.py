import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

class DataLoader:
    def __init__(self, root):
        self.root = root
        self.root.title("Carga de Datos a PostgreSQL")
        self.root.geometry("500x400")
        
        # Variable para rastrear el progreso
        self.progress_var = tk.DoubleVar()
        
        self.create_widgets()

    def create_widgets(self):
        # Botón para seleccionar archivos
        tk.Button(
            self.root, 
            text="Seleccionar Archivos CSV", 
            command=self.select_files
        ).pack(pady=10)

        # Listbox para mostrar archivos seleccionados
        self.file_listbox = tk.Listbox(self.root, width=60, height=5)
        self.file_listbox.pack(pady=10)

        # Botón para procesar
        tk.Button(
            self.root, 
            text="Procesar Archivos", 
            command=self.process_files
        ).pack(pady=10)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            self.root, 
            variable=self.progress_var, 
            maximum=100, 
            length=400
        )
        self.progress_bar.pack(pady=10)

        # Etiqueta de estado
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

    def select_files(self):
        # Diálogo para seleccionar archivos CSV
        files = filedialog.askopenfilenames(
            title="Selecciona archivos CSV", 
            filetypes=[("Archivos CSV", "*.csv")]
        )
        
        if files:
            # Limpiar listbox anterior
            self.file_listbox.delete(0, tk.END)
            
            # Agregar archivos seleccionados
            for file in files:
                self.file_listbox.insert(tk.END, file)

    def process_files(self):
        # Obtener lista de archivos
        files = self.file_listbox.get(0, tk.END)
        
        if not files:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return

        try:
            # Conexión a PostgreSQL
            conn = psycopg2.connect(
                dbname="Gabriela_Fragancias", 
                user="postgres", 
                password="salmos23", 
                host="localhost"
            )
            conn.autocommit = False
            cursor = conn.cursor()

            total_processed = 0
            total_files = len(files)

            for index, file_path in enumerate(files, 1):
                # Actualizar estado
                self.status_label.config(
                    text=f"Procesando archivo {index} de {total_files}: {file_path}"
                )
                self.root.update_idletasks()

                # Leer CSV
                df = pd.read_csv(file_path, encoding='latin1', dtype=str)
                
                # Columnas de la tabla
                columns = [
                    'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 
                    'sexo', 'direccion', 'id_barrio', 'id_distrito', 'id_dpto', 
                    'zona', 'lugar_nacimiento', 'fecha_defuncion'
                ]

                # Seleccionar solo las columnas necesarias
                try:
                    df_subset = df[columns]
                except KeyError as e:
                    messagebox.showwarning("Advertencia", 
                        f"Columnas faltantes en {file_path}: {e}")
                    continue

                # Reemplazar NaN con None
                df_subset = df_subset.where(pd.notnull(df_subset), None)

                # Convertir a lista de tuplas
                records = [tuple(row) for row in df_subset.values]

                # Inserción con ON CONFLICT
                insert_query = """
                INSERT INTO gf.cedulas (
                    numero_cedula, nombre, apellido, fecha_nacimiento, sexo,
                    direccion, id_barrio, id_distrito, id_dpto, zona,
                    lugar_nacimiento, fecha_defuncion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (numero_cedula) 
                DO UPDATE SET 
                    nombre = EXCLUDED.nombre,
                    updated_at = CURRENT_TIMESTAMP
                """
                
                # Ejecutar inserción por lotes
                execute_batch(cursor, insert_query, records, page_size=1000)
                conn.commit()

                total_processed += len(records)
                
                # Actualizar barra de progreso
                self.progress_var.set((index / total_files) * 100)
                self.root.update_idletasks()

            # Mensaje de éxito
            messagebox.showinfo(
                "Completado", 
                f"Se procesaron {total_processed} registros en {total_files} archivos."
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            conn.rollback()

        finally:
            # Cerrar conexión
            if conn:
                cursor.close()
                conn.close()
            
            # Resetear progreso
            self.progress_var.set(0)
            self.status_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataLoader(root)
    root.mainloop()
