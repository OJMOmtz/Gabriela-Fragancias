def create_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS geodatos (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(255),
                    geom GEOMETRY(Point, 4326)
                );
            """)
            conn.commit()
    except Exception as e:
        print(f"Error creando la tabla: {e}")

