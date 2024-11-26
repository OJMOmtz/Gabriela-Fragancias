-- Tabla Vendedor
CREATE TABLE Vendedor (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cedula VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    zona VARCHAR(50)
);

-- Vendedores (Sales Representatives)
CREATE TABLE vendedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_ingreso DATE NOT NULL,
    zona_id INTEGER REFERENCES zonas(id),
    estado BOOLEAN DEFAULT true
);

--Tabla Vendedores
CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    zona VARCHAR(50) NOT NULL,
    comision DECIMAL(10, 2) DEFAULT 50000
);

-- Tabla Vendedores
CREATE TABLE vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    comision NUMERIC(10,2) DEFAULT 50000
);

-- Tabla Vendedores
CREATE TABLE vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    comision NUMERIC(10,2) DEFAULT 50000
);

-- Tabla de Vendedores
CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    id_zona INTEGER REFERENCES Zona(id_zona);
	nombre VARCHAR(100) NOT NULL,
    zona VARCHAR(50) NOT NULL,
    comision DECIMAL(10, 2) DEFAULT 50000
);

-- Tabla de Vendedores
CREATE TABLE vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    comision NUMERIC(10,2)
);

--Tabla Vendedores
CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    zona VARCHAR(50) NOT NULL,
    comision DECIMAL(10, 2) DEFAULT 50000
);

-- Tabla Vendedores
CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    comision NUMERIC(10,2) DEFAULT 50000
);

-- Tabla de Vendedores
CREATE TABLE vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cedula VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    zona VARCHAR(50)
);