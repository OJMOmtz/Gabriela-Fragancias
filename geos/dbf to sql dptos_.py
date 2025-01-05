import dbfread
import psycopg2
from tqdm import tqdm

# Establecer conexión con la base de datos (ajusta los parámetros según tu configuración)
conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Read data from DBF file
dbf_file = 'D:/PADRONES/GPS/INEC/CARTOGRAFÍA/PAIS/Departamentos_Paraguay.dbf'

# Contar el número total de registros
num_records = sum(1 for _ in dbfread.DBF(dbf_file, encoding='latin-1'))

# Crear una barra de progreso
pbar = tqdm(total=num_records, desc="Cargando datos")

for record in dbfread.DBF(dbf_file, encoding='latin-1'):
    # Insert into SQL table
    cur.execute("""
        INSERT INTO gf.departamentos (dpto, dpto_desc)
        VALUES (%s, %s)
    """, (record['DPTO'], record['DPTO_DESC']))
    
    # Actualizar la barra de progreso
    pbar.update(1)

# Cerrar la barra de progreso
pbar.close()

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()
