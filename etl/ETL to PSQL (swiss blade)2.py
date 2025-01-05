import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import psycopg2
from dbfread import DBF
from threading import Thread

# PostgreSQL connection details
PG_HOST = "localhost"
PG_DATABASE = "Gabriela_Fragancias"
PG_USER = "postgres"
PG_PASSWORD = "salmos23"
PG_SCHEMA = "gf"

class DataLoaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Loader Tool")

        # File selection
        self.file_label = tk.Label(root, text="Archivo de Origen:")
        self.file_label.grid(row=0, column=0, sticky="w")
        self.file_entry = tk.Entry(root, width=50)
        self.file_entry.grid(row=0, column=1)
        self.file_button = tk.Button(root, text="Seleccionar", command=self.select_file)
        self.file_button.grid(row=0, column=2)

        # Destination table
        self.table_label = tk.Label(root, text="Tabla de Destino:")
        self.table_label.grid(row=1, column=0, sticky="w")
        self.table_entry = tk.Entry(root, width=50)
        self.table_entry.grid(row=1, column=1)

        # Preview data button
        self.preview_button = tk.Button(root, text="Previsualizar Datos", command=self.preview_data)
        self.preview_button.grid(row=2, column=1)

        # Map columns button
        self.map_button = tk.Button(root, text="Mapear Columnas", command=self.map_columns)
        self.map_button.grid(row=3, column=1)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=4, column=1, pady=10)

        # Start loading button
        self.start_button = tk.Button(root, text="Iniciar Carga", command=self.start_loading)
        self.start_button.grid(row=5, column=1)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV, TXT, DBF files", "*.csv *.txt *.dbf")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def preview_data(self):
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Por favor selecciona un archivo de origen")
            return
        
        try:
            if file_path.endswith(".csv") or file_path.endswith(".txt"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".dbf"):
                table = DBF(file_path)
                df = pd.DataFrame(iter(table))
            else:
                raise ValueError("Formato no soportado")
            
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Previsualización de Datos")
            text = tk.Text(preview_window, wrap=tk.NONE)
            text.pack(expand=True, fill="both")
            text.insert(tk.END, df.head().to_string(index=False))
        except Exception as e:
            messagebox.showerror("Error", f"Error al previsualizar datos: {e}")

    def map_columns(self):
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Por favor selecciona un archivo de origen")
            return

        # Load file to get columns
        try:
            if file_path.endswith(".csv") or file_path.endswith(".txt"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".dbf"):
                table = DBF(file_path)
                df = pd.DataFrame(iter(table))
            else:
                raise ValueError("Formato no soportado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer archivo: {e}")
            return

        # Display columns for mapping
        self.columns = list(df.columns)
        messagebox.showinfo("Mapeo de Columnas", f"Columnas detectadas: {', '.join(self.columns)}")

    def start_loading(self):
        file_path = self.file_entry.get()
        table_name = self.table_entry.get()
        if not file_path or not table_name:
            messagebox.showerror("Error", "Por favor selecciona un archivo y tabla destino")
            return

        # Start loading in a separate thread
        Thread(target=self.load_data, args=(file_path, table_name)).start()

    def load_data(self, file_path, table_name):
        try:
            self.progress["value"] = 0
            conn = psycopg2.connect(host=PG_HOST, database=PG_DATABASE, user=PG_USER, password=PG_PASSWORD)
            cur = conn.cursor()

            if file_path.endswith(".csv") or file_path.endswith(".txt"):
                df = pd.read_csv(file_path)
            elif file_path.endswith(".dbf"):
                table = DBF(file_path)
                df = pd.DataFrame(iter(table))
            else:
                raise ValueError("Formato no soportado")

            # Build INSERT INTO statement
            columns = ", ".join(df.columns)
            placeholders = ", ".join(["%s"] * len(df.columns))
            insert_query = f"INSERT INTO {PG_SCHEMA}.{table_name} ({columns}) VALUES ({placeholders})"

            # Insert rows with progress
            total_rows = len(df)
            for i, row in df.iterrows():
                cur.execute(insert_query, tuple(row))
                self.progress["value"] = (i + 1) / total_rows * 100
                self.root.update_idletasks()

            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Éxito", "Datos cargados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataLoaderApp(root)
    root.mainloop()
