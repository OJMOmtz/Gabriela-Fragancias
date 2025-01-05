import subprocess

def load_data_to_postgres(dbf_path, shp_path, table_name, dbname, user, password, host, port, schema):
    dbf_command = f'ogr2ogr -f "PostgreSQL" PG:"dbname={dbname} user={user} password={password} host={host} port={port}" "{dbf_path}" -nln {table_name} -nlt CONVERT_TO_INTEGER -lco SCHEMA={schema}'
    shp_command = f'ogr2ogr -f "PostgreSQL" PG:"dbname={dbname} user={user} password={password} host={host} port={port}" "{shp_path}" -nln {table_name} -nlt CONVERT_TO_INTEGER -lco SCHEMA={schema}'
    
    subprocess.run(dbf_command, shell=True)
    subprocess.run(shp_command, shell=True)

# Ejemplo de uso
load_data_to_postgres(
    "path/to/your/file.dbf",
    "path/to/your/file.shp",
    "your_table_name",
    "your_database",
    "your_user",
    "your_password",
    "localhost",
    "5432",
    "gf"
)

ogr2ogr -f "PostgreSQL" PG:"dbname=your_database user=your_user password=your_password host=localhost port=5432" "path/to/your/file.dbf" -nln your_table_name -nlt CONVERT_TO_INTEGER -lco SCHEMA=gf
ogr2ogr -f "PostgreSQL" PG:"dbname=your_database user=your_user password=your_password host=localhost port=5432" "path/to/your/file.shp" -nln your_table_name -nlt CONVERT_TO_INTEGER -lco SCHEMA=gf