-- Tabla de cédulas (referencia)
CREATE TABLE gf.cedulas (
    numero_cedula VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    sexo CHAR(1),
    direccion TEXT,
    id_barrio VARCHAR(3),
    id_distrito VARCHAR(2),
    id_dpto VARCHAR(2),
    zona VARCHAR(2),
    id_via VARCHAR(50),
    lugar_nacimiento VARCHAR(100),
    fecha_defuncion DATE,
    email VARCHAR(100)
);

-- Tabla de RUC
CREATE TABLE gf.ruc (
    numero_ruc VARCHAR(20) PRIMARY KEY,
    razon_social VARCHAR(200),
    direccion TEXT,
    telefono VARCHAR(20),
    estado VARCHAR(20)
);

-- Tabla de clientes modificada
CREATE TABLE gf.clientes (
    id_cliente SERIAL PRIMARY KEY,
    numero_tarjeta VARCHAR(10),  -- Número de tarjeta agregado aquí
    numero_cedula VARCHAR(20) REFERENCES gf.cedulas(numero_cedula),
    numero_ruc VARCHAR(20) REFERENCES gf.ruc(numero_ruc),
    -- Estos campos se llenarán automáticamente desde gf.cedulas
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    celular VARCHAR(20),
    barrio VARCHAR(100),
    calle VARCHAR(100),
    numero VARCHAR(20),
    local VARCHAR(255),
    cerca_de TEXT,
    domicilio_particular TEXT,
    estado VARCHAR(20) DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'moroso')),
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Trigger para auto-completar datos desde la tabla cédulas
CREATE OR REPLACE FUNCTION gf.autocompletar_datos_cedula()
RETURNS TRIGGER AS $$
BEGIN
    -- Si se ingresa un número de cédula, completar datos automáticamente
    IF NEW.numero_cedula IS NOT NULL THEN
        SELECT 
            nombre,
            apellido,
            direccion
        INTO 
            NEW.nombre,
            NEW.apellido,
            NEW.domicilio_particular
        FROM gf.cedulas
        WHERE numero_cedula = NEW.numero_cedula;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_autocompletar_cedula
BEFORE INSERT OR UPDATE ON gf.clientes
FOR EACH ROW
EXECUTE FUNCTION gf.autocompletar_datos_cedula();

-- Trigger para auto-completar datos desde RUC
CREATE OR REPLACE FUNCTION gf.autocompletar_datos_ruc()
RETURNS TRIGGER AS $$
BEGIN
    -- Si se ingresa un RUC, completar datos del negocio
    IF NEW.numero_ruc IS NOT NULL THEN
        SELECT 
            razon_social,
            direccion,
            telefono
        INTO 
            NEW.local,
            NEW.domicilio_particular,
            NEW.celular
        FROM gf.ruc
        WHERE numero_ruc = NEW.numero_ruc;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_autocompletar_ruc
BEFORE INSERT OR UPDATE ON gf.clientes
FOR EACH ROW
EXECUTE FUNCTION gf.autocompletar_datos_ruc();

-- Índices adicionales para optimizar búsquedas
CREATE INDEX idx_clientes_tarjeta ON gf.clientes(numero_tarjeta);
CREATE INDEX idx_clientes_cedula ON gf.clientes(numero_cedula);
CREATE INDEX idx_clientes_ruc ON gf.clientes(numero_ruc);

-- Vista para facilitar la consulta de datos completos del cliente
CREATE VIEW gf.vista_cliente_completo AS
SELECT 
    c.*,
    ced.fecha_nacimiento,
    ced.sexo,
    ced.lugar_nacimiento,
    r.razon_social,
    r.estado AS estado_ruc
FROM gf.clientes c
LEFT JOIN gf.cedulas ced ON c.numero_cedula = ced.numero_cedula
LEFT JOIN gf.ruc r ON c.numero_ruc = r.numero_ruc;
