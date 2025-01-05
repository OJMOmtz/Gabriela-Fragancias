import pandas as pd
from dbfread import DBF
import geopandas as gpd
import psycopg2

conn = psycopg2.connect(host="localhost", database="Gabriela_Fragancias", user="usuario", password="contraseña")
cur = conn.cursor()

# Función para leer DBF
def importar_dbf(archivo_dbf):
    table = DBF(archivo_dbf)
    df = pd.DataFrame(iter(table))
    return df

# Insertar datos de DBF en PostgreSQL
df_vehiculos = importar_dbf('ruta/vehiculos.dbf')
for _, row in df_vehiculos.iterrows():
    cur.execute(
        "INSERT INTO Vehiculos (placa, marca, modelo, numero_motor, numero_chasis) VALUES (%s, %s, %s, %s, %s)",
        (row['NROCHAPA'], row['MARCA'], row['MODELO'], row['NROMOTOR'], row['NROCHASIS'])
    )

conn.commit()
cur.close()