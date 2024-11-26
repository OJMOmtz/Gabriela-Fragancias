-- Tabla Departamento
CREATE TABLE Departamento (
    id_departamento SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL,
    codigo_departamento VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla de Departamentos
CREATE TABLE gf.departamentos (
    id_dpto SERIAL PRIMARY KEY,
    dpto VARCHAR(2) NOT NULL,
    dpto_desc VARCHAR(20) NOT NULL
);

-- Tabla Departamento
CREATE TABLE departamentos (
    id_departamento SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL,
    codigo_departamento VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Departamento
CREATE TABLE Departamento (
    id_departamento SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_departamento VARCHAR(10) UNIQUE NOT NULL
);

