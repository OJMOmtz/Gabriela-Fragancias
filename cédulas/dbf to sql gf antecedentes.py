import dbfread
import psycopg2
from tqdm import tqdm
from datetime import datetime

# Establecer conexión con la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Crear la tabla "Antecedentes_Judiciales" en la base de datos
cur.execute('''
    CREATE TABLE IF NOT EXISTS gf.antecedentes_judiciales (
        id_antecedente integer NOT NULL,
        numero_cedula character varying(20),
        causa_penal text,
        fecha_causa date,
        unidad_procesadora character varying(100),
        juez character varying(100),
        estado_proceso character varying(50)
    )
''')

# Contar el número total de registros
num_records = len(dbfread.DBF('D:\\PADRONES\\Automotores\\cap001.dbf', encoding='utf-8'))

# Crear una variable para llevar la cuenta del progreso
progress = 0

# Leer los datos del archivo DBF
tabla_original = dbfread.DBF('D:\\PADRONES\\Automotores\\cap001.dbf', load=True)

# Insertar los datos en la nueva tabla
for fila in tqdm(tabla_original):
    cedula = fila['CIDCAP']
    causa = fila['CAUSA']
    unidad = fila['UNIDAD']
    fecha_nota = fila['FECNOTA']
    juez = fila['JUEZ']
    estado = fila['ESTADO']
    
    try:
        # Convertir la fecha de formato número a fecha
        fecha_causa = datetime.strptime(str(fecha_nota), '%Y%m%d').date()
    except ValueError:
        try:
            # Intentar con otro formato de fecha (por ejemplo, '%d%m%Y')
            fecha_causa = datetime.strptime(str(fecha_nota), '%d%m%Y').date()
        except ValueError:
            # Si la fecha no es válida, asignar un valor por defecto (por ejemplo, None)
            fecha_causa = None
    
    # Insertar los datos en la nueva tabla
    cur.execute('''
        INSERT INTO gf.Antecedentes_Judiciales (numero_cedula, causa_penal, fecha_causa, unidad_procesadora, juez, estado_proceso)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (cedula, causa, fecha_causa, unidad, juez, estado))

    # Actualizar el progreso
    progress += 1
    print(f"Progreso: {progress}/{num_records}")
    
# Guardar los cambios en la base de datos
conn.commit()

# Cerrar la conexión
conn.close()
