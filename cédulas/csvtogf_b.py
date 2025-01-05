import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm
from time import time

# Función mejorada para cargar datos
def cargar_archivos_csv_a_postgresql(archivos_csv, tabla_destino):
    """Carga datos de múltiples CSVs a una tabla de PostgreSQL, manejando errores."""
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for archivo_csv, estructura in archivos_csv.items():
            print(f"Procesando archivo: {archivo_csv}")

            # Leer archivo CSV
            df = pd.read_csv(archivo_csv, encoding='iso-8859-1', on_bad_lines='skip')

            # Mapeo de columnas dinámico
            columnas_mapeo = estructura['mapeo_columnas']
            df.rename(columns=columnas_mapeo, inplace=True)

            # Añadir columnas faltantes con valores nulos
            for columna in estructura['columnas_tabla']:
                if columna not in df.columns:
                    df[columna] = None

            # Convertir el campo 'sexo'
            if 'sexo' in df.columns:
                df['sexo'] = df['sexo'].map({1: 'F', 2: 'M'})

            # Filtrar columnas necesarias para la tabla destino
            columnas = estructura['columnas_tabla']
            df = df[columnas]

            # Preparar datos para insertar
            datos = [tuple(row) for row in df.to_numpy()]
            errores = []

            # Insertar datos
            start_time = time()
            with tqdm(total=len(datos), desc=f"Cargando {os.path.basename(archivo_csv)}", unit="registro") as pbar:
                for i in range(len(datos)):
                    try:
                        cursor.execute(f"""
                            INSERT INTO {tabla_destino} ({', '.join(columnas)})
                            VALUES %s
                            ON CONFLICT (numero_cedula) DO NOTHING
                        """, (datos[i],))
                        conn.commit()
                    except Exception as e:
                        # Registrar fila conflictiva
                        errores.append((datos[i], str(e)))
                    finally:
                        pbar.update(1)

            # Guardar errores en un archivo
            if errores:
                errores_df = pd.DataFrame(errores, columns=['fila', 'error'])
                error_file = f"{os.path.basename(archivo_csv).split('.')[0]}_errores.csv"
                errores_df.to_csv(error_file, index=False, encoding='utf-8')
                print(f"Errores guardados en {error_file}")

            end_time = time()
            print(f"Carga de {archivo_csv} completada en {end_time - start_time:.2f} segundos.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error global: {e}")
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
    "D:/PADRONES/csvs/Cédulas/padrón 2017 anr_w1252.csv": {
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
