CREATE DATABASE Gabriela_Fragancias;
-- Tabla Empresa
CREATE TABLE Empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    -- Otros campos específicos para Empresa
);

-- Tabla Usuario
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    -- Otros campos específicos para Usuario
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

-- Tabla de Clientes
CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
	tarjeta VARCHAR(7) UNIQUE NOT NULL,  -- Número de tarjeta obligatorio y valor reemplazado por otro cliente y zona
    id_persona INTEGER REFERENCES Persona(id_persona),
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    email VARCHAR(100),
    ruc VARCHAR(20) UNIQUE,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    tipo_pago VARCHAR(20) CHECK (tipo_pago IN ('SEM', 'QUIN', 'MENS')),  -- SEM (semanal), QUIN (quincenal), MENS (mensual)
    saldo DECIMAL(10, 2) DEFAULT 0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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

-- Tabla de Marcas
CREATE TABLE Marcas (
    ID_Marca INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Año_Fundacion INT,
    Sede VARCHAR(100),
    Sitio_Web VARCHAR(255),
    UNIQUE (Nombre)
);

-- Tabla de Perfumistas
CREATE TABLE Perfumistas (
    ID_Perfumista INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Nacionalidad VARCHAR(50),
    UNIQUE (Nombre, Apellido)
);

-- Tabla de Notas Olfativas
CREATE TABLE Notas_Olfativas (
    ID_Nota INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion TEXT,
    UNIQUE (Nombre)
);

-- Tabla de relación entre Productos y Notas Olfativas
CREATE TABLE Producto_Notas (
    ID_Producto INT,
    ID_Nota INT,
    Tipo_Nota ENUM('Alta', 'Media', 'Base'),
    PRIMARY KEY (ID_Producto, ID_Nota, Tipo_Nota),
    FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
    FOREIGN KEY (ID_Nota) REFERENCES Notas_Olfativas(ID_Nota)
);

-- Tabla de Productos (Perfumes)
CREATE TABLE Productos (
    ID_Producto INT PRIMARY KEY AUTO_INCREMENT,
    ID_Marca INT,
    Nombre VARCHAR(100) NOT NULL,
	Año_Lanzamiento INT,
    ID_Perfumista INT,
    Codigo_Barras VARCHAR(13) UNIQUE,
    Precio_Costo DECIMAL(10, 2),
    Precio_Venta DECIMAL(10, 2),
    Duracion_Horas INT,
    Stock INT DEFAULT 0,
    FOREIGN KEY (ID_Marca) REFERENCES Marcas(ID_Marca),
    FOREIGN KEY (ID_Perfumista) REFERENCES Perfumistas(ID_Perfumista)
);

-- Tabla Presentacion
CREATE TABLE Presentacion (
    id_presentacion SERIAL PRIMARY KEY,
    id_perfume INTEGER REFERENCES Perfume(id_perfume) ON DELETE CASCADE,
    codigo_barra VARCHAR(50) UNIQUE NOT NULL,
    tamano_ml INTEGER CHECK (tamano_ml > 0),
    imagen_url VARCHAR(255)
);

-- Tabla de Vendedores
CREATE TABLE Vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    id_zona INTEGER REFERENCES Zona(id_zona);
	nombre VARCHAR(100) NOT NULL,
    zona VARCHAR(50) NOT NULL,
    comision DECIMAL(10, 2) DEFAULT 50000
);

-- Tabla de Inventario por Vendedora
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL
);

-- Tabla Ventas
CREATE TABLE Ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_producto INTEGER REFERENCES Productos(id_producto),
    fecha DATE DEFAULT CURRENT_DATE,
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('Contado', 'Crédito')),  -- Contado, Crédito (SEM, QUIN, MENS)
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

-- Tabla Cédula
CREATE TABLE Cedula (
    numero_ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT NOT NULL
);

-- Tabla AntecedentesJudiciales
CREATE TABLE AntecedentesJudiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_ci VARCHAR(20) REFERENCES Cedula(numero_ci),
    causa_penal TEXT
);

-- Tabla de RUC
CREATE TABLE ruc (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    digito_verificador INT NOT NULL,
    razon_social VARCHAR(100) NOT NULL
);

