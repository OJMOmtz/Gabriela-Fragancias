-- Tabla Venta
CREATE TABLE Venta (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Cliente(id_cliente) ON DELETE CASCADE,
    id_vendedor INTEGER REFERENCES Vendedor(id_vendedor) ON DELETE CASCADE,
    fecha_venta TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2),
    estado VARCHAR(20) CHECK (estado IN ('pendiente', 'pagado', 'cancelado')),
    entrega_inmediata BOOLEAN DEFAULT TRUE
);

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

-- Tabla Ventas
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    total NUMERIC(10,2) NOT NULL,
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor)
);

-- Tabla Ventas
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    total NUMERIC(10,2) NOT NULL,
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor)
);

-- Tabla Ventas
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    fecha DATE,
    total NUMERIC(10,2),
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor)
);

-- Tabla Ventas
CREATE TABLE Ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_producto INTEGER REFERENCES Productos(id_producto),
    fecha DATE DEFAULT CURRENT_DATE,
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('Contado', 'Crédito')),  -- Contado, Crédito (SEM, QUIN, MENS)
    total DECIMAL(10, 2) NOT NULL,
    saldo DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Ventas
CREATE TABLE Ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_producto INTEGER REFERENCES Productos(id_producto),
    fecha DATE DEFAULT CURRENT_DATE,
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('Contado', 'Crédito')),
    total DECIMAL(10, 2) NOT NULL,
    saldo DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Ventas
CREATE TABLE Ventas (
    id_venta SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    total NUMERIC(10,2) NOT NULL,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor)
);

-- Tabla de Ventas
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    fecha_venta DATE,
    total DECIMAL(10, 2),
    tipo_pago VARCHAR(20),
    estado VARCHAR(20),
    entrega_inmediata BOOLEAN DEFAULT TRUE
);