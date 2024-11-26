--Tabla de Maletines
CREATE TABLE Maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INT REFERENCES Vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE
);

--Tabla de Productos en Maletines: Vincula productos con maletines, especificando la cantidad de productos asignados.
CREATE TABLE Productos_Maletin (
	id_maletin INT REFERENCES Maletines(id_maletin),
	id_producto INT REFERENCES Productos(id_producto),
	cantidad INT NOT NULL,
	PRIMARY KEY (id_maletin, id_producto)
);

--Tabla Maletines
CREATE TABLE maletines (
    id_maletin SERIAL PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    fecha_asignacion DATE DEFAULT CURRENT_DATE
);

-- Inventario de Maletines
CREATE TABLE inventario_maletines (
    id_inventario SERIAL PRIMARY KEY,
    id_maletin INTEGER REFERENCES maletines(id_maletin),
    id_producto INTEGER REFERENCES productos(id_producto),
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    cantidad INTEGER NOT NULL
);

-- Tabla Inventario_Maletines (para manejar los productos en los maletines de vendedoras)
CREATE TABLE Inventario_Maletines (
    id_inventario SERIAL PRIMARY KEY,
    id_maletin INTEGER REFERENCES Maletines(id_maletin),
    id_producto INTEGER REFERENCES Productos(id_producto),
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE,
	cantidad INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Productos de Maletines
CREATE TABLE productos_maletin (
    id_maletin INT REFERENCES maletines(id_maletin),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    PRIMARY KEY (id_maletin, id_producto)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Maletines
CREATE TABLE maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE
);

-- Tabla de Productos en Maletín
CREATE TABLE productos_maletin (
    id_maletin INTEGER REFERENCES maletines(id_maletin),
    id_presentacion INTEGER REFERENCES presentaciones(id_presentacion),
    cantidad INTEGER,
    PRIMARY KEY (id_maletin, id_presentacion)
);