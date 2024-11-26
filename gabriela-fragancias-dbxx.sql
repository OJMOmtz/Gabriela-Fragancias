-- Tabla de Clientes
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE,
    ruc VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_registro DATE DEFAULT CURRENT_DATE,
    grupo_economico VARCHAR(50),
    sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
    edad_grupo VARCHAR(20) CHECK (edad_grupo IN ('Niño', 'Púber', 'Adolescente', 'Joven', 'Adulto', 'Mayor')),
    afiliacion_politica VARCHAR(50)
);

-- Tabla de Empleados
CREATE TABLE empleados (
    id_empleado SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) CHECK (cargo IN ('Vendedor', 'Cobrador', 'Chofer')),
    fecha_contratacion DATE,
    salario DECIMAL(10, 2)
);

-- Tabla de Vehículos
CREATE TABLE vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE,
    modelo VARCHAR(50),
    año INT,
    ultima_revision DATE
);

-- Tabla de Zonas
CREATE TABLE zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE
);

-- Tabla de Productos
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    origen VARCHAR(50),
    calidad VARCHAR(50),
    presentacion VARCHAR(50),
    volumen INT,
    costo DECIMAL(10, 2),
    precio_venta DECIMAL(10, 2)
);

-- Tabla de Ventas
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES clientes(id_cliente),
    id_empleado INT REFERENCES empleados(id_empleado),
    id_zona INT REFERENCES zonas(id_zona),
    fecha_venta DATE DEFAULT CURRENT_DATE,
    tipo_pago VARCHAR(20) CHECK (tipo_pago IN ('Contado', 'Semanal', 'Quincenal', 'Mensual')),
    estado VARCHAR(20) DEFAULT 'Pendiente'
);

-- Tabla de Detalles de Venta
CREATE TABLE detalles_venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INT REFERENCES ventas(id_venta),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2)
);

-- Tabla de Pagos
CREATE TABLE pagos (
    id_pago SERIAL PRIMARY KEY,
    id_venta INT REFERENCES ventas(id_venta),
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto DECIMAL(10, 2)
);

-- Tabla de Inventario
CREATE TABLE inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Gastos de Vehículos
CREATE TABLE gastos_vehiculos (
    id_gasto SERIAL PRIMARY KEY,
    id_vehiculo INT REFERENCES vehiculos(id_vehiculo),
    tipo_gasto VARCHAR(50),
    monto DECIMAL(10, 2),
    fecha DATE DEFAULT CURRENT_DATE
);

-- Tabla de Tracking GPS
CREATE TABLE tracking_gps (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INT REFERENCES vehiculos(id_vehiculo),
    latitud DECIMAL(9, 6),
    longitud DECIMAL(9, 6),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Proveedores
CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100)
);

-- Tabla de Compras a Proveedores
CREATE TABLE compras_proveedores (
    id_compra SERIAL PRIMARY KEY,
    id_proveedor INT REFERENCES proveedores(id_proveedor),
    fecha_compra DATE DEFAULT CURRENT_DATE,
    total DECIMAL(10, 2)
);

-- Tabla de Detalles de Compra
CREATE TABLE detalles_compra (
    id_detalle SERIAL PRIMARY KEY,
    id_compra INT REFERENCES compras_proveedores(id_compra),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2)
);
