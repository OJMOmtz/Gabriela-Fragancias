import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from tqdm import tqdm
from time import time

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

def cargar_archivos_csv_a_postgresql(archivos_csv, tabla_destino, batch_size=1000):
    """Carga datos de múltiples CSVs a una tabla de PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Agregar columnas faltantes
        agregar_columnas_faltantes(cursor)
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
                    df['fecha_nacimiento'] = pd.to_datetime(
                        df['fecha_nacimiento'],
                        format='%Y%m%d',
                        errors='coerce'
                    )
                    df['fecha_nacimiento'] = df['fecha_nacimiento'].where(pd.notnull(df['fecha_nacimiento']), None)  # Convierte NaT a None
                                
                # Añadir solo las columnas faltantes que existen en la tabla
                columnas_a_insertar = []
                for col in estructura['columnas_tabla']:
                    if col in columnas_existentes:
                        if col not in df.columns:
                            df[col] = None
                        columnas_a_insertar.append(col)
                
                # Preparar datos para inserción
                datos = [tuple(x) for x in df[columnas_a_insertar].values]
                
                # Insertar datos en lotes con barra de progreso
                start_time = time()
                total_lotes = (len(datos) + batch_size - 1) // batch_size
                
                with tqdm(total=len(datos), 
                         desc="Insertando registros", 
                         unit="reg", 
                         miniters=batch_size, 
                         smoothing=0.1) as pbar:
                    
                    for i in range(0, len(datos), batch_size):
                        batch = datos[i:i + batch_size]
                        execute_batch(cursor, f"""
                            INSERT INTO {tabla_destino} ({', '.join(columnas_a_insertar)})
                            VALUES ({', '.join(['%s'] * len(columnas_a_insertar))})
                            ON CONFLICT (numero_cedula) DO NOTHING
                        """, batch)
                        conn.commit()
                        pbar.update(len(batch))
                
                tiempo_total = time() - start_time
                registros_por_segundo = len(datos) / tiempo_total
                print(f"\nRegistros procesados: {len(datos):,}")
                print(f"Tiempo total: {tiempo_total:.2f} segundos")
                print(f"Velocidad: {registros_por_segundo:.2f} registros/segundo")
                
            except Exception as e:
                print(f"Error procesando {nombre_archivo}: {str(e)}")
                conn.rollback()
                continue
        
        cursor.close()
        conn.close()
        print("\nProceso completado exitosamente.")
        
    except Exception as e:
        print(f"Error de conexión: {str(e)}")

# Configuración de archivos y estructura
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
            "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", 
            "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", 
            "fecha_defuncion"
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
    }
}

# Ejecutar el proceso
if __name__ == "__main__":
    cargar_archivos_csv_a_postgresql(detalle_archivos, "gf.cedulas")
