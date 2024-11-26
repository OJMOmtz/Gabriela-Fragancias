-- Gabriela Fragancias Optimized Database Schema

-- Create extension for advanced functionality
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database with proper configuration
CREATE DATABASE "gabriela_fragancias"
    WITH
    OWNER = postgres
    ENCODING = 'WIN1252'
    LC_COLLATE = 'Spanish_Paraguay.1252'
    LC_CTYPE = 'Spanish_Paraguay.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

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

-- =================================================================
-- TABLAS BASE (Core Tables with Optimized Constraints and Indexing)
-- =================================================================

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

-- Extensión para funcionalidades geoespaciales
CREATE EXTENSION postgis;

-- Modificación de las tablas de ubicación geográfica según INEC
-- Dominios y tipos personalizados
CREATE TYPE gf.estado_registro AS ENUM ('activo', 'inactivo', 'eliminado');
CREATE TYPE gf.tipo_pago AS ENUM ('contado', 'semanal', 'quincenal', 'mensual');
CREATE TYPE gf.estado_pago AS ENUM ('pendiente', 'pagado', 'cancelado');
CREATE DOMAIN gf.cargo_empleado AS VARCHAR(20);
CREATE TYPE gf.grupo_edad AS ENUM ('niño', 'púber', 'adolescente', 'joven', 'adulto', 'mayor');
CREATE TYPE gf.sexo AS ENUM ('M', 'F');

--Tabla Cédulas
CREATE TABLE gf.cedulas (
    numero_cedula VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    sexo CHAR(1),
    direccion TEXT,
	id_barrio INTEGER REFERENCES gf.barrios_localidades(id_barrio),
	id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
	id_dpto INTEGER REFERENCES gf.departamentos(id_dpto),
	id_via INTEGER REFERENCES gf.vias(id_via),
	id_prefijo INTEGER REFERENCES gf.prefijos(id_prefijo),
    lugar_nacimiento VARCHAR(100),
    fecha_defuncion DATE,
    email VARCHAR(100),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla RUC
CREATE TABLE gf.ruc (
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(255),
    digito_verificador VARCHAR(1) UNIQUE NOT NULL,  -- Añadir UNIQUE aquí
    cedula_tributaria VARCHAR(20) UNIQUE,
    estado VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--Tabla Antecedentes Judiciales
CREATE TABLE gf.antecedentes_judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) REFERENCES gf.cedulas(numero_cedula),
    causa_penal TEXT,
    fecha_causa DATE,
    unidad_procesadora VARCHAR(100),
    juez VARCHAR(100),
    estado_proceso VARCHAR(50),
    fuente VARCHAR(50)
);


-- Tabla Tipo de Vehiculo
CREATE TABLE gf.tipo_vehiculo (
    id_tipo_vehiculo SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo'
);

-- Tabla Marca de Vehiculo
CREATE TABLE gf.automarca (
    codigo INT PRIMARY KEY,
    xxx VARCHAR(50),  -- Puedes cambiar 'xxx' a un nombre más descriptivo
    marca VARCHAR(50)
);

-- Tabla Vehículo
CREATE TABLE gf.vehiculo (
    id_vehiculo SERIAL PRIMARY KEY,
    clave INT,
    placa VARCHAR(20) UNIQUE NOT NULL,
    automarca INT REFERENCES gf.automarca(codigo),
    tipo_vehiculo_id INT REFERENCES gf.tipo_vehiculo(id_tipo_vehiculo),
    autocolor VARCHAR(50) NOT NULL,
    motor VARCHAR(50) NOT NULL,
    chassis VARCHAR(50) NOT NULL,
    año INTEGER NOT NULL,
    tipo_documento VARCHAR(50),
    cedula INT,
    titulo VARCHAR(50),
    km_recorridos INTEGER,
    ultima_revision DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo'
);

-- Tabla Color de Vehiculo
CREATE TABLE gf.autocolor (
  codigo INT PRIMARY KEY,  -- Asegúrate de que esta columna sea única
  xxx VARCHAR,  -- Cambia 'xxx' a un nombre más descriptivo
  color VARCHAR(50) NOT NULL
);

