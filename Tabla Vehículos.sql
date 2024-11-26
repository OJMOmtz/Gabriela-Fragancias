-- Tabla Vehículos
CREATE TABLE Vehiculo (
    id_vehiculo SERIAL PRIMARY KEY,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    placa VARCHAR(20) UNIQUE,
    ano INTEGER
);

-- Vehículos (Delivery Vehicles)
CREATE TABLE vehiculos (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INTEGER,
    capacidad_kg DECIMAL(10,2),
    vendedor_id INTEGER REFERENCES vendedores(id),
    estado BOOLEAN DEFAULT true
);

--Tabla de Vehículos
CREATE TABLE Vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    año INT,
    numero_motor VARCHAR(50) UNIQUE,
    numero_chasis VARCHAR(50) UNIQUE,
    km_recorridos DECIMAL(10, 2),
    fecha_revision DATE
);

--Tabla de Vehículos
CREATE TABLE vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    anio INT,
    chasis VARCHAR(50),
    motor VARCHAR(50),
    ultima_revision DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Vehículos
CREATE TABLE vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE,
    marca VARCHAR(50), CHARACTER SET utf8mb4;
    modelo VARCHAR(50), CHARACTER SET utf8mb4;
    año INT,
	chassis VARCHAR(50), CHARACTER SET utf8mb4;
	motor VARCHAR(50), CHARACTER SET utf8mb4;
    ultima_revision DATE
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Vehiculos
CREATE TABLE Vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,  -- Número de placa obligatorio y único
    marca VARCHAR(50),
    modelo VARCHAR(50),
    año INT,
    numero_motor VARCHAR(50) UNIQUE,  -- Número de motor obligatorio y único
    numero_chasis VARCHAR(50) UNIQUE, -- Número de chasis obligatorio y único
    fecha_revision DATE,  -- Fecha de última revisión técnica
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Vehiculos
CREATE TABLE Vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    numero_motor VARCHAR(50) UNIQUE,
    numero_chasis VARCHAR(50) UNIQUE,
    fecha_revision DATE
);

-- Tabla Vehiculos
CREATE TABLE Vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    año INT,
    numero_motor VARCHAR(50) UNIQUE,
    numero_chasis VARCHAR(50) UNIQUE,
    km_recorridos DECIMAL(10, 2),
    fecha_revision DATE
);

-- Tabla de Vehículos
CREATE TABLE vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    placa VARCHAR(20) UNIQUE,
    ano INTEGER
);