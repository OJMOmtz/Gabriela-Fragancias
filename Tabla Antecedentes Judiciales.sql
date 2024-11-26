--Tabla Antecedentes Judiciales
CREATE TABLE gf.antecedentes_judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) REFERENCES gf.cedulas(numero_cedula),
    causa_penal TEXT,
    fecha_causa DATE,
    unidad_procesadora VARCHAR(100),
    juez VARCHAR(100),
    estado_proceso VARCHAR(50),
    fuente VARCHAR(50)
);

--Tabla Antecedentes Judiciales
CREATE TABLE Antecedentes_Judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) REFERENCES Cedulas(numero_cedula),
    causa_penal TEXT,  -- Descripción de la causa penal
    fecha_causa DATE,
    unidad_procesadora VARCHAR(100),
    juez VARCHAR(100),
    estado_proceso VARCHAR(50),
    fuente VARCHAR(50)  -- 'capt01.dbf'
);

--Tabla Antecedentes Judiciales
CREATE TABLE Antecedentes_Judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) REFERENCES Personas_Cedulas(numero_cedula),
    causa_penal TEXT,  -- Descripción de la causa penal
    fecha_causa DATE,
    unidad_procesadora VARCHAR(100),
    juez VARCHAR(100),
    estado_proceso VARCHAR(50),
    fuente VARCHAR(50)  -- 'capt01.dbf'
);

--Tabla Antecedentes Judiciales
CREATE TABLE Antecedentes_Judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) REFERENCES Personas(numero_cedula),
    causa_penal TEXT,  -- Descripción de la causa penal
    fecha_causa DATE,
    unidad_procesadora VARCHAR(100),
    juez VARCHAR(100),
    estado_proceso VARCHAR(50),
    fuente VARCHAR(50)  -- 'capt01.dbf'
);

-- Tabla AntecedentesJudiciales
CREATE TABLE AntecedentesJudiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_ci VARCHAR(20) REFERENCES Cedula(numero_ci),
    causa_penal TEXT
);

--Tabla Antecedentes Judiciales
CREATE TABLE antecedentes_judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_ci VARCHAR(20) REFERENCES cedulas(numero_ci),
    causa_penal TEXT NOT NULL
);

--Tabla Antecedentes Judiciales
CREATE TABLE Antecedentes_Judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) REFERENCES Clientes(cedula),
    causa_penal TEXT
);

-- Tabla AntecedentesJudiciales (para verificar los antecedentes de los clientes)
CREATE TABLE AntecedentesJudiciales (
    id_antecedente SERIAL PRIMARY KEY,
    cedula VARCHAR(20) REFERENCES Personas(cedula),
    causa_penal TEXT
);
