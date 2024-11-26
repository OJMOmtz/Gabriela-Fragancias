-- Crear la tabla Empresa con logotipo
CREATE TABLE Empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    logo BYTEA  -- Columna para almacenar el logotipo
);

-- Tabla Usuario
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL
);

-- Tabla Personas
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
    fecha_defuncion DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla AntecedentesJudiciales (para verificar los antecedentes de los clientes)
CREATE TABLE AntecedentesJudiciales (
    id_antecedente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) REFERENCES Personas(cedula),
    causa_penal TEXT,
    cidcap INT,
    causa TEXT
);

-- Tabla Clientes
CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES Personas(id_persona),
    tarjeta VARCHAR(7) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    email VARCHAR(100),
    ruc VARCHAR(20) UNIQUE,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    tipo_pago VARCHAR(20) CHECK (tipo_pago IN ('SEM', 'QUIN', 'MENS')),
    saldo DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Productos
CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio_contado DECIMAL(10, 2) NOT NULL,
    precio_credito DECIMAL(10, 2) NOT NULL,
    stock INTEGER NOT NULL,
    descripcion TEXT,
    presentacion VARCHAR(50),
    volumen INT CHECK (volumen BETWEEN 5 AND 200),
    es_kit BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Ventas
CREATE TABLE Ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_producto INTEGER REFERENCES Productos(id_producto),
    fecha DATE DEFAULT CURRENT_DATE,
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('Contado', 'Crédito')),
    total DECIMAL(10, 2) NOT NULL,
    saldo DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Pagos
