-- Tabla Municipio
CREATE TABLE Municipio (
    id_municipio SERIAL PRIMARY KEY,
    id_departamento INTEGER REFERENCES Departamento(id_departamento),
    nombre_municipio VARCHAR(100) NOT NULL,
    codigo_municipio VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Municipio
CREATE TABLE municipios (
    id_municipio SERIAL PRIMARY KEY,
    id_departamento INTEGER REFERENCES departamentos(id_departamento),
    nombre_municipio VARCHAR(100) NOT NULL,
    codigo_municipio VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Municipio
CREATE TABLE Municipio (
    id_municipio SERIAL PRIMARY KEY,
    id_departamento INTEGER REFERENCES Departamento(id_departamento),
    nombre_municipio VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_municipio VARCHAR(10) UNIQUE NOT NULL
);

