-- Tabla de Vías Principales
CREATE TABLE gf.vias_principales (
    id_via SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    long_km_en NUMERIC(6),
    ruta_nro VARCHAR(2),
    ancho NUMERIC(2),
    tipo NUMERIC(2),
    long_mts NUMERIC(10)
);

-- Tabla de Vías
CREATE TABLE gf.vias (
    id_via SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    tipo NUMERIC(2),
    ancho NUMERIC(2),
    id_dpto INTEGER REFERENCES gf.departamentos(id_dpto)
);

-- Tabla de Locales de Salud
CREATE TABLE locales_salud (
    id_local_salud SERIAL PRIMARY KEY,
    id_dpto INTEGER REFERENCES gf.departamentos(id_dpto),
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
    nombre VARCHAR(50),
    ubicacion GEOGRAPHY(POINT, 4326)
);

-- Tabla de Locales Educativos
CREATE TABLE gf.locales_educativos (
    id_local_edu SERIAL PRIMARY KEY,
    id_dpto_id INTEGER REFERENCES gf.departamentos(id_dpto),
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
    nombre VARCHAR(56),
    ubicacion GEOGRAPHY(POINT, 4326)
);

-- Tabla de Locales Policiales
CREATE TABLE gf.locales_policiales (
    id_local_policial SERIAL PRIMARY KEY,
    id_dpto INTEGER REFERENCES gf.departamentos(id_dpto),
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
    nombre VARCHAR(51),
    ubicacion GEOGRAPHY(POINT, 4326)
);

-- Tabla de Comunidades Indígenas
CREATE TABLE gf.comunidades_indigenas (
    id_comunidad SERIAL PRIMARY KEY,
    id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
    area VARCHAR(1),
    bar_loc VARCHAR(3),
    barlo_desc VARCHAR(50),
    comunidad VARCHAR(4),
    aldea VARCHAR(2),
    com_desc VARCHAR(50),
    pueblo_etn VARCHAR(30),
    cod_pueblo VARCHAR(2),
    familia VARCHAR(20)
);

