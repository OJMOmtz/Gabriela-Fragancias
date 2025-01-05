import pandas as pd
import sqlalchemy
from dbf import Table
import tkinter as tk
from tkinter import filedialog, messagebox
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='etl_debug.log'
)

# Cadena de conexión predeterminada
DEFAULT_CONNECTION_STRING = "postgresql://postgres:salmos23@localhost:5432/Gabriela_Fragancias"

def select_file():
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo DBF o CSV",
        filetypes=[("Archivos DBF", "*.dbf"), ("Archivos CSV", "*.csv")]
    )
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(tk.END, file_path)

def run_etl():
    file_path = file_entry.get()
    connection_str = connection_entry.get() or DEFAULT_CONNECTION_STRING
    chunk_size = int(chunk_entry.get() or 1000)
    
    if not file_path:
        messagebox.showerror("Error", "No se ha seleccionado un archivo")
        return
    
    has_header = header_var.get()
    
    try:
        logging.info(f"Iniciando proceso ETL para archivo: {file_path}")
        process_file_in_chunks(file_path, connection_str, chunk_size, has_header)
        messagebox.showinfo("Completado", "Proceso ETL finalizado exitosamente.")
    
    except Exception as e:
        error_msg = f"Error en proceso ETL: {str(e)}"
        logging.error(error_msg, exc_info=True)
        messagebox.showerror("Error", error_msg)

# GUI Setup
root = tk.Tk()
root.title("Carga de Datos a PostgreSQL")

# File path input
file_label = tk.Label(root, text="Archivo:")
file_label.pack()
file_entry = tk.Entry(root, width=50)
file_entry.pack()
file_button = tk.Button(root, text="Seleccionar Archivo", command=select_file)
file_button.pack()

# Connection string input
conn_label = tk.Label(root, text="Cadena de Conexión:")
conn_label.pack()
connection_entry = tk.Entry(root, width=50)
connection_entry.insert(0, DEFAULT_CONNECTION_STRING)
connection_entry.pack()

# Chunk size input
chunk_label = tk.Label(root, text="Tamaño de Chunk:")
chunk_label.pack()
chunk_entry = tk.Entry(root, width=10)
chunk_entry.insert(0, "1000")
chunk_entry.pack()

# Header option
header_var = tk.BooleanVar()
header_check = tk.Checkbutton(
    root, 
    text="El archivo tiene encabezado", 
    variable=header_var
)
header_check.pack()

# ETL button
run_button = tk.Button(root, text="Procesar Archivo", command=run_etl)
run_button.pack()

# [Rest of the previous script remains the same]
# ... (process_file_in_chunks and transform_data functions)
def process_file_in_chunks(file_path, connection_string, chunk_size=1000, has_header=False):
    """
    Procesa el archivo en chunks para manejar archivos grandes
    """
    engine = sqlalchemy.create_engine(connection_string)
    total_processed = 0

    try:
        # Procesar archivos DBF
        if file_path.lower().endswith('.dbf'):
            table = Table(file_path)
            table.open()
            
            # Convertir records a chunks
            records = list(table.records)
            df_total = pd.DataFrame(records)
            
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
                logging.info(f"Procesados {total_processed} registros")
            
            table.close()

        # Procesar archivos CSV
        elif file_path.lower().endswith('.csv'):
            for chunk in pd.read_csv(file_path, encoding='latin1', chunksize=chunk_size):
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
        
        logging.info(f"Total de registros procesados: {total_processed}")
    
    except Exception as e:
        logging.error(f"Error en procesamiento por chunks: {e}", exc_info=True)
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
    
    # Mapear valores de sexo
    df['sexo'] = df['sexo'].map({1: 'F', 2: 'M'})
    
    # Eliminar registros sin cédula
    df = df.dropna(subset=['cedula'])
    
    return df

# Ejecutar la aplicación
root.mainloop()
