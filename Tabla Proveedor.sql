-- Tabla Proveedor
CREATE TABLE Proveedor (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nit VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT
);

-- Tabla de Proveedores
CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    direccion TEXT, CHARACTER SET utf8mb4;
    telefono VARCHAR(20),
    email VARCHAR(100) CHARACTER SET utf8mb4;
);

-- Tabla de Compras a Proveedores
CREATE TABLE compras_proveedores (
    id_compra SERIAL PRIMARY KEY,
    id_proveedor INT REFERENCES proveedores(id_proveedor),
    fecha_compra DATE DEFAULT CURRENT_DATE,
    total DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Detalles de Compra
CREATE TABLE detalles_compra (
    id_detalle SERIAL PRIMARY KEY,
    id_compra INT REFERENCES compras_proveedores(id_compra),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