-- Tabla Origen de Vehiculo (Nacionalidades)
CREATE TABLE gf.nacionalidades (
    clave INT PRIMARY KEY,
    descri VARCHAR(50)
);


-- =============================================
-- TABLAS DE NEGOCIO
-- =============================================

-- Tabla Clientes
CREATE TABLE gf.clientes (
    id_cliente INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    tarjeta VARCHAR(5), -- este número se puede repetir en otras zonas y en la misma con otro cliente
    numero_cedula VARCHAR(20) UNIQUE NOT NULL,
	numero_ruc VARCHAR(20) REFERENCES gf.ruc(numero_ruc), -- referencia a la tabla gf.ruc
    digito_verificador VARCHAR(255) REFERENCES gf.ruc(digito_verificador), -- referencia a la tabla gf.ruc	
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    id_prefijo INT REFERENCES gf.prefijos(id_prefijo),
    numero_telefono VARCHAR(20),
    numero_celular VARCHAR(20),
    numero_tarjeta VARCHAR(20) UNIQUE,
    id_zona INT REFERENCES gf.zonas(id_zona),
    id_direccion INT REFERENCES gf.direcciones(id_direccion),
    direccion GEOGRAPHY(POINT, 4326),
	barlo_desc VARCHAR(51) INTEGER REFERENCES gf.barrios_localidades(barlo_desc),
	dist_desc VARCHAR(40) REFERENCES gf.distritos(dist_desc),
    dpto_desc VARCHAR(20) REFERENCES gf.departamentos(dpto_desc),
    nombre VARCHAR(50) REFERENCES gf.vias(nombre),	
    saldo INT DEFAULT 0,
    tipo_pago VARCHAR(20) CHECK (tipo_pago IN ('SEM', 'QUIN', 'MENS')),
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    estado VARCHAR(20) CHECK (estado IN ('activo', 'inactivo')) DEFAULT 'activo',
    ultimo_inicio_sesion TIMESTAMP WITH TIME ZONE
);

-- Tabla de Empleados
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

-- Tabla Marca
CREATE TABLE gf.marca (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
	año_fundacion INT,
	sede TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo'
);

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

--Tabla Tarjetas
CREATE TABLE gf.tarjetas (
    id_tarjeta SERIAL PRIMARY KEY,
    numero_tarjeta VARCHAR(7) NOT NULL,
    id_cliente INT REFERENCES gf.clientes(id_cliente),
    id_vendedor INT REFERENCES gf.vendedores(id_vendedor),
    id_zona INT REFERENCES gf.zonas(id_zona),
    total_gs INT NOT NULL,
    saldo INT DEFAULT 0,
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('SEM', 'QUIN', 'MENS')),
    estado VARCHAR(20) CHECK (estado IN ('activa', 'cancelada')) DEFAULT 'activa',
    fecha_emision DATE DEFAULT CURRENT_DATE,
    id_tarjeta_anterior INT REFERENCES gf.tarjetas(id_tarjeta)
);

-- Tabla Kit
CREATE TABLE gf.kit (
    id_kit SERIAL PRIMARY KEY,
    id_producto INTEGER NOT NULL REFERENCES gf.producto(id_producto),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo'
);

-- Tabla Productos_Kit
CREATE TABLE gf.producto_kit (
    id_kit INTEGER REFERENCES gf.kit(id_kit),
    id_producto INTEGER REFERENCES gf.producto(id_producto),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    PRIMARY KEY (id_kit, id_producto),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo'
);

-- Tabla Inventario (Enhanced Inventory Management)
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

-- Tabla Venta (Advanced Geospatial Sale Tracking)
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

-- Tabla Detalle_Venta
CREATE TABLE gf.detalle_venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INTEGER NOT NULL REFERENCES gf.venta(id_venta) ON DELETE CASCADE,
    id_producto INTEGER NOT NULL REFERENCES gf.producto(id_producto) ON DELETE RESTRICT,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario INTEGER NOT NULL CHECK (precio_unitario >= 0),
    subtotal INTEGER GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo'
);

