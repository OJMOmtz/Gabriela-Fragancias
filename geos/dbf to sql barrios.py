import psycopg2
from dbfread import DBF

# Establecer conexión con la base de datos (ajusta los parámetros según tu configuración)
conn = psycopg2.connect(
    dbname="Brisa_Assistance",
    user="postgres",
    password="salmos23",
    host="localhost",
    port="5432"
)

# Abrir el archivo DBF
dbf_path = "D:/SOFTWARE/GPS/INEC/CARTOGRAFÍA/PAIS/Barrios_Localidades_Paraguay.dbf"
table = DBF(dbf_path, encoding='latin-1')

# Crear la tabla si no existe
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS barrios_localidades (
        dpto VARCHAR(2),
        distrito VARCHAR(2),
        dpto_desc VARCHAR(20),
        dist_desc VARCHAR(40),
        area VARCHAR(1),
        bar_loc VARCHAR(3),
        barlo_desc VARCHAR(51),
        clave VARCHAR(7)
    );
""")
conn.commit()

# Insertar los datos del DBF a la tabla
for record in table:
    cur.execute("""
        INSERT INTO barrios_localidades (dpto, distrito, dpto_desc, dist_desc, area, bar_loc, barlo_desc, clave)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (record['dpto'], record['distrito'], record['dpto_desc'], record['dist_desc'], record['area'], record['bar_loc'], record['barlo_desc'], record['clave']))
    conn.commit()

# Cerrar la conexión
cur.close()
conn.close()