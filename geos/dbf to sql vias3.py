import dbfread
import psycopg2

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

# Reiniciar la posición del archivo DBF
table = dbfread.DBF(dbf_file, encoding='latin-1')

processed_records = 0
increment = 5000  # Cambiar a 1000 si prefieres incrementos de 1000
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
    
    processed_records += 1
    if processed_records % increment == 0 or processed_records == total_records:
        print(f"Registros procesados: {processed_records}/{total_records}", end='\r')

print()  # Agregar un salto de línea después de la etiqueta de progreso

cur.close()
conn.close()

print(f"Registros procesados: {total_records}/{total_records} - Completado")
