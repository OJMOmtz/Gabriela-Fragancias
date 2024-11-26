--Creación de la Base de Datos
CREATE DATABASE Gabriela_Fragancias;

--Tabla Zonas
CREATE TABLE Zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre_zona VARCHAR(100) NOT NULL UNIQUE
);

--Tabla Clientes
CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    email VARCHAR(100),
    ruc VARCHAR(20) UNIQUE,
    fecha_registro DATE DEFAULT CURRENT_DATE
);

--Tabla Vendedores
CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    zona VARCHAR(50) NOT NULL,
    comision DECIMAL(10, 2) DEFAULT 50000
);

--Tabla Tarjetas
CREATE TABLE Tarjetas (
    id_tarjeta SERIAL PRIMARY KEY,
    numero_tarjeta VARCHAR(7) NOT NULL,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_zona INTEGER REFERENCES Zonas(id_zona),
    total_gs DECIMAL(10, 2) NOT NULL,
    saldo DECIMAL(10, 2) DEFAULT 0,
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('SEM', 'QUIN', 'MENS')),
    estado VARCHAR(20) CHECK (estado IN ('activa', 'cancelada')) DEFAULT 'activa',
    fecha_emision DATE DEFAULT CURRENT_DATE,
    id_tarjeta_anterior INTEGER REFERENCES Tarjetas(id_tarjeta)
);

--Tabla de Productos
CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_barras VARCHAR(13) UNIQUE NOT NULL,
    precio_costo DECIMAL(10, 2),
    precio_venta DECIMAL(10, 2),
    stock INTEGER DEFAULT 0,
    descripcion TEXT
);

--Tabla Productos Vendidos
CREATE TABLE Productos_Vendidos (
    id_producto_vendido SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER CHECK (cantidad > 0),
    precio DECIMAL(10, 2)
);

--Tabla Pagos
CREATE TABLE Pagos (
    id_pago SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto DECIMAL(10, 2) NOT NULL,
    saldo_restante DECIMAL(10, 2) NOT NULL,
    entrega_inicial BOOLEAN DEFAULT FALSE,
    recargo BOOLEAN DEFAULT FALSE
);

--Tabla Antecedentes Judiciales
CREATE TABLE Antecedentes_Judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) REFERENCES Clientes(cedula),
    causa_penal TEXT
);

--Tabla de Inventario (Maletines de Productos)
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL
);

--Tabla de Rutas
CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_zona INTEGER REFERENCES Zonas(id_zona),
    fecha DATE DEFAULT CURRENT_DATE,
    coordenadas GEOGRAPHY(POINT, 4326)  -- Integración con GIS
);

--Triggers y Funciones
CREATE OR REPLACE FUNCTION actualizar_saldo_cliente() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Tarjetas 
    SET saldo = saldo - NEW.monto
    WHERE id_tarjeta = NEW.id_tarjeta;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--Trigger para actualizar saldo tras un pago:
CREATE TRIGGER tg_actualizar_saldo
AFTER INSERT ON Pagos
FOR EACH ROW
EXECUTE FUNCTION actualizar_saldo_cliente();

--Función para actualizar inventario tras una venta:
CREATE OR REPLACE FUNCTION actualizar_inventario() 
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.cantidad > (SELECT stock FROM Productos WHERE id_producto = NEW.id_producto) THEN
        RAISE EXCEPTION 'No hay suficiente stock para este producto';
    ELSE
        UPDATE Productos 
        SET stock = stock - NEW.cantidad 
        WHERE id_producto = NEW.id_producto;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--Trigger para actualizar inventario tras una venta:
CREATE TRIGGER tg_actualizar_inventario
AFTER INSERT ON Productos_Vendidos
FOR EACH ROW
EXECUTE FUNCTION actualizar_inventario();

--Vista para Reportes de Ventas
CREATE VIEW VW_Ventas_Por_Cliente AS
SELECT 
    c.id_cliente, 
    c.nombre, 
    c.apellido, 
    COUNT(v.id_tarjeta) AS total_ventas, 
    SUM(v.total_gs) AS monto_total
FROM 
    Clientes c
JOIN 
    Tarjetas v ON c.id_cliente = v.id_cliente
GROUP BY 
    c.id_cliente;

--Optimización con Índices
CREATE INDEX idx_tarjetas_cliente ON Tarjetas(id_cliente);
CREATE INDEX idx_productos_codigo_barras ON Productos(codigo_barras);
CREATE INDEX idx_pagos_fecha ON Pagos(fecha_pago);
CREATE INDEX idx_rutas_vendedor_fecha ON Rutas(id_vendedor, fecha);
CREATE INDEX idx_pagos_cliente_metodo ON Pagos(id_cliente, metodo_pago);
CREATE INDEX idx_antecedentes_cedula ON AntecedentesJudiciales(cedula);
CREATE INDEX idx_inventario_maletines_producto ON Inventario_Maletines(id_maletin, id_producto);
CREATE INDEX idx_vehiculos_motor_chasis_placa ON Vehiculos(numero_motor, numero_chasis, placa);

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

