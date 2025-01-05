import csv
import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="Gabriela_Fragancias",
    user="postgres",
    password="salmos23"
)
cur = conn.cursor()
cur.execute("SET search_path TO gf")

# Obtener los valores existentes de id_tipo_vehiculo de la tabla tipo_vehiculo
cur.execute("SELECT id_tipo_vehiculo FROM tipo_vehiculo")
existing_tipo_vehiculo_ids = [row[0] for row in cur.fetchall()]

# Obtener los valores existentes de codigo de la tabla automarca
cur.execute("SELECT codigo FROM automarca")
existing_automarca_ids = [row[0] for row in cur.fetchall()]

# Conjunto para almacenar las placas insertadas
inserted_placas = set()

# Lectura del archivo CSV
with open(r'D:\PADRONES\Automotores\autov1.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Verificar si la placa está vacía o es nula
        if not row['placa']:
            continue

        # Verificar si la placa ya ha sido insertada
        if row['placa'] in inserted_placas:
            continue

        # Convertir tipo_vehiculo_id a entero
        tipo_vehiculo_id = int(row['tipo_vehiculo']) if row['tipo_vehiculo'] else None

        # Verificar si tipo_vehiculo_id existe en la tabla tipo_vehiculo
        if tipo_vehiculo_id not in existing_tipo_vehiculo_ids:
            continue

        # Convertir automarca a entero
        automarca = int(row['automarca']) if row['automarca'] else None

        # Verificar si automarca existe en la tabla automarca
        if automarca not in existing_automarca_ids:
            continue

        # Mapeo de columnas y conversión de tipos de datos si es necesario
        clave = int(row['clave']) if row['clave'] else None
        placa = row['placa']
        autocolor = row['autocolor'] if row['autocolor'] else None
        chassis = row['chassis'] if row['chassis'] else None
        motor = row['motor'] if row['motor'] else None
        cedula = int(row['numero_cedula']) if row['numero_cedula'] else None

        # Inserción de datos en la base de datos
        cur.execute("""
            INSERT INTO vehiculo (clave, placa, automarca, tipo_vehiculo_id, autocolor, chassis, motor, numero_cedula)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (clave, placa, automarca, tipo_vehiculo_id, autocolor, chassis, motor, cedula))

        # Agregar la placa al conjunto de placas insertadas
        inserted_placas.add(placa)

# Confirmación de cambios y cierre de conexión
conn.commit()
cur.close()
conn.close()
