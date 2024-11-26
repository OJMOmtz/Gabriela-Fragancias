-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- Para búsquedas textuales mejoradas

-- Configuración de esquema
CREATE SCHEMA IF NOT EXISTS gabriela;
SET search_path TO gabriela, public;

-- Tablas base del sistema
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    rol_id INTEGER REFERENCES roles(id),
    vendedor_id INTEGER,
    ultimo_login TIMESTAMP,
    intentos_fallidos INTEGER DEFAULT 0,
    bloqueado BOOLEAN DEFAULT false,
    fecha_bloqueo TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

CREATE TABLE roles_permisos (
    rol_id INTEGER REFERENCES roles(id),
    permiso_id INTEGER REFERENCES permisos(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rol_id, permiso_id)
);

-- Tablas de negocio
CREATE TABLE zonas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    area geography(POLYGON, 4326),
    meta_ventas DECIMAL(12,2),
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vendedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_ingreso DATE NOT NULL,
    zona_id INTEGER REFERENCES zonas(id),
    comision_porcentaje DECIMAL(5,2) DEFAULT 0,
    meta_mensual DECIMAL(12,2),
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Actualizar referencia en usuarios
ALTER TABLE usuarios
ADD CONSTRAINT fk_usuarios_vendedores
FOREIGN KEY (vendedor_id) REFERENCES vendedores(id);

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE,
    tipo_documento VARCHAR(10),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    ubicacion geography(POINT, 4326),
    zona_id INTEGER REFERENCES zonas(id),
    vendedor_id INTEGER REFERENCES vendedores(id),
    limite_credito DECIMAL(12,2) DEFAULT 0,
    categoria VARCHAR(20) DEFAULT 'REGULAR',
    fecha_registro DATE DEFAULT CURRENT_DATE,
    ultimo_contacto TIMESTAMP,
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    historial_compras JSONB DEFAULT '[]'::jsonb,
    preferencias JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50),
    precio_costo DECIMAL(10,2) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 5,
    stock_maximo INTEGER DEFAULT 100,
    fragancia VARCHAR(100),
    volumen_ml INTEGER,
    imagen_url VARCHAR(255),
    proveedor VARCHAR(100),
    tiempo_reposicion INTEGER, -- días
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE vehiculos (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INTEGER,
    capacidad_kg DECIMAL(10,2),
    vendedor_id INTEGER REFERENCES vendedores(id),
    ultimo_mantenimiento DATE,
    proximo_mantenimiento DATE,
    kilometraje_actual INTEGER DEFAULT 0,
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    historial_mantenimiento JSONB DEFAULT '[]'::jsonb
);

CREATE TABLE rutas (
    id SERIAL PRIMARY KEY,
    vendedor_id INTEGER REFERENCES vendedores(id),
    vehiculo_id INTEGER REFERENCES vehiculos(id),
    fecha DATE NOT NULL,
    inicio_ruta geography(POINT, 4326),
    fin_ruta geography(POINT, 4326),
    distancia_km DECIMAL(10,2),
    tiempo_estimado INTEGER, -- minutos
    tiempo_real INTEGER,
    estado VARCHAR(20) DEFAULT 'planificada',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    CHECK (estado IN ('planificada', 'en_progreso', 'completada', 'cancelada'))
);

CREATE TABLE puntos_ruta (
    id SERIAL PRIMARY KEY,
    ruta_id INTEGER REFERENCES rutas(id),
    cliente_id INTEGER REFERENCES clientes(id),
    orden INTEGER NOT NULL,
    hora_planificada TIME,
    hora_real TIME,
    ubicacion geography(POINT, 4326),
    estado VARCHAR(20) DEFAULT 'pendiente',
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (estado IN ('pendiente', 'visitado', 'no_visitado', 'reprogramado'))
);

CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    numero_factura VARCHAR(20) UNIQUE,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cliente_id INTEGER REFERENCES clientes(id),
    vendedor_id INTEGER REFERENCES vendedores(id),
    subtotal DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    impuesto DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    forma_pago VARCHAR(20),
    numero_cuotas INTEGER DEFAULT 1,
    estado VARCHAR(20) DEFAULT 'pendiente',
    punto_ruta_id INTEGER REFERENCES puntos_ruta(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    CHECK (estado IN ('pendiente', 'pagada', 'cancelada', 'anulada'))
);

