import os
from dbfread import DBF
import pandas as pd
from sqlalchemy import create_engine

# Configurar la conexión a la base de datos PostgreSQL
engine = create_engine('postgresql://postgres:salmos23@localhost/cédula')

# Función para cargar y limpiar los datos de un archivo DBF
def load_and_clean_data(file_path, alerta=None):
    table = DBF(file_path, encoding='latin-1')
    df = pd.DataFrame(iter(table))
    
    # Limpieza de datos (por ejemplo, eliminar filas con valores nulos en la columna CEDULA)
    df = df.dropna(subset=['CEDULA'])
    
    # Renombrar columnas si es necesario
    df = df.rename(columns={"FEC_NAC": "FECHA_NACIMIENTO", "FEC_DEFUNC": "FECHA_DEFUNCION", "FEC_DEF": "FECHA_DEFUNCION"})
    
    # Agregar columna de alerta si es necesario
    if alerta:
        df['ALERTA'] = alerta
    
    return df

# Lista de rutas de archivos DBF y las columnas deseadas
dbf_paths = [
    ("D:\\PADRONES\\Automotores\\poli01.dbf", ['NROCED', 'APELLI', 'NOMBRE', 'FECHANAC', 'DOMICILIO']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
    ("D:\\PADRONES\\Automotores\\cap001.dbf", ['CIDCAP', 'ORDEN', 'CAUSA']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\deshabilitados.dbf", ['CEDULA', 'OBS']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\desh_exte.dbf", ['CEDULA', 'DESCRI_EST']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\pol_y_mil.dbf", ['CEDULA', 'TIPO', 'GRADO']),
    ("D:\\PADRONES\\Consulta Padron 2013\\data\\difuntos.dbf", ['CEDULA', 'FECHA_DEFUNCION']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\deshabilitados.dbf", ['CEDULA', 'OBS']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\desh_exte.dbf", ['CEDULA', 'DESCRI_EST']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\difuntos.dbf", ['CEDULA', 'FECHA_DEFUNCION']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\inhabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'SEXO', 'FECHA_NACIMIENTO', 'FECHA_DEFUNCION']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\interdictos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\menores.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL', 'DIRECCION']),
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\pol_y_mil.dbf", ['CEDULA', 'TIPO', 'GRADO']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\deshabilitados.dbf", ['CEDULA', 'OBS']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\desh_exte.dbf", ['CEDULA', 'DESCRI_EST']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\difuntos.dbf", ['CEDULA', 'FECHA_DEFUNCION']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\extranjeros.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\interdictos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\menores.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL', 'DIRECCION']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\pol_y_mil.dbf", ['CEDULA', 'TIPO', 'GRADO']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\regciv_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\deshabilitados.dbf", ['CEDULA', 'OBS']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\desh_exte.dbf", ['CEDULA', 'DESCRI_EST']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\difuntos.dbf", ['CEDULA', 'FECHA_DEFUNCION']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\extranjeros.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\interdictos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\menores.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL', 'DIRECCION']),
	("D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\pol_y_mil.dbf", ['CEDULA', 'TIPO', 'GRADO']),
	("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\desh_exte.dbf", ['CEDULA', 'DESCRI_EST']),
	("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\inhabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'SEXO', 'FECHA_NACIMIENTO', 'FECHA_DEFUNCION']),
	("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\regciv_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2017 HC (datos.dbc)\\mas_pda.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2017 pre ANR (datos.dbc)\\mas_pda.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\desh_exte.dbf", ['CEDULA', 'DESCRI_EST']),
	("D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\inhabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'SEXO', 'FECHA_NACIMIENTO', 'FECHA_DEFUNCION']),
	("D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\regciv_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\desh_exte.dbf", ['CEDULA', 'DESCRI_EST']),
	("D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\inhabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'SEXO', 'FECHA_NACIMIENTO', 'FECHA_DEFUNCION']),
	("D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\regciv_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2021\\data\\desh_exte.dbf", ['CEDULA', 'DESCRI_EST']),
	("D:\\PADRONES\\Padrón 2021\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2021\\data\\inhabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'SEXO', 'FECHA_NACIMIENTO', 'FECHA_DEFUNCION']),
	("D:\\PADRONES\\Padrón 2021\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2021\\data\\regciv_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\desh_exte.dbf", ['CEDULA', 'DESCRI_EST']),
	("D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\inhabilitados.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'SEXO', 'FECHA_NACIMIENTO', 'FECHA_DEFUNCION']),
	("D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\regciv_exte.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón 2021 ANR (datos.dbc)\\mas_pda.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\deshabilitados.dbf", ['CEDULA', 'OBS']),
	("D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\difuntos.dbf", ['CEDULA', 'FECHA_DEFUNCION']),
	("D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\dobles.DBF", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\interdictos.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL']),
	("D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\menores.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'SEXO', 'NACIONAL', 'DIRECCION']),
	("D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\pol_y_mil.dbf", ['CEDULA', 'TIPO', 'GRADO']),
	("D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
	("D:\\PADRONES\\RUC\\RUC.dbf", ['RUC', 'RAZON', 'DIGITO']),
	("D:\\PADRONES\\RUC\\RUC2017.dbf", ['RUC', 'RAZON', 'DIGITO']),
    # Agregue el resto de las rutas de los archivos DBF y las columnas deseadas aquí
]

# Procesar cada archivo DBF en la lista de rutas
for dbf_path, columns in dbf_paths:
    if os.path.isfile(dbf_path):
        # Definir la alerta según el archivo DBF
        if dbf_path.endswith('cap001.dbf'):
            alerta = 'Posible fraude: Orden de captura'
        elif 'deshabilitados' in dbf_path or 'desh_exte' in dbf_path:
            alerta = 'Posible fraude: Deshabilitado'
        elif 'pol_y_mil' in dbf_path:
            alerta = 'Atención: Policía o militar'
        elif 'difuntos' in dbf_path:
            alerta = 'DIFUNTO'
        else:
            alerta = None
        
        df = load_and_clean_data(dbf_path, alerta)
        df = df[columns + (['ALERTA'] if alerta else [])]
        
        # Enviar los datos a la base de datos PostgreSQL
        table_name = os.path.splitext(os.path.basename(dbf_path))[0]  # Utilizar el nombre del archivo como nombre de la tabla
        df.to_sql(table_name, engine, if_exists='replace', index=False)
    else:
        print(f"\nEl archivo '{dbf_path}' no existe.")
