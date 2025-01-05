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
    CREATE TABLE IF NOT EXISTS Antecedentes_Judiciales (
        id_antecedente SERIAL PRIMARY KEY,
        id_persona INTEGER REFERENCES Cedulas(id_persona),
        causa_penal TEXT,
        fecha_causa DATE,
        unidad_procesadora VARCHAR(100),
        juez VARCHAR(100),
        estado_proceso VARCHAR(50),
        fuente VARCHAR(50)
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
    causa = fila['CAUSA']
    unidad = fila['UNIDAD']
    fecha_nota = fila['FECNOTA']
    juez = fila['JUEZ']
    estado = fila['ESTADO']
    fuente = 'cap001.dbf'
    
    # Convertir la fecha de formato número a fecha
    fecha_causa = datetime.strptime(str(fecha_nota), '%Y%m%d').date()
    
    # Insertar los datos en la nueva tabla
    cur.execute('''
        INSERT INTO Antecedentes_Judiciales (causa_penal, fecha_causa, unidad_procesadora, juez, estado_proceso, fuente)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (causa, fecha_causa, unidad, juez, estado, fuente))

    # Actualizar el progreso
    progress += 1
    print(f"Progreso: {progress}/{num_records}")

# Guardar los cambios en la base de datos
conn.commit()

# Cerrar la conexión
conn.close()