-- Tabla de Maletines de Vendedoras
CREATE TABLE gf.maletines (
	id_maletin SERIAL PRIMARY KEY,
    id_empleado INT REFERENCES empleados(id_empleado),
    codigo_barra VARCHAR(50) UNIQUE NOT NULL,	
    fecha_carga DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPZ NULL DEFAULT NULL
);

-- Tabla Productos de Maletines
CREATE TABLE gf.productos_maletin (
    id_maletin INT REFERENCES maletines(id_maletin),
    id_producto INT REFERENCES productos(id_producto),
    codigo_barra VARCHAR(50) UNIQUE NOT NULL,	
    cantidad INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (id_maletin, id_producto)
);

-- Tabla de Liquidaciones
CREATE TABLE gf.liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_empleado INT REFERENCES empleados(id_empleado),
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas INTEGER,
    comision INTEGER,
    total_pagar INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

--Tabla Productos Vendidos
CREATE TABLE gf.productos_vendidos (
	id_tarjeta INTEGER REFERENCES gf.tarjetas(id_tarjeta),
	id_producto INTEGER REFERENCES gf.producto(id_producto),
    id_producto_vendido SERIAL PRIMARY KEY,
    cantidad INTEGER CHECK (cantidad > 0),
    precio INTEGER
);

-- Tabla Pago
CREATE TABLE gf.pago (
    id_pago SERIAL PRIMARY KEY,
    id_venta INTEGER NOT NULL REFERENCES gf.venta(id_venta),
	id_tarjeta INTEGER REFERENCES gf.tarjetas(id_tarjeta),	
    monto INTEGER NOT NULL CHECK (monto > 0),
    saldo_restante INTEGER NOT NULL,
    entrega_inicial BOOLEAN DEFAULT FALSE,
    recargo BOOLEAN DEFAULT FALSE,	
    fecha_pago TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo'
);

-- Tabla de Proveedores
CREATE TABLE gf.proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100)
);

-- Tabla de Compras a Proveedores
CREATE TABLE gf.compras_proveedores (
    id_compra SERIAL PRIMARY KEY,
    id_proveedor INT REFERENCES proveedores(id_proveedor),
    fecha_compra DATE DEFAULT CURRENT_DATE,
    total INTEGER,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Detalles de Compra
CREATE TABLE gf.detalles_compra (
    id_detalle SERIAL PRIMARY KEY,
    id_compra INT REFERENCES compras_proveedores(id_compra),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    precio_unitario INTEGER,
    subtotal INTEGER,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- =============================================
-- TABLAS DE GEOGRÁFICAS Y ESPACIALES
-- =============================================

-- Tabla de Departamentos
CREATE TABLE gf.departamentos (
    id_dpto SERIAL PRIMARY KEY,
    dpto VARCHAR(2) NOT NULL,
    dpto_desc VARCHAR(20) NOT NULL
);

-- Tabla de Distritos
CREATE TABLE gf.distritos (
    id_distrito SERIAL PRIMARY KEY,
    id_dpto INTEGER REFERENCES gf.departamentos(id_dpto),
    distrito VARCHAR(2) NOT NULL,
    dist_desc VARCHAR(40) NOT NULL,
    clave VARCHAR(4) NOT NULL
);

-- Tabla de Barrios y Localidades
CREATE TABLE gf.barrios_localidades (
    id_barrio SERIAL PRIMARY KEY,
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
    area VARCHAR(1),
    bar_loc VARCHAR(3),
    barlo_desc VARCHAR(51),
    clave VARCHAR(7)
);

-- Tabla de Vías Principales
CREATE TABLE gf.vias_principales (
    id_via SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    long_km_en NUMERIC(6),
    ruta_nro VARCHAR(2),
    ancho NUMERIC(2),
    tipo NUMERIC(2),
    long_mts NUMERIC(10)
);

-- Tabla de Vías
CREATE TABLE gf.vias (
    id_via SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    tipo NUMERIC(2),
    ancho NUMERIC(2),
    id_dpto INTEGER REFERENCES gf.departamentos(id_dpto)
);

-- Tabla de Locales de Salud
CREATE TABLE gf.locales_salud (
    id_local_salud SERIAL PRIMARY KEY,
    id_dpto INTEGER REFERENCES gf.departamentos(id_dpto),
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
    nombre VARCHAR(50),
    ubicacion GEOGRAPHY(POINT, 4326)
);

-- Tabla de Locales Educativos
CREATE TABLE gf.locales_educativos (
    id_local_edu SERIAL PRIMARY KEY,
    id_dpto_id INTEGER REFERENCES gf.departamentos(id_dpto),
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
    nombre VARCHAR(56),
    ubicacion GEOGRAPHY(POINT, 4326)
);

-- Tabla de Locales Policiales
CREATE TABLE gf.locales_policiales (
    id_local_policial SERIAL PRIMARY KEY,
    id_dpto INTEGER REFERENCES gf.departamentos(id_dpto),
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
    nombre VARCHAR(51),
    ubicacion GEOGRAPHY(POINT, 4326)
);

--Tabla Zonas
CREATE TABLE gf.zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE,
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito)
);

