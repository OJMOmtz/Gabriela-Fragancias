-- Tabla Zona
CREATE TABLE Zona (
    id_zona SERIAL PRIMARY KEY,
    id_municipio INTEGER REFERENCES Municipio(id_municipio),
    nombre_zona VARCHAR(100) NOT NULL,
    codigo_zona VARCHAR(10) UNIQUE NOT NULL,
    geometria GEOGRAPHY(POLYGON, 4326)
);

-- Zonas de ventas (Sales Territories)
CREATE TABLE zonas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    area geography(POLYGON, 4326),
    estado BOOLEAN DEFAULT true
);

--Tabla Zonas
CREATE TABLE Zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre_zona VARCHAR(100) NOT NULL UNIQUE,
	dia_visita VARCHAR (12),
    geom GEOGRAPHY(POLYGON, 4326)
);

-- Tabla Zonas para asociar vendedores a áreas específicas
CREATE TABLE zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre_zona VARCHAR(100) NOT NULL,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    UNIQUE(id_zona, id_vendedor)
);

-- Tabla Zona o Ciudad
CREATE TABLE zonas (
    id_zona SERIAL PRIMARY KEY,
    id_municipio INTEGER REFERENCES municipios(id_municipio),
    nombre_zona VARCHAR(100) NOT NULL,
    codigo_zona VARCHAR(10) UNIQUE NOT NULL,
    geometria GEOGRAPHY(POLYGON, 4326) -- Definición de zonas geográficas
);

-- Tabla Zona
CREATE TABLE Zona (
    id_zona SERIAL PRIMARY KEY,
    id_municipio INTEGER REFERENCES Municipio(id_municipio),
    nombre_zona VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_zona VARCHAR(10) UNIQUE NOT NULL,
    geometria GEOGRAPHY(POLYGON, 4326)
);

--Tabla Zonas
CREATE TABLE Zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre_zona VARCHAR(100) NOT NULL UNIQUE
);

--Tabla Zonas
CREATE TABLE Zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre_zona VARCHAR(100) NOT NULL UNIQUE,
    geom GEOGRAPHY(POLYGON, 4326)
);