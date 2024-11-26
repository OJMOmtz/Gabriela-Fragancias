-- Tabla de Barrios y Localidades
CREATE TABLE gf.barrios_localidades (
    id_barrio SERIAL PRIMARY KEY,
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
    area VARCHAR(1),
    bar_loc VARCHAR(3),
    barlo_desc VARCHAR(51),
    clave VARCHAR(7)
);