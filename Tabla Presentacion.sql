-- Tabla Presentacion
CREATE TABLE Presentacion (
    id_presentacion SERIAL PRIMARY KEY,
    id_perfume INTEGER REFERENCES Perfume(id_perfume) ON DELETE CASCADE,
    codigo_barra VARCHAR(50) UNIQUE NOT NULL,
    tamano_ml INTEGER CHECK (tamano_ml > 0),
    imagen_url VARCHAR(255)
);

-- Tabla Presentacion
CREATE TABLE Presentacion (
    id_presentacion SERIAL PRIMARY KEY,
    id_perfume INTEGER REFERENCES Perfume(id_perfume) ON DELETE CASCADE,
    codigo_barra VARCHAR(50) UNIQUE NOT NULL,
    tamano_ml INTEGER CHECK (tamano_ml > 0),
    imagen_url VARCHAR(255)
);

-- Tabla de Presentaciones
CREATE TABLE presentaciones (
    id_presentacion SERIAL PRIMARY KEY,
    id_perfume INTEGER REFERENCES perfumes(id_perfume),
    codigo_barra VARCHAR(50) UNIQUE,
    tamano_ml INTEGER CHECK (tamano_ml BETWEEN 5 AND 200),
    imagen_url VARCHAR(255),
    es_kit BOOLEAN DEFAULT FALSE
);