-- Tabla Inventario_Maletines (para manejar los productos en los maletines de vendedoras)
CREATE TABLE Inventario_Maletines (
    id_inventario SERIAL PRIMARY KEY,
    id_maletin INTEGER REFERENCES Maletines(id_maletin),
    id_producto INTEGER REFERENCES Productos(id_producto),
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE,
	cantidad INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Productos de Maletines
CREATE TABLE productos_maletin (
    id_maletin INT REFERENCES maletines(id_maletin),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    PRIMARY KEY (id_maletin, id_producto)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
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

-- Tabla de Vehículos
CREATE TABLE vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE,
    marca VARCHAR(50), CHARACTER SET utf8mb4;
    modelo VARCHAR(50), CHARACTER SET utf8mb4;
    año INT,
	chassis VARCHAR(50), CHARACTER SET utf8mb4;
	motor VARCHAR(50), CHARACTER SET utf8mb4;
    ultima_revision DATE
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Gastos de Vehículos
CREATE TABLE gastos_vehiculos (
    id_gasto SERIAL PRIMARY KEY,
    id_vehiculo INT REFERENCES vehiculos(id_vehiculo),
    tipo_gasto VARCHAR(50) CHECK (tipo_gasto IN ('Combustible', 'Lubricantes', 'Gomería', 'Mecánica', 'Electricidad', 'Otro')); CHARACTER SET utf8mb4;
    monto DECIMAL(10, 2),
    fecha DATE DEFAULT CURRENT_DATE
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
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

-- Tabla de Tracking GPS
CREATE TABLE tracking_gps (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INT REFERENCES vehiculos(id_vehiculo),
	coordenadas GEOGRAPHY(Point, 4326);
    latitud DECIMAL(9, 6),
    longitud DECIMAL(9, 6),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Proveedores
CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    direccion TEXT, CHARACTER SET utf8mb4;
    telefono VARCHAR(20),
    email VARCHAR(100) CHARACTER SET utf8mb4;
);

-- Tabla de Compras a Proveedores
CREATE TABLE compras_proveedores (
    id_compra SERIAL PRIMARY KEY,
    id_proveedor INT REFERENCES proveedores(id_proveedor),
    fecha_compra DATE DEFAULT CURRENT_DATE,
    total DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Detalles de Compra
CREATE TABLE detalles_compra (
    id_detalle SERIAL PRIMARY KEY,
    id_compra INT REFERENCES compras_proveedores(id_compra),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Departamento
CREATE TABLE Departamento (
    id_departamento SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_departamento VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Municipio
CREATE TABLE Municipio (
    id_municipio SERIAL PRIMARY KEY,
    id_departamento INTEGER REFERENCES Departamento(id_departamento),
    nombre_municipio VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_municipio VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Zona
CREATE TABLE Zona (
    id_zona SERIAL PRIMARY KEY,
    id_municipio INTEGER REFERENCES Municipio(id_municipio),
    nombre_zona VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_zona VARCHAR(10) UNIQUE NOT NULL,
    geometria GEOGRAPHY(POLYGON, 4326)
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

-- Tabla de Equipos (para manejar lectores de códigos, impresoras, etc.)
CREATE TABLE equipos (
    id_equipo SERIAL PRIMARY KEY,
    tipo VARCHAR(50) CHECK (tipo IN ('Lector Código Barras', 'Impresora Ticket', 'Impresora Matricial', 'Impresora Láser', 'Impresora Inyección')),
    marca VARCHAR(50), CHARACTER SET utf8mb4;
    modelo VARCHAR(50), CHARACTER SET utf8mb4;
    fecha_adquisicion DATE
);

-- Índices para optimizar consultas frecuentes
CREATE INDEX idx_productos_marca ON Productos(ID_Marca);
CREATE INDEX idx_ventas_cliente ON Ventas(ID_Cliente);
CREATE INDEX idx_ventas_fecha ON Ventas(Fecha_Venta);
CREATE INDEX idx_inventario_producto ON Inventario(ID_Producto);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_clientes_cedula ON clientes(cedula);
CREATE INDEX idx_clientes_ruc ON clientes(ruc);
CREATE INDEX idx_productos_codigo_barras ON productos(codigo_barras);
CREATE INDEX idx_ventas_fecha ON ventas(fecha_venta);
CREATE INDEX idx_empleados_cargo ON empleados(cargo);
CREATE INDEX idx_cliente_cedula ON Cliente(cedula);

-- Trigger que ejecuta la función al insertar una venta
CREATE TRIGGER tg_actualizar_saldo
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_saldo_cliente();
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

CREATE OR REPLACE FUNCTION actualizar_saldo_cliente() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Clientes 
    SET saldo = saldo - NEW.total
    WHERE id_cliente = NEW.id_cliente;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que ejecuta la función al insertar una venta
CREATE TRIGGER tg_actualizar_stock
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock_producto();

-- Función para verificar antecedentes judiciales al insertar un cliente
CREATE OR REPLACE FUNCTION verificar_antecedentes_judiciales()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM AntecedentesJudiciales
        WHERE numero_ci = NEW.cedula
    ) THEN
        RAISE NOTICE 'El cliente con cédula % tiene antecedentes judiciales', NEW.cedula;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para llamar a la función al insertar un cliente
CREATE TRIGGER tg_verificar_antecedentes_judiciales
BEFORE INSERT ON Clientes
FOR EACH ROW
EXECUTE FUNCTION verificar_antecedentes_judiciales();

-- Trigger para actualizar el stock al vender
CREATE OR REPLACE FUNCTION actualizar_stock() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.cantidad > OLD.stock THEN
        RAISE EXCEPTION 'No hay suficiente stock';
    ELSE
        UPDATE Inventario SET stock = stock - NEW.cantidad WHERE id_presentacion = NEW.id_presentacion;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_stock
AFTER INSERT ON DetalleVenta
FOR EACH ROW EXECUTE FUNCTION actualizar_stock();

CREATE OR REPLACE FUNCTION actualizar_saldo_cliente() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Clientes 
    SET saldo = saldo - NEW.total
    WHERE id_cliente = NEW.id_cliente;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Vistas para reportes comunes
CREATE VIEW VW_Ventas_Por_Cliente AS
SELECT 
    c.ID_Cliente, 
    c.Nombre, 
    c.Apellido, 
    COUNT(v.ID_Venta) AS Total_Ventas, 
    SUM(v.Total) AS Monto_Total
FROM 
    Clientes c
LEFT JOIN 
    Ventas v ON c.ID_Cliente = v.ID_Cliente
GROUP BY 
    c.ID_Cliente;

CREATE VIEW VW_Stock_Productos AS
SELECT 
    p.ID_Producto, 
    p.Nombre, 
    m.Nombre AS Marca, 
    p.Stock, 
    p.Precio_Venta
FROM 
    Productos p
JOIN 
    Marcas m ON p.ID_Marca = m.ID_Marca;

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