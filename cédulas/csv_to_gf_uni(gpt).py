import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from typing import List

def conectar_bd():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="Gabriela_Fragancias",
        user="postgres",
        password="salmos23"
    )

def cargar_csv_directo(csv_files: List[str], tabla_destino: str):
    """
    Procesa y carga los CSV directamente a PostgreSQL.
    """
    conn = conectar_bd()
    cur = conn.cursor()

    try:
        # Desactivar índices y triggers para optimizar la inserción masiva
        cur.execute(f"ALTER TABLE {tabla_destino} DISABLE TRIGGER ALL;")
        conn.commit()

        for csv_file in csv_files:
            print(f"Procesando archivo: {csv_file}")

            # Leer el CSV
            data = pd.read_csv(csv_file, encoding="windows-1252", on_bad_lines="skip")

            # Normalizar columnas
            columnas_esperadas = [
                "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo",
                "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
            ]

            for col in columnas_esperadas:
                if col not in data.columns:
                    data[col] = None  # Añadir columnas faltantes

            data = data[columnas_esperadas]  # Asegurar el orden de las columnas

            # Insertar en la base de datos por lotes
            registros = data.values.tolist()
            execute_batch(
                cur,
                f"""
                INSERT INTO {tabla_destino} (
                    numero_cedula, nombre, apellido, fecha_nacimiento, sexo,
                    direccion, id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                registros,
                page_size=1000
            )
            conn.commit()

            print(f"Archivo {csv_file} cargado correctamente.")

    except Exception as e:
        print(f"Error durante la carga: {e}")
        conn.rollback()
    finally:
        # Reactivar índices y triggers
        cur.execute(f"ALTER TABLE {tabla_destino} ENABLE TRIGGER ALL;")
        conn.commit()
        cur.close()
        conn.close()

def unificar_csvs(csv_files: List[str], output_file: str):
    """
    Combina múltiples CSV en un único archivo ajustado a las columnas de la tabla destino.
    """
    columnas_esperadas = [
        "numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo",
        "direccion", "id_distrito", "id_dpto", "zona", "lugar_nacimiento", "fecha_defuncion"
    ]

    datos_unificados = []

    for csv_file in csv_files:
        print(f"Leyendo archivo: {csv_file}")
        try:
            data = pd.read_csv(csv_file, encoding="windows-1252", on_bad_lines="skip")

            # Normalizar columnas
            for col in columnas_esperadas:
                if col not in data.columns:
                    data[col] = None  # Añadir columnas faltantes

            data = data[columnas_esperadas]  # Ordenar las columnas
            datos_unificados.append(data)

        except Exception as e:
            print(f"Error leyendo {csv_file}: {e}")

    # Combinar todos los datos y exportar
    if datos_unificados:
        df_final = pd.concat(datos_unificados, ignore_index=True)
        df_final.to_csv(output_file, index=False, encoding="windows-1252")
        print(f"CSV unificado guardado en: {output_file}")
    else:
        print("No se pudieron procesar los archivos CSV.")

if __name__ == "__main__":
    # Lista de archivos CSV a procesar
    ruta_csvs = "D:/PADRONES/csvs/Cédulas"
    archivos_csv = [os.path.join(ruta_csvs, f) for f in os.listdir(ruta_csvs) if f.endswith(".csv")]

    # Opción 1: Cargar directamente a PostgreSQL
    print("--- Carga directa a PostgreSQL ---")
    cargar_csv_directo(archivos_csv, "gf.cedulas")

    # Opción 2: Unificar todos los CSV
    print("--- Unificación de CSVs ---")
    archivo_unificado = "D:/PADRONES/csvs/Cédulas/unificado.csv"
    unificar_csvs(archivos_csv, archivo_unificado)
