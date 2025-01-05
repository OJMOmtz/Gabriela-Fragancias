-- Actualizaciones a la tabla de Productos
ALTER TABLE productos
ADD COLUMN presentacion VARCHAR(50),
ADD COLUMN volumen INT CHECK (volumen BETWEEN 5 AND 200),
ADD COLUMN es_kit BOOLEAN DEFAULT FALSE;

-- Tabla de Kits (para manejar kits con varios productos)
CREATE TABLE kits (
    id_kit SERIAL PRIMARY KEY,
    id_producto INT REFERENCES productos(id_producto),
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE productos_kit (
    id_kit INT REFERENCES kits(id_kit),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    PRIMARY KEY (id_kit, id_producto)
);

-- Tabla de Maletines de Vendedoras
CREATE TABLE maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_empleado INT REFERENCES empleados(id_empleado),
    fecha_carga DATE DEFAULT CURRENT_DATE
);

CREATE TABLE productos_maletin (
    id_maletin INT REFERENCES maletines(id_maletin),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    PRIMARY KEY (id_maletin, id_producto)
);

-- Tabla de Liquidaciones
CREATE TABLE liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_empleado INT REFERENCES empleados(id_empleado),
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas DECIMAL(10, 2),
    comision DECIMAL(10, 2),
    total_pagar DECIMAL(10, 2)
);

-- Actualización a la tabla de Ventas
ALTER TABLE ventas
ADD COLUMN entrega_inmediata BOOLEAN DEFAULT TRUE;

-- Tabla de Equipos (para manejar lectores de códigos, impresoras, etc.)
CREATE TABLE equipos (
    id_equipo SERIAL PRIMARY KEY,
    tipo VARCHAR(50) CHECK (tipo IN ('Lector Código Barras', 'Impresora Ticket', 'Impresora Matricial', 'Impresora Láser', 'Impresora Inyección')),
    marca VARCHAR(50),
    modelo VARCHAR(50),
    fecha_adquisicion DATE
);

-- Actualización a la tabla de Gastos de Vehículos
ALTER TABLE gastos_vehiculos
ADD COLUMN tipo_gasto VARCHAR(50) CHECK (tipo_gasto IN ('Combustible', 'Lubricantes', 'Gomería', 'Mecánica', 'Electricidad', 'Otro'));

-- Tabla para manejar afiliaciones políticas (si es necesario)
CREATE TABLE afiliaciones_politicas (
    id_afiliacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE
);

-- Agregar referencia a la tabla de clientes
ALTER TABLE clientes
ADD COLUMN id_afiliacion INT REFERENCES afiliaciones_politicas(id_afiliacion);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_clientes_cedula ON clientes(cedula);
CREATE INDEX idx_clientes_ruc ON clientes(ruc);
CREATE INDEX idx_productos_codigo_barras ON productos(codigo_barras);
CREATE INDEX idx_ventas_fecha ON ventas(fecha_venta);
CREATE INDEX idx_empleados_cargo ON empleados(cargo);
