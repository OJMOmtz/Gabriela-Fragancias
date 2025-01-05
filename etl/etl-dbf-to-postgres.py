import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import sqlalchemy
import os
import logging
from dbfread import DBF
from sqlalchemy.exc import SQLAlchemyError

class ETLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL DBF a PostgreSQL - Gabriela Fragancias")
        self.root.geometry("800x600")

        # Configuración de logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            filename='etl_process.log',
            filemode='w'
        )

        # Variables de configuración
        self.files_selected = []
        self.pg_table = "cedulas"
        self.pg_schema = "gf"
        self.connection_string = "postgresql://postgres:salmos23@localhost:5432/Gabriela_Fragancias"

        # Interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Frame de selección de archivos
        files_frame = ttk.LabelFrame(self.root, text="Archivos de entrada DBF")
        files_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(files_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5)
        self.files_listbox = tk.Listbox(files_frame, height=5, width=80)
        self.files_listbox.pack(padx=5, pady=5)

        # Frame de configuración
        config_frame = ttk.LabelFrame(self.root, text="Configuración de Base de Datos")
        config_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(config_frame, text="Cadena de conexión:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.connection_entry = ttk.Entry(config_frame, width=60)
        self.connection_entry.insert(0, self.connection_string)
        self.connection_entry.grid(row=0, column=1, padx=5, pady=5)

        # Frame de progreso
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill="x", padx=10, pady=5)

        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(pady=5)

        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack(pady=5)

        # Botón de inicio
        ttk.Button(self.root, text="Iniciar migración", command=self.process_files).pack(pady=10)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("DBF files", "*.dbf")])
        if files:
            self.files_selected = list(files)
            self.files_listbox.delete(0, tk.END)
            for file in self.files_selected:
                self.files_listbox.insert(tk.END, file)

    def convert_date(self, date_input):
        """Convierte diferentes formatos de fecha a datetime"""
        if pd.isna(date_input):
            return None
        
        date_str = str(date_input)
        try:
            # Formatos: AAAAMMDD, MM/DD/AA, DD/MM/AA
            if len(date_str) == 8 and date_str.isdigit():
                return pd.to_datetime(date_str, format='%Y%m%d')
            elif '/' in date_str:
                # Intenta varios formatos de fecha con separador
                try:
                    return pd.to_datetime(date_str, format='%m/%d/%y')
                except:
                    return pd.to_datetime(date_str, format='%d/%m/%y')
        except Exception as e:
            logging.warning(f"Error convirtiendo fecha {date_input}: {e}")
            return None

    def load_dbf(self, file_path):
        """Carga archivos DBF con manejo de diferentes estructuras"""
        table = DBF(file_path, encoding='latin1')
        df = pd.DataFrame(table)
        
        # Mapeo de columnas de origen a destino
        column_mapping = {
            'numero_cedula': ['CEDULA', 'cedula'],
            'nombre': ['NOMBRE', 'nombre'],
            'apellido': ['APELLIDO', 'apellidos'],
            'fecha_nacimiento': ['FEC_NAC', 'fecha_nac', 'fecha_nacimiento'],
            'sexo': ['SEXO', 'sexo', 'cod_sex'],
            'direccion': ['DIRECC', 'direcc', 'direccion', 'DIREC_RCP', 'domicilio'],
            'id_distrito': ['DISTRITO', 'cod_dist', 'distrito'],
            'id_dpto': ['DEPART', 'cod_dpto', 'depart'],
            'zona': ['ZONA', 'zona'],
            'lugar_nacimiento': ['LUG_NAC', 'lug_nac', 'lugar_nacimiento']
        }

        # Encontrar las columnas correspondientes
        new_columns = {}
        for pg_col, possible_names in column_mapping.items():
            match = next((col for col in df.columns if col.upper() in [name.upper() for name in possible_names]), None)
            if match:
                new_columns[match] = pg_col

        # Renombrar columnas
        df = df.rename(columns=new_columns)

        # Limpiar y transformar datos
        if 'numero_cedula' in df.columns:
            df['numero_cedula'] = df['numero_cedula'].astype(str).str.zfill(8)
            df['numero_cedula'] = df['numero_cedula'].str.replace('-', '').str.replace('.', '')

        # Convertir fecha de nacimiento
        if 'fecha_nacimiento' in df.columns:
            df['fecha_nacimiento'] = df['fecha_nacimiento'].apply(self.convert_date)

        # Limitar longitud de campos de texto
        text_columns = ['nombre', 'apellido', 'direccion', 'lugar_nacimiento', 'email']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str[:100]

        # Seleccionar y limpiar columnas
        columns_to_keep = [
            'numero_cedula', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo', 
            'direccion', 'id_distrito', 'id_dpto', 'zona', 'lugar_nacimiento'
        ]
        df = df[[col for col in columns_to_keep if col in df.columns]]

        return df

    def process_files(self):
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos DBF")
            return

        try:
            engine = sqlalchemy.create_engine(self.connection_entry.get())
            
            total_files = len(self.files_selected)
            self.progress['maximum'] = total_files

            with engine.begin() as conn:
                for i, file_path in enumerate(self.files_selected):
                    logging.info(f"Procesando archivo: {file_path}")
                    self.progress_label.config(text=f"Procesando {os.path.basename(file_path)}...")

                    # Cargar datos del DBF
                    df = self.load_dbf(file_path)
                    
                    # Eliminar filas duplicadas por cédula
                    df = df.drop_duplicates(subset=['numero_cedula'])
                    
                    # Insertar datos
                    df.to_sql(
                        self.pg_table, 
                        conn, 
                        schema=self.pg_schema, 
                        if_exists='append', 
                        index=False, 
                        method='multi',
                        chunksize=1000
                    )

                    logging.info(f"Insertados {len(df)} registros desde {file_path}")
                    
                    self.progress['value'] = i + 1
                    self.root.update_idletasks()

            messagebox.showinfo("Éxito", "Migración completada exitosamente")
            logging.info("Proceso de migración finalizado con éxito")

        except SQLAlchemyError as e:
            messagebox.showerror("Error de Base de Datos", str(e))
            logging.error(f"Error en la migración: {e}")
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))
            logging.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ETLApp(root)
    root.mainloop()
