import os
from dbfread import DBF
import pandas as pd
from sqlalchemy import create_engine

# Configurar la conexión a la base de datos PostgreSQL
engine = create_engine('postgresql://username:password@host:port/database_name')

# Función para cargar y limpiar los datos de un archivo DBF
def load_and_clean_data(file_path):
    table = DBF(file_path, encoding='latin-1')
    df = pd.DataFrame(iter(table))
    
    # Limpieza de datos (por ejemplo, eliminar filas con valores nulos en la columna CEDULA)
    df = df.dropna(subset=['CEDULA'])
    
    # Renombrar columnas si es necesario
    df = df.rename(columns={"FEC_NAC": "FECHA_NACIMIENTO", "FEC_DEFUNC": "FECHA_DEFUNCION"})
    
    return df

# Lista de rutas de archivos DBF
dbf_paths = [
"D:\\PADRONES\\Automotores\\cap001.dbf",
    "D:\\PADRONES\\Automotores\\poli01.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\deshabilitados.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\desh_exte.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\difuntos.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\dobles.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\extranjeros.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\interdictos.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\menores.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\nacionalidades.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\part.dbf",
	"D:\\PADRONES\\Consulta Padron 2013\\data\\pol_y_mil.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\deshabilitados.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\desh_exte.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\difuntos.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\inhabilitados.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\interdictos.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\menores.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\part.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\pol_y_mil.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\regciv.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\regciv_exte.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc) 31-08\\data\\deshabilitados.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc) 31-08\\data\\difuntos.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc) 31-08\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc) 31-08\\data\\interdictos.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc) 31-08\\data\\menores.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc) 31-08\\data\\part.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc) 31-08\\data\\pol_y_mil.dbf",
	"D:\\PADRONES\\Padrón 2010 (rcp2008.dbc) 31-08\\data\\regciv.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\deshabilitados.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\desh_exte.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\difuntos.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\extranjeros.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\interdictos.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\menores.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\nacionalidades.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\part.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\pol_y_mil.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\regciv.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)\\data\\regciv_exte.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\deshabilitados.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\desh_exte.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\difuntos.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\extranjeros.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\interdictos.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\menores.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\nacionalidades.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\part.dbf",
	"D:\\PADRONES\\Padrón 2013 Generales (rcp2008.dbc)-\\data\\pol_y_mil.dbf",
	"D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\desh_exte.dbf",
	"D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\inhabilitados.dbf",
	"D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\part.dbf",
	"D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\regciv.dbf",
	"D:\\PADRONES\\Padrón 2015 (rcp2008.dbc)\\data\\regciv_exte.dbf",
	"D:\\PADRONES\\Padrón 2017 HC (datos.dbc)\\mas_pda.dbf",
	"D:\\PADRONES\\Padrón 2017 pre ANR (datos.dbc)\\mas_pda.dbf",
	"D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\desh_exte.dbf",
	"D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\inhabilitados.dbf",
	"D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\part.dbf",
	"D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\regciv.dbf",
	"D:\\PADRONES\\Padrón 2018 (rcp2008.dbc)\\data\\regciv_exte.dbf",
	"D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\desh_exte.dbf",
	"D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\inhabilitados.dbf",
	"D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\part.dbf",
	"D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\regciv.dbf",
	"D:\\PADRONES\\Padrón 2020 (rcp2008.dbc)\\data\\regciv_exte.dbf",
	"D:\\PADRONES\\Padrón 2021\\data\\desh_exte.dbf",
	"D:\\PADRONES\\Padrón 2021\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón 2021\\data\\inhabilitados.dbf",
	"D:\\PADRONES\\Padrón 2021\\data\\part.dbf",
	"D:\\PADRONES\\Padrón 2021\\data\\regciv.dbf",
	"D:\\PADRONES\\Padrón 2021\\data\\regciv_exte.dbf",
	"D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\regciv.dbf",
	"D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\desh_exte.dbf",
	"D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\inhabilitados.dbf",
	"D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\nacionalidades.dbf",
	"D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\part.dbf",
	"D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\regciv.dbf",
	"D:\\PADRONES\\Padrón 2021 (rcp2008.dbc)\\data\\regciv_exte.dbf",
	"D:\\PADRONES\\Padrón 2021 ANR (datos.dbc)\\mas_pda.dbf",
	"D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\deshabilitados.dbf",
	"D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\difuntos.dbf",
	"D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\dobles.dbf",
	"D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\interdictos.dbf",
	"D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\menores.dbf",
	"D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\part.dbf",
	"D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\pol_y_mil.dbf",
	"D:\\PADRONES\\Padrón UNACE (rcp2008.dbc)\\data\\regciv.dbf",
	"D:\\PADRONES\\RUC\\RUC.dbf",
	"D:\\PADRONES\\RUC\\RUC2017.dbf",
	"D:\\PADRONES\\SATI\\DATOS\\cedauto.dbf",
	"D:\\PADRONES\\SATI\\DATOS\\celulares.dbf",
	"D:\\PADRONES\\SATI\\DATOS\\provisorios.dbf",
    # Agregue el resto de las rutas de los archivos DBF aquí
]

# Procesar cada archivo DBF en la lista de rutas
for dbf_path in dbf_paths:
    if os.path.isfile(dbf_path):
        df = load_and_clean_data(dbf_path)
        
        # Enviar los datos a la base de datos PostgreSQL
        table_name = os.path.splitext(os.path.basename(dbf_path))[0]  # Utilizar el nombre del archivo como nombre de la tabla
        df.to_sql(table_name, engine, if_exists='replace', index=False)
    else:
        print(f"\nEl archivo '{dbf_path}' no existe.")