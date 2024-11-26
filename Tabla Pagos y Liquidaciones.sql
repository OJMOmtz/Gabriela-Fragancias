-- Pagos (Payments)
CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES ventas(id),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto DECIMAL(10,2) NOT NULL,
    forma_pago VARCHAR(20) NOT NULL,
    numero_comprobante VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'procesado',
    CHECK (estado IN ('procesado', 'anulado'))
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

--Tabla de Liquidaciones
CREATE TABLE Liquidaciones (
	id_liquidacion SERIAL PRIMARY KEY,
	id_vendedor INT REFERENCES Vendedores(id_vendedor),
	fecha_liquidacion DATE DEFAULT CURRENT_DATE,
	total_ventas DECIMAL(10, 2),
	comision DECIMAL(10, 2),
	total_pagar DECIMAL(10, 2)
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Liquidaciones
CREATE TABLE liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_empleado INT REFERENCES empleados(id_empleado),
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas DECIMAL(10, 2),
    comision DECIMAL(10, 2),
    total_pagar DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla para almacenar las comisiones por producto
CREATE TABLE Comisiones (
    id_producto INTEGER,
    comision NUMERIC,
    PRIMARY KEY (id_producto),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
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

-- Tabla Pagos
CREATE TABLE Pagos (
    id_pago SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto DECIMAL(10, 2) NOT NULL,  -- Monto pagado
    saldo_restante DECIMAL(10, 2) NOT NULL,  -- Saldo pendiente después del pago
    entrega_inicial BOOLEAN DEFAULT FALSE,  -- Indica si es un pago inicial
    recargo BOOLEAN DEFAULT FALSE  -- Indica si hubo recargo por retraso
);

--Tabla Liquidaciones
CREATE TABLE Liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Personas(id_persona),  -- Relación con la tabla Personas
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,  -- Fecha de la liquidación
    total_ventas DECIMAL(10, 2),  -- Total de ventas del vendedor
    comision DECIMAL(10, 2),  -- Comisión calculada sobre las ventas
    total_pagar DECIMAL(10, 2)  -- Total a pagar al vendedor
);


--Tabla Liquidaciones
CREATE TABLE Liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_vendedor INT REFERENCES Personas(id_persona),  -- Vendedor que recibe la liquidación
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas DECIMAL(10, 2),  -- Total de ventas del periodo
    comision DECIMAL(10, 2),  -- Comisión por las ventas realizadas
    total_pagar DECIMAL(10, 2)  -- Total a pagar al vendedor
);

-- Tabla Pagos
CREATE TABLE Pagos (
    id_pago SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),  -- Tarjeta sobre la que se realiza el pago
    fecha_pago DATE DEFAULT CURRENT_DATE,  -- Fecha del pago
    monto DECIMAL(10, 2) NOT NULL,  -- Monto del pago
    saldo_restante DECIMAL(10, 2) NOT NULL,  -- Saldo pendiente después del pago
    entrega_inicial BOOLEAN DEFAULT FALSE,  -- Indica si es el primer pago
    recargo BOOLEAN DEFAULT FALSE  -- Indica si hubo recargo por retraso
);

-- Tabla Pagos
CREATE TABLE Pagos (
    id_pago SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),  -- Relación con la tarjeta
    fecha_pago DATE DEFAULT CURRENT_DATE,  -- Fecha en que se realiza el pago
    monto DECIMAL(10, 2) NOT NULL,  -- Monto del pago realizado
    saldo_restante DECIMAL(10, 2) NOT NULL,  -- Saldo pendiente en la tarjeta después del pago
    nueva_venta BOOLEAN DEFAULT FALSE,  -- Indica si el pago está relacionado con una nueva venta
    interes_moratorio DECIMAL(10, 2) DEFAULT 0  -- Interés moratorio aplicado (5% mensual si aplica)
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