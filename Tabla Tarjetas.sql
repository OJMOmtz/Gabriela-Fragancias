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

--Tabla Tarjetas
CREATE TABLE Tarjetas (
    id_tarjeta SERIAL PRIMARY KEY,
    numero_tarjeta VARCHAR(7) NOT NULL,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),
    id_vendedor INTEGER REFERENCES Personas(id_persona),  -- Relación con la persona que actúa como vendedor
    id_zona INTEGER REFERENCES Zonas(id_zona),  -- Relación con la zona de ventas
    total_gs DECIMAL(10, 2) NOT NULL,  -- Total en guaraníes de la tarjeta
    saldo DECIMAL(10, 2) DEFAULT 0,  -- Saldo pendiente en la tarjeta
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('SEM', 'QUIN', 'MENS')),  -- Periodicidad del pago
    estado VARCHAR(20) CHECK (estado IN ('activa', 'cancelada')) DEFAULT 'activa',  -- Estado de la tarjeta
    fecha_emision DATE DEFAULT CURRENT_DATE,
    id_tarjeta_anterior INTEGER REFERENCES Tarjetas(id_tarjeta)  -- Referencia a la tarjeta anterior en caso de reemplazo
);

--Tabla Tarjetas
CREATE TABLE Tarjetas (
    id_tarjeta SERIAL PRIMARY KEY,
    numero_tarjeta VARCHAR(7) NOT NULL,
    id_cliente INTEGER REFERENCES Clientes(id_cliente),  -- Cliente al que pertenece la tarjeta
    id_vendedor INTEGER REFERENCES Personas(id_persona),  -- Vendedor que emitió la tarjeta
    id_zona INTEGER REFERENCES Zonas(id_zona),  -- Zona geográfica vinculada a la tarjeta
    total_gs DECIMAL(10, 2) NOT NULL,  -- Monto total de la tarjeta
    saldo DECIMAL(10, 2) DEFAULT 0,  -- Saldo pendiente en la tarjeta
    forma_pago VARCHAR(20) CHECK (forma_pago IN ('SEM', 'QUIN', 'MENS')),  -- Periodicidad del pago
    estado VARCHAR(20) CHECK (estado IN ('activa', 'cancelada')) DEFAULT 'activa',  -- Estado actual de la tarjeta
    fecha_emision DATE DEFAULT CURRENT_DATE,  -- Fecha de emisión de la tarjeta
    id_tarjeta_anterior INTEGER REFERENCES Tarjetas(id_tarjeta)  -- Tarjeta anterior en caso de reemplazo
);