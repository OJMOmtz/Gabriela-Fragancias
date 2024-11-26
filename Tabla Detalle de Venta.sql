-- Tabla Detalle de Venta
CREATE TABLE DetalleVenta (
    id_detalle_venta SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES Venta(id_venta) ON DELETE CASCADE,
    id_presentacion INTEGER REFERENCES Presentacion(id_presentacion) ON DELETE CASCADE,
    cantidad INTEGER CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED
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

-- Tabla Detalle de Ventas
CREATE TABLE ventas_detalle (
    id_venta_detalle SERIAL PRIMARY KEY,
    cantidad INTEGER NOT NULL,
    id_venta INTEGER REFERENCES ventas(id_venta),
    id_producto INTEGER REFERENCES productos(id_producto)
);

-- Tabla Detalle de Ventas
CREATE TABLE ventas_detalle (
    id_venta_detalle SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES ventas(id_venta) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER NOT NULL
);

-- Tabla Detalle de Ventas
CREATE TABLE ventas_detalle (
    id_venta_detalle SERIAL PRIMARY KEY,
    cantidad INTEGER,
    id_venta INTEGER REFERENCES ventas(id_venta),
    id_producto INTEGER REFERENCES productos(id_producto)
);

-- Tabla Detalles de Venta
CREATE TABLE Detalles_Venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES Ventas(id_venta) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Detalle de Ventas
CREATE TABLE Ventas_Detalle (
    id_venta_detalle SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES Ventas(id_venta) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL
);

-- Tabla de Detalle de Ventas
CREATE TABLE detalle_ventas (
    id_detalle_venta SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES ventas(id_venta),
    id_presentacion INTEGER REFERENCES presentaciones(id_presentacion),
    cantidad INTEGER,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2)
);