-- Tabla Clientes
CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES Personas(id_persona),
    tarjeta VARCHAR(7) UNIQUE NOT NULL,  -- Número de tarjeta obligatorio y único
    saldo DECIMAL(10, 2) DEFAULT 0,
    tipo_pago VARCHAR(20) CHECK (tipo_pago IN ('SEM', 'QUIN', 'MENS')),
    fecha_registro DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Marcas
CREATE TABLE Marcas (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    año_fundacion INT
);

-- Tabla Productos
CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    id_marca INTEGER REFERENCES Marcas(id_marca),
    precio_contado DECIMAL(10, 2) NOT NULL,
    precio_credito DECIMAL(10, 2) NOT NULL,
    stock INTEGER NOT NULL,
    descripcion TEXT,
    presentacion VARCHAR(50),
    volumen INT CHECK (volumen BETWEEN 5 AND 200),
    es_kit BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

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

-- Tabla Pagos
CREATE TABLE Pagos (
    id_pago SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_venta INTEGER REFERENCES Ventas(id_venta),
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto DECIMAL(10, 2) NOT NULL,
    metodo_pago VARCHAR(20) CHECK (metodo_pago IN ('Efectivo', 'Tarjeta', 'Transferencia')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Detalles de Venta
CREATE TABLE Detalles_Venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES Ventas(id_venta) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Vehiculos
CREATE TABLE Vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,  -- Número de placa obligatorio y único
    marca VARCHAR(50),
    modelo VARCHAR(50),
    año INT,
    numero_motor VARCHAR(50) UNIQUE,  -- Número de motor obligatorio y único
    numero_chasis VARCHAR(50) UNIQUE, -- Número de chasis obligatorio y único
    fecha_revision DATE,  -- Fecha de última revisión técnica
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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

-- Tabla Inventario_Maletines (para manejar los productos en los maletines de vendedoras)
CREATE TABLE Inventario_Maletines (
    id_inventario SERIAL PRIMARY KEY,
    id_maletin INTEGER REFERENCES Maletines(id_maletin),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Maletines (gestión de los maletines de las vendedoras)
CREATE TABLE Maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla AntecedentesJudiciales (para verificar los antecedentes de los clientes)
CREATE TABLE AntecedentesJudiciales (
    id_antecedente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) REFERENCES Personas(cedula),
    causa_penal TEXT
);

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

-- Índices faltantes para optimización de consultas
CREATE INDEX idx_rutas_vendedor_fecha ON Rutas(id_vendedor, fecha);
CREATE INDEX idx_pagos_cliente_metodo ON Pagos(id_cliente, metodo_pago);
CREATE INDEX idx_antecedentes_cedula ON AntecedentesJudiciales(cedula);
CREATE INDEX idx_inventario_maletines_producto ON Inventario_Maletines(id_maletin, id_producto);
CREATE INDEX idx_vehiculos_motor_chasis_placa ON Vehiculos(numero_motor, numero_chasis, placa);


-- Relaciones Clave

Clientes y Personas: La tabla personas puede utilizarse para almacenar información adicional sobre las personas, como sus cédulas y contactos. Los clientes pueden estar relacionados con personas si hay un esquema más complejo.
Rutas y Vehículos: Los vendedores pueden estar asignados a rutas, y cada ruta puede tener asociado un vehículo para facilitar la movilidad y el seguimiento GPS.
Antecedentes Judiciales: Se verifica si los clientes tienen antecedentes judiciales antes de ser ingresados, lo que podría afectar las decisiones comerciales.
Geolocalización: Las rutas están asociadas con zonas geográficas (ciudades, municipios, departamentos) para un mejor control territorial.
A ESTA TABLA QUISIERA INGRESAR UNA COLUMNA PARA LA IMAGEN DEL LOGOTIPO
Y UNA SENTENCIA SQL
CON el RUC 4974638-3
razón social Gabriela Fragancias 

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



-- Consulta de Clientes con Antecedentes Judiciales

SELECT p.nombre, p.apellido, a.causa_penal
FROM personas p
INNER JOIN antecedentes_judiciales a ON p.cedula = a.numero_ci;

-- Consulta de Vehículos Asignados a Vendedores

SELECT v.nombre, v.apellido, veh.marca, veh.modelo, veh.placa
FROM vendedores v
INNER JOIN rutas r ON v.id_vendedor = r.id_vendedor
INNER JOIN vehiculos veh ON r.id_vehiculo = veh.id_vehiculo;

-- Consulta de Geolocalización de Vehículos

SELECT veh.placa, t.latitud, t.longitud, t.fecha_hora
FROM vehiculos veh
INNER JOIN tracking_gps t ON veh.id_vehiculo = t.id_vehiculo
ORDER BY t.fecha_hora DESC;