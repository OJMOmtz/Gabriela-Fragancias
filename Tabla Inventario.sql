-- Tabla Inventario
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    ubicacion VARCHAR(50),
    id_presentacion INTEGER REFERENCES Presentacion(id_presentacion) ON DELETE CASCADE,
    stock INTEGER CHECK (stock >= 0)
);

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

--Tabla de Inventario (Maletines de Productos)
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL
);

-- Tabla de Inventario por Vendedor (relaciona productos con vendedores)
CREATE TABLE inventario_vendedores (
    id_inventario SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER NOT NULL
);

-- Tabla de Inventario por Vendedora
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL
);

-- Tabla Inventario_Maletines (para manejar los productos en los maletines de vendedoras)
CREATE TABLE Inventario_Maletines (
    id_inventario SERIAL PRIMARY KEY,
    id_maletin INTEGER REFERENCES Maletines(id_maletin),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--Tabla de Inventario (Maletines de Productos)
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL
);

-- Tabla Maletines (gestión de los maletines de las vendedoras)
CREATE TABLE Maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Maletines (gestión de los maletines de las vendedoras)
CREATE TABLE Maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INT REFERENCES Vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE
);

--Productos en Maletines: Para asociar productos con maletines.
    CREATE TABLE Productos_Maletin (
        id_maletin INT REFERENCES Maletines(id_maletin),
        id_producto INT REFERENCES Productos(id_producto),
        cantidad INT NOT NULL,
        PRIMARY KEY (id_maletin, id_producto)
    );
	
-- Tabla Maletines (gestión de los maletines de las vendedoras)
CREATE TABLE Maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Personas(id_persona),
    fecha_carga DATE DEFAULT CURRENT_DATE
);

--Productos en Maletines: Para asociar productos con maletines.
CREATE TABLE Productos_Maletin (
    id_maletin INT REFERENCES Maletines(id_maletin),
    id_producto INT REFERENCES Productos(id_producto),
    cantidad INT NOT NULL,
    PRIMARY KEY (id_maletin, id_producto)
);

--Tabla de Productos Vendidos
CREATE TABLE Productos_Vendidos (
    id_producto_vendido SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),  -- Relación con la tabla Tarjetas
    id_producto INTEGER REFERENCES Productos(id_producto),  -- Relación con la tabla Productos
    cantidad INTEGER CHECK (cantidad > 0),  -- Cantidad vendida de ese producto
    precio DECIMAL(10, 2)  -- Precio de venta del producto
);

--Tabla de Productos Vendidos
CREATE TABLE Productos_Vendidos (
    id_producto_vendido SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER CHECK (cantidad > 0),  -- Cantidad vendida
    precio DECIMAL(10, 2)  -- Precio de venta de cada producto
);

8. Triggers y Funciones
a. Trigger para Verificar Antecedentes Judiciales

Este trigger verificará automáticamente si una persona tiene antecedentes judiciales al ser registrada como cliente.

sql

CREATE OR REPLACE FUNCTION verificar_antecedentes_judiciales() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM Antecedentes_Judiciales WHERE numero_cedula = NEW.numero_cedula) THEN
        RAISE NOTICE 'La persona con cédula % tiene antecedentes judiciales', NEW.numero_cedula;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_verificar_antecedentes
BEFORE INSERT ON Personas
FOR EACH ROW
EXECUTE FUNCTION verificar_antecedentes_judiciales();