import geopandas as gpd
from sqlalchemy import create_engine
import fiona
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
    "barrios_localidades": [r"D:\Web\Barrios_Localidades_Paraguay.shp"],
    "ciudades_paraguay": [r"D:\Web\Ciudades_Paraguay.shp"],
    "comunidades_indigenas": [r"D:\Web\Comunidades_Indigenas_Paraguay.shp"],
    "departamentos": [r"D:\Web\Departamentos_Paraguay.shp"],
    "distritos": [r"D:\Web\Distritos_Paraguay.shp"],
    "hidrografia": [r"D:\Web\Hidrografia_Paraguay.shp"],
    "locales_de_salud": [r"D:\Web\LOCALES_DE_SALUD_DGEEC2012.shp"],
    "locales_educativos": [r"D:\Web\LOCALES_EDUCATIVOS_DGEEC2012.shp"],
    "locales_policiales": [r"D:\Web\LOCALES_POLICIALES_DGEEC2012.shp"],
    "manzanas": [r"D:\Web\Manzanas_Paraguay.shp"],
    "vias_principales": [r"D:\Web\Vias_principales_Paraguay.shp"],
    "vias": [r"D:\Web\Vias_Paraguay.shp"],
    "codigos_postales": [r"D:\Web\ZONA_POSTAL_PARAGUAY.shp"]
}

# Función para procesar diferentes formatos
def read_geospatial_file(file_paths):
    for path in file_paths:
        try:
            with fiona.Env(SHAPE_RESTORE_SHX="YES"):
                return gpd.read_file(path)
        except Exception as e:
            print(f"Error leyendo {path}: {e}")
    raise FileNotFoundError("No se pudo leer ningún archivo válido.")

# Función para extraer coordenadas
def extract_coordinates(gdf):
    gdf = gdf.copy()
    gdf = gdf.to_crs("EPSG:3857")  # Re-project to a projected CRS (e.g., EPSG:3857)
    gdf["longitude"] = gdf.geometry.centroid.x
    gdf["latitude"] = gdf.geometry.centroid.y
    return gdf

# Set SHAPE_RESTORE_SHX configuration option
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

# Procesar y cargar datos para cada tabla
for table, file_paths in sources.items():
    try:
        print(f"Procesando la tabla {table} desde {file_paths}...")
        gdf = read_geospatial_file(file_paths)
        gdf = extract_coordinates(gdf)

        # Ajustar columnas según la tabla y los nombres de columna reales
        if table == "barrios_localidades":
            gdf = gdf[["CLAVE", "longitude", "latitude"]]
        elif table == "ciudades_paraguay":
            gdf = gdf[["CLAVE", "longitude", "latitude"]]
        elif table == "codigos_postales":
            gdf = gdf[["COD_POST", "longitude", "latitude"]]
        elif table == "departamentos":
            gdf = gdf[["DPTO_DESC", "longitude", "latitude"]]
        elif table == "distritos":
            gdf = gdf[["CLAVE", "longitude", "latitude"]]
        elif table == "hidrografia":
            gdf = gdf[["NOMBRE", "longitude", "latitude"]]
        elif table in ["locales_de_salud", "locales_educativos", "locales_policiales"]:
            gdf = gdf[["NOMBRE", "longitude", "latitude"]]
        elif table == "manzanas":
            gdf = gdf[["CLAVE", "longitude", "latitude"]]
        elif table in ["vias", "vias_principales"]:
            gdf = gdf[["NOMBRE", "longitude", "latitude"]]
        else:
            gdf = gdf[["longitude", "latitude"]]

        # Cargar a la base de datos
        gdf.to_sql(f"gf.{table}", engine, if_exists="replace", index=False)
        print(f"Datos cargados exitosamente para la tabla {table}.")

    except Exception as e:
        print(f"Error procesando {table}: {e}")

print("Proceso finalizado.")
