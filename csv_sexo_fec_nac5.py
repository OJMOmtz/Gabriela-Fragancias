import pandas as pd

# Lee el archivo CSV con la codificación ISO-8859-1 y omite las líneas con errores
df = pd.read_csv(r'D:\PADRONES\csvs\.idea\CÉDULAS-2024-1_ISO-8859-1.csv', sep=';', encoding='ISO-8859-1', on_bad_lines='skip')

# Obteniendo los nombres de las columnas
columnas = df.columns.tolist()

# Cambiando el orden de las columnas
indice_fecha = columnas.index('fecha_nacimiento')
indice_sexo = columnas.index('sexo')
columnas[indice_sexo], columnas[indice_fecha] = columnas[indice_fecha], columnas[indice_sexo]

# Reordenando el DataFrame
df = df[columnas]

# Guardando el DataFrame en un nuevo archivo CSV
df.to_csv(r'D:\PADRONES\csvs\.idea\CÉDULAS-2024-1_ISO-8859-1_nuevo.csv', sep=';', index=False, encoding='ISO-8859-1')
