CREATE DATABASE Gabriela_Fragancias;

-- Tabla Usuario
CREATE TABLE gf.usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Empresa
CREATE TABLE gf.empresa (
    id_empresa SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    logo VARCHAR(255),
    descripcion TEXT
);

-- Tabla Cédula
CREATE TABLE gf.cedula (
    numero_ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT NOT NULL,
	barrio TEXT NOT NULL,
	distrito TEXT NOT NULL,
	departamento TEXT NOT NULL,	
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla AntecedentesJudiciales
CREATE TABLE gf.antecedentes_judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_ci VARCHAR(20) REFERENCES gf.cedula(numero_ci),
    causa_penal TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Clientes
CREATE TABLE gf.clientes (
    id_cliente SERIAL PRIMARY KEY,
    tarjeta VARCHAR(5),
    cedula VARCHAR(20) UNIQUE,
    ruc VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion TEXT,
    direccion laboral TEXT,
    direccion particular TEXT,	
	barrio TEXT,
	distrito TEXT,
	departamento TEXT,	
    telefono VARCHAR(20),
    celular VARCHAR(20),	
    email VARCHAR(100),
    fecha_registro DATE DEFAULT CURRENT_DATE,
    total_pagar DECIMAL(50),
    tipo_pago VARCHAR(20),
    sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
    edad_grupo VARCHAR(20) CHECK (edad_grupo IN ('Niño', 'Púber', 'Adolescente', 'Joven', 'Adulto', 'Mayor')),
    afiliacion_politica VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL	
);

-- Tabla para manejar afiliaciones políticas (si es necesario)
CREATE TABLE gf.afiliaciones_politicas (
    id_afiliacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE
);

-- Tabla de Empleados
CREATE TABLE gf.empleados (
    id_empleado SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    zona VARCHAR(50),
    cargo VARCHAR(50) CHECK (cargo IN ('Vendedor', 'Cobrador', 'Chofer')),
    fecha_contratacion DATE,
    salario INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Zonas
CREATE TABLE gf.zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE
);

-- Tabla de Productos
CREATE TABLE gf.productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    id_marca INTEGER REFERENCES gf.marca(id_marca),
    descripcion TEXT,
    presentacion VARCHAR(50),
    volumen INT CHECK (volumen BETWEEN 5 AND 200),
    es_kit BOOLEAN DEFAULT FALSE,
    costo DECIMAL(10, 2),
    precio_venta_credito DECIMAL(10, 2),
    precio_venta_contado DECIMAL(10, 2),
    segmento VARCHAR(50),
    franja_etaria VARCHAR(50),
    ocasion VARCHAR(50),
    ano_lanzamiento INTEGER,
    origen VARCHAR(50),
    perfumero VARCHAR(100),
    notas_olfativas TEXT,
    notas_salida TEXT,
    notas_corazon TEXT,
    notas_fondo TEXT,
    intensidad VARCHAR(20),
    concentracion VARCHAR(20),
    duracion VARCHAR(50),
    estilo VARCHAR(50),
    imagen_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_clientes_cedula ON gf.clientes(cedula);
CREATE INDEX idx_clientes_ruc ON gf.clientes(ruc);
CREATE INDEX idx_productos_codigo_barras ON gf.productos(codigo_barras);

-- Tabla de Empleados
CREATE TABLE gf.empleados (
    id_empleado SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    apellido VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    telefono VARCHAR(20),
	id_zona INTEGER REFERENCES gf.zona(id_zona);
    cargo VARCHAR(50) CHECK (cargo IN ('Vendedor', 'Cobrador', 'Chofer')), CHARACTER SET utf8mb4;
    fecha_contratacion DATE,
    salario DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Departamento
CREATE TABLE gf.departamento (
    id_departamento SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_departamento VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Municipio
CREATE TABLE gf.municipio (
    id_municipio SERIAL PRIMARY KEY,
    id_departamento INTEGER REFERENCES gf.departamento(id_departamento),
    nombre_municipio VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_municipio VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Zona
CREATE TABLE gf.zona (
    id_zona SERIAL PRIMARY KEY,
    id_municipio INTEGER REFERENCES gf.municipio(id_municipio),
    nombre_zona VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_zona VARCHAR(10) UNIQUE NOT NULL,
    geometria GEOGRAPHY(POLYGON, 4326)
);

-- Tabla Ubicacion
CREATE TABLE gf.ubicacion (
    id_ubicacion SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES gf.vendedor(id_vendedor),
    fecha_hora TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    coordenadas GEOGRAPHY(POINT, 4326)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Productos
CREATE TABLE gf.productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE,
    nombre VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
	id_marca INTEGER REFERENCES gf.marca(id_marca),
	descripcion TEXT,  CHARACTER SET utf8mb4;
    presentacion VARCHAR(50),
    volumen INT CHECK (volumen BETWEEN 5 AND 200),
	es_kit BOOLEAN DEFAULT FALSE;
    costo DECIMAL(10, 2),
    precio_venta_credito DECIMAL(10, 2),
    precio_venta_contado DECIMAL(10, 2),
    segmento VARCHAR(50), CHARACTER SET utf8mb4;
    franja_etaria VARCHAR(50),
    ocasion VARCHAR(50), CHARACTER SET utf8mb4;
    ano_lanzamiento INTEGER,
	origen VARCHAR(50),
    perfumero VARCHAR(100), CHARACTER SET utf8mb4;
    notas_olfativas TEXT, CHARACTER SET utf8mb4;
    notas_salida TEXT, CHARACTER SET utf8mb4;
    notas_corazon TEXT, CHARACTER SET utf8mb4;
    notas_fondo TEXT, CHARACTER SET utf8mb4;
    intensidad VARCHAR(20), CHARACTER SET utf8mb4;
    concentracion VARCHAR(20),
    duracion VARCHAR(50), CHARACTER SET utf8mb4;
    estilo VARCHAR(50), CHARACTER SET utf8mb4;
    imagen_url VARCHAR(255)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Kits (para manejar kits con varios productos)
CREATE TABLE gf.kits (
    id_kit SERIAL PRIMARY KEY,
    id_producto INT REFERENCES gf.productos(id_producto),
    nombre VARCHAR(100) NOT NULL CHARACTER SET utf8mb4;
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

CREATE TABLE gf.productos_kit (
    id_kit INT REFERENCES gf.kits(id_kit),
    id_producto INT REFERENCES gf.productos(id_producto),
    cantidad INT,
    PRIMARY KEY (id_kit, id_producto)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Presentacion
CREATE TABLE gf.presentacion (
    id_presentacion SERIAL PRIMARY KEY,
    id_perfume INTEGER REFERENCES gf.perfume(id_perfume) ON DELETE CASCADE,
    codigo_barra VARCHAR(50) UNIQUE NOT NULL,
    tamano_ml INTEGER CHECK (tamano_ml > 0),
    imagen_url VARCHAR(255)
);

-- Tabla de Maletines de Vendedoras
CREATE TABLE gf.maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_empleado INT REFERENCES gf.empleados(id_empleado),
    codigo_barra VARCHAR(50) UNIQUE NOT NULL,	
    fecha_carga DATE DEFAULT CURRENT_DATE
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

CREATE TABLE gf.productos_maletin (
    id_maletin INT REFERENCES gf.maletines(id_maletin),
    id_producto INT REFERENCES gf.productos(id_producto),
    codigo_barra VARCHAR(50) UNIQUE NOT NULL,	
    cantidad INT,
    PRIMARY KEY (id_maletin, id_producto)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Liquidaciones
CREATE TABLE gf.liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_empleado INT REFERENCES gf.empleados(id_empleado),
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas DECIMAL(10, 2),
    comision DECIMAL(10, 2),
    total_pagar DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Equipos (para manejar lectores de códigos, impresoras, etc.)
CREATE TABLE gf.equipos (
    id_equipo SERIAL PRIMARY KEY,
    tipo VARCHAR(50) CHECK (tipo IN ('Lector Código Barras', 'Impresora Ticket', 'Impresora Matricial', 'Impresora Láser', 'Impresora Inyección')),
    marca VARCHAR(50), CHARACTER SET utf8mb4;
    modelo VARCHAR(50), CHARACTER SET utf8mb4;
    fecha_adquisicion DATE
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_clientes_cedula ON gf.clientes(cedula);
CREATE INDEX idx_clientes_ruc ON gf.clientes(ruc);
CREATE INDEX idx_productos_codigo_barras ON gf.productos(codigo_barras);
CREATE INDEX idx_ventas_fecha ON gf.ventas(fecha_venta);
CREATE INDEX idx_empleados_cargo ON gf.empleados(cargo);
CREATE INDEX idx_cliente_cedula ON gf.liente(cedula);

-- Tabla de Ventas
CREATE TABLE gf.ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INT REFERENCES gf.clientes(id_cliente) ON DELETE CASCADE,
    id_empleado INT REFERENCES gf.empleados(id_empleado) ON DELETE CASCADE,
    id_zona INT REFERENCES gf.zonas(id_zona),
    fecha_venta TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
	total DECIMAL(10, 2),
    tipo_pago VARCHAR(20) CHECK (tipo_pago IN ('Contado', 'Semanal', 'Quincenal', 'Mensual')),
    estado VARCHAR(20) CHECK (estado IN ('pendiente', 'pagado', 'cancelado')),
	entrega_inmediata BOOLEAN DEFAULT TRUE;
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Detalles de Venta
CREATE TABLE gf.detalles_venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES gf.ventas(id_venta) ON DELETE CASCADE,
    id_presentacion INTEGER REFERENCES gf.presentacion(id_presentacion) ON DELETE CASCADE,
    cantidad INTEGER CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Pagos
CREATE TABLE gf.pagos (
    id_pago SERIAL PRIMARY KEY,
    id_venta INT REFERENCES gf.ventas(id_venta),
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Inventario
CREATE TABLE gf.inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_producto INT REFERENCES gf.productos(id_producto),
    cantidad INT,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ubicacion VARCHAR(50),
    id_presentacion INTEGER REFERENCES gf.presentacion(id_presentacion) ON DELETE CASCADE,
    stock INTEGER CHECK (stock >= 0)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Trigger para actualizar el stock al vender
CREATE OR REPLACE FUNCTION actualizar_stock() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.cantidad > OLD.stock THEN
        RAISE EXCEPTION 'No hay suficiente stock';
    ELSE
        UPDATE gf.inventario SET stock = stock - NEW.cantidad WHERE id_presentacion = NEW.id_presentacion;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_stock
AFTER INSERT ON gf.detalle_venta
FOR EACH ROW EXECUTE FUNCTION actualizar_stock();

-- Tabla de Vehículos
CREATE TABLE gf.vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE,
    marca VARCHAR(50), CHARACTER SET utf8mb4;
    modelo VARCHAR(50), CHARACTER SET utf8mb4;
    año INT,
    ultima_revision DATE
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Gastos de Vehículos
CREATE TABLE gf.gastos_vehiculos (
    id_gasto SERIAL PRIMARY KEY,
    id_vehiculo INT REFERENCES gf.vehiculos(id_vehiculo),
    tipo_gasto VARCHAR(50) CHECK (tipo_gasto IN ('Combustible', 'Lubricantes', 'Gomería', 'Mecánica', 'Electricidad', 'Otro')); CHARACTER SET utf8mb4;
    monto DECIMAL(10, 2),
    fecha DATE DEFAULT CURRENT_DATE
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla RutaVenta
CREATE TABLE gf.ruta_venta (
   id_ruta SERIAL PRIMARY KEY,
   id_vehiculo INTEGER REFERENCES gf.vehiculos(id_vehiculo),
   fecha DATE
);

-- Tabla de Tracking GPS
CREATE TABLE gf.tracking_gps (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INT REFERENCES gf.vehiculos(id_vehiculo),
	coordenadas GEOGRAPHY(Point, 4326);
    latitud DECIMAL(9, 6),
    longitud DECIMAL(9, 6),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Proveedores
CREATE TABLE gf.proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    direccion TEXT, CHARACTER SET utf8mb4;
    telefono VARCHAR(20),
    email VARCHAR(100) CHARACTER SET utf8mb4;
);

-- Tabla de Compras a Proveedores
CREATE TABLE gf.compras_proveedores (
    id_compra SERIAL PRIMARY KEY,
    id_proveedor INT REFERENCES gf.proveedores(id_proveedor),
    fecha_compra DATE DEFAULT CURRENT_DATE,
    total DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Detalles de Compra
CREATE TABLE gf.detalles_compra (
    id_detalle SERIAL PRIMARY KEY,
    id_compra INT REFERENCES gf.compras_proveedores(id_compra),
    id_producto INT REFERENCES gf.productos(id_producto),
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);
