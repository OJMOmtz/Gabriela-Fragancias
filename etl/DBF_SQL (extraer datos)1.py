import dbf

# Lista de rutas y campos a extraer
dbf_files = [
    ("D:\\PADRONES\\Padrón 2010 (rcp2008.dbc)\\data\\regciv.dbf", ['CEDULA', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO']),
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
    ("D:\\PADRONES\\RUC\\RUC2017.dbf", ['RUC', 'RAZON', 'DIGITO'])
]

# Función para extraer datos de una tabla DBF
def extract_data(file_path, fields):
    table = dbf.Table(file_path)
    table.open()

    data = []
    for record in table:
        row = [record[field] for field in fields]
        data.append(row)

    table.close()
    return data

# Extraer datos de todas las tablas DBF
for file_path, fields in dbf_files:
    data = extract_data(file_path, fields)
    
    # Procesar los datos extraídos
    for row in data:
        # Hacer algo con cada fila de datos
        print(row)