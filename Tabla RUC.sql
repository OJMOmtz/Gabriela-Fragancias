--Tabla RUC
CREATE TABLE gf.ruc (
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(255),
    digito_verificador INTEGER NOT NULL,
    cedula_tributaria VARCHAR(20) UNIQUE,
    estado VARCHAR(20) CHECK (estado IN ('activo', 'inactivo', 'suspendido')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla RUC
CREATE TABLE ruc (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    digito_verificador INT NOT NULL,
    razon_social VARCHAR(100) NOT NULL
);

-- Tabla de RUC
CREATE TABLE ruc (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    digito_verificador INT NOT NULL,
    razon_social VARCHAR(100) NOT NULL
);

--Tabla RUC
CREATE TABLE RUC (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(255),
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    tipo VARCHAR(20),  -- Tipo de entidad: 'Persona', 'Empresa'
    fuente VARCHAR(50)  -- 'ruc.dbf', 'ruc.txt'
);

--Tabla RUC
CREATE TABLE RUC (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(255),
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    tipo VARCHAR(20),  -- Tipo de entidad: 'Persona', 'Empresa'
    fuente VARCHAR(50)  -- 'ruc.dbf', 'ruc.txt'
);

--Tabla RUC
CREATE TABLE RUC (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    digito_verificador INT NOT NULL,
    razon_social VARCHAR(255),
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    tipo VARCHAR(20) CHECK (tipo IN ('Persona', 'Empresa')),
    fuente VARCHAR(50)  -- 'ruc.dbf', 'ruc.txt'
);

