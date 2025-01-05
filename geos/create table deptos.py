from dbfread import DBF
import psycopg2

conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost"
)

cur = conn.cursor()

# Crear la tabla departamentos
cur.execute("""
    CREATE TABLE departamentos (
        dpto_id SERIAL PRIMARY KEY,
        dpto VARCHAR(2) NOT NULL,
        dpto_desc VARCHAR(20) NOT NULL
    )
""")

# Cargar datos desde el archivo DBF
dbf_path = "D:/SOFTWARE/GPS/INEC/CARTOGRAFÍA/PAIS/Departamentos_Paraguay.dbf"
table = DBF(dbf_path, encoding='latin1')

for record in table:
    cur.execute(
        "INSERT INTO departamentos (dpto, dpto_desc) VALUES (%s, %s)",
        (record["DPTO"], record["DPTO_DESC"])
    )

conn.commit()
cur.close()
conn.close()
