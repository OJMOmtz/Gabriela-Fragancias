import pandas as pd
import sqlalchemy
from dbf import Table
import tkinter as tk
from tkinter import filedialog, messagebox

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
    if not file_path:
        messagebox.showerror("Error", "No se ha seleccionado un archivo")
        return
    
    has_header = header_var.get()
    
    try:
        df = load_dbf_or_csv(file_path)
        
        if has_header:
            df.columns = df.iloc[0]
            df = df[1:]
        
        df_transformed = transform_data(df)
        insert_to_postgres(df_transformed, connection_string)
        
        messagebox.showinfo("Completado", f"Se procesaron {len(df)} registros exitosamente.")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

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
    Carga datos desde archivo DBF o CSV
    
    Args:
        file_path (str): Ruta del archivo a cargar
    
    Returns:
        pandas.DataFrame: DataFrame con los datos
    """
    if file_path.lower().endswith('.dbf'):
        # Cargar desde DBF
        table = Table(file_path)
        table.open()
        df = pd.DataFrame(table.records)
        table.close()
    elif file_path.lower().endswith('.csv'):
        # Cargar desde CSV
        df = pd.read_csv(file_path, encoding='latin1')
    else:
        raise ValueError("Formato de archivo no soportado. Use .dbf o .csv")
    
    return df

def transform_data(df):
    """
    Transforma los datos para su inserción en PostgreSQL
    
    Args:
        df (pandas.DataFrame): DataFrame original
    
    Returns:
        pandas.DataFrame: DataFrame transformado
    """
    # Mapear valores de sexo
    df['sexo'] = df['sexo'].map({1: 'Femenino', 2: 'Masculino'})
    
    # Opcional: Validaciones adicionales
    df = df.dropna(subset=['cedula'])  # Eliminar registros sin cédula
    
    return df

def insert_to_postgres(df, connection_string):
    """
    Inserta datos en la tabla cedulas del esquema gf
    
    Args:
        df (pandas.DataFrame): DataFrame a insertar
        connection_string (str): Cadena de conexión de PostgreSQL
    """
    try:
        # Crear conexión
        engine = sqlalchemy.create_engine(connection_string)
        
        # Insertar datos
        df.to_sql(
            name='cedulas', 
            schema='gf', 
            con=engine, 
            if_exists='append',  # Añadir nuevos registros
            index=False,  # No incluir índice
            method='multi'  # Inserción por lotes para mejor rendimiento
        )
        print(f"Se insertaron {len(df)} registros exitosamente.")
    
    except Exception as e:
        print(f"Error al insertar datos: {e}")
    finally:
        engine.dispose()

def main(file_path, connection_string):
    """
    Función principal para ejecutar el proceso ETL
    
    Args:
        file_path (str): Ruta del archivo de origen
        connection_string (str): Cadena de conexión de PostgreSQL
    """
    # Cargar datos
    df = load_dbf_or_csv(file_path)
    
    # Transformar datos
    df_transformed = transform_data(df)
    
    # Insertar en PostgreSQL
    insert_to_postgres(df_transformed, connection_string)

if __name__ == "__main__":
    # Ejemplo de uso
    archivo = "ruta/a/tu/archivo.dbf"  # o .csv
    conexion = "postgresql://postgres:salmos23@localhost:5432/Gabriela_Fragancias"
    
    main(archivo, conexion)
