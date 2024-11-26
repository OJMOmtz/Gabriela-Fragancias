-- Gabriela Fragancias Optimized Database Schema

-- Create extension for advanced functionality
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database with proper configuration
CREATE DATABASE "gabriela_fragancias"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_PY.UTF-8'
    LC_CTYPE = 'es_PY.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Switch to the database
\c gabriela_fragancias;

-- Create schema
CREATE SCHEMA IF NOT EXISTS gf;
SET search_path TO gf, public;

-- Custom Types for Data Validation
CREATE TYPE estado_registro AS ENUM ('activo', 'inactivo', 'eliminado');
CREATE TYPE tipo_pago AS ENUM ('contado', 'semanal', 'quincenal', 'mensual');
CREATE TYPE estado_pago AS ENUM ('pendiente', 'pagado', 'cancelado');
CREATE TYPE grupo_edad AS ENUM ('niño', 'púber', 'adolescente', 'joven', 'adulto', 'mayor');

-- Timestamp Update Function
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Core Tables with Optimized Constraints and Indexing

-- Empresa (Company) Table
CREATE TABLE gf.empresa (
    id_empresa UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    estado estado_registro DEFAULT 'activo'
);

-- Create trigger for automatic timestamp update
CREATE TRIGGER update_empresa_modtime
BEFORE UPDATE ON gf.empresa
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Optimization Indexes
CREATE INDEX idx_empresa_ruc ON gf.empresa(ruc);
CREATE INDEX idx_empresa_razon_social ON gf.empresa(razon_social);

-- Usuario (User) Table with Enhanced Security
CREATE TABLE gf.usuario (
    id_usuario UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    ultimo_inicio_sesion TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,
    estado estado_registro DEFAULT 'activo'
);

-- Indexes for User Table
CREATE INDEX idx_usuario_cedula ON gf.usuario(cedula);
CREATE INDEX idx_usuario_email ON gf.usuario(email);
CREATE INDEX idx_usuario_ultimo_inicio_sesion ON gf.usuario(ultimo_inicio_sesion);

-- Trigger for User Table
CREATE TRIGGER update_usuario_modtime
BEFORE UPDATE ON gf.usuario
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Product Table with Comprehensive Constraints
CREATE TABLE gf.producto (
    id_producto UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    id_marca UUID NOT NULL,
    descripcion TEXT,
    volumen INTEGER CHECK (volumen BETWEEN 5 AND 200),
    es_kit BOOLEAN DEFAULT FALSE,
    costo NUMERIC(10,2) NOT NULL,
    precio_venta_credito NUMERIC(10,2) NOT NULL,
    precio_venta_contado NUMERIC(10,2) NOT NULL,
    franja_etaria grupo_edad,
    ano_lanzamiento INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    estado estado_registro DEFAULT 'activo',
    CONSTRAINT precios_validos CHECK (
        precio_venta_contado >= costo AND 
        precio_venta_credito >= precio_venta_contado
    ),
    CONSTRAINT fk_producto_marca FOREIGN KEY (id_marca) 
        REFERENCES gf.marca(id_marca)
);

-- Optimization for Product Table
CREATE INDEX idx_producto_codigo_barras ON gf.producto(codigo_barras);
CREATE INDEX idx_producto_nombre ON gf.producto(nombre);
CREATE INDEX idx_producto_marca ON gf.producto(id_marca);

-- Enhanced Inventory Management
CREATE TABLE gf.inventario (
    id_inventario UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_producto UUID NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    ubicacion VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    estado estado_registro DEFAULT 'activo',
    CONSTRAINT fk_inventario_producto FOREIGN KEY (id_producto)
        REFERENCES gf.producto(id_producto)
);

-- Stock Update Function
CREATE OR REPLACE FUNCTION actualizar_stock()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE gf.inventario 
    SET stock = stock - NEW.cantidad, 
        updated_at = CURRENT_TIMESTAMP
    WHERE id_producto = NEW.id_producto;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Advanced Geospatial Sale Tracking
CREATE TABLE gf.venta (
    id_venta UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_cliente UUID NOT NULL,
    id_empleado UUID NOT NULL,
    fecha_venta TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    tipo_pago tipo_pago NOT NULL,
    estado estado_pago DEFAULT 'pendiente',
    total NUMERIC(10,2) NOT NULL CHECK (total >= 0),
    ubicacion_venta GEOGRAPHY(Point, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    estado_registro estado_registro DEFAULT 'activo'
);

-- Performance Indexes for Sale Table
CREATE INDEX idx_venta_cliente ON gf.venta(id_cliente);
CREATE INDEX idx_venta_empleado ON gf.venta(id_empleado);
CREATE INDEX idx_venta_fecha ON gf.venta(fecha_venta);
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_venta_texto ON gf.venta USING gin (to_tsvector('spanish', id_venta::text));

-- Row-Level Security for Sensitive Tables
ALTER TABLE gf.venta ENABLE ROW LEVEL SECURITY;
CREATE POLICY ventas_policy ON gf.venta 
    FOR ALL 
    USING (current_user = (SELECT usuario FROM gf.empleados WHERE id_empleado = venta.id_empleado));

-- Performance and Security Recommendations
-- 1. Use UUID for primary keys
-- 2. Implement comprehensive foreign key constraints
-- 3. Add row-level security
-- 4. Use advanced indexing techniques
-- 5. Implement comprehensive audit trails
