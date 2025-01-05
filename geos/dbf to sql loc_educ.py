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
dbf_file = 'D:/SOFTWARE/GPS/INEC/CARTOGRAFÍA/Códigos cartográficos/LOCALES_EDUCATIVOS_DGEEC2012.dbf'

# Contar el número total de registros
num_records = sum(1 for _ in dbfread.DBF(dbf_file, encoding='latin-1'))

# Crear una barra de progreso
pbar = tqdm(total=num_records, desc="Cargando datos")

for record in dbfread.DBF(dbf_file, encoding='latin-1'):
    # Buscar el dpto_id correspondiente
    cur.execute("SELECT dpto_id FROM departamentos WHERE dpto = %s", (record['DPTO'],))
    dpto_id = cur.fetchone()[0]
    
    # Buscar el distrito_id correspondiente
    cur.execute("SELECT distrito_id FROM distritos WHERE distrito = %s", (record['DISTRITO'],))
    distrito_id = cur.fetchone()[0]
    
    # Insertar datos en la tabla locales_educativos
    cur.execute("""
        INSERT INTO locales_educativos (dpto_id, distrito_id, nombre, ubicacion)
        VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
    """, (dpto_id, distrito_id, record['NOMBRE'], record['LONGITUD'], record['LATITUD']))
    
    # Actualizar la barra de progreso
    pbar.update(1)

# Commitear los cambios
conn.commit()

# Cerrar la barra de progreso
pbar.close()