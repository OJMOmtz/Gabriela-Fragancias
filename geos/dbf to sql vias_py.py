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

# Contar el número total de registros
num_records = sum(1 for _ in dbfread.DBF(dbf_file, encoding='latin-1'))

# Crear una barra de progreso
pbar = tqdm(total=num_records, desc="Cargando datos")

# Agregar un diccionario para llevar la cuenta de los nombres
name_count = {}

# Contador para la barra de progreso
progress_count = 0

for record in dbfread.DBF(dbf_file, encoding='latin-1'):
    # Obtener el nombre y manejar espacios vacíos
    nombre = record['NOMBRE'].strip() if record['NOMBRE'] else 'N/A'
    
    # Manejar nombres duplicados
    if nombre in name_count:
        name_count[nombre] += 1
        nombre = f"{nombre}_{name_count[nombre]}"
    else:
        name_count[nombre] = 1
    
    try:
        # Intentar insertar en la tabla SQL
        cur.execute("""
            INSERT INTO gf.vias (nombre, tipo, ancho, dpto, dpto_desc)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, record['TIPO'], record['ANCHO'], record['DPTO'], record['DPTO_DESC']))
    except Exception as e:
        # Revertir la transacción en caso de error
        conn.rollback()
        # Imprimir cualquier error que ocurra durante la inserción
        print(f"Error inserting record: {e}")
    
    # Actualizar la barra de progreso cada 1000 registros
    progress_count += 1
    if progress_count % 1000 == 0:
        pbar.update(1000)

# Cerrar la barra de progreso
pbar.close()

# Confirmar cambios y cerrar conexión
conn.commit()
cur.close()
conn.close()
