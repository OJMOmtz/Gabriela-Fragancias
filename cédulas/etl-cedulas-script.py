import os
import pandas as pd
import sqlalchemy
from dbf import Table
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def load_dbf_or_csv(file_path):
    """
    Carga datos desde archivo DBF o CSV con manejo de diferentes encodings
    
    Args:
        file_path (str): Ruta del archivo a cargar
    
    Returns:
        pandas.DataFrame: DataFrame con los datos
    """
    try:
        if file_path.lower().endswith('.dbf'):
            # Cargar desde DBF
            table = Table(file_path)
            table.open()
            df = pd.DataFrame(table.records)
            table.close()
        elif file_path.lower().endswith('.csv'):
            # Intentar diferentes encodings
            encodings = ['latin1', 'utf-8', 'iso-8859-1', 'cp1252']
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError(f"No se pudo leer el archivo con los encodings probados: {encodings}")
        else:
            raise ValueError("Formato de archivo no soportado. Use .dbf o .csv")
        
        return df
    
    except Exception as e:
        logging.error(f"Error al cargar el archivo {file_path}: {e}")
        raise

def map_columns(df, column_mapping=None):
    """
    Mapea columnas del DataFrame a los nombres esperados para la tabla cedulas
    
    Args:
        df (pandas.DataFrame): DataFrame original
        column_mapping (dict, optional): Mapeo personalizado de columnas
    
    Returns:
        pandas.DataFrame: DataFrame con columnas mapeadas
    """
    # Mapeo predeterminado (puede ser extendido/personalizado)
    default_mapping = {
        'numero_cedula': ['cedula', 'documento', 'nro_cedula', 'id_cedula'],
        'nombre': ['nombre', 'nombres', 'first_name'],
        'apellido': ['apellido', 'apellidos', 'last_name'],
        'fecha_nacimiento': ['fecha_nac', 'nacimiento', 'birth_date'],
        'sexo': ['sexo', 'genero'],
        'direccion': ['direccion', 'domicilio', 'address'],
        'id_barrio': ['barrio', 'id_barrio'],
        'id_distrito': ['distrito', 'id_distrito'],
        'id_dpto': ['departamento', 'dpto', 'id_dpto'],
        'zona': ['zona'],
        'id_via': ['via', 'id_via'],
        'lugar_nacimiento': ['lugar_nac', 'ciudad_nacimiento'],
        'fecha_defuncion': ['fecha_def', 'defuncion'],
        'email': ['correo', 'email', 'mail']
    }
    
    # Combinar mapeo personalizado si se proporciona
    if column_mapping:
        for key, value in column_mapping.items():
            if key in default_mapping:
                default_mapping[key].extend(value)
    
    # Mapear columnas
    mapped_columns = {}
    for target_col, possible_sources in default_mapping.items():
        found_col = next((col for col in possible_sources if col in df.columns), None)
        if found_col:
            mapped_columns[target_col] = found_col
    
    # Seleccionar columnas mapeadas
    df_mapped = df[[v for v in mapped_columns.values()]].copy()
    df_mapped.rename(columns={v: k for k, v in mapped_columns.items()}, inplace=True)
    
    # Transformaciones específicas
    if 'sexo' in df_mapped.columns:
        df_mapped['sexo'] = df_mapped['sexo'].map({1: 'F', 2: 'M', 'F': 'F', 'M': 'M'}).fillna('M')
    
    return df_mapped

def transform_data(df):
    """
    Transformaciones adicionales de datos
    
    Args:
        df (pandas.DataFrame): DataFrame a transformar
    
    Returns:
        pandas.DataFrame: DataFrame transformado
    """
    # Convertir fechas
    date_columns = ['fecha_nacimiento', 'fecha_defuncion']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Limpiar campos de texto
    text_columns = ['nombre', 'apellido', 'direccion', 'lugar_nacimiento']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    return df

def insert_to_postgres(df, connection_string, table_name='cedulas', schema='gf'):
    """
    Inserta datos en PostgreSQL con manejo de columnas faltantes
    
    Args:
        df (pandas.DataFrame): DataFrame a insertar
        connection_string (str): Cadena de conexión de PostgreSQL
        table_name (str): Nombre de la tabla
        schema (str): Esquema de la base de datos
    """
    try:
        # Crear conexión
        engine = sqlalchemy.create_engine(connection_string)
        
        # Obtener columnas de la tabla existente
        inspector = sqlalchemy.inspect(engine)
        existing_columns = inspector.get_columns(table_name, schema=schema)
        existing_column_names = [col['name'] for col in existing_columns]
        
        # Filtrar columnas del DataFrame que existen en la tabla
        columns_to_insert = [col for col in df.columns if col in existing_column_names]
        df_to_insert = df[columns_to_insert]
        
        # Insertar datos
        df_to_insert.to_sql(
            name=table_name, 
            schema=schema, 
            con=engine, 
            if_exists='append',  # Añadir nuevos registros
            index=False,  # No incluir índice
            method='multi'  # Inserción por lotes para mejor rendimiento
        )
        logging.info(f"Se insertaron {len(df_to_insert)} registros exitosamente.")
        logging.info(f"Columnas insertadas: {', '.join(columns_to_insert)}")
    
    except Exception as e:
        logging.error(f"Error al insertar datos: {e}")
    finally:
        if 'engine' in locals():
            engine.dispose()

def process_files(input_directory, connection_string, column_mapping=None):
    """
    Procesa múltiples archivos DBF y CSV en un directorio
    
    Args:
        input_directory (str): Directorio con archivos a procesar
        connection_string (str): Cadena de conexión de PostgreSQL
        column_mapping (dict, optional): Mapeo personalizado de columnas
    """
    # Obtener archivos DBF y CSV
    files = [f for f in os.listdir(input_directory) if f.lower().endswith(('.dbf', '.csv'))]
    
    for file in files:
        file_path = os.path.join(input_directory, file)
        logging.info(f"Procesando archivo: {file}")
        
        try:
            # Cargar datos
            df_raw = load_dbf_or_csv(file_path)
            
            # Mapear columnas
            df_mapped = map_columns(df_raw, column_mapping)
            
            # Transformar datos
            df_transformed = transform_data(df_mapped)
            
            # Insertar en PostgreSQL
            insert_to_postgres(df_transformed, connection_string)
            
        except Exception as e:
            logging.error(f"Error procesando {file}: {e}")

def main():
    # Configuración de parámetros
    input_directory = "/ruta/a/directorio/con/archivos"
    connection_string = "postgresql://usuario:contraseña@localhost:5432/Gabriela_Fragancias"
    
    # Mapeo personalizado de columnas (opcional)
    custom_mapping = {
        # Ejemplo: 'numero_cedula': ['mi_columna_personalizada']
    }
    
    # Ejecutar procesamiento
    process_files(input_directory, connection_string, custom_mapping)

if __name__ == "__main__":
    main()
