CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cedula VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    direccion TEXT,
    tipo_pago VARCHAR(20),
    saldo DECIMAL(10,2)
);

CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    codigo_barras VARCHAR(50) UNIQUE,
    precio_contado DECIMAL(10,2),
    precio_credito DECIMAL(10,2),
    stock INTEGER
);

CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    zona VARCHAR(50),
    comision DECIMAL(10,2)
);

CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    zona VARCHAR(50),
    fecha DATE,
    datos_geo GEOJSON
);

CREATE TABLE Ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_producto INTEGER REFERENCES Productos(id_producto),
    fecha DATE,
    forma_pago VARCHAR(20),
    total DECIMAL(10,2),
    saldo DECIMAL(10,2)
);

CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER
);
