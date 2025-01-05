import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import sqlalchemy
import os

class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL DBF/CSV a PostgreSQL")
        self.root.geometry("800x600")

        # Variables
        self.files_selected = []
        self.pg_table = "cedulas"
        self.pg_schema = "gf"
        self.connection_string = "postgresql://postgres:salmos23@localhost:5432/Gabriela_Fragancias"

        # Interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Selección de archivos
        files_frame = ttk.LabelFrame(self.root, text="Archivos de entrada")
        files_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(files_frame, text="Seleccionar archivos", command=self.select_files).pack(pady=5)
        self.files_listbox = tk.Listbox(files_frame, height=5, width=80)
        self.files_listbox.pack(padx=5, pady=5)

        # Configuración
        config_frame = ttk.LabelFrame(self.root, text="Configuración")
        config_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(config_frame, text="Cadena de conexión:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.connection_entry = ttk.Entry(config_frame, width=60)
        self.connection_entry.insert(0, self.connection_string)
        self.connection_entry.grid(row=0, column=1, padx=5, pady=5)

        # Barra de progreso
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill="x", padx=10, pady=5)

        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(pady=5)

        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack(pady=5)

        # Botón de inicio
        ttk.Button(self.root, text="Iniciar proceso", command=self.process_files).pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("DBF/CSV files", "*.dbf;*.csv")])
        if files:
            self.files_selected = list(files)
            self.files_listbox.delete(0, tk.END)
            for file in self.files_selected:
                self.files_listbox.insert(tk.END, file)

    def load_file_in_chunks(self, file_path, chunk_size=10000):
        if file_path.lower().endswith('.csv'):
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                yield chunk
        elif file_path.lower().endswith('.dbf'):
            from dbfread import DBF
            table = DBF(file_path, encoding='latin1')
            yield pd.DataFrame(table)
        else:
            raise ValueError("Formato de archivo no soportado.")

    def process_files(self):
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return

        connection_string = self.connection_entry.get()
        try:
            engine = sqlalchemy.create_engine(connection_string)
            with engine.connect() as conn:
                total_files = len(self.files_selected)
                self.progress['maximum'] = total_files

                for i, file_path in enumerate(self.files_selected):
                    self.progress_label.config(text=f"Procesando {os.path.basename(file_path)}...")
                    for chunk in self.load_file_in_chunks(file_path):
                        self.map_and_insert(chunk, conn)

                    self.progress['value'] = i + 1
                    self.root.update_idletasks()

                messagebox.showinfo("Éxito", "¡Proceso completado exitosamente!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def map_and_insert(self, df, conn):
        column_mapping = {
            'numero_cedula': ['cedula', 'numero_ced'],
            'nombre': ['nombre', 'nombres'],
            'apellido': ['apellido', 'apellidos'],
            'fecha_nacimiento': ['fecha_nac', 'fecha_naci'],
            'sexo': ['sexo', 'cod_sex'],
            'direccion':['direcc', 'direccion', 'domicilio', 'direcc_rcp'],
            'id_distrito':['cod_dist','distrito'],
            'id_barrio':['barrio'],
            'id_dpto':['cod_dpto', 'depart'],
            'zona':['zona'],
            'lugar_nacimiento':['lug_nac', 'lugnac'],
            'fecha_defuncion':['fecha_def', 'fecha_defunc']
            # Agregar más columnas según sea necesario
        }
        mapped_columns = {pg_col: next((col for col in df.columns if col in possible), None)
                          for pg_col, possible in column_mapping.items()}
        df = df.rename(columns={v: k for k, v in mapped_columns.items() if v})
        df = df.dropna(subset=['numero_cedula'])

        # Insertar en PostgreSQL
        df.to_sql(self.pg_table, conn, schema=self.pg_schema, if_exists='append', index=False, method='multi')

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
