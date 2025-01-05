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

def select_and_process_files():
    files = filedialog.askopenfilenames(
        title="Selecciona archivos DBF o CSV",
        filetypes=[("Archivos DBF", "*.dbf"), ("Archivos CSV", "*.csv")]
    )
    
    if not files:
        messagebox.showerror("Error", "No se han seleccionado archivos")
        return
    
    connection_str = "postgresql://postgres:salmos23@localhost:5432/Gabriela_Fragancias"
    chunk_size = 1000
    has_header = header_var.get()
    
    try:
        for file_path in files:
            logging.info(f"Procesando archivo: {file_path}")
            process_file_in_chunks(file_path, connection_str, chunk_size, has_header)
        
        messagebox.showinfo("Completado", f"Procesados {len(files)} archivos exitosamente.")
    
    except Exception as e:
        error_msg = f"Error en proceso ETL: {str(e)}"
        logging.error(error_msg, exc_info=True)
        messagebox.showerror("Error", error_msg)

# Crear ventana principal
root = tk.Tk()
root.title("Carga de Datos a PostgreSQL")

# Opción para indicar si el archivo tiene encabezado
header_var = tk.BooleanVar()
header_check = tk.Checkbutton(
    root, 
    text="Los archivos tienen encabezado", 
    variable=header_var
)
header_check.pack()

# Botón para seleccionar y procesar archivos
run_button = tk.Button(root, text="Seleccionar y Procesar Archivos", command=select_and_process_files)
run_button.pack(pady=20)

def process_file_in_chunks(file_path, connection_string, chunk_size=1000, has_header=False):
    engine = sqlalchemy.create_engine(connection_string)
    total_processed = 0

    try:
        if file_path.lower().endswith('.dbf'):
            # Updated DBF processing
            with Table(file_path) as table:
                # Convert directly to DataFrame
                df_total = pd.DataFrame(iter(table))
                
                if has_header:
                    df_total.columns = df_total.iloc[0]
                    df_total = df_total[1:]
                
                for i in range(0, len(df_total), chunk_size):
                    chunk = df_total.iloc[i:i+chunk_size]
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

        elif file_path.lower().endswith('.csv'):
            for chunk in pd.read_csv(file_path, encoding='latin1', chunksize=chunk_size, engine='python'):
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
        
        logging.info(f"Total de registros procesados en {file_path}: {total_processed}")
    
    except Exception as e:
        logging.error(f"Error en procesamiento de {file_path}: {e}", exc_info=True)
        raise
    finally:
        engine.dispose()

def transform_data(df):
    required_columns = ['cedula', 'sexo']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Columnas faltantes: {missing_columns}")
    
    df['sexo'] = df['sexo'].map({1: 'F', 2: 'M'})
    df = df.dropna(subset=['cedula'])
    
    return df

# Ejecutar la aplicación
root.mainloop()
