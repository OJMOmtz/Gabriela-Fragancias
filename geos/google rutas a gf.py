import geopandas as gpd
from geoalchemy2 import Geography
from sqlalchemy import create_engine

# Leer el archivo KML
file_path = "D:/IA provechar/GPS_DB_ANALYZER/Rutas GF.kml"
gdf = gpd.read_file(file_path)

# Extraer las coordenadas de los puntos
gdf["longitude"] = gdf.geometry.x
gdf["latitude"] = gdf.geometry.y

# Renombrar la columna "Name" a "nombre"
gdf = gdf.rename(columns={"Name": "nombre"})

# Seleccionar las columnas relevantes
gdf = gdf[["nombre", "longitude", "latitude"]]

# Convertir las columnas de longitud y latitud a cadenas WKT
gdf["ubicacion"] = gdf.apply(lambda row: f"POINT({row['longitude']} {row['latitude']})", axis=1)

# Eliminar las columnas "longitude" y "latitude"
gdf = gdf.drop(columns=["longitude", "latitude"])

# Configurar la conexión a la base de datos
DB_CONFIG = {
    'dbname': 'Gabriela_Fragancias',
    'user': 'postgres',
    'password': 'salmos23',
    'host': 'localhost',
    'port': 5432
}
db_connection = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
engine = create_engine(db_connection)

# Cargar los datos en la tabla `gf.puntos_ruta`
gdf.to_sql("gf.puntos_ruta", engine, if_exists="append", index=False, dtype={"ubicacion": Geography("Point", srid=4326)})
