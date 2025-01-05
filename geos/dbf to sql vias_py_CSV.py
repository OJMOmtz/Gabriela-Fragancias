import csv
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

# Leer datos del archivo CSV
csv_file = 'D:/PADRONES/GPS/INEC/CARTOGRAFÍA/PAIS/Vias principales_Paraguay.csv'

# Contar el número total de registros
with open(csv_file, 'r', encoding='utf-8') as f:
    num_records = sum(1 for _ in csv.reader(f))

# Crear una barra de progreso
pbar = tqdm(total=num_records, desc="Cargando datos")

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for record in reader:
        # Insertar en la tabla SQL
        cur.execute("""
            INSERT INTO gf.vias_principales (nombre, long_km_en, ruta_nro, ancho, tipo, long_mts)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (record['NOMBRE'], record['LONG_KM_EN'], record['RUTA_NRO'], record['ANCHO'], record['TIPO'], record['LONG_MTS']))
        
        # Actualizar la barra de progreso
        pbar.update(1)

# Cerrar la barra de progreso
pbar.close()

# Confirmar cambios y cerrar conexión
conn.commit()
cur.close()
conn.close()
