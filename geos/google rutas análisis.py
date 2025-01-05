import geopandas as gpd

file_path = "D:/IA provechar/GPS_DB_ANALYZER/Rutas GF.kml"
gdf = gpd.read_file(file_path)

print(gdf.columns)
