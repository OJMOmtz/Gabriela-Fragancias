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
dbf_file = 'D:/PADRONES/GPS/INEC/CARTOGRAFÍA/PAIS/Vias_Paraguay.dbf'

# Contar el número total de registros en el archivo DBF
table = dbfread.DBF(dbf_file, encoding='latin-1')
total_records = len(list(table))

# Crear una barra de progreso
progress_bar = tqdm(total=total_records, unit='registro')

# Reiniciar la posición del archivo DBF
table = dbfread.DBF(dbf_file, encoding='latin-1')

for record in table:
    try:
        cur.execute(
            "INSERT INTO gf.vias (nombre, tipo, ancho, dpto, dpto_desc) VALUES (%s, %s, %s, %s, %s)",
            (record['NOMBRE'], record['TIPO'], record['ANCHO'], record['DPTO'], record['DPTO_DESC'])
        )
    except psycopg2.errors.UniqueViolation:
        # Duplicado, omitir inserción
        conn.rollback()
    else:
        # Confirmar cambios si no hay error
        conn.commit()
    
    # Actualizar la barra de progreso
    progress_bar.update(1)

cur.close()
conn.close()

# Cerrar la barra de progreso
progress_bar.close()