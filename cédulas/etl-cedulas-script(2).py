import pandas as pd
import sqlalchemy
from dbf import Table
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='etl_debug.log'
)

def select_files():
    files = filedialog.askopenfilenames(
        title="Selecciona archivos DBF o CSV",
        filetypes=[("Archivos DBF", "*.dbf"), ("Archivos CSV", "*.csv")]
    )
    if files:
        files_entry.delete(0, tk.END)
        files_entry.insert(tk.END, '; '.join(files))

def run_etl():
    file_paths = files_entry.get().split('; ')
    connection_str = "postgresql://postgres:salmos23@localhost:5432/Gabriela_Fragancias"
    chunk_size = 1000
    
    if not file_paths:
        messagebox.showerror("Error", "No se han seleccionado archivos")
        return
    
    has_header = header_var.get()
    
    try:
        for file_path in file_paths:
            logging.info(f"Procesando archivo: {file_path}")
            process_file_in_chunks(file_path, connection_str, chunk_size, has_header)
        
        messagebox.showinfo("Completado", "Todos los archivos procesados exitosamente.")
    
    except Exception as e:
        error_msg = f"Error en proceso ETL: {str(e)}"
        logging.error(error_msg, exc_info=True)
        messagebox.showerror("Error", error_msg)

# Crear ventana principal
root = tk.Tk()
root.title("Carga de Datos a PostgreSQL")

# Entrada para las rutas de los archivos
files_label = tk.Label(root, text="Archivos:")
files_label.pack()
files_entry = tk.Entry(root, width=50)
files_entry.pack()
files_button = tk.Button(root, text="Seleccionar Archivos", command=select_files)
files_button.pack()

# Opción para indicar si el archivo tiene encabezado
header_var = tk.BooleanVar()
header_check = tk.Checkbutton(
    root, 
    text="Los archivos tienen encabezado", 
    variable=header_var
)
header_check.pack()

# Botón para ejecutar el proceso ETL
run_button = tk.Button(root, text="Procesar Archivos", command=run_etl)
run_button.pack()

def process_file_in_chunks(file_path, connection_string, chunk_size=1000, has_header=False):
    engine = sqlalchemy.create_engine(connection_string)
    total_processed = 0

    try:
        # Procesar archivos CSV con configuración flexible
        if file_path.lower().endswith('.csv'):
            # Intentar diferentes encodings y configuraciones de parsing
            for encoding in ['latin1', 'utf-8', 'ISO-8859-1']:
                try:
                    df_chunks = pd.read_csv(
                        file_path, 
                        encoding=encoding, 
                        chunksize=chunk_size, 
                        sep=None,  # Autodetectar separador
                        engine='python',  # Modo de parseo más flexible
                        error_bad_lines=False,  # Ignorar líneas problemáticas
                        warn_bad_lines=True  # Advertir sobre líneas saltadas
                    )
                    
                    for chunk in df_chunks:
                        if has_header:
                            chunk.columns = chunk.iloc[0]
                            chunk = chunk[1:]
                        
                        processed_chunk = transform_data(chunk)
                        
                        processed_chunk.to_sql(
                            name='cedulas', 
                            schema='gf', 
                            con=engine, 
                            if_exists='append',
                            index=False,
                            method='multi'
                        )
                        
                        total_processed += len(processed_chunk)
                        logging.info(f"Procesados {total_processed} registros")
                    
                    break  # Salir si se procesa exitosamente
                
                except Exception as e:
                    logging.warning(f"Falló parsing con encoding {encoding}: {e}")
                    continue
        
        logging.info(f"Total de registros procesados: {total_processed}")
    
    except Exception as e:
        logging.error(f"Error en procesamiento: {e}", exc_info=True)
        raise
    finally:
        engine.dispose()

def transform_data(df):
    """
    Transforma los datos para su inserción en PostgreSQL
    """
    # Validar columnas requeridas
    required_columns = ['cedula', 'sexo']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Columnas faltantes: {missing_columns}")
    
    # Mapear valores de sexo con el mapeo original
    df['sexo'] = df['sexo'].map({1: 'Femenino', 2: 'Masculino'})
    
    # Eliminar registros sin cédula
    df = df.dropna(subset=['cedula'])
    
    return df

# Ejecutar la aplicación
root.mainloop()
