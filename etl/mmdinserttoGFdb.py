def insert_data(conn, name, geom):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO geodatos (nombre, geom) 
                VALUES (%s, ST_SetSRID(ST_GeomFromText(%s), 4326));
            """, (name, geom))
            conn.commit()
    except Exception as e:
        print(f"Error insertando datos: {e}")
