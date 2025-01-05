import psycopg2

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'dbname': 'Gabriela_Fragancias',
    'user': 'postgres',
    'password': 'salmos23',
    'host': 'localhost',
    'port': 5432
}

# Conectar a la base de datos
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# Lista de tablas geográficas a mover
tables = [
    "barrios_localidades",
    "ciudades_paraguay",
    "comunidades_indigenas",
    "departamentos",
    "distritos",
    "hidrografia",
    "locales_de_salud",
    "locales_educativos",
    "locales_policiales",
    "manzanas",
    "vias_principales",
    "vias",
    "codigos_postales"
]

# Mover tablas del esquema gf al esquema public
for table in tables:
    cur.execute(f"ALTER TABLE gf.{table} SET SCHEMA public;")

# Confirmar cambios y cerrar la conexión
conn.commit()
cur.close()
conn.close()