CREATE TABLE detalles_venta (
    id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES ventas(id),
    producto_id INTEGER REFERENCES productos(id),
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    subtotal DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES ventas(id),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto DECIMAL(10,2) NOT NULL,
    forma_pago VARCHAR(20) NOT NULL,
    numero_comprobante VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'procesado',
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    CHECK (estado IN ('procesado', 'anulado', 'rechazado'))
);

CREATE TABLE log_actividad (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    accion VARCHAR(50) NOT NULL,
    tabla_afectada VARCHAR(50),
    registro_id INTEGER,
    detalles JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tablas para funcionalidades futuras
CREATE TABLE notificaciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    titulo VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL,
    tipo VARCHAR(20),
    leida BOOLEAN DEFAULT false,
    fecha_lectura TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE metas_ventas (
    id SERIAL PRIMARY KEY,
    vendedor_id INTEGER REFERENCES vendedores(id),
    zona_id INTEGER REFERENCES zonas(id),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    monto_objetivo DECIMAL(12,2) NOT NULL,
    monto_alcanzado DECIMAL(12,2) DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'activa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE promociones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    tipo VARCHAR(20),
    descuento DECIMAL(5,2),
    condiciones JSONB,
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_clientes_documento ON clientes(documento);
CREATE INDEX idx_clientes_zona ON clientes(zona_id);
CREATE INDEX idx_vendedores_zona ON vendedores(zona_id);
CREATE INDEX idx_ventas_cliente ON ventas(cliente_id);
CREATE INDEX idx_ventas_vendedor ON ventas(vendedor_id);
CREATE INDEX idx_ventas_fecha ON ventas(fecha);
CREATE INDEX idx_pagos_venta ON pagos(venta_id);
CREATE INDEX idx_rutas_vendedor ON rutas(vendedor_id);
CREATE INDEX idx_productos_codigo ON productos(codigo);
CREATE INDEX idx_productos_nombre ON productos USING gin(nombre gin_trgm_ops);

-- Índices espaciales
CREATE INDEX idx_zonas_area ON zonas USING GIST(area);
CREATE INDEX idx_clientes_ubicacion ON clientes USING GIST(ubicacion);
CREATE INDEX idx_rutas_inicio ON rutas USING GIST(inicio_ruta);
CREATE INDEX idx_rutas_fin ON rutas USING GIST(fin_ruta);
CREATE INDEX idx_puntos_ruta_ubicacion ON puntos_ruta USING GIST(ubicacion);

-- Funciones útiles
CREATE OR REPLACE FUNCTION actualizar_stock() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE productos
    SET stock_actual = stock_actual - NEW.cantidad
    WHERE id = NEW.producto_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calcular_comision_vendedor() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE vendedores
    SET meta_mensual = meta_mensual + NEW.total * (comision_porcentaje / 100)
    WHERE id = NEW.vendedor_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER tr_actualizar_stock
AFTER INSERT ON detalles_venta
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock();

CREATE TRIGGER tr_calcular_comision
AFTER INSERT ON ventas
FOR EACH ROW
EXECUTE FUNCTION calcular_comision_vendedor();

-- Datos iniciales
INSERT INTO roles (nombre, descripcion) VALUES
('admin', 'Administrador del sistema'),
('vendedor', 'Vendedor con acceso a clientes y ventas'),
('supervisor', 'Supervisor de ventas'),
('contador', 'Acceso a información financiera'),
('almacen', 'Gestión de inventario');

INSERT INTO permisos (nombre, descripcion) VALUES
('crear_venta', 'Puede crear nuevas ventas'),
('ver_ventas', 'Puede ver listado de ventas'),
('modificar_venta', 'Puede modificar ventas existentes'),
('eliminar_venta', 'Puede eliminar ventas'),
('ver_reportes', 'Puede ver reportes del sistema'),
('gestionar_usuarios', 'Puede gestionar usuarios'),
('gestionar_productos', 'Puede gestionar productos'),
('ver_estadisticas', 'Puede ver estadísticas del sistema'),
('gestionar_rutas', 'Puede gestionar rutas de venta'),
('gestionar_inventario', 'Puede gestionar inventario');

-- Comentarios para documentación
COMMENT ON TABLE usuarios IS 'Almacena información de usuarios del sistema';
COMMENT ON TABLE ventas IS 'Registro de ventas realizadas';
COMMENT ON TABLE rutas IS 'Planificación de rutas de vendedores';
COMMENT ON TABLE productos IS 'Catálogo de productos disponibles';
