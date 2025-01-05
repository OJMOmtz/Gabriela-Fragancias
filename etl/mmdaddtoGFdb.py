import psycopg2

def insertar_datos_gabriela(conn, nombre, md5, tipo_archivo, estructura):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO gabriela_fragancias (nombre, md5, tipo_archivo, estructura)
                VALUES (%s, %s, %s, %s);
            """, (nombre, md5, tipo_archivo, estructura))
            conn.commit()
    except Exception as e:
        print(f"Error al insertar datos en GABRIELA_FRAGANCIAS: {e}")
