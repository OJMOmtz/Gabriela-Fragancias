import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm
from time import time
from datetime import datetime
import logging

logging.basicConfig(
    filename='proceso_csv.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_cedula(cedula):
    try:
        return str(int(cedula)) if pd.notna(cedula) else None
    except (ValueError, TypeError):
        return None

def format_date(date_str):
    if pd.isna(date_str):
        return None
    try:
        for fmt in ['%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d']:
            try:
                return datetime.strptime(str(date_str), fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        return None
    except Exception:
        return None

def clean_string(text):
    if pd.isna(text):
        return None
    return str(text).strip().upper()

def cargar_archivos_csv_a_postgresql(archivos_csv, tabla_destino):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        df_consolidado = pd.DataFrame()

        for archivo_csv, estructura in archivos_csv.items():
            try:
                logging.info(f"Iniciando procesamiento de: {archivo_csv}")
                df = pd.read_csv(archivo_csv, encoding='iso-8859-1', dtype=str, on_bad_lines='skip')
                
                df['numero_cedula'] = df.apply(lambda row: validate_cedula(row[estructura['mapeo_columnas'].get('numero_cedula')]), axis=1)
                df = df[df['numero_cedula'].notna()]
                
                df.rename(columns=estructura['mapeo_columnas'], inplace=True)
                
                if df_consolidado.empty:
                    df_consolidado = df
                else:
                    df_consolidado = pd.merge(
                        df_consolidado, 
                        df,
                        on='numero_cedula',
                        how='outer',
                        suffixes=('', '_new')
                    )
                    
                    for col in df.columns:
                        if col != 'numero_cedula':
                            col_new = f"{col}_new"
                            if col_new in df_consolidado.columns:
                                df_consolidado[col] = df_consolidado[col].fillna(df_consolidado[col_new])
                                df_consolidado.drop(col_new, axis=1, inplace=True)
                
                logging.info(f"Archivo {archivo_csv} procesado exitosamente")
            
            except Exception as e:
                logging.error(f"Error procesando archivo {archivo_csv}: {str(e)}")
                continue

        # Limpiar datos consolidados
        try:
            for col, func in {
                'nombre': clean_string,
                'apellido': clean_string,
                'fecha_nacimiento': format_date
            }.items():
                if col in df_consolidado.columns:
                    df_consolidado[col] = df_consolidado[col].apply(func)

            if 'sexo' in df_consolidado.columns:
                df_consolidado['sexo'] = df_consolidado['sexo'].map({'1': 'F', '2': 'M', 'F': 'F', 'M': 'M'})

            columnas_tabla = list(set().union(*[e['columnas_tabla'] for e in archivos_csv.values()]))
            for columna in columnas_tabla:
                if columna not in df_consolidado.columns:
                    df_consolidado[columna] = None

            batch_size = 1000
            for i in range(0, len(df_consolidado), batch_size):
                batch = df_consolidado.iloc[i:i + batch_size]
                
                try:
                    records = [tuple(None if pd.isna(val) else val for val in row[columnas_tabla]) 
                             for _, row in batch.iterrows()]
                    
                    execute_values(
                        cursor,
                        f"""
                        INSERT INTO {tabla_destino} ({', '.join(columnas_tabla)})
                        VALUES %s
                        ON CONFLICT (numero_cedula) 
                        DO UPDATE SET 
                        {', '.join(f"{col} = COALESCE(EXCLUDED.{col}, {tabla_destino}.{col})" 
                                 for col in columnas_tabla if col != 'numero_cedula')}
                        """,
                        records
                    )
                    conn.commit()
                    logging.info(f"Batch {i//batch_size + 1} procesado exitosamente")
                
                except Exception as e:
                    conn.rollback()
                    logging.error(f"Error en batch {i//batch_size + 1}: {str(e)}")
                    continue

        except Exception as e:
            logging.error(f"Error en procesamiento de datos: {str(e)}")

    except Exception as e:
        logging.error(f"Error general: {str(e)}")
    
    finally:
        if conn:
            conn.close()
            logging.info("Conexión cerrada")

# Configuración de base de datos
DB_CONFIG = {
    'dbname': 'Gabriela_Fragancias',
    'user': 'postgres',
    'password': 'salmos23',
    'host': 'localhost',
    'port': 5432
}
# Archivos CSV y su estructura
detalle_archivos = {
    "D:/PADRONES/csvs/Cédulas/poli01_W1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "direccion": "direccion"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },
    "D:/PADRONES/csvs/Cédulas/padrón 2017 anr_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "direccion": "direccion",
            "id_distrito": "id_distrito",
            "dpto": "id_dpto",
            "zona": "zona"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },
    "D:/PADRONES/csvs/Cédulas/padrón 2021 anr_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "direccion": "direccion",
            "id_distrito": "id_distrito",
            "dpto": "id_dpto"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    }, 
    "D:/PADRONES/csvs/Cédulas/padrón_UNACE_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "direccion": "direccion",
            "id_distrito": "id_distrito",
            "id_dpto": "id_dpto",
            "zona": "zona"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },     
    "D:/PADRONES/csvs/Cédulas/regciv_2010_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "id_distrito": "id_distrito",
            "id_dpto": "id_dpto",
            "zona": "zona"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },
    "D:/PADRONES/csvs/Cédulas/regciv_2013_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "id_distrito": "id_distrito",
            "id_dpto": "id_dpto",
            "zona": "zona"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },
    "D:/PADRONES/csvs/Cédulas/regciv_2015_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "id_distrito": "id_distrito",
            "id_dpto": "id_dpto",
            "zona": "zona"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },
    "D:/PADRONES/csvs/Cédulas/regciv_2018_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "id_distrito": "id_distrito",
            "id_dpto": "id_dpto",
            "zona": "zona"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },
    "D:/PADRONES/csvs/Cédulas/regciv_2020_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "id_distrito": "id_distrito",
            "id_dpto": "id_dpto",
            "zona": "zona"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },
    "D:/PADRONES/csvs/Cédulas/regciv_2021_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "id_distrito": "id_distrito",
            "id_dpto": "id_dpto",
            "zona": "zona"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },
    "D:/PADRONES/csvs/Cédulas/regciv_UNACE_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "id_distrito": "id_distrito",
            "id_dpto": "id_dpto",
            "zona": "zona"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },      
    "D:/PADRONES/csvs/Cédulas/regcivext_2015_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]      
    },
    "D:/PADRONES/csvs/Cédulas/regcivext_2020_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]      
    },    
    "D:/PADRONES/csvs/Cédulas/regcivext_2021_w1252.csv": {
        "mapeo_columnas": {
            "numero_cedula": "numero_cedula",
            "nombre": "nombre",
            "apellido": "apellido",
            "fecha_nacimiento": "fecha_nacimiento",
            "sexo": "sexo",
            "direccion": "direccion"
        },
        "columnas_tabla": [
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
        ]
    },
    }
# Uso de la función
cargar_archivos_csv_a_postgresql(detalle_archivos, "gf.cedulas")
