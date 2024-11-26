-- Tabla Ruta de Venta
CREATE TABLE RutaVenta (
   id_ruta SERIAL PRIMARY KEY,
   id_vehiculo INTEGER REFERENCES Vehiculo(id_vehiculo),
   fecha DATE
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

-- Tabla Rutas
CREATE TABLE rutas (
    id SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_vehiculo INTEGER REFERENCES vehiculos(id_vehiculo),
    fecha DATE NOT NULL,
    inicio_ruta GEOGRAPHY(POINT, 4326),
    fin_ruta GEOGRAPHY(POINT, 4326),
    distancia_km DECIMAL(10,2),
    tiempo_estimado INTEGER, -- minutos
    tiempo_real INTEGER,
    estado VARCHAR(20) CHECK (estado IN ('planificada', 'en_progreso', 'completada', 'cancelada')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Tabla Puntos Ruta
CREATE TABLE puntos_ruta (
    id SERIAL PRIMARY KEY,
    ruta_id INTEGER REFERENCES rutas(id),
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    orden INTEGER NOT NULL,
    hora_planificada TIME,
    hora_real TIME,
    ubicacion GEOGRAPHY(POINT, 4326),
    estado VARCHAR(20) CHECK (estado IN ('pendiente', 'visitado', 'no_visitado', 'reprogramado')),
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla Rutas (vendedores y geolocalización)
CREATE TABLE rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    nombre_ruta VARCHAR(100) NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    zona VARCHAR(50),
    id_vehiculo INTEGER REFERENCES vehiculos(id_vehiculo),
    coordenadas GEOGRAPHY(POINT, 4326) -- Integración con GIS para geolocalización
);

-- Tabla Rutas (para vendedores y manejo de geolocalización)
CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    nombre_ruta VARCHAR(100) NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    zona VARCHAR(50),
    id_vehiculo INTEGER REFERENCES Vehiculo(id_vehiculo),
	coordenadas GEOGRAPHY(POINT, 4326)  -- Integración con GIS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--Tabla de Rutas
CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_zona INTEGER REFERENCES Zonas(id_zona),
    fecha DATE DEFAULT CURRENT_DATE,
    coordenadas GEOGRAPHY(POINT, 4326)  -- Integración con GIS
);

-- Tabla Rutas (para vendedores y manejo de geolocalización)
CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    nombre_ruta VARCHAR(100) NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    coordenadas GEOGRAPHY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--Tabla de Rutas
CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Personas(id_persona),
    fecha DATE DEFAULT CURRENT_DATE,
    coordenadas GEOGRAPHY(LINESTRING, 4326),  -- Integración con GIS
    fuente VARCHAR(50)  -- JSON, GeoJSON, KML
);