CREATE TABLE Pagos (
    id_pago SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_venta INTEGER REFERENCES Ventas(id_venta),
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto DECIMAL(10, 2) NOT NULL,
    metodo_pago VARCHAR(20) CHECK (metodo_pago IN ('Efectivo', 'Tarjeta', 'Transferencia')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Vendedores
CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    id_zona INTEGER REFERENCES Zonas(id_zona),
    nombre VARCHAR(100) NOT NULL,
    comision DECIMAL(10, 2) DEFAULT 50000
);

-- Tabla de Liquidaciones
CREATE TABLE liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_vendedor INT REFERENCES vendedores(id_vendedor),
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas DECIMAL(10, 2),
    comision DECIMAL(10, 2),
    total_pagar DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Maletines
CREATE TABLE Maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Vehículos
CREATE TABLE Vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    id_marca INTEGER REFERENCES Marcas_vehículos(id_marca),
    modelo VARCHAR(50),
    año INT,
    chasis VARCHAR(50),
    id_color INTEGER REFERENCES Colores(id_color),
    id_nacionalidad INTEGER REFERENCES Nacionalidades(id_nacionalidad),
    motor VARCHAR(50),
    ultima_revision DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla Colores:
CREATE TABLE Colores (
    id_color SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla Marcas Vehículos:
CREATE TABLE Marcas_vehículos (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla Nacionalidades:
CREATE TABLE Nacionalidades (
    id_nacionalidad SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Rutas
CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    nombre_ruta VARCHAR(100) NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    zona VARCHAR(50),
    id_vehiculo INTEGER REFERENCES Vehiculos(id_vehiculo),
    coordenadas GEOGRAPHY(POINT, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Tracking GPS
CREATE TABLE Tracking_GPS (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INTEGER REFERENCES Vehiculos(id_vehiculo),
    coordenadas GEOGRAPHY(POINT, 4326),
    latitud DECIMAL(9,6),
    longitud DECIMAL(9,6),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Departamento
CREATE TABLE Departamentos (
    id_departamento SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL,
    codigo_departamento VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Municipio
CREATE TABLE Municipios (
    id_municipio SERIAL PRIMARY KEY,
    id_departamento INTEGER REFERENCES Departamentos(id_departamento),
    nombre_municipio VARCHAR(100) NOT NULL,
    codigo_municipio VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Zonas o Ciudades
CREATE TABLE Zonas (
    id_zona SERIAL PRIMARY KEY,
    id_municipio INTEGER REFERENCES Municipios(id_municipio),
    nombre_zona VARCHAR(100) NOT NULL,
    codigo_zona VARCHAR(10) UNIQUE NOT NULL,
    geometria GEOGRAPHY(POLYGON, 4326)
);

-- Función para registrar ubicaciones GPS
CREATE OR REPLACE FUNCTION registrar_gps()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Tracking_GPS (id_vehiculo, coordenadas, latitud, longitud)
    VALUES (NEW.id_vehiculo, ST_SetSRID(ST_MakePoint(NEW.longitud, NEW.latitud), 4326), NEW.latitud, NEW.longitud);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que se ejecuta tras registrar una ubicación GPS
CREATE TRIGGER tg_registrar_gps
AFTER INSERT ON Tracking_GPS
FOR EACH ROW
EXECUTE FUNCTION registrar_gps();

-- Trigger para actualizar la comisión de las vendedoras tras una venta
CREATE OR REPLACE FUNCTION actualizar_comision_vendedora() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Liquidaciones 
    SET total_ventas = total_ventas + NEW.total,
        comision = comision + (50000 * NEW.cantidad)  -- Comisión por producto
    WHERE id_vendedor = NEW.id_vendedor;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_comision
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_comision_vendedora();

-- Trigger para actualizar el saldo de los clientes tras una venta
CREATE OR REPLACE FUNCTION actualizar_saldo_cliente() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Clientes 
    SET saldo = saldo - NEW.total
    WHERE id_cliente = NEW.id_cliente;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_saldo
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_saldo_cliente();

-- Trigger para actualizar el stock de productos después de una venta
CREATE OR REPLACE FUNCTION actualizar_stock_producto() 
RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.cantidad > (SELECT stock FROM Productos WHERE id_producto = NEW.id_producto)) THEN
        RAISE EXCEPTION 'No hay suficiente stock para este producto';
    ELSE
        UPDATE Productos 
        SET stock = stock - NEW.cantidad 
        WHERE id_producto = NEW.id_producto;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql

-- Función para registrar ubicaciones GPS
CREATE OR REPLACE FUNCTION registrar_gps()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Tracking_GPS (id_vehiculo, coordenadas, latitud, longitud)
    VALUES (NEW.id_vehiculo, ST_SetSRID(ST_MakePoint(NEW.longitud, NEW.latitud), 4326), NEW.latitud, NEW.longitud);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que se ejecuta tras registrar una ubicación GPS
CREATE TRIGGER tg_registrar_gps
AFTER INSERT ON Tracking_GPS
FOR EACH ROW
EXECUTE FUNCTION registrar_gps();

-- Trigger para actualizar la comisión de las vendedoras tras una venta
CREATE OR REPLACE FUNCTION actualizar_comision_vendedora() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Liquidaciones 
    SET total_ventas = total_ventas + NEW.total,
        comision = comision + (50000 * NEW.cantidad)  -- Comisión por producto
    WHERE id_vendedor = NEW.id_vendedor;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_comision
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_comision_vendedora();

-- Trigger para actualizar el saldo de los clientes tras una venta
CREATE OR REPLACE FUNCTION actualizar_saldo_cliente() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Clientes 
    SET saldo = saldo - NEW.total
    WHERE id_cliente = NEW.id_cliente;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_saldo
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_saldo_cliente();

-- Trigger para actualizar el stock de productos después de una venta
CREATE OR REPLACE FUNCTION actualizar_stock_producto() 
RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.cantidad > (SELECT stock FROM Productos WHERE id_producto = NEW.id_producto)) THEN
        RAISE EXCEPTION 'No hay suficiente stock para este producto';
    ELSE
        UPDATE Productos 
        SET stock = stock - NEW.cantidad 
        WHERE id_producto = NEW.id_producto;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_stock
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock_producto();

-- Trigger para verificar si un cliente tiene antecedentes judiciales
CREATE OR REPLACE FUNCTION verificar_antecedentes() 
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM AntecedentesJudiciales WHERE cedula = NEW.cedula) THEN
        RAISE NOTICE 'El cliente con cédula % tiene antecedentes judiciales', NEW.cedula;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_verificar_antecedentes
BEFORE INSERT ON Clientes
FOR EACH ROW
EXECUTE FUNCTION verificar_antecedentes();

-- Trigger para alerta de defunción
CREATE OR REPLACE FUNCTION verificar_defuncion() 
RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.fecha_defuncion IS NOT NULL) THEN
        RAISE NOTICE 'La persona con cédula % ha sido marcada como fallecida.', NEW.cedula;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_verificar_defuncion
AFTER INSERT OR UPDATE ON Personas
FOR EACH ROW
EXECUTE FUNCTION verificar_defuncion();

-- Indices para optimizar consultas
CREATE INDEX idx_antecedentes_cedula ON AntecedentesJudiciales(cedula);
CREATE INDEX idx_clientes_tarjeta ON Clientes(tarjeta);
CREATE INDEX idx_inventario_maletines_producto ON Inventario_Maletines(id_maletin, id_producto);
CREATE INDEX idx_pagos_cliente ON Pagos(id_cliente);
CREATE INDEX idx_pagos_cliente_metodo ON Pagos(id_cliente, metodo_pago);
CREATE INDEX idx_pagos_venta ON Pagos(id_venta);
CREATE INDEX idx_productos_codigo_barras ON Productos(codigo_barras);
CREATE INDEX idx_rutas_vendedor_fecha ON Rutas(id_vendedor, fecha);
CREATE INDEX idx_vehiculos_motor_chasis_placa ON Vehiculos(numero_motor, numero_chasis, placa);
CREATE INDEX idx_ventas_cliente ON Ventas(id_cliente);
CREATE INDEX idx_ventas_producto ON Ventas(id_producto);
# da este ERROR:  error de sintaxis en o cerca de «ON»
LINE 17: ...   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE ...
                                                              ^ 

SQL state: 42601
Character: 584

-- Crear la tabla Empresa con logotipo
CREATE TABLE Empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    logo BYTEA  -- Columna para almacenar el logotipo
);

-- Tabla Personas
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
    fecha_defuncion DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla AntecedentesJudiciales (para verificar los antecedentes de los clientes)
CREATE TABLE AntecedentesJudiciales (
    id_antecedente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) REFERENCES Personas(cedula),
    causa_penal TEXT,
    cidcap INT,
    causa TEXT
);

-- Tabla Clientes
CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES Personas(id_persona),
    tarjeta VARCHAR(7) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    email VARCHAR(100),
    ruc VARCHAR(20) UNIQUE,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    tipo_pago VARCHAR(20) CHECK (tipo_pago IN ('SEM', 'QUIN', 'MENS')),
    saldo DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Productos
CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio_contado DECIMAL(10, 2) NOT NULL,
    precio_credito DECIMAL(10, 2) NOT NULL,
    stock INTEGER NOT NULL,
    descripcion TEXT,
    presentacion VARCHAR(50),
    volumen INT CHECK (volumen BETWEEN 5 AND 200),
    es_kit BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Ventas
CREATE TABLE Ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_producto INTEGER REFERENCES Productos(id_producto),
    fecha DATE DEFAULT CURRENT_DATE,
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('Contado', 'Crédito')),
    total DECIMAL(10, 2) NOT NULL,
    saldo DECIMAL(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Pagos
CREATE TABLE Pagos (
    id_pago SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_venta INTEGER REFERENCES Ventas(id_venta),
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto DECIMAL(10, 2) NOT NULL,
    metodo_pago VARCHAR(20) CHECK (metodo_pago IN ('Efectivo', 'Tarjeta', 'Transferencia')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Vendedores
CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    id_zona INTEGER REFERENCES Zonas(id_zona),
    nombre VARCHAR(100) NOT NULL,
    comision DECIMAL(10, 2) DEFAULT 50000
);

-- Tabla de Liquidaciones
CREATE TABLE liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_vendedor INT REFERENCES vendedores(id_vendedor),
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas DECIMAL(10, 2),
    comision DECIMAL(10, 2),
    total_pagar DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Maletines
CREATE TABLE Maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Vehículos
CREATE TABLE Vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    id_marca INTEGER REFERENCES Marcas_vehículos(id_marca),
    modelo VARCHAR(50),
    año INT,
    chasis VARCHAR(50),
    id_color INTEGER REFERENCES Colores(id_color),
    id_nacionalidad INTEGER REFERENCES Nacionalidades(id_nacionalidad),
    motor VARCHAR(50),
    ultima_revision DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla Colores:
CREATE TABLE Colores (
    id_color SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla Marcas Vehículos:
CREATE TABLE Marcas_vehículos (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabla Nacionalidades:
CREATE TABLE Nacionalidades (
    id_nacionalidad SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Rutas
CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    nombre_ruta VARCHAR(100) NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    zona VARCHAR(50),
    id_vehiculo INTEGER REFERENCES Vehiculos(id_vehiculo),
    coordenadas GEOGRAPHY(POINT, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Tracking GPS
CREATE TABLE Tracking_GPS (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INTEGER REFERENCES Vehiculos(id_vehiculo),
    coordenadas GEOGRAPHY(POINT, 4326),
    latitud DECIMAL(9,6),
    longitud DECIMAL(9,6),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Departamento
CREATE TABLE Departamentos (
    id_departamento SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL,
    codigo_departamento VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Municipio
CREATE TABLE Municipios (
    id_municipio SERIAL PRIMARY KEY,
    id_departamento INTEGER REFERENCES Departamentos(id_departamento),
    nombre_municipio VARCHAR(100) NOT NULL,
    codigo_municipio VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Zonas o Ciudades
CREATE TABLE Zonas (
    id_zona SERIAL PRIMARY KEY,
    id_municipio INTEGER REFERENCES Municipios(id_municipio),
    nombre_zona VARCHAR(100) NOT NULL,
    codigo_zona VARCHAR(10) UNIQUE NOT NULL,
    geometria GEOGRAPHY(POLYGON, 4326)
);

