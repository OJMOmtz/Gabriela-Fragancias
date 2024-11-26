--Tabla de Direcciones
CREATE TABLE direcciones (
    id_direccion SERIAL PRIMARY KEY,
    calle VARCHAR(100),
    numero VARCHAR(10),
    barrio VARCHAR(50),
    ciudad VARCHAR(50),
    codigo_postal VARCHAR(10),
    ubicacion GEOGRAPHY(POINT, 4326)
);