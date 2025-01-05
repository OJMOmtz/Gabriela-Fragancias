# -*- coding: utf-8 -*-
"""
Script para actualizar tablas en una base de datos PostgreSQL
con coordenadas geográficas extraídas de archivos GeoJSON.
"""

import geopandas as gpd
from sqlalchemy import create_engine

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'dbname': 'Gabriela_Fragancias',
    'user': 'postgres',
    'password': 'salmos23',
    'host': 'localhost',
    'port': 5432
}
db_connection = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
engine = create_engine(db_connection)

# Definir archivos y tablas
sources = {
    "barrios_localidades": "Barrios_Localidades_Paraguay.geojson",
    "ciudades_paraguay": "Ciudades_Paraguay.geojson",
    "comunidades_indigenas": "Comunidades_Indigenas_Paraguay.geojson",
    "departamentos": "Departamentos_Paraguay.geojson",
    "distritos": "Distritos_Paraguay.geojson",
    "vias_principales": "Vias_principales_Paraguay.geojson",
    "manzanas": "Manzanas_Paraguay.geojson"
}

# Función para extraer coordenadas

def extract_coordinates(gdf):
    """
    Extrae las coordenadas centroides de un GeoDataFrame
    y agrega columnas de longitud y latitud.
    """
    gdf = gdf.copy()
    gdf["longitude"] = gdf.geometry.centroid.x
    gdf["latitude"] = gdf.geometry.centroid.y
    return gdf

# Procesar y cargar datos para cada tabla
for table, file_path in sources.items():
    try:
        print(f"Procesando la tabla {table} desde {file_path}...")
        gdf = gpd.read_file(file_path)
        gdf = extract_coordinates(gdf)

        # Seleccionar columnas relevantes para exportar
        if table == "barrios_localidades":
            gdf = gdf[["CLAVE", "longitude", "latitude"]]
        elif table == "ciudades_paraguay":
            gdf = gdf[["CLAVE", "longitude", "latitude"]]
        elif table == "comunidades_indigenas":
            gdf = gdf[["COMUNIDAD", "longitude", "latitude"]]
        else:
            gdf = gdf[["longitude", "latitude"]]

        # Cargar a la base de datos
        gdf.to_sql(f"gf.{table}", engine, if_exists="replace", index=False)
        print(f"Datos cargados exitosamente para la tabla {table}.")

    except Exception as e:
        print(f"Error procesando {table}: {e}")

print("Proceso finalizado.")
