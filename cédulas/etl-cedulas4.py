import pandas as pd
import psycopg2
from datetime import datetime
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CedulasETL:
    def __init__(self):
        self.db_params = {
            "dbname": "Gabriela_Fragancias",
            "user": "postgres",
            "password": "salmos23",
            "host": "localhost"
        }

        # Lista de archivos fuente con ruta completa
        self.archivos_fuente = [
            "D:/PADRONES/csvs/Cédulas/CÉDULAS-2001-limpio_utf8.csv",
            "D:/PADRONES/csvs/Cédulas/CÉDULAS-2001-l_w1252.csv",
            "D:/PADRONES/csvs/Cédulas/CÉDULAS-2001-utf8.csv",
            "D:/PADRONES/csvs/Cédulas/CÉDULAS-2024-1_ISO-8859-1.csv",
            "D:/PADRONES/csvs/Cédulas/pad_col_2017_1_w1252.csv",
            "D:/PADRONES/csvs/Cédulas/pad_col_2021_utf8.csv",
            "D:/PADRONES/csvs/Cédulas/poli02-ISO-8859-1.csv",
            "D:/PADRONES/csvs/Cédulas/regcivext_2015_utf8.csv",
            "D:/PADRONES/csvs/Cédulas/regcivext_2020_utf8.csv",
            "D:/PADRONES/csvs/Cédulas/regcivext_2021_utf8.csv",
            "D:/PADRONES/csvs/Cédulas/regciv_2010_MacRoman.csv",
            "D:/PADRONES/csvs/Cédulas/regciv_2013_ISO-8859-1.csv",
            "D:/PADRONES/csvs/Cédulas/regciv_2015_ISO-8859-1.csv",
            "D:/PADRONES/csvs/Cédulas/regciv_2018_ISO-8859-1.csv",
            "D:/PADRONES/csvs/Cédulas/regciv_2020_ISO-8859-1.csv",
            "D:/PADRONES/csvs/Cédulas/regciv_2021_ISO-8859-1.csv",
            "D:/PADRONES/csvs/Cédulas/regciv_unace_utf8.csv"
        ]

    def connect_db(self):
        """Establecer conexión con la base de datos."""
        try:
            conn = psycopg2.connect(**self.db_params)
            return conn
        except Exception as e:
            logging.error(f"Error conectando a la base de datos: {e}")
            raise

    def alter_table_to_allow_nulls(self):
        """Alterar la tabla para permitir valores nulos temporalmente."""
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                ALTER TABLE gf.cedulas ALTER COLUMN lugar_nacimiento DROP NOT NULL;
                ALTER TABLE gf.cedulas ALTER COLUMN sexo DROP NOT NULL;
            """)
            conn.commit()
            logging.info("Tabla gf.cedulas modificada para permitir valores nulos.")
        except Exception as e:
            conn.rollback()
            logging.error(f"Error alterando la tabla: {e}")
        finally:
            conn.close()

    def restore_table_constraints(self):
        """Restaurar restricciones originales."""
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                ALTER TABLE gf.cedulas ALTER COLUMN lugar_nacimiento SET NOT NULL;
                ALTER TABLE gf.cedulas ALTER COLUMN sexo SET NOT NULL;
            """)
            conn.commit()
            logging.info("Restricciones originales restauradas.")
        except Exception as e:
            conn.rollback()
            logging.error(f"Error restaurando restricciones: {e}")
        finally:
            conn.close()

    def detect_encoding(self, filename):
        """Detectar la codificación basada en el nombre del archivo."""
        if "utf8" in filename.lower():
            return "utf-8"
        elif "w1252" in filename.lower():
            return "windows-1252"
        elif "iso-8859-1" in filename.lower():
            return "iso-8859-1"
        elif "macroman" in filename.lower():
            return "macroman"
        else:
            return "utf-8"  # Valor por defecto

    def complete_null_values(self):
        """Completar valores nulos en la tabla desde otros archivos."""
        conn = self.connect_db()
        try:
            cursor = conn.cursor()

            # Leer filas con valores nulos
            query = """
                SELECT numero_cedula FROM gf.cedulas 
                WHERE lugar_nacimiento IS NULL OR sexo IS NULL;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cedulas_con_nulos = [row[0] for row in rows]

            # Procesar otros archivos para completar los datos
            for archivo in self.archivos_fuente:
                try:
                    encoding = self.detect_encoding(archivo)
                    df = pd.read_csv(archivo, dtype=str, encoding=encoding)
                    for cedula in cedulas_con_nulos:
                        match = df[df['numero_cedula'] == cedula]
                        if not match.empty:
                            # Completar datos faltantes
                            lugar_nacimiento = match['lugar_nacimiento'].iloc[0] if 'lugar_nacimiento' in match.columns else None
                            sexo = match['sexo'].iloc[0] if 'sexo' in match.columns else None

                            update_query = """
                                UPDATE gf.cedulas
                                SET lugar_nacimiento = COALESCE(lugar_nacimiento, %s),
                                    sexo = COALESCE(sexo, %s)
                                WHERE numero_cedula = %s;
                            """
                            cursor.execute(update_query, (lugar_nacimiento, sexo, cedula))
                except Exception as e:
                    logging.error(f"Error procesando archivo {archivo}: {e}")
            conn.commit()
            logging.info("Valores nulos completados.")
        except Exception as e:
            conn.rollback()
            logging.error(f"Error completando valores nulos: {e}")
        finally:
            conn.close()

    def run(self):
        """Ejecutar el ETL."""
        # Paso 1: Alterar tabla
        self.alter_table_to_allow_nulls()

        # Paso 2: Procesar y cargar datos
        logging.info("Procesar y cargar datos.")
        # Aquí usarías tu lógica existente para procesar los CSV

        # Paso 3: Completar valores nulos
        self.complete_null_values()

        # Paso 4: Restaurar restricciones
        self.restore_table_constraints()

if __name__ == "__main__":
    etl = CedulasETL()
    etl.run()
