import dbfread
import psycopg2
from tqdm import tqdm

# Establecer conexión con la base de datos
conn = psycopg2.connect(
    dbname="Brisa_Assistance",
    user="postgres",
    password="salmos23",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Leer datos del archivo DBF
dbf_file = 'D:/SOFTWARE/GPS/INEC/CARTOGRAFÍA/Códigos cartográficos/LOCALES_DE_SALUD_DGEEC2012.dbf'

# Contar el número total de registros
num_records = sum(1 for _ in dbfread.DBF(dbf_file, encoding='latin-1'))

# Crear una barra de progreso
pbar = tqdm(total=num_records, desc="Cargando datos")

for record in dbfread.DBF(dbf_file, encoding='latin-1'):
    # Buscar el dpto_id correspondiente
    cur.execute("SELECT dpto_id FROM departamentos WHERE dpto = %s", (record['DPTO'],))
    dpto_id = cur.fetchone()[0]
    
    # Buscar el distrito_id correspondiente
    cur.execute("SELECT distrito_id FROM distritos WHERE dpto = %s AND distrito = %s", (record['DPTO'], record['DISTRITO']))
    distrito_id = cur.fetchone()[0]
    
    # Crear el objeto GEOGRAPHY a partir de la longitud y latitud
    ubicacion = f"POINT({record['LONGITUD']} {record['LATITUD']})"
    
    # Insertar en la tabla SQL
    cur.execute("""
        INSERT INTO locales_salud (dpto_id, distrito_id, nombre, ubicacion)
        VALUES (%s, %s, %s, ST_GeographyFromText(%s))
    """, (dpto_id, distrito_id, record['NOMBRE'], ubicacion))
    
    # Actualizar la barra de progreso
    pbar.update(1)

# Cerrar la barra de progreso
pbar.close()

# Confirmar cambios y cerrar conexión
conn.commit()
cur.close()
conn.close()