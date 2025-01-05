import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm
from time import time
from datetime import datetime

DB_CONFIG = {
    'dbname': 'Gabriela_Fragancias',
    'user': 'postgres',
    'password': 'salmos23',
    'host': 'localhost',
    'port': 5432
}

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
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Crear DataFrame consolidado
        df_consolidado = pd.DataFrame()

        # Primera pasada: Leer y consolidar todos los CSVs
        for archivo_csv, estructura in archivos_csv.items():
            print(f"Leyendo archivo: {archivo_csv}")
            
            df = pd.read_csv(archivo_csv, encoding='iso-8859-1', dtype=str)
            
            # Mapeo de columnas
            df.rename(columns=estructura['mapeo_columnas'], inplace=True)
            
            # Validar cédula
            df['numero_cedula'] = df.apply(lambda row: validate_cedula(row['numero_cedula']), axis=1)
            df = df[df['numero_cedula'].notna()]
            
            # Consolidar datos
            if df_consolidado.empty:
                df_consolidado = df
            else:
                # Merge basado en número de cédula
                df_consolidado = pd.merge(
                    df_consolidado, 
                    df,
                    on='numero_cedula',
                    how='outer',
                    suffixes=('', '_new')
                )
                
                # Combinar columnas
                for col in df.columns:
                    if col != 'numero_cedula':
                        col_new = f"{col}_new"
                        if col_new in df_consolidado.columns:
                            df_consolidado[col] = df_consolidado[col].fillna(df_consolidado[col_new])
                            df_consolidado.drop(col_new, axis=1, inplace=True)

        # Limpiar y estandarizar datos consolidados
        if 'nombre' in df_consolidado.columns:
            df_consolidado['nombre'] = df_consolidado['nombre'].apply(clean_string)
        if 'apellido' in df_consolidado.columns:
            df_consolidado['apellido'] = df_consolidado['apellido'].apply(clean_string)
        if 'fecha_nacimiento' in df_consolidado.columns:
            df_consolidado['fecha_nacimiento'] = df_consolidado['fecha_nacimiento'].apply(format_date)
        if 'sexo' in df_consolidado.columns:
            df_consolidado['sexo'] = df_consolidado['sexo'].map({'1': 'F', '2': 'M', 'F': 'F', 'M': 'M'})

        # Asegurar todas las columnas necesarias
        columnas_tabla = list(set().union(*[e['columnas_tabla'] for e in archivos_csv.values()]))
        for columna in columnas_tabla:
            if columna not in df_consolidado.columns:
                df_consolidado[columna] = None

        # Insertar o actualizar datos
        data_to_insert = []
        errors = []
        
        for idx, row in df_consolidado.iterrows():
            try:
                record = tuple(None if pd.isna(val) else val for val in row[columnas_tabla])
                data_to_insert.append(record)
            except Exception as e:
                errors.append({
                    'row_number': idx + 2,
                    'data': row.to_dict(),
                    'error': str(e)
                })

        if data_to_insert:
            try:
                # Crear tabla temporal
                temp_table = f"temp_{tabla_destino.replace('.', '_')}"
                cursor.execute(f"""
                    CREATE TEMP TABLE {temp_table} AS 
                    SELECT * FROM {tabla_destino} WITH NO DATA
                """)

                # Insertar datos en tabla temporal
                execute_values(
                    cursor,
                    f"INSERT INTO {temp_table} ({', '.join(columnas_tabla)}) VALUES %s",
                    data_to_insert,
                    page_size=1000
                )

                # Realizar upsert
                cursor.execute(f"""
                    INSERT INTO {tabla_destino}
                    SELECT DISTINCT ON (numero_cedula) *
                    FROM {temp_table}
                    ON CONFLICT (numero_cedula) DO UPDATE
                    SET 
                        nombre = COALESCE(EXCLUDED.nombre, {tabla_destino}.nombre),
                        apellido = COALESCE(EXCLUDED.apellido, {tabla_destino}.apellido),
                        fecha_nacimiento = COALESCE(EXCLUDED.fecha_nacimiento, {tabla_destino}.fecha_nacimiento),
                        sexo = COALESCE(EXCLUDED.sexo, {tabla_destino}.sexo),
                        direccion = COALESCE(EXCLUDED.direccion, {tabla_destino}.direccion),
                        id_distrito = COALESCE(EXCLUDED.id_distrito, {tabla_destino}.id_distrito),
                        id_dpto = COALESCE(EXCLUDED.id_dpto, {tabla_destino}.id_dpto),
                        zona = COALESCE(EXCLUDED.zona, {tabla_destino}.zona),
                        lugar_nacimiento = COALESCE(EXCLUDED.lugar_nacimiento, {tabla_destino}.lugar_nacimiento),
                        fecha_defuncion = COALESCE(EXCLUDED.fecha_defuncion, {tabla_destino}.fecha_defuncion)
                """)

                conn.commit()
                print(f"Procesados {len(data_to_insert)} registros")

            except Exception as e:
                conn.rollback()
                print(f"Error en inserción: {e}")

        if errors:
            error_df = pd.DataFrame(errors)
            error_df.to_csv("log_errores_consolidado.csv", index=False, encoding='utf-8')
            print(f"Se encontraron {len(errors)} errores. Ver log_errores_consolidado.csv")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error general: {e}")
        if 'conn' in locals() and conn:
            conn.close()
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
# Uso con el detalle_archivos existente
cargar_archivos_csv_a_postgresql(detalle_archivos, "gf.cedulas")
