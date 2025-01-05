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
    "vias": [r"D:\Web\Vias_Paraguay.dbf", r"D:\Web\Vias_Paraguay.shp"]
}

# Función para extraer coordenadas
def extract_coordinates(gdf):
    gdf = gdf.copy()
    gdf = gdf.to_crs("EPSG:3857")  # Re-project to a projected CRS (e.g., EPSG:3857)
    gdf["longitude"] = gdf.geometry.centroid.x
    gdf["latitude"] = gdf.geometry.centroid.y
    return gdf

# Procesar y cargar datos para la tabla vias
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

print("Proceso finalizado.")