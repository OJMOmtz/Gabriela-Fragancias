from dbfread import DBF
import psycopg2
from tqdm import tqdm

conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost"
)

dbf_path = "D:/SOFTWARE/GPS/INEC/CARTOGRAFÍA/PAIS/Distritos_Paraguay.dbf"
table = DBF(dbf_path, encoding='latin1')

cur = conn.cursor()

# Contar el número total de registros en el archivo DBF
total_records = len(list(table))

# Crear una barra de progreso
progress_bar = tqdm(total=total_records, unit='registro')

# Reiniciar la posición del archivo DBF
table = DBF(dbf_path, encoding='latin1')

for record in table:
    cur.execute("SELECT dpto_id FROM departamentos WHERE dpto = %s", (record["DPTO"],))
    dpto_id = cur.fetchone()[0]
    
    cur.execute(
        "INSERT INTO distritos (dpto_id, distrito, dist_desc, clave) VALUES (%s, %s, %s, %s)",
        (dpto_id, record["DISTRITO"], record["DIST_DESC"], record["CLAVE"])
    )
    
    # Actualizar la barra de progreso
    progress_bar.update(1)

conn.commit()
cur.close()
conn.close()

# Cerrar la barra de progreso
progress_bar.close()
