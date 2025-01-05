import dbfread
import psycopg2

# Establecer conexión con la base de datos (ajusta los parámetros según tu configuración)
conn = psycopg2.connect(
    dbname="Brisa_Assistance",
    user="postgres",
    password="salmos23",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Read data from DBF file
dbf_file = 'D:/SOFTWARE/GPS/INEC/CARTOGRAFÍA/PAIS/Departamentos_Paraguay.dbf'
for record in dbfread.DBF(dbf_file, encoding='latin-1'):
    # Insert into SQL table
    cur.execute("""
        INSERT INTO departamentos (dpto, dpto_desc)
        VALUES (%s, %s)
    """, (record['DPTO'], record['DPTO_DESC']))

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()