-- Tabla Usuario
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
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

-- Tabla de Clientes
CREATE TABLE Tarjeta (
    id_tarjeta SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) UNIQUE
);

CREATE TABLE RUC (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE
);

CREATE TABLE GrupoEconomico (
    id_grupo SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) UNIQUE
);

CREATE TABLE TipoPago (
    id_tipo_pago SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) UNIQUE
);

CREATE TABLE EdadGrupo (
    id_edad_grupo SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) UNIQUE
);

CREATE TABLE AfiliacionPolitica (
    id_afiliacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE
);

CREATE TABLE Clientes (
    id_cliente SERIAL PRIMARY KEY,
    id_tarjeta INT REFERENCES Tarjeta(id_tarjeta),
    cedula VARCHAR(20) UNIQUE,
    id_ruc INT REFERENCES RUC(id_ruc),
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_registro DATE DEFAULT CURRENT_DATE,
    id_grupo INT REFERENCES GrupoEconomico(id_grupo),
    id_tipo_pago INT REFERENCES TipoPago(id_tipo_pago),
    sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
    id_edad_grupo INT REFERENCES EdadGrupo(id_edad_grupo),
    id_afiliacion INT REFERENCES AfiliacionPolitica(id_afiliacion)
);

-- Tabla de Empleados
CREATE TABLE Empleados (
    id_empleado SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    id_zona INT REFERENCES Zonas(id_zona),
    cargo VARCHAR(50) CHECK (cargo IN ('Vendedor', 'Cobrador', 'Chofer')),
    fecha_contratacion DATE,
    salario DECIMAL(10, 2)
);

-- Tabla de Zonas
CREATE TABLE Zonas (
    id_zona SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE
);

-- Tabla de Productos
CREATE TABLE Marca (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Productos (
    id_producto SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    id_marca INT REFERENCES Marca(id_marca),
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
    ano_lanzamiento INT,
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
    imagen_url VARCHAR(255)
);

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