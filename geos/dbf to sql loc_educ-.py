import dbfread
import psycopg2
from unidecode import unidecode

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
dbf_file = 'D:/PADRONES/GPS/INEC/CARTOGRAFÍA/Códigos cartográficos/LOCALES_EDUCATIVOS_DGEEC2012.dbf'

# Contar el número total de registros
num_records = len(dbfread.DBF(dbf_file, encoding='utf-8'))

# Crear una variable para llevar la cuenta del progreso
progress = 0

for record in dbfread.DBF(dbf_file, encoding='utf-8'):
    # Buscar el dpto_id correspondiente
    cur.execute("SELECT id_dpto FROM gf.departamentos WHERE dpto = %s", (record['DPTO'],))
    dpto_id = cur.fetchone()[0]
    
    # Buscar el distrito_id correspondiente
    cur.execute("SELECT id_distrito FROM gf.distritos WHERE distrito = %s", (record['DISTRITO'],))
    distrito_id = cur.fetchone()[0]
    
    # Convertir el nombre a ASCII usando unidecode y acortarlo a 56 caracteres
    nombre = unidecode(record['NOMBRE'])[:56]
    
    # Insertar datos en la tabla locales_educativos
    cur.execute("""
        INSERT INTO gf.locales_educativos (id_dpto, id_distrito, nombre, ubicacion)
        VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
    """, (id_dpto, id_distrito, nombre, record['LONGITUD'], record['LATITUD']))
    
    # Actualizar el progreso
    progress += 1
    print(f"Progreso: {progress}/{num_records}")

# Commitear los cambios
conn.commit()

# Cerrar la conexión
conn.close()

print("¡Proceso finalizado con éxito!")
