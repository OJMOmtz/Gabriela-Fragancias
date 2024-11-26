-- Crear la base de datos
CREATE DATABASE gabriela_fragancias;

-- Conectarse a la base de datos
\c gabriela_fragancias;

-- Crear el esquema
CREATE SCHEMA gf;

-- Crear las tablas
-- Tabla Clientes
CREATE TABLE gf.clientes (
    id_cliente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Antecedentes Judiciales
CREATE TABLE gf.antecedentes_judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES gf.clientes(id_cliente),
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Productos
CREATE TABLE gf.productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio INTEGER NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Tarjetas
CREATE TABLE gf.tarjetas (
    id_tarjeta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES gf.clientes(id_cliente),
    id_producto INTEGER REFERENCES gf.productos(id_producto),
    total_gs INTEGER NOT NULL,
    saldo INTEGER DEFAULT 0,
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('SEM', 'QUIN', 'MENS')),
    estado VARCHAR(20) CHECK (estado IN ('activa', 'cancelada')) DEFAULT 'activa',
    fecha_emision DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Pagos
CREATE TABLE gf.pagos (
    id_pago SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES gf.tarjetas(id_tarjeta),
    monto INTEGER NOT NULL CHECK (monto > 0),
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Maletines
CREATE TABLE gf.maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_empleado INTEGER REFERENCES gf.empleados(id_empleado),
    fecha_carga DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Productos Maletin
CREATE TABLE gf.productos_maletin (
    id_maletin INTEGER REFERENCES gf.maletines(id_maletin),
    id_producto INTEGER REFERENCES gf.productos(id_producto),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    PRIMARY KEY (id_maletin, id_producto),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Empleados
CREATE TABLE gf.empleados (
    id_empleado SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    zona VARCHAR(50),
    cargo VARCHAR(50) CHECK (cargo IN ('Vendedor', 'Cobrador', 'Chofer')),
    fecha_contratacion DATE,
    salario INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Rutas
CREATE TABLE gf.rutas (
    id_ruta SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Zonas
CREATE TABLE gf.zonas (
    id_zona SERIAL PRIMARY KEY,
    id_ruta INTEGER REFERENCES gf.rutas(id_ruta),
    nombre VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);