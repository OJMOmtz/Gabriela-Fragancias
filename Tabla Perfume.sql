-- Tabla Perfume
CREATE TABLE Perfume (
    id_perfume SERIAL PRIMARY KEY,
    nombre_perfume VARCHAR(200) NOT NULL,
    id_marca INTEGER REFERENCES Marca(id_marca),
    costo DECIMAL(10, 2),
    precio_venta_credito DECIMAL(10, 2),
    precio_venta_contado DECIMAL(10, 2),
    segmento VARCHAR(50),
    franja_etaria VARCHAR(50),
    ocasion VARCHAR(50),
    ano_lanzamiento INTEGER,
    perfumero VARCHAR(100),
    notas_olfativas TEXT,
    notas_salida TEXT,
    notas_corazon TEXT,
    notas_fondo TEXT,
    intensidad VARCHAR(20),
    concentracion VARCHAR(20),
    duracion VARCHAR(50),
    estilo VARCHAR(50),
    imagen_url VARCHAR(255)
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

-- Product Table with Comprehensive Constraints
CREATE TABLE gf.producto (
    id_producto UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    id_marca UUID NOT NULL,
    descripcion TEXT,
    volumen INTEGER CHECK (volumen BETWEEN 5 AND 200),
    es_kit BOOLEAN DEFAULT FALSE,
    costo NUMERIC(10,2) NOT NULL,
    precio_venta_credito NUMERIC(10,2) NOT NULL,
    precio_venta_contado NUMERIC(10,2) NOT NULL,
    franja_etaria grupo_edad,
    ano_lanzamiento INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    estado estado_registro DEFAULT 'activo',
    CONSTRAINT precios_validos CHECK (
        precio_venta_contado >= costo AND 
        precio_venta_credito >= precio_venta_contado
    ),
    CONSTRAINT fk_producto_marca FOREIGN KEY (id_marca) 
        REFERENCES gf.marca(id_marca)
);

-- Productos (Products)
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_venta DECIMAL(10,2) NOT NULL,
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 5,
    fragancia VARCHAR(100),
    volumen_ml INTEGER,
    estado BOOLEAN DEFAULT true
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

-- Tabla Productos
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    categoria VARCHAR(50),
    codigo_barras VARCHAR(13) UNIQUE
);

-- Tabla Productos
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    categoria VARCHAR(50),
    codigo_barras VARCHAR(13) UNIQUE NOT NULL,
    stock INTEGER NOT NULL
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

-- Tabla de Productos (Perfumes)
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    precio NUMERIC(10,2),
    categoria VARCHAR(50)
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

-- Tabla Productos
CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    id_marca INTEGER REFERENCES Marcas(id_marca),
    precio_contado DECIMAL(10, 2) NOT NULL,  -- Precio al contado
    precio_credito DECIMAL(10, 2) NOT NULL,  -- Precio a crédito
    stock INTEGER NOT NULL,
    descripcion TEXT,
    presentacion VARCHAR(50),
    volumen INT CHECK (volumen BETWEEN 5 AND 200),  -- En mililitros, entre 5ml y 200ml
    es_kit BOOLEAN DEFAULT FALSE,  -- Indica si es un producto en kit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Productos
CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    id_marca INTEGER REFERENCES Marcas(id_marca),  -- Relación con la tabla Marcas
    precio_contado DECIMAL(10, 2) NOT NULL,  -- Precio de venta al contado
    precio_credito DECIMAL(10, 2) NOT NULL,  -- Precio de venta a crédito
    stock INTEGER NOT NULL,  -- Cantidad de productos disponibles
    descripcion TEXT,
    presentacion VARCHAR(50),  -- Formato del producto
    volumen INT CHECK (volumen BETWEEN 5 AND 200),  -- Volumen en mililitros
    es_kit BOOLEAN DEFAULT FALSE,  -- Indica si es un producto en kit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla Productos
CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    categoria VARCHAR(50),
    codigo_barras VARCHAR(13) UNIQUE NOT NULL,
    stock INTEGER NOT NULL
);

--Tabla Productos Vendidos
CREATE TABLE Productos_Vendidos (
    id_producto_vendido SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER CHECK (cantidad > 0),
    precio DECIMAL(10, 2)
);