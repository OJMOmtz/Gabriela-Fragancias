import os
from dbfread import DBF
import psycopg2

# Configurar la conexión a la base de datos
DB_HOST = "localhost"
DB_NAME = "Gabriela_Fragancias"
DB_USER = "postgres"
DB_PASS = "salmos23"

# Establecer la conexión a la base de datos
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor()

# Lista de rutas y campos a extraer
dbf_files = [
    # ...
    ("D:\\PADRONES\\Automotores\\poli01.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\deshabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL', 'OBS']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\desh_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\difuntos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\dobles.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\extranjeros.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\interdictos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\menores.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\deshabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL', 'OBS']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\difuntos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\inhabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\interdictos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\menores.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\pol_y_mil.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\deshabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL', 'OBS']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\desh_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\difuntos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\dobles.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\extranjeros.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\interdictos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\menores.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\pol_y_mil.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\regciv_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\desh_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\inhabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO']),
    ("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\regciv_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2017 HC (datos.dbc)\\mas_pda.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2017 pre ANR (datos.dbc)\\mas_pda.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\desh_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC']),
    ("D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\inhabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NAC', 'SEXO']),
]

# Función para extraer datos de una tabla DBF
def extract_data(file_path, fields):
    table = DBF(file_path)
    
    data = []
    for record in table:
        row = [record[field] for field in fields]
        data.append(row)

    return data

# Extraer e insertar datos de cédulas
for file_path, fields in dbf_files:
    if 'CAUSA' not in fields:
        data = extract_data(file_path, fields)
        
        for row in data:
            cedula = row[0]
            nombre = row[1]
            apellido = row[2]
            fecha_nacimiento = row[3] if len(row) > 3 else None
            
            # Insertar el registro en la tabla Cedula
            cur.execute("INSERT INTO Cedula (numero_ci, nombre, apellido, fecha_nacimiento) VALUES (%s, %s, %s, %s)", (cedula, nombre, apellido, fecha_nacimiento))

# Confirmar los cambios
conn.commit()

# Crear la tabla RUC aquí si es necesario
# ...

# Extraer e insertar datos de antecedentes judiciales
for file_path, fields in dbf_files:
    if 'CAUSA' in fields:
        data = extract_data(file_path, fields)
        
        for row in data:
            cidcap = row[0]
            orden = row[1]
            causa = row[2]
            
            # Insertar el registro en la tabla AntecedentesJudiciales
            cur.execute("INSERT INTO AntecedentesJudiciales (numero_ci, causa_penal) VALUES (%s, %s)", (cidcap, causa))
            
            # Agregar una alerta si se encuentra un registro con antecedentes
            print(f"Alerta: Se encontró un registro con antecedentes judiciales. CIDCAP: {cidcap}, Orden: {orden}, Causa: {causa}")

# Confirmar los cambios y cerrar la conexión
conn.commit()
cur.close()
conn.close()

print("Datos insertados correctamente en la tabla Cedula.")