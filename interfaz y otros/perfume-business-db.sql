-- Enable PostGIS extension for geographical data
CREATE EXTENSION IF NOT EXISTS postgis;

-- Zonas de ventas (Sales Territories)
CREATE TABLE zonas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    area geography(POLYGON, 4326),
    estado BOOLEAN DEFAULT true
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

-- Clientes (Customers)
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    ubicacion geography(POINT, 4326),
    zona_id INTEGER REFERENCES zonas(id),
    fecha_registro DATE DEFAULT CURRENT_DATE,
    estado BOOLEAN DEFAULT true
);

-- Productos (Products)
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_venta DECIMAL(10,2) NOT NULL,
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 5,
    fragancia VARCHAR(100),
    volumen_ml INTEGER,
    estado BOOLEAN DEFAULT true
);

-- Rutas de venta (Sales Routes)
CREATE TABLE rutas (
    id SERIAL PRIMARY KEY,
    vendedor_id INTEGER REFERENCES vendedores(id),
    fecha DATE NOT NULL,
    inicio_ruta geography(POINT, 4326),
    fin_ruta geography(POINT, 4326),
    distancia_km DECIMAL(10,2),
    estado VARCHAR(20) DEFAULT 'planificada',
    CHECK (estado IN ('planificada', 'en_progreso', 'completada', 'cancelada'))
);

-- Puntos de la ruta (Route Waypoints)
CREATE TABLE puntos_ruta (
    id SERIAL PRIMARY KEY,
    ruta_id INTEGER REFERENCES rutas(id),
    cliente_id INTEGER REFERENCES clientes(id),
    orden INTEGER NOT NULL,
    hora_planificada TIME,
    hora_real TIME,
    ubicacion geography(POINT, 4326),
    estado VARCHAR(20) DEFAULT 'pendiente',
    CHECK (estado IN ('pendiente', 'visitado', 'no_visitado'))
);

-- Ventas (Sales)
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cliente_id INTEGER REFERENCES clientes(id),
    vendedor_id INTEGER REFERENCES vendedores(id),
    total DECIMAL(10,2) NOT NULL,
    forma_pago VARCHAR(20),
    numero_cuotas INTEGER DEFAULT 1,
    estado VARCHAR(20) DEFAULT 'pendiente',
    CHECK (estado IN ('pendiente', 'pagada', 'cancelada'))
);

-- Detalles de venta (Sale Details)
CREATE TABLE detalles_venta (
    id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES ventas(id),
    producto_id INTEGER REFERENCES productos(id),
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL
);

-- Pagos (Payments)
CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES ventas(id),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto DECIMAL(10,2) NOT NULL,
    forma_pago VARCHAR(20) NOT NULL,
    numero_comprobante VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'procesado',
    CHECK (estado IN ('procesado', 'anulado'))
);

-- Índices para optimización
CREATE INDEX idx_clientes_zona ON clientes(zona_id);
CREATE INDEX idx_vendedores_zona ON vendedores(zona_id);
CREATE INDEX idx_ventas_cliente ON ventas(cliente_id);
CREATE INDEX idx_ventas_vendedor ON ventas(vendedor_id);
CREATE INDEX idx_rutas_vendedor ON rutas(vendedor_id);

-- Índices espaciales
CREATE INDEX idx_zonas_area ON zonas USING GIST(area);
CREATE INDEX idx_clientes_ubicacion ON clientes USING GIST(ubicacion);
CREATE INDEX idx_rutas_inicio ON rutas USING GIST(inicio_ruta);
CREATE INDEX idx_rutas_fin ON rutas USING GIST(fin_ruta);
CREATE INDEX idx_puntos_ruta_ubicacion ON puntos_ruta USING GIST(ubicacion);
