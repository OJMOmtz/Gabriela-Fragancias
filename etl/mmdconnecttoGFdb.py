import psycopg2

def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            dbname="nombre_bd", 
            user="usuario", 
            password="contraseña", 
            host="localhost", 
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error conectando a PostgreSQL: {e}")
        return None
