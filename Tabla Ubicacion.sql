-- Tabla Ubicacion
CREATE TABLE Ubicacion (
    id_ubicacion SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedor(id_vendedor),
    fecha_hora TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    coordenadas GEOGRAPHY(POINT, 4326)
);

--Tabla de Geolocalización (GPS)
CREATE TABLE tracking_gps (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INTEGER REFERENCES vehiculos(id_vehiculo),
    coordenadas GEOGRAPHY(POINT, 4326), -- Para almacenar latitud y longitud
    latitud DECIMAL(9,6),
    longitud DECIMAL(9,6),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Tracking GPS
CREATE TABLE tracking_gps (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INT REFERENCES vehiculos(id_vehiculo),
	coordenadas GEOGRAPHY(Point, 4326);
    latitud DECIMAL(9, 6),
    longitud DECIMAL(9, 6),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Ubicacion
CREATE TABLE Ubicacion (
    id_ubicacion SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedor(id_vendedor),
    fecha_hora TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    coordenadas GEOGRAPHY(POINT, 4326)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

