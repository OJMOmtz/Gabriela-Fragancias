--Tabla Personas
CREATE TABLE personas (
    id_persona SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    zona VARCHAR(50),
    fecha_registro DATE DEFAULT CURRENT_DATE
);

-- Tabla Personas (con alerta de defunción)
CREATE TABLE Personas (
    id_persona SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT NOT NULL,
    departamento VARCHAR(100),
    distrito_municipio VARCHAR(100),
    barrio_localidad VARCHAR(100),
    zona VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    orden_captura INTEGER,
    causa TEXT,
    observacion TEXT,
    descripcion_estado TEXT,
    tipo_pol_mil VARCHAR(50),
    grado_pol_mil VARCHAR(50),	
    fecha_defuncion DATE,  -- Campo para gestionar defunciones
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Personas (con alerta de defunción)
CREATE TABLE Personas (
    id_persona SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    direccion TEXT,
    departamento VARCHAR(100),
    distrito_municipio VARCHAR(100),
    barrio_localidad VARCHAR(100),
    zona VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    fecha_defuncion DATE,  -- Campo para gestionar defunciones
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
);

--Tabla Personas
CREATE TABLE Personas (
    id_persona SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    email VARCHAR(100),
    ruc VARCHAR(20) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--Tabla Personas
CREATE TABLE Personas (
    id_persona SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    email VARCHAR(100),
    ruc VARCHAR(20) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--Tabla Personas
CREATE TABLE Personas_Cedulas (
    id_persona SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    sexo CHAR(1),  -- M: Masculino, F: Femenino
    fecha_nacimiento DATE,
    lugar_nacimiento VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    email VARCHAR(100),
    id_ruc INTEGER REFERENCES RUC(id_ruc),  -- Referencia a la tabla RUC
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

--Tabla Personas
CREATE TABLE Personas (
    id_persona SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    sexo CHAR(1),  -- M: Masculino, F: Femenino
    fecha_nacimiento DATE,
    lugar_nacimiento VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    email VARCHAR(100),
    id_ruc INTEGER REFERENCES RUC(id_ruc),  -- Referencia a la tabla RUC
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
