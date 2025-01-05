import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from tqdm import tqdm
from time import time
from datetime import datetime

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'dbname': 'Gabriela_Fragancias',
    'user': 'postgres',
    'password': 'salmos23',
    'host': 'localhost',
    'port': 5432
}

def obtener_columnas_existentes(cursor, tabla):
    """Obtiene las columnas existentes en la tabla destino."""
    cursor.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'gf' AND table_name = 'cedulas'
    """)
    return [row[0] for row in cursor.fetchall()]

def agregar_columnas_faltantes(cursor):
    """Agrega columnas faltantes a la tabla si no existen."""
    columnas_faltantes = {
        'direccion': 'text',
        'id_distrito': 'character varying(2)',
        'id_dpto': 'character varying(2)',
        'zona': 'character varying(2)',
        'lugar_nacimiento': 'character varying(100)',
        'fecha_defuncion': 'date'
    }
    for columna, tipo in columnas_faltantes.items():
        cursor.execute(f"""
            DO $$ BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_schema = 'gf' AND table_name = 'cedulas' AND column_name = '{columna}'
                ) THEN
                    ALTER TABLE gf.cedulas ADD COLUMN {columna} {tipo};
                END IF;
            END $$;
        """)

def es_fecha_valida(fecha):
    """Verifica si una fecha es válida, considerando años bisiestos."""
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def cargar_archivos_csv_a_postgresql(archivos_csv, tabla_destino):
    """Carga datos de múltiples CSVs a una tabla de PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Agregar columnas faltantes
        agregar_columnas_faltantes(cursor)
        conn.commit()

        # Desactivar índices temporalmente
        cursor.execute("ALTER TABLE gf.cedulas DISABLE TRIGGER ALL;")
        conn.commit()
        
        # Obtener columnas existentes en la tabla
        columnas_existentes = obtener_columnas_existentes(cursor, tabla_destino)
        
        total_archivos = len(archivos_csv)
        for idx, (archivo_csv, estructura) in enumerate(archivos_csv.items(), 1):
            nombre_archivo = os.path.basename(archivo_csv)
            print(f"\n[{idx}/{total_archivos}] Procesando: {nombre_archivo}")
            
            try:
                # Leer archivo CSV con conteo de filas
                total_rows = sum(1 for _ in open(archivo_csv, encoding='iso-8859-1')) - 1
                print(f"Total registros a procesar: {total_rows:,}")
                
                # Leer solo las columnas necesarias
                columnas_necesarias = list(estructura['mapeo_columnas'].keys())
                df = pd.read_csv(
                    archivo_csv,
                    encoding='iso-8859-1',
                    usecols=columnas_necesarias,
                    on_bad_lines='skip',
                    dtype={'sexo': str, 'fecha_nacimiento': str},
                    low_memory=False
                )
                
                print(f"Registros cargados en memoria: {len(df):,}")
                
                # Mapeo de columnas y conversiones
                df.rename(columns=estructura['mapeo_columnas'], inplace=True)
                if 'sexo' in df.columns:
                    df['sexo'] = df['sexo'].astype(str).str[:1]
                if 'fecha_nacimiento' in df.columns:
                    # Validar fechas y manejar errores
                    df['fecha_nacimiento'] = pd.to_datetime(
                        df['fecha_nacimiento'],
                        format='%Y%m%d',
                        errors='coerce'
                    )
                    df['fecha_valida'] = df['fecha_nacimiento'].apply(
                        lambda x: es_fecha_valida(str(x.date())) if pd.notnull(x) else False
                    )
                
                # Filtrar registros válidos y guardar errores
                registros_validos = df[df['fecha_valida']].copy()
                registros_invalidos = df[~df['fecha_valida']].copy()
                if not registros_invalidos.empty:
                    ruta_errores = f"{archivo_csv}_errores.csv"
                    registros_invalidos.to_csv(ruta_errores, index=False, encoding='utf-8')
                    print(f"Registros inválidos guardados en: {ruta_errores}")
                
                # Añadir solo las columnas faltantes que existen en la tabla
                columnas_a_insertar = []
                for col in estructura['columnas_tabla']:
                    if col in columnas_existentes:
                        if col not in registros_validos.columns:
                            registros_validos[col] = None
                        columnas_a_insertar.append(col)
                
                # Usar execute_batch para inserción eficiente
                placeholders = ', '.join(['%s'] * len(columnas_a_insertar))
                insert_query = f"INSERT INTO {tabla_destino} ({', '.join(columnas_a_insertar)}) VALUES ({placeholders})"
                execute_batch(cursor, insert_query, registros_validos[columnas_a_insertar].values.tolist())
                conn.commit()
                print(f"Registros insertados en {nombre_archivo}: {len(registros_validos):,}")
                
            except Exception as e:
                print(f"Error procesando {nombre_archivo}: {str(e)}")
                conn.rollback()
                continue
        
        # Reactivar índices
        cursor.execute("ALTER TABLE gf.cedulas ENABLE TRIGGER ALL;")
        conn.commit()
        cursor.close()
        conn.close()
        print("\nProceso completado exitosamente.")
        
    except Exception as e:
        print(f"Error de conexión: {str(e)}")

# Configuración de archivos y estructura
detalle_archivos = {
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
        ]
    },
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
        ]
    },
}

# Ejecutar el proceso
if __name__ == "__main__":
    cargar_archivos_csv_a_postgresql(detalle_archivos, "gf.cedulas")
