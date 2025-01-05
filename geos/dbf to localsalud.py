from dbfread import DBF
import psycopg2
from tqdm import tqdm

conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost"
)

dbf_path = "D:/SOFTWARE/GPS/INEC/CARTOGRAFÍA/Códigos cartográficos/LOCALES_DE_SALUD_DGEEC2012.dbf"
table = DBF(dbf_path, encoding='latin1')

cur = conn.cursor()

total_records = len(list(table))
progress_bar = tqdm(total=total_records, unit='registro')

table = DBF(dbf_path, encoding='latin1')

for record in table:
    cur.execute("SELECT dpto_id FROM departamentos WHERE dpto = %s", (record["DPTO"],))
    dpto_id = cur.fetchone()[0]
    
    cur.execute("SELECT distrito_id FROM distritos WHERE distrito = %s AND dpto_id = %s", (record["DISTRITO"], dpto_id))
    distrito_id = cur.fetchone()[0]
    
    cur.execute(
        "INSERT INTO locales_salud (dpto_id, distrito_id, nombre, ubicacion) VALUES (%s, %s, %s, ST_GeographyFromText(%s))",
        (dpto_id, distrito_id, record["NOMBRE"], f'POINT({record["LONGITUD"]} {record["LATITUD"]})')
    )
    
    progress_bar.update(1)

conn.commit()
cur.close()
conn.close()

progress_bar.close()