import pandas as pd

# Lee la primera línea del archivo CSV para obtener los nombres de las columnas
with open(r'D:\PADRONES\csvs\.idea\CÉDULAS-2024-1_ISO-8859-1.csv', 'r', encoding='ISO-8859-1') as file:
    columnas = file.readline().strip().split(';')

# Lee el archivo CSV con la codificación ISO-8859-1, omite las líneas con errores y especifica los nombres de las columnas
df = pd.read_csv(r'D:\PADRONES\csvs\.idea\CÉDULAS-2024-1_ISO-8859-1.csv', sep=';', encoding='ISO-8859-1', on_bad_lines='skip', names=columnas, skiprows=1)

# Cambiando el orden de las columnas
indice_fecha = columnas.index('fecha_nacimiento')
indice_sexo = columnas.index('sexo')
columnas[indice_sexo], columnas[indice_fecha] = columnas[indice_fecha], columnas[indice_sexo]

# Reordenando el DataFrame
df = df[columnas]

# Guardando el DataFrame en un nuevo archivo CSV
df.to_csv(r'D:\PADRONES\csvs\.idea\CÉDULAS-2024-1_ISO-8859-1_nuevo.csv', sep=';', index=False, encoding='ISO-8859-1')
