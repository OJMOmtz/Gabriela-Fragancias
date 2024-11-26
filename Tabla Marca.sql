-- Tabla de Marcas
CREATE TABLE Marcas (
    ID_Marca INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Año_Fundacion INT,
    Sede VARCHAR(100),
    Sitio_Web VARCHAR(255),
    UNIQUE (Nombre)
);

-- Tabla Marca
CREATE TABLE Marca (
    id_marca SERIAL PRIMARY KEY,
    nombre_marca VARCHAR(100) NOT NULL,
    ano_fundacion INTEGER,
    sede VARCHAR(100)
);

-- Tabla de Marcas
CREATE TABLE marcas (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ano_fundacion INTEGER,
    sede VARCHAR(100)
);

-- Tabla Marcas
CREATE TABLE Marcas (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,  -- Nombre único de la marca
    año_fundacion INT
);

