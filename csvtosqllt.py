import psycopg2
import csv
from pathlib import Path
from datetime import datetime

# Configuración de la conexión a la base de datos
db_config = {
    'dbname': 'Gabriela_Fragancias',
    'user': 'postgres',
    'password': 'salmos23',
    'host': 'localhost',
    'port': '5432'
}

# Ruta al directorio que contiene los archivos CSV
csv_directory = Path('D:/PADRONES/csvs/cedulas')

# Archivo de registro para guardar los errores
log_file = 'errores.csv'
with open(log_file, 'w') as f:
    f.write('archivo,fila,error,detalle\n')

# Conexión a la base de datos
conn = psycopg2.connect(**db_config)
cur = conn.cursor()

# Procesar cada archivo CSV en el directorio
for csv_file in csv_directory.glob('*.csv'):
    print(f'Procesando {csv_file}...')
    
    with open(csv_file, 'r', encoding='latin1') as f:
        csv_reader = csv.reader(f)
        headers = next(csv_reader)  # Leer la línea de encabezados
        column_mapping = {h.lower(): i for i, h in enumerate(headers)}
        
        for row_number, row in enumerate(csv_reader, start=2):
            try:
                fecha_nacimiento = datetime.strptime(row[column_mapping['fecha_nacimiento']], '%m-%d-%Y').date() if 'fecha_nacimiento' in column_mapping else None
            except ValueError:
                fecha_nacimiento = None

            try:
                # Insertar la fila en la tabla cedulas
                cur.execute("""
                    INSERT INTO gf.cedulas (numero_cedula, nombre, apellido, fecha_nacimiento, sexo, direccion, id_distrito, id_dpto, zona)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (numero_cedula) DO NOTHING;
                """, (
                    row[column_mapping['numero_cedula' if 'numero_cedula' in column_mapping else 'cedula']],
                    row[column_mapping['nombre']],
                    row[column_mapping['apellido']],
                    fecha_nacimiento,
                    row[column_mapping['sexo']] if 'sexo' in column_mapping else None,
                    row[column_mapping['direccion']] if 'direccion' in column_mapping else None,
                    row[column_mapping['id_distrito']] if 'id_distrito' in column_mapping else None,
                    row[column_mapping['id_dpto']] if 'id_dpto' in column_mapping else None,
                    row[column_mapping['zona']] if 'zona' in column_mapping else None
                ))
            except psycopg2.DataError as e:
                # Registrar el error en el archivo de registro
                error_detalle = str(e).split(':')[-1].strip()
                with open(log_file, 'a') as f:
                    f.write(f'{csv_file},{row_number},"{error_detalle}","{','.join(row)}"\n')
                print(f"Omitiendo fila {row_number} con error de datos: {e}")
                conn.rollback()  # Revertir la transacción
                continue

    conn.commit()
    print(f'{csv_file} procesado correctamente.')

# Cerrar la conexión a la base de datos
cur.close()
conn.close()
