# -*- coding: utf-8 -*-
"""
Script para actualizar tablas en una base de datos PostgreSQL
con coordenadas geográficas extraídas de archivos geoespaciales.
Incluye todas las tablas del esquema gf.
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
    "barrios_localidades": ["Barrios_Localidades_Paraguay.shp", "Barrios_Localidades_Paraguay.kml"],
    "ciudades_paraguay": ["Ciudades_Paraguay.shp"],
    "comunidades_indigenas": ["Comunidades_Indigenas_Paraguay.shp"],
    "departamentos": ["Departamentos_Paraguay.shp"],
    "distritos": ["Distritos_Paraguay.shp"],
    "hidrografia": ["Hidografia_Paraguay.shp"],
    "vias_principales": ["Vias_principales_Paraguay.shp"],
    "vias": ["Vias_Paraguay.shp"],
    "manzanas": ["Manzanas_Paraguay.shp"],
    "locales_de_salud": ["LOCALES_DE_SALUD_DGEEC2012.shp"],
    "locales_educativos": ["LOCALES_EDUCATIVOS_DGEEC2012.shp"],
    "locales_policiales": ["LOCALES_POLICIALES_DGEEC2012.shp"],
    "codigos_postales": ["ZONA_POSTAL_PARAGUAY.shp"]
}

# Función para procesar diferentes formatos
def read_geospatial_file(file_paths):
    for path in file_paths:
        try:
            return gpd.read_file(path)
        except Exception as e:
            print(f"Error leyendo {path}: {e}")
    raise FileNotFoundError("No se pudo leer ningún archivo válido.")

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
for table, file_paths in sources.items():
    try:
        print(f"Procesando la tabla {table} desde {file_paths}...")
        gdf = read_geospatial_file(file_paths)
        gdf = extract_coordinates(gdf)

        # Ajustar columnas según la tabla
        if table == "barrios_localidades":
            gdf = gdf[["clave", "longitude", "latitude"]]
        elif table == "ciudades_paraguay":
            gdf = gdf[["clave", "longitude", "latitude"]]
        elif table == "comunidades_indigenas":
            gdf = gdf[["comunidad", "longitude", "latitude"]]
        elif table in ["locales_de_salud", "locales_educativos", "locales_policiales"]:
            gdf = gdf[["nombre", "longitude", "latitude"]]
        elif table == "codigos_postales":
            gdf = gdf[["cod_post", "longitude", "latitude"]]
        elif table in ["vias", "vias_principales"]:
            gdf = gdf[["nombre", "longitude", "latitude"]]
        else:
            gdf = gdf[["longitude", "latitude"]]

        # Cargar a la base de datos
        gdf.to_sql(f"gf.{table}", engine, if_exists="replace", index=False)
        print(f"Datos cargados exitosamente para la tabla {table}.")

    except Exception as e:
        print(f"Error procesando {table}: {e}")

print("Proceso finalizado.")
