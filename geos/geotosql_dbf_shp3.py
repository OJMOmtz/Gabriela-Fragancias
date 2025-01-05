import geopandas as gpd
from sqlalchemy import create_engine
import os

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
    "barrios_localidades": [r"D:\Web\Barrios_Localidades_Paraguay.dbf", r"D:\Web\Barrios_Localidades_Paraguay.shp"],
    "ciudades_paraguay": [r"D:\Web\Ciudades_Paraguay.dbf", r"D:\Web\Ciudades_Paraguay.shp"],
    "comunidades_indigenas": [r"D:\Web\Comunidades_Indigenas_Paraguay.dbf", r"D:\Web\Comunidades_Indigenas_Paraguay.shp"],
    "departamentos": [r"D:\Web\Departamentos_Paraguay.dbf", r"D:\Web\Departamentos_Paraguay.shp"],
    "distritos": [r"D:\Web\Distritos_Paraguay.dbf", r"D:\Web\Distritos_Paraguay.shp"],
    "hidrografia": [r"D:\Web\Hidrografia_Paraguay.dbf", r"D:\Web\Hidrografia_Paraguay.shp"],
    "locales_de_salud": [r"D:\Web\LOCALES_DE_SALUD_DGEEC2012.dbf", r"D:\Web\LOCALES_DE_SALUD_DGEEC2012.shp"],
    "locales_educativos": [r"D:\Web\LOCALES_EDUCATIVOS_DGEEC2012.dbf", r"D:\Web\LOCALES_EDUCATIVOS_DGEEC2012.shp"],
    "locales_policiales": [r"D:\Web\LOCALES_POLICIALES_DGEEC2012.dbf", r"D:\Web\LOCALES_POLICIALES_DGEEC2012.shp"],
    "manzanas": [r"D:\Web\Manzanas_Paraguay.dbf", r"D:\Web\Manzanas_Paraguay.shp"],
    "vias_principales": [r"D:\Web\Vias_principales_Paraguay.dbf", r"D:\Web\Vias_principales_Paraguay.shp"],
    "vias": [r"D:\Web\Vias_Paraguay.dbf", r"D:\Web\Vias_Paraguay.shp"],
    "codigos_postales": [r"D:\Web\ZONA_POSTAL_PARAGUAY.dbf", r"D:\Web\ZONA_POSTAL_PARAGUAY.shp"]
}

# Función para extraer coordenadas
def extract_coordinates(gdf):
    gdf = gdf.copy()
    gdf = gdf.to_crs("EPSG:3857")  # Re-project to a projected CRS (e.g., EPSG:3857)
    gdf["longitude"] = gdf.geometry.centroid.x
    gdf["latitude"] = gdf.geometry.centroid.y
    return gdf

# Procesar y cargar datos para cada tabla
for table, file_paths in sources.items():
    try:
        print(f"Procesando la tabla {table} desde {file_paths}...")
        dbf_path, shp_path = file_paths
        gdf_dbf = gpd.read_file(dbf_path)
        gdf_shp = gpd.read_file(shp_path)
        gdf = gdf_dbf.merge(gdf_shp, on="geometry")
        gdf = extract_coordinates(gdf)

        # Seleccionar columnas relevantes
        relevant_columns = list(gdf_dbf.columns) + ["longitude", "latitude"]
        gdf = gdf[relevant_columns]

        # Cargar a la base de datos
        gdf.to_sql(f"gf.{table}", engine, if_exists="append", index=False)
        print(f"Datos cargados exitosamente para la tabla {table}.")

    except Exception as e:
        print(f"Error procesando {table}: {e}")

print("Proceso finalizado