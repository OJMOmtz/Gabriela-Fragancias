-- Modificación de las tablas de ubicación geográfica según INEC

-- Tabla Departamento (según Departamentos_Paraguay.dbf)
CREATE TABLE gf.departamento (
    id_departamento SERIAL PRIMARY KEY,
    dpto CHAR(2) NOT NULL UNIQUE,              -- DPTO: código oficial del departamento
    dpto_desc VARCHAR(100) NOT NULL,           -- DPTO_DESC: nombre oficial del departamento
    geometria GEOGRAPHY(MULTIPOLYGON, 4326),   -- geometría espacial del departamento
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo'
);

-- Tabla Distrito (según Distritos_Paraguay.dbf)
CREATE TABLE gf.distrito (
    id_distrito SERIAL PRIMARY KEY,
    objectid INTEGER,                          -- OBJECTID_1: identificador único original
    dpto CHAR(2) NOT NULL,                     -- DPTO: código del departamento
    distrito CHAR(2) NOT NULL,                 -- DISTRITO: código del distrito
    dpto_desc VARCHAR(100) NOT NULL,           -- DPTO_DESC: nombre del departamento
    dist_desc VARCHAR(100) NOT NULL,           -- DIST_DESC: nombre del distrito
    clave CHAR(4) NOT NULL UNIQUE,             -- CLAVE: código único combinado (DPTO+DISTRITO)
    geometria GEOGRAPHY(MULTIPOLYGON, 4326),   -- geometría espacial del distrito
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo',
    FOREIGN KEY (dpto) REFERENCES gf.departamento(dpto),
    CONSTRAINT distrito_clave_check CHECK (clave = dpto || distrito)
);

-- Tabla Barrio_Localidad (según Barrios_Localidades_Paraguay.dbf)
CREATE TABLE gf.barrio_localidad (
    id_barrio_localidad SERIAL PRIMARY KEY,
    dpto CHAR(2) NOT NULL,                     -- DPTO: código del departamento
    distrito CHAR(2) NOT NULL,                 -- DISTRITO: código del distrito
    dpto_desc VARCHAR(100) NOT NULL,           -- DPTO_DESC: nombre del departamento
    dist_desc VARCHAR(100) NOT NULL,           -- DIST_DESC: nombre del distrito
    area CHAR(1) NOT NULL,                     -- AREA: clasificación del área
    bar_loc CHAR(3) NOT NULL,                  -- BAR_LOC: código del barrio/localidad
    barlo_desc VARCHAR(100) NOT NULL,          -- BARLO_DESC: nombre del barrio/localidad
    clave CHAR(7) NOT NULL UNIQUE,             -- CLAVE: código único (DPTO+DISTRITO+BAR_LOC)
    geometria GEOGRAPHY(MULTIPOLYGON, 4326),   -- geometría espacial del barrio
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado gf.estado_registro DEFAULT 'activo',
    FOREIGN KEY (dpto, distrito) REFERENCES gf.distrito(dpto, distrito),
    CONSTRAINT barrio_clave_check CHECK (clave = dpto || distrito || bar_loc)
);

-- Modificación de la tabla persona para usar los nuevos códigos
ALTER TABLE gf.persona
    ADD COLUMN dpto CHAR(2),
    ADD COLUMN distrito CHAR(2),
    ADD COLUMN bar_loc CHAR(3),
    ADD FOREIGN KEY (dpto, distrito, bar_loc) 
        REFERENCES gf.barrio_localidad(dpto, distrito, bar_loc);

-- Índices para optimizar búsquedas geográficas
CREATE INDEX idx_departamento_geometria ON gf.departamento USING GIST (geometria);
CREATE INDEX idx_distrito_geometria ON gf.distrito USING GIST (geometria);
CREATE INDEX idx_barrio_geometria ON gf.barrio_localidad USING GIST (geometria);

-- Índices para búsquedas por código
CREATE INDEX idx_distrito_clave ON gf.distrito(clave);
CREATE INDEX idx_barrio_clave ON gf.barrio_localidad(clave);

-- Función para obtener la ubicación completa
CREATE OR REPLACE FUNCTION gf.obtener_ubicacion_completa(
    p_dpto CHAR(2),
    p_distrito CHAR(2),
    p_bar_loc CHAR(3)
)
RETURNS TABLE (
    departamento VARCHAR(100),
    distrito VARCHAR(100),
    barrio_localidad VARCHAR(100),
    area CHAR(1)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        b.dpto_desc,
        b.dist_desc,
        b.barlo_desc,
        b.area
    FROM gf.barrio_localidad b
    WHERE b.dpto = p_dpto
        AND b.distrito = p_distrito
        AND b.bar_loc = p_bar_loc;
END;
$$ LANGUAGE plpgsql;

-- Función para encontrar la ubicación por coordenada
CREATE OR REPLACE FUNCTION gf.obtener_ubicacion_por_punto(
    latitud DOUBLE PRECISION,
    longitud DOUBLE PRECISION
)
RETURNS TABLE (
    dpto CHAR(2),
    distrito CHAR(2),
    bar_loc CHAR(3),
    dpto_desc VARCHAR(100),
    dist_desc VARCHAR(100),
    barlo_desc VARCHAR(100)
) AS $$
DECLARE
    punto GEOGRAPHY;
BEGIN
    punto := ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)::GEOGRAPHY;
    
    RETURN QUERY
    SELECT 
        b.dpto,
        b.distrito,
        b.bar_loc,
        b.dpto_desc,
        b.dist_desc,
        b.barlo_desc
    FROM gf.barrio_localidad b
    WHERE ST_Contains(b.geometria::geometry, punto::geometry)
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;
