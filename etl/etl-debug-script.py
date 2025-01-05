import pandas as pd
import sqlalchemy
from dbf import Table
import tkinter as tk
from tkinter import filedialog, messagebox
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='etl_debug.log'
)

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
    connection_str = connection_entry.get()
    
    if not file_path:
        messagebox.showerror("Error", "No se ha seleccionado un archivo")
        return
    
    if not connection_str:
        messagebox.showerror("Error", "Ingrese la cadena de conexión")
        return
    
    has_header = header_var.get()
    
    try:
        # Detailed logging
        logging.info(f"Iniciando proceso ETL para archivo: {file_path}")
        
        df = load_dbf_or_csv(file_path)
        logging.info(f"Datos cargados. Registros: {len(df)}")
        logging.info(f"Columnas: {list(df.columns)}")
        
        if has_header:
            df.columns = df.iloc[0]
            df = df[1:]
        
        df_transformed = transform_data(df)
        logging.info(f"Datos transformados. Registros: {len(df_transformed)}")
        
        insert_to_postgres(df_transformed, connection_str)
        
        messagebox.showinfo("Completado", f"Se procesaron {len(df_transformed)} registros exitosamente.")
    
    except Exception as e:
        error_msg = f"Error en proceso ETL: {str(e)}"
        logging.error(error_msg, exc_info=True)
        messagebox.showerror("Error", error_msg)

# Crear ventana principal
root = tk.Tk()
root.title("Carga de Datos a PostgreSQL")

# Entrada para la ruta del archivo
file_label = tk.Label(root, text="Archivo:")
file_label.pack()
file_entry = tk.Entry(root, width=50)
file_entry.pack()
file_button = tk.Button(root, text="Seleccionar Archivo", command=select_file)
file_button.pack()

# Entrada para cadena de conexión
conn_label = tk.Label(root, text="Cadena de Conexión:")
conn_label.pack()
connection_entry = tk.Entry(root, width=50)
connection_entry.pack()

# Opción para indicar si el archivo tiene encabezado
header_var = tk.BooleanVar()
header_check = tk.Checkbutton(
    root, 
    text="El archivo tiene encabezado", 
    variable=header_var
)
header_check.pack()

# Botón para ejecutar el proceso ETL
run_button = tk.Button(root, text="Procesar Archivo", command=run_etl)
run_button.pack()

# Ejecutar la aplicación
root.mainloop()

def load_dbf_or_csv(file_path):
    """
    Carga datos desde archivo DBF o CSV con validaciones
    """
    try:
        if file_path.lower().endswith('.dbf'):
            table = Table(file_path)
            table.open()
            df = pd.DataFrame(table.records)
            table.close()
        elif file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path, encoding='latin1')
        else:
            raise ValueError("Formato de archivo no soportado. Use .dbf o .csv")
        
        if df.empty:
            raise ValueError("El archivo está vacío")
        
        return df
    except Exception as e:
        logging.error(f"Error al cargar archivo: {e}", exc_info=True)
        raise

def transform_data(df):
    """
    Transforma los datos para su inserción en PostgreSQL con validaciones
    """
    try:
        # Validar columnas requeridas
        required_columns = ['cedula', 'sexo']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Columnas faltantes: {missing_columns}")
        
        # Mapear valores de sexo
        df['sexo'] = df['sexo'].map({1: 'Femenino', 2: 'Masculino'})
        
        # Eliminar registros sin cédula
        df = df.dropna(subset=['cedula'])
        
        return df
    except Exception as e:
        logging.error(f"Error en transformación de datos: {e}", exc_info=True)
        raise

def insert_to_postgres(df, connection_string):
    """
    Inserta datos en la tabla cedulas del esquema gf con manejo de errores
    """
    try:
        engine = sqlalchemy.create_engine(connection_string)
        
        # Verificar conexión
        with engine.connect() as connection:
            connection.execute(sqlalchemy.text("SELECT 1"))
        
        df.to_sql(
            name='cedulas', 
            schema='gf', 
            con=engine, 
            if_exists='append',
            index=False,
            method='multi'
        )
        logging.info(f"Se insertaron {len(df)} registros exitosamente.")
    
    except Exception as e:
        logging.error(f"Error al insertar datos: {e}", exc_info=True)
        raise
    finally:
        if 'engine' in locals():
            engine.dispose()

def main(file_path, connection_string):
    """
    Función principal para ejecutar el proceso ETL con logging
    """
    try:
        logging.info(f"Iniciando proceso ETL con archivo: {file_path}")
        df = load_dbf_or_csv(file_path)
        df_transformed = transform_data(df)
        insert_to_postgres(df_transformed, connection_string)
    except Exception as e:
        logging.error(f"Error en proceso ETL: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    # Ejemplo de uso
    archivo = "ruta/a/tu/archivo.dbf"  # o .csv
    conexion = "postgresql://usuario:contraseña@localhost:5432/Gabriela_Fragancias"
    
    main(archivo, conexion)
