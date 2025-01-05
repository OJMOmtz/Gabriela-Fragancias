import dbfread
import psycopg2
from tqdm import tqdm

# Establecer conexión con la base de datos
conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Leer datos del archivo DBF
dbf_file = 'D:/SOFTWARE/GPS/INEC/CARTOGRAFÍA/PAIS/Comunidades_Indigenas_Paraguay.dbf'

# Contar el número total de registros
num_records = sum(1 for _ in dbfread.DBF(dbf_file, encoding='latin-1'))

# Crear una barra de progreso
pbar = tqdm(total=num_records, desc="Cargando datos")

for record in dbfread.DBF(dbf_file, encoding='latin-1'):
    # Buscar el distrito_id correspondiente
    cur.execute("SELECT distrito_id FROM distritos WHERE dist_desc = %s", (record['DIST_DESC'],))
    result = cur.fetchone()
    distrito_id = result[0] if result else None
    
    # Insertar en la tabla SQL
    cur.execute("""
        INSERT INTO comunidades_indigenas (distrito_id, area, bar_loc, barlo_desc, comunidad, aldea, com_desc, pueblo_etn, cod_pueblo, familia)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (distrito_id, record['AREA'], record['BAR_LOC'], record['BARLO_DESC'], record['COMUNIDAD'], record['ALDEA'], record['COM_DESC'], record['PUEBLO_ETN'], record['COD_PUEBLO'], record['FAMILIA']))
    
    # Actualizar la barra de progreso
    pbar.update(1)

# Cerrar la barra de progreso
pbar.close()

# Confirmar cambios y cerrar conexión
conn.commit()
cur.close()
conn.close()