--Tabla Prefijos
CREATE TABLE gf.prefijos (
    id_prefijo SERIAL PRIMARY KEY,
    prefijo VARCHAR(4) UNIQUE NOT NULL,
    descripcion VARCHAR(50)
);

INSERT INTO gf.prefijos (prefijo, descripcion) 
VALUES 
    ('+595961', 'HOLA PARAGUAY-VOX'),
    ('+595971', 'PERSONAL'),
    ('+595972', 'PERSONAL'),
    ('+595973', 'PERSONAL'),
    ('+595975', 'PERSONAL'),
    ('+595976', 'PERSONAL'),
    ('+595981', 'TELECEL-TIGO'),
    ('+595982', 'TELECEL-TIGO'),
    ('+595983', 'TELECEL-TIGO'),
    ('+595984', 'TELECEL-TIGO'),
    ('+595985', 'TELECEL-TIGO'),
    ('+595991', 'AMX MOVIL CLARO'),
    ('+595992', 'AMX MOVIL CLARO'),
    ('+595993', 'AMX MOVIL CLARO'),
    ('+595995', 'AMX MOVIL CLARO');

-- Tabla de Códigos Postales
CREATE TABLE gf.codigos_postales (
    id_codigo_postal SERIAL PRIMARY KEY,
    dpto VARCHAR(2),
    dpto_desc VARCHAR(50),
    distrito VARCHAR(2),
    dist_desc VARCHAR(50),
    area_1 VARCHAR(50),
    barloc VARCHAR(50),
    barlo_desc VARCHAR(100),
    viv_2014 INTEGER,
    div_post VARCHAR(50),
    zona VARCHAR(50),
    cod_post VARCHAR(10),
    obs TEXT,
    cod_bar VARCHAR(50)
);

-- Tabla de Envío de Encomiendas
CREATE TABLE gf.envio_encomiendas (
    id_envio SERIAL PRIMARY KEY,
    id_cliente INTEGER,
    destinatario VARCHAR(100),
    direccion_destino TEXT,
    ciudad_destino VARCHAR(50),
    codigo_postal VARCHAR(20),
    pais_destino VARCHAR(50),
    peso DECIMAL(10, 2),
    valor_declarado DECIMAL(10, 2),
    fecha_envio DATE,
    fecha_entrega_estimada DATE,
    estado VARCHAR(20),
    numero_seguimiento VARCHAR(50),
    compania_envio VARCHAR(50),
    costo_envio DECIMAL(10, 2),
    notas TEXT
);

-- Tabla SMS
CREATE TABLE gf.sms (
    id_sms SERIAL PRIMARY KEY,
    destinatario VARCHAR(20),
    enviado BOOLEAN,
    fecha DATE,
    hora TIME,
    modulo VARCHAR(50),
    referencia VARCHAR(100),
    fecha_env DATE,
    id_cliente INTEGER,
    id_mensaje_preestablecido INTEGER REFERENCES gf.mensajes_preestablecidos(id_mensaje)
);

