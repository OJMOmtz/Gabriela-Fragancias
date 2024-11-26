-- Tabla Empresa
CREATE TABLE Empresa (
    id_empresa SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    logo VARCHAR(255),
    descripcion TEXT
);

-- Empresa (Company) Table
CREATE TABLE gf.empresa (
    id_empresa UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    estado estado_registro DEFAULT 'activo'
);

--Tabla Empresa
CREATE TABLE gf.empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL
);

-- Tabla Empresa
CREATE TABLE Empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    -- Otros campos específicos para Empresa
);

-- Tabla Empresa
CREATE TABLE Empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL
	logotipo BYTEA;
);

-- Insertar los datos de la empresa con logotipo
INSERT INTO Empresa (ruc, razon_social, logotipo)
VALUES ('4974638-3', 'Gabriela Fragancias', pg_read_binary_file("D:\Gabriela Fragancias\Datos\Diseños\Gabriela Fragancias (logo torre).png"));

