import tkinter as tk
from tkinter import filedialog, ttk
import psycopg2
from datetime import datetime
import dbfread

# Función para procesar cada archivo DBF
def process_dbf_file(file_path):
    table = dbfread.DBF(file_path, lowernames=True)

    for record in table:
        # Extraer los datos del registro
        cedula = record["cedula"]
        nombre = record["nombre"]
        apellido = record["apellido"]
        fecha_nacimiento = record["fec_nac"]
        sexo = record["sexo"]

        # Transformar la fecha de nacimiento al formato deseado (YYYY-MM-DD)
        if isinstance(fecha_nacimiento, str):
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%d/%m/%Y").strftime("%Y-%m-%d")
        elif isinstance(fecha_nacimiento, datetime):
            fecha_nacimiento = fecha_nacimiento.strftime("%Y-%m-%d")

        # Insertar los datos en la base de datos PostgreSQL
        cur.execute("""
            INSERT INTO tu_tabla (cedula, nombre, apellido, fecha_nacimiento, sexo)
            VALUES (%s, %s, %s, %s, %s)
        """, (cedula, nombre, apellido, fecha_nacimiento, sexo))

    # Commit para confirmar los cambios en la base de la base de la base de la base de la base de los cambios en la base de la base de la base de la base de la tabla de la tabla = conn.commit()
        
def standardize_date(date_value):
    if isinstance(date_value, str):
        if '/' in date_value:
            # El formato es 'DD/MM/YYYY'
            return datetime.strptime(date_value, '%d/%m/%Y').date()
        else:
            # El formato es 'YYYYMMDD'
            return datetime.strptime(date_value, '%Y%m%d').date()
    elif isinstance(date_value, datetime):
        return date_value.date()
    else:
        # Si el valor no es una cadena o un objeto datetime, devolver None
        return None

def insert_record(cur, record):
    # Mapear las columnas
    cedula = record.get('cedula')
    nombre = record.get('nombre')
    apellido = record.get('apellido')
    sexo = record.get('sexo')
    fec_nac = record.get('fec_nac')
    direcc = record.get('direcc')
    
    # Estandarizar la fecha si no es None
    if fec_nac is not None:
        fec_nac = standardize_date(fec_nac)
    
    # Verificar si el registro ya existe
    cur.execute("SELECT COUNT(*) FROM Cedulas WHERE numero_cedula = %s", (cedula,))
    count = cur.fetchone()[0]
    
    if count == 0:
        # Si el registro no existe, insertarlo
        query = """
            INSERT INTO Cedulas (numero_cedula, nombre, apellido, sexo, fecha_nacimiento, direccion)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        values = (cedula, nombre, apellido, sexo, fec_nac, direcc)
        cur.execute(query, values)
        
def read_data(table):
    return dbfread.DBF(table, lowernames=True)
    
def load_data():
    # Conexión a la base de datos PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="Gabriela_Fragancias",
        user="postgres",
        password="salmos23"
    )
    cur = conn.cursor()

    # Actualizar la etiqueta de progreso
    progress_label.config(text="Cargando datos...")
    window.update()

    # Inicializar la barra de progreso
    progress_bar['maximum'] = len(tables)
    progress_bar['value'] = 0

    for i, table in enumerate(tables):
        # Leer los datos de la tabla origen
        data = read_data(table)
        
        for record in data:
            insert_record(cur, record)
        
        # Actualizar la barra de progreso
        progress_bar['value'] = i+1
        progress_label.config(text=f"Procesando tabla {i+1} de {len(tables)}...")
        window.update()

    # Hacer commit de los cambios
    conn.commit()

    # Cerrar la conexión
    cur.close()
    conn.close()

    # Actualizar la etiqueta de progreso
    progress_label.config(text="¡Carga completada!")

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("DBF Files", "*.dbf")])
    for file_path in file_paths:
        tables.append(file_path)

tables = []

# Crear la ventana principal
window = tk.Tk()
window.title("Cargador de tablas DBF")

# Crear un botón para seleccionar archivos
select_button = tk.Button(window, text="Seleccionar tablas", command=select_files)
select_button.pack()

# Crear un botón para cargar datos
load_button = tk.Button(window, text="Cargar datos", command=load_data)
load_button.pack()

# Crear una etiqueta de progreso
progress_label = tk.Label(window, text="")
progress_label.pack()

# Crear una barra de progreso
progress_bar = ttk.Progressbar(window, length=200, mode='determinate')
progress_bar.pack()

# Ejecutar la ventana
window.mainloop()