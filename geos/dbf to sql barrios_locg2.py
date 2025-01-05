from dbfread import DBF
import psycopg2

conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost"
)

dbf_path = "D:/PADRONES/GPS/INEC/CARTOGRAFÍA/PAIS/Barrios_Localidades_Paraguay.dbf"
table = DBF(dbf_path, encoding='utf-8')

cur = conn.cursor()

print("Conexión a la base de datos establecida. Iniciando proceso de inserción...")

for record in table:
    try:
        cur.execute(
            "INSERT INTO gf.barrios_localidades (dpto, distrito, dpto_desc, dist_desc, area, bar_loc, barlo_desc, clave) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (record["DPTO"], record["DISTRITO"], record["DPTO_DESC"], record["DIST_DESC"], record["AREA"], record["BAR_LOC"], record["BARLO_DESC"], record["CLAVE"])
        )
    except psycopg2.errors.UniqueViolation:
        # Duplicado, omitir inserción
        conn.rollback()
        print(f"Registro duplicado: {record['CLAVE']}. Omitiendo inserción...")
    else:
        # Confirmar cambios si no hay error
        conn.commit()
        print(f"Registro insertado: {record['CLAVE']}")

cur.close()
conn.close()

print("Proceso de inserción finalizado.")
