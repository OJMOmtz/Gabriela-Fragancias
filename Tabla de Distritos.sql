-- Tabla de Distritos
CREATE TABLE gf.distritos (
    id_distrito SERIAL PRIMARY KEY,
    id_dpto INTEGER REFERENCES gf.departamentos(id_dpto),
    distrito VARCHAR(2) NOT NULL,
    dist_desc VARCHAR(40) NOT NULL,
    clave VARCHAR(4) NOT NULL
);