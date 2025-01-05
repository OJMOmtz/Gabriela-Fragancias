from dbfread import DBF
import psycopg2
from tqdm import tqdm

conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost"
)

dbf_path = "D:/PADRONES/GPS/INEC/CARTOGRAFÍA/PAIS/Barrios_Localidades_Paraguay.dbf"
table = DBF(dbf_path, encoding='utf-8')

cur = conn.cursor()

# Contar el número total de registros en el archivo DBF
total_records = len(list(table))

# Crear una barra de progreso
progress_bar = tqdm(total=total_records, unit='registro')

# Reiniciar la posición del archivo DBF
table = DBF(dbf_path, encoding='utf-8')

for record in table:
    cur.execute("SELECT id_dpto FROM gf.departamentos WHERE dpto = %s", (record["DPTO"],))
    dpto_id = cur.fetchone()[0]
    
    cur.execute("SELECT id_distrito FROM gf.distritos WHERE distrito = %s", (record["DISTRITO"],))
    distrito_id = cur.fetchone()[0]
    
    try:
        cur.execute(
            "INSERT INTO gf.barrios_localidades (id_dpto, id_distrito, area, bar_loc, barlo_desc, clave) VALUES (%s, %s, %s, %s, %s, %s)",
            (dpto_id, distrito_id, record["AREA"], record["BAR_LOC"], record["BARLO_DESC"], record["CLAVE"])
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
