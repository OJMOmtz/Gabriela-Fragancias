--Tabla Cédulas
CREATE TABLE gf.cedulas (
    numero_cedula VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    sexo CHAR(1),
    direccion TEXT,
	id_barrio INTEGER REFERENCES gf.barrios_localidades(id_barrio),
	id_distrito INTEGER REFERENCES gf.distritos(id_distrito),
	id_dpto INTEGER REFERENCES gf.departamentos(id_dpto),
	id_via INTEGER REFERENCES gf.vias(id_via),
	id_prefijo INTEGER REFERENCES gf.prefijos(id_prefijo),
    lugar_nacimiento VARCHAR(100),
    fecha_defuncion DATE,
    email VARCHAR(100),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla Cédulas
CREATE TABLE gf.cedulas (
    numero_cedula VARCHAR(20) UNIQUE NOT NULL, --(debe ser la primary key)
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
	sexo CHAR(1),
    direccion TEXT,
	lugar_nacimiento VARCHAR(100),
    telefono VARCHAR(20),
    fecha_defuncion DATE,
    email VARCHAR(100),
    id_ruc INTEGER REFERENCES ruc(ruc_id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla Cédulas
CREATE TABLE Cedulas (
    id_cedula SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    sexo CHAR(1),  -- M: Masculino, F: Femenino
    fecha_nacimiento DATE,
    lugar_nacimiento VARCHAR(100),
    fecha_registro DATE,
    fuente VARCHAR(50)  -- 'poli01', 'regciv', 'regciv_ext'
);

--Tabla Cédulas
CREATE TABLE Cedulas (
    id_cedula SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    sexo CHAR(1),  -- M: Masculino, F: Femenino
    fecha_nacimiento DATE,
    lugar_nacimiento VARCHAR(100),
    fecha_registro DATE,
    fuente VARCHAR(50)  -- 'poli01', 'regciv', 'regciv_ext'
);

-- Tabla Cédula
CREATE TABLE Cedula (
    id_cedula SERIAL PRIMARY KEY,
    numero_ci VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT NOT NULL
);

--Tabla Cédulas
CREATE TABLE cedulas (
    numero_ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT NOT NULL
);

-- Tabla Cédula
CREATE TABLE Cedula (
    numero_ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT NOT NULL
);



