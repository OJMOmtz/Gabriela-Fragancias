from dbfread import DBF
import psycopg2
from tqdm import tqdm

conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost"
)

dbf_path = "D:/PADRONES/GPS/INEC/CARTOGRAFÍA/PAIS/Ciudades_Paraguay.dbf"
table = DBF(dbf_path, encoding='iso-8859-1')

cur = conn.cursor()

# Contar el número total de registros en el archivo DBF
total_records = len(list(table))

# Crear una barra de progreso
progress_bar = tqdm(total=total_records, unit='registro')

# Reiniciar la posición del archivo DBF
table = DBF(dbf_path, encoding='utf-8')

for record in table:
    try:
        cur.execute(
            "INSERT INTO gf.ciudades_paraguay (dpto, dpto_desc, distrito,  dist_desc, clave) VALUES (%s, %s, %s, %s, %s)",
            (record["DPTO"], record["DPTO_DESC"],  record["DISTRITO"],record["DIST_DESC"], record["CLAVE"])
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