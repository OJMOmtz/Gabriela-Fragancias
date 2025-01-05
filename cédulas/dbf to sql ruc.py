import psycopg2

conn = psycopg2.connect(
    dbname="Gabriela_Fragancias",
    user="postgres",
    password="salmos23",
    host="localhost"
)

cur = conn.cursor()

csv_path = "D:/IA provechar/GabrielaFragancias/ruc.csv"

print("Conexión a la base de datos establecida. Iniciando proceso de carga de datos...")

with open(csv_path, 'r') as f:
    cur.copy_from(f, 'gf.ruc', sep=',', columns=('numero_ruc', 'razon_social', 'digito_verificador', 'cedula_tributaria', 'estado'))
    conn.commit()

print("Proceso de carga de datos finalizado.")

cur.close()
conn.close()