-- Tabla de Mensajes Preestablecidos
CREATE TABLE gf.mensajes_preestablecidos (
    id_mensaje SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    contenido TEXT
);

INSERT INTO gf.mensajes_preestablecidos (tipo, contenido)
VALUES
    ('Cumpleaños', '¡Feliz cumpleaños! Le deseamos un maravilloso día.'),
    ('Pago Retrasado', 'Estimado cliente, le recordamos que tiene un pago retrasado. Por favor, realice el pago lo antes posible.'),
    ('Promoción', '¡No te pierdas nuestra última promoción! Con un descuento especial en todos nuestros productos.');

INSERT INTO gf.sms (destinatario, enviado, fecha, hora, modulo, referencia, fecha_env, id_cliente, id_mensaje_preestablecido)
VALUES
    ('+595981234567', true, '2023-06-01', '10:00:00', 'Cumpleaños', 'Cliente ID: 123', '2023-05-31', 123, 1);

-- Tabla Tracking_GPS
CREATE TABLE gf.tracking_gps (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INTEGER NOT NULL REFERENCES gf.vehiculo(id_vehiculo),
    ubicacion GEOGRAPHY(POINT, 4326) NOT NULL,
    fecha_hora TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo'
);

-- Tabla Rutas
CREATE TABLE gf.rutas (
    id SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_vehiculo INTEGER REFERENCES vehiculos(id_vehiculo),
    fecha DATE NOT NULL,
    inicio_ruta GEOGRAPHY(POINT, 4326),
    fin_ruta GEOGRAPHY(POINT, 4326),
    distancia_km DECIMAL(10,2),
    tiempo_estimado INTEGER, -- minutos
    tiempo_real INTEGER,
    estado VARCHAR(20) CHECK (estado IN ('planificada', 'en_progreso', 'completada', 'cancelada')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Tabla Puntos Ruta
CREATE TABLE gf.puntos_ruta (
    id SERIAL PRIMARY KEY,
    ruta_id INTEGER REFERENCES rutas(id),
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    orden INTEGER NOT NULL,
    hora_planificada TIME,
    hora_real TIME,
    ubicacion GEOGRAPHY(POINT, 4326),
    estado VARCHAR(20) CHECK (estado IN ('pendiente', 'visitado', 'no_visitado', 'reprogramado')),
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_persona_cedula ON gf.persona(cedula);
CREATE INDEX idx_cliente_ruc ON gf.cliente(ruc);
CREATE INDEX idx_producto_codigo ON gf.producto(codigo_barras);
CREATE INDEX idx_venta_fecha ON gf.venta(fecha_venta);
CREATE INDEX idx_pago_fecha ON gf.pago(fecha_pago);
CREATE INDEX idx_tracking_fecha ON gf.tracking_gps(fecha_hora);

-- Índices normales para columnas de texto
CREATE INDEX idx_barrios_localidades_barlo_desc ON gf.barrios_localidades (barlo_desc);
CREATE INDEX idx_comunidades_indigenas_barlo_desc ON gf.comunidades_indigenas (barlo_desc);
CREATE INDEX idx_clientes_direccion ON gf.clientes (direccion);

-- Índices espaciales para columnas de ubicación
CREATE INDEX idx_locales_salud_ubicacion ON gf.locales_salud USING GIST (ubicacion);
CREATE INDEX idx_locales_educativos_ubicacion ON gf.locales_educativos USING GIST (ubicacion);
CREATE INDEX idx_locales_policiales_ubicacion ON gf.locales_policiales USING GIST (ubicacion);

-- Índice para la columna de fecha de último inicio de sesión
CREATE INDEX idx_clientes_ultimo_inicio_sesion ON gf.clientes (ultimo_inicio_sesion);

-- Índices para subcadenas del código de barras
CREATE INDEX idx_productos_codigo_barras_inicio ON gf.productos (LEFT(codigo_barras, 3));
CREATE INDEX idx_productos_codigo_barras_fin ON gf.productos (RIGHT(codigo_barras, 3));

-- Función para actualizar timestamps
CREATE OR REPLACE FUNCTION gf.update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar timestamps
CREATE TRIGGER update_timestamp
    BEFORE UPDATE ON gf.persona
    FOR EACH ROW
    EXECUTE FUNCTION gf.update_timestamp();

-- Repetir para todas las tablas que necesiten actualización de timestamp

-- Índices para optimizar búsquedas geográficas
CREATE INDEX idx_departamento_geometria ON gf.departamento USING GIST (geometria);
CREATE INDEX idx_distrito_geometria ON gf.distrito USING GIST (geometria);
CREATE INDEX idx_barrio_geometria ON gf.barrio_localidad USING GIST (geometria);

-- Índices para búsquedas por código
CREATE INDEX idx_distrito_clave ON gf.distrito(clave);
CREATE INDEX idx_barrio_clave ON gf.barrio_localidad(clave);

-- Función para obtener la ubicación completa
CREATE OR REPLACE FUNCTION gf.obtener_ubicacion_completa(
    p_dpto CHAR(2),
    p_distrito CHAR(2),
    p_bar_loc CHAR(3)
)
RETURNS TABLE (
    departamento VARCHAR(100),
    distrito VARCHAR(100),
    barrio_localidad VARCHAR(100),
    area CHAR(1)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        b.dpto_desc,
        b.dist_desc,
        b.barlo_desc,
        b.area
    FROM gf.barrio_localidad b
    WHERE b.dpto = p_dpto
        AND b.distrito = p_distrito
        AND b.bar_loc = p_bar_loc;
END;
$$ LANGUAGE plpgsql;

-- Función para encontrar la ubicación por coordenada
CREATE OR REPLACE FUNCTION gf.obtener_ubicacion_por_punto(
    latitud DOUBLE PRECISION,
    longitud DOUBLE PRECISION
)
RETURNS TABLE (
    dpto CHAR(2),
    distrito CHAR(2),
    bar_loc CHAR(3),
    dpto_desc VARCHAR(100),
    dist_desc VARCHAR(100),
    barlo_desc VARCHAR(100)
) AS $$
DECLARE
    punto GEOGRAPHY;
BEGIN
    punto := ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)::GEOGRAPHY;
    
    RETURN QUERY
    SELECT 
        b.dpto,
        b.distrito,
        b.bar_loc,
        b.dpto_desc,
        b.dist_desc,
        b.barlo_desc
    FROM gf.barrio_localidad b
    WHERE ST_Contains(b.geometria::geometry, punto::geometry)
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

--Optimización con Índices
CREATE INDEX idx_tarjetas_cliente ON Tarjetas(id_cliente);
CREATE INDEX idx_productos_codigo_barras ON Productos(codigo_barras);
CREATE INDEX idx_pagos_fecha ON Pagos(fecha_pago);
CREATE INDEX idx_rutas_vendedor_fecha ON Rutas(id_vendedor, fecha);
CREATE INDEX idx_pagos_cliente_metodo ON Pagos(id_cliente, metodo_pago);
CREATE INDEX idx_antecedentes_cedula ON AntecedentesJudiciales(cedula);
CREATE INDEX idx_inventario_maletines_producto ON Inventario_Maletines(id_maletin, id_producto);
CREATE INDEX idx_vehiculos_motor_chasis_placa ON Vehiculos(numero_motor, numero_chasis, placa);
CREATE INDEX idx_tarjetas_numero ON Tarjetas(numero_tarjeta);
CREATE INDEX idx_maletin_empleado ON Maletines(id_empleado);
CREATE INDEX idx_liquidacion_empleado ON Liquidaciones(id_empleado);
CREATE INDEX ON barrios_localidades (barlo_desc);
CREATE INDEX ON comunidades_indigenas (barlo_desc);
CREATE INDEX idx_rutas_inicio_ruta ON rutas USING GIST (inicio_ruta);
CREATE INDEX idx_puntos_ruta_ubicacion ON puntos_ruta USING GIST (ubicacion);
CREATE INDEX idx_zonas_geom ON zonas USING GIST (geom);

-- Índices espaciales para optimizar consultas
CREATE INDEX ON barrios_localidades USING GIST (barlo_desc);
CREATE INDEX ON comunidades_indigenas USING GIST (barlo_desc);
CREATE INDEX ON locales_salud USING GIST (ubicacion);
CREATE INDEX ON locales_educativos USING GIST (ubicacion);
CREATE INDEX ON locales_policiales USING GIST (ubicacion);
CREATE INDEX idx_clientes_direccion ON Clientes USING GIST (direccion);
CREATE INDEX idx_clientes_ultimo_inicio_sesion ON Clientes (ultimo_inicio_sesion);
CREATE INDEX idx_productos_codigo_barras_inicio ON Productos (LEFT(codigo_barras, 3));
CREATE INDEX idx_productos_codigo_barras_fin ON Productos (RIGHT(codigo_barras, 3));

CREATE TRIGGER update_ultimo_inicio_sesion
BEFORE UPDATE ON Clientes
FOR EACH ROW
WHEN (NEW.estado = 'activo')
EXECUTE PROCEDURE update_ultimo_inicio_sesion();

-- Ejemplo de consulta para encontrar clientes activos en una zona específica
WITH clientes_en_zona AS (
  SELECT id_cliente
  FROM Clientes
  WHERE ST_DWithin(direccion, ST_MakePoint(-58.3816, -34.6037), 1000) -- Buscar clientes a 1 km de un punto
)
SELECT * FROM Clientes
WHERE id_cliente IN (SELECT id_cliente FROM clientes_en_zona);
CREATE OR REPLACE FUNCTION update_ultimo_inicio_sesion()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.estado = 'activo' THEN
        NEW.ultimo_inicio_sesion = CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_ultimo_inicio_sesion
BEFORE UPDATE ON Clientes
FOR EACH ROW
WHEN (NEW.estado = 'activo')
EXECUTE FUNCTION update_ultimo_inicio_sesion();

CREATE FUNCTION calcular_edad(fecha_nacimiento DATE)
RETURNS INTEGER AS $$
DECLARE
  edad INTEGER;
BEGIN
  SELECT AGE(CURRENT_DATE, fecha_nacimiento) INTO edad;
  RETURN edad;
END;
$$ LANGUAGE plpgsql;

--Triggers y Funciones

--Actualizar saldo del cliente
CREATE OR REPLACE FUNCTION actualizar_saldo_cliente() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Tarjetas 
    SET saldo = saldo - NEW.monto
    WHERE id_tarjeta = NEW.id_tarjeta;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--Trigger para actualizar saldo tras un pago:
CREATE TRIGGER tg_actualizar_saldo
AFTER INSERT ON Pagos
FOR EACH ROW
EXECUTE FUNCTION actualizar_saldo_cliente();

--Función para actualizar inventario tras una venta:
CREATE OR REPLACE FUNCTION actualizar_inventario() 
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.cantidad > (SELECT stock FROM Productos WHERE id_producto = NEW.id_producto) THEN
        RAISE EXCEPTION 'No hay suficiente stock para este producto';
    ELSE
        UPDATE Productos 
        SET stock = stock - NEW.cantidad 
        WHERE id_producto = NEW.id_producto;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--Trigger para actualizar inventario tras una venta:
CREATE TRIGGER tg_actualizar_inventario
AFTER INSERT ON Productos_Vendidos
FOR EACH ROW
EXECUTE FUNCTION actualizar_inventario();

CREATE OR REPLACE FUNCTION actualizar_stock_maletin() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.cantidad > (SELECT stock FROM Productos WHERE id_producto = NEW.id_producto) THEN
        RAISE EXCEPTION 'No hay suficiente stock';
    ELSE
        UPDATE Productos SET stock = stock - NEW.cantidad WHERE id_producto = NEW.id_producto;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--Trigger para Actualizar Stock,
CREATE TRIGGER tg_actualizar_stock
AFTER INSERT ON Productos_Maletin
FOR EACH ROW EXECUTE FUNCTION actualizar_stock_maletin();

CREATE OR REPLACE FUNCTION actualizar_stock_producto() RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.cantidad > (SELECT stock FROM Productos WHERE id_producto = NEW.id_producto)) THEN
        RAISE EXCEPTION 'No hay suficiente stock para este producto';
    ELSE
        UPDATE Productos 
        SET stock = stock - NEW.cantidad 
        WHERE id_producto = NEW.id_producto;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_stock
AFTER INSERT ON DetalleVenta
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock_producto();

--Trigger para Control de Stock en Maletines: Disminuye el stock de productos cuando se asignan a un maletín.

CREATE OR REPLACE FUNCTION actualizar_stock_maletin() RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.cantidad > (SELECT stock FROM Productos WHERE id_producto = NEW.id_producto)) THEN
        RAISE EXCEPTION 'No hay suficiente stock para el producto %', NEW.id_producto;
    ELSE
        UPDATE Productos 
        SET stock = stock - NEW.cantidad 
        WHERE id_producto = NEW.id_producto;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_stock_maletin
AFTER INSERT ON Productos_Maletin
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock_maletin();

--Trigger para Actualizar Liquidación por Venta: Calcula la liquidación de la vendedora al final del día.

CREATE OR REPLACE FUNCTION calcular_liquidacion() RETURNS TRIGGER AS $$
BEGIN
	NEW.total_pagar := NEW.total_ventas * 50000;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_calcular_liquidacion
BEFORE INSERT ON Liquidaciones
FOR EACH ROW
EXECUTE FUNCTION calcular_liquidacion();

--Trigger de antecedentes judiciales: Verificar si un cliente tiene antecedentes antes de ser registrado.

CREATE OR REPLACE FUNCTION verificar_antecedentes_judiciales() RETURNS TRIGGER AS $$
BEGIN
	IF EXISTS (SELECT 1 FROM AntecedentesJudiciales WHERE numero_ci = NEW.cedula) THEN
		RAISE NOTICE 'El cliente con cédula % tiene antecedentes judiciales', NEW.cedula;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_verificar_antecedentes_judiciales
BEFORE INSERT ON Clientes
FOR EACH ROW
EXECUTE FUNCTION verificar_antecedentes_judiciales();

--Vista para Reportes de Ventas
CREATE VIEW VW_Ventas_Por_Cliente AS
SELECT 
    c.id_cliente, 
    c.nombre, 
    c.apellido, 
    COUNT(v.id_tarjeta) AS total_ventas, 
    SUM(v.total_gs) AS monto_total
FROM 
    Clientes c
JOIN 
    Tarjetas v ON c.id_cliente = v.id_cliente
GROUP BY 
    c.id_cliente;

CREATE VIEW VW_Ventas_Por_Zona AS
SELECT Z.nombre_zona, SUM(T.total_gs) AS total_ventas
FROM Zonas Z
JOIN Rutas R ON Z.id_zona = R.id_zona
JOIN Tarjetas T ON R.id_ruta = T.id_ruta
GROUP BY Z.nombre_zona;

-- 1. Corregir tipos de datos y charset
ALTER DATABASE Gabriela_Fragancias SET DEFAULT_TEXT_SEARCH_CONFIG = 'spanish';

-- 2. Agregar columnas faltantes
ALTER TABLE gf.cliente ADD COLUMN IF NOT EXISTS ultimo_inicio_sesion TIMESTAMPTZ;

-- 3. Crear índices parciales
CREATE INDEX idx_cliente_activo ON gf.cliente(id_cliente) 
WHERE estado = 'activo';

-- 4. Mejorar índices espaciales
CREATE INDEX idx_tracking_ubicacion_tiempo ON gf.tracking_gps 
USING GIST (ubicacion, fecha_hora);

-- 5. Implementar RLS
ALTER TABLE gf.cliente ENABLE ROW LEVEL SECURITY;
CREATE POLICY cliente_access_policy ON gf.cliente
    USING (id_empleado = current_user_id());

CREATE OR REPLACE FUNCTION actualizar_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_updated_at
BEFORE UPDATE ON gf.productos_maletin
FOR EACH ROW
EXECUTE FUNCTION actualizar_updated_at();

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