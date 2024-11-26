-- Tabla de Marcas
CREATE TABLE marcas (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ano_fundacion INTEGER,
    sede VARCHAR(100)
);

-- Tabla de Perfumes
CREATE TABLE perfumes (
    id_perfume SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    id_marca INTEGER REFERENCES marcas(id_marca),
    ano_lanzamiento INTEGER,
    perfumero VARCHAR(100),
    notas_olfativas TEXT,
    costo DECIMAL(10, 2),
    precio_venta_credito DECIMAL(10, 2),
    precio_venta_contado DECIMAL(10, 2),
    segmento VARCHAR(50),
    franja_etaria VARCHAR(50),
    ocasion VARCHAR(50),
    notas_salida TEXT,
    notas_corazon TEXT,
    notas_fondo TEXT,
    intensidad VARCHAR(20),
    concentracion VARCHAR(20),
    duracion VARCHAR(50),
    estilo VARCHAR(50)
);

-- Tabla de Presentaciones
CREATE TABLE presentaciones (
    id_presentacion SERIAL PRIMARY KEY,
    id_perfume INTEGER REFERENCES perfumes(id_perfume),
    codigo_barra VARCHAR(50) UNIQUE,
    tamano_ml INTEGER CHECK (tamano_ml BETWEEN 5 AND 200),
    imagen_url VARCHAR(255),
    es_kit BOOLEAN DEFAULT FALSE
);

-- Tabla de Clientes
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cedula VARCHAR(20) UNIQUE,
    ruc VARCHAR(20) UNIQUE,
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    tipo_pago VARCHAR(20),
    grupo_economico VARCHAR(50),
    sexo VARCHAR(10),
    edad INTEGER,
    afiliacion_politica VARCHAR(50)
);

-- Tabla de Vendedores
CREATE TABLE vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cedula VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    zona VARCHAR(50)
);

-- Tabla de Ventas
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    fecha_venta DATE,
    total DECIMAL(10, 2),
    tipo_pago VARCHAR(20),
    estado VARCHAR(20),
    entrega_inmediata BOOLEAN DEFAULT TRUE
);

-- Tabla de Detalle de Ventas
CREATE TABLE detalle_ventas (
    id_detalle_venta SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES ventas(id_venta),
    id_presentacion INTEGER REFERENCES presentaciones(id_presentacion),
    cantidad INTEGER,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2)
);

-- Tabla de Vehículos
CREATE TABLE vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    placa VARCHAR(20) UNIQUE,
    ano INTEGER
);

-- Tabla de Gastos de Vehículos
CREATE TABLE gastos_vehiculos (
    id_gasto SERIAL PRIMARY KEY,
    id_vehiculo INTEGER REFERENCES vehiculos(id_vehiculo),
    tipo_gasto VARCHAR(50),
    monto DECIMAL(10, 2),
    fecha DATE
);

-- Tabla de Maletines
CREATE TABLE maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    fecha_carga DATE DEFAULT CURRENT_DATE
);

-- Tabla de Productos en Maletín
CREATE TABLE productos_maletin (
    id_maletin INTEGER REFERENCES maletines(id_maletin),
    id_presentacion INTEGER REFERENCES presentaciones(id_presentacion),
    cantidad INTEGER,
    PRIMARY KEY (id_maletin, id_presentacion)
);

-- Tabla de Liquidaciones
CREATE TABLE liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas DECIMAL(10, 2),
    comision DECIMAL(10, 2),
    total_pagar DECIMAL(10, 2)
);