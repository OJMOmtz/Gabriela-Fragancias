-- Primero nos aseguramos que no haya conexiones a la base de datos
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'gabriela_fragancias'
AND pid <> pg_backend_pid();

-- Eliminamos la base de datos si existe
DROP DATABASE IF EXISTS gabriela_fragancias;

-- Creamos la nueva base de datos
CREATE DATABASE gabriela_fragancias;

-- Nos conectamos a la nueva base de datos
\c gabriela_fragancias

-- Configuración inicial
SET client_encoding = 'UTF8';
SET standard_conforming_strings = ON;

-- Creamos la extensión PostGIS si no existe
CREATE EXTENSION IF NOT EXISTS postgis;

-- Tabla Empresa
CREATE TABLE Empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Usuario
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL CHECK (rol IN ('admin', 'vendedor', 'supervisor')),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla RUC
CREATE TABLE RUC (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    digito_verificador INT NOT NULL,
    razon_social VARCHAR(255),
    tipo VARCHAR(20) CHECK (tipo IN ('Persona', 'Empresa'))
);

-- Tabla Personas_Cedulas
CREATE TABLE Personas_Cedulas (
    id_persona SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
    fecha_nacimiento DATE,
    lugar_nacimiento VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    email VARCHAR(100),
    id_ruc INTEGER REFERENCES RUC(id_ruc) ON DELETE SET NULL,
    estado VARCHAR(20) DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'fallecido')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Antecedentes_Judiciales
CREATE TABLE Antecedentes_Judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) REFERENCES Personas_Cedulas(numero_cedula),
    causa_penal TEXT,
    fecha_causa DATE,
    unidad_procesadora VARCHAR(100),
    juez VARCHAR(100),
    estado_proceso VARCHAR(50),
    fuente VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Vehiculos
CREATE TABLE Vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    año INT CHECK (año BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE)),
    numero_motor VARCHAR(50) UNIQUE,
    numero_chasis VARCHAR(50) UNIQUE,
    km_recorridos DECIMAL(10, 2),
    fecha_revision DATE,
    estado VARCHAR(20) DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'vendido')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Zonas
CREATE TABLE Zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre_zona VARCHAR(100) NOT NULL UNIQUE,
    geom GEOGRAPHY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Rutas
CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Personas_Cedulas(id_persona),
    fecha DATE DEFAULT CURRENT_DATE,
    coordenadas GEOGRAPHY(LINESTRING, 4326),
    json_data JSONB,
    kml_data XML,
    fuente VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Equipos
CREATE TABLE equipos (
    id_equipo SERIAL PRIMARY KEY,
    tipo VARCHAR(50) CHECK (tipo IN ('Lector Código Barras', 'Impresora Ticket', 'Impresora Matricial', 'Impresora Láser', 'Impresora Inyección')),
    marca VARCHAR(50),
    modelo VARCHAR(50),
    fecha_adquisicion DATE DEFAULT CURRENT_DATE
);

-- Tabla Marcas
CREATE TABLE Marcas (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    año_fundacion INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Productos
CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    id_marca INTEGER REFERENCES Marcas(id_marca),
    precio_contado DECIMAL(10, 2) NOT NULL CHECK (precio_contado > 0),
    precio_credito DECIMAL(10, 2) NOT NULL CHECK (precio_credito > 0),
    stock INTEGER NOT NULL DEFAULT 0,
    descripcion TEXT,
    presentacion VARCHAR(50),
    volumen INT CHECK (volumen BETWEEN 5 AND 200),
    es_kit BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Tarjetas (creamos esta tabla primero porque Clientes la referencia)
CREATE TABLE Tarjetas (
    id_tarjeta SERIAL PRIMARY KEY,
    numero_tarjeta VARCHAR(7) NOT NULL,
    id_cliente INTEGER,
    id_vendedor INTEGER REFERENCES Personas_Cedulas(id_persona),
    id_zona INTEGER,
    total_gs DECIMAL(10, 2) NOT NULL CHECK (total_gs > 0),
    saldo DECIMAL(10, 2) DEFAULT 0 CHECK (saldo >= 0),
    forma_pago VARCHAR(20) DEFAULT 'SEM' CHECK (forma_pago IN ('SEM', 'QUIN', 'MENS')),
    estado VARCHAR(20) DEFAULT 'activa' CHECK (estado IN ('activa', 'cancelada')),
    fecha_emision DATE DEFAULT CURRENT_DATE,
    local_laboral VARCHAR(100),
    barrio VARCHAR(100),
    ciudad VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT tarjeta_unique_active UNIQUE (numero_tarjeta, estado)
);

-- Tabla Clientes
CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES Personas_Cedulas(id_persona),
    tarjeta VARCHAR(7) UNIQUE NOT NULL,
    saldo DECIMAL(10, 2) DEFAULT 0,
    tipo_pago VARCHAR(20) DEFAULT 'SEM' CHECK (tipo_pago IN ('SEM', 'QUIN', 'MENS')),
    fecha_registro DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(20) DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'moroso')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tarjeta) REFERENCES Tarjetas(numero_tarjeta)
);

-- Tabla Pagos
CREATE TABLE Pagos (
    id_pago SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),
    fecha_pago DATE DEFAULT CURRENT_DATE,
    fecha_control DATE,
    fecha_entrega DATE,
    monto DECIMAL(10, 2) NOT NULL CHECK (monto > 0),
    monto_entrega DECIMAL(10, 2) CHECK (monto_entrega > 0),
    saldo_restante DECIMAL(10, 2) NOT NULL,
    nueva_venta BOOLEAN DEFAULT FALSE,
    interes_moratorio DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Productos_Vendidos
CREATE TABLE Productos_Vendidos (
    id_producto_vendido SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER CHECK (cantidad > 0),
    precio DECIMAL(10, 2) CHECK (precio > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Maletines
CREATE TABLE Maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Personas_Cedulas(id_persona),
    fecha_carga DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(20) DEFAULT 'activo' CHECK (estado IN ('activo', 'devuelto', 'perdido')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Productos_Maletin
CREATE TABLE Productos_Maletin (
    id_maletin INTEGER REFERENCES Maletines(id_maletin),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_maletin, id_producto)
);

-- Tabla Liquidaciones
CREATE TABLE Liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Personas_Cedulas(id_persona),
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas DECIMAL(10, 2) DEFAULT 0,
    comision DECIMAL(10, 2) DEFAULT 0,
    total_pagar DECIMAL(10, 2) DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'aprobada', 'pagada')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Log
CREATE TABLE Log (
    id_log SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evento TEXT NOT NULL,
    usuario VARCHAR(100),
    ip_address VARCHAR(45)
);

-- Creación de índices
CREATE INDEX idx_personas_cedulas_numero_cedula ON Personas_Cedulas(numero_cedula);
CREATE INDEX idx_clientes_tarjeta ON Clientes(tarjeta);
CREATE INDEX idx_tarjetas_numero ON Tarjetas(numero_tarjeta);
CREATE INDEX idx_productos_vendidos_tarjeta ON Productos_Vendidos(id_tarjeta);
CREATE INDEX idx_tarjetas_ubicacion ON Tarjetas(local_laboral, barrio);
CREATE INDEX idx_pagos_fechas ON Pagos(fecha_control, fecha_entrega);
CREATE INDEX idx_rutas_gis ON Rutas USING GIST(coordenadas);
CREATE INDEX idx_zonas_gis ON Zonas USING GIST(geom);
