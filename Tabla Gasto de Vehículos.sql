-- Tabla Gasto de Vehículos
CREATE TABLE GastoVehiculo (
   id_gasto SERIAL PRIMARY KEY,
   tipo_gasto VARCHAR(50),
   monto DECIMAL(10, 2),
   fecha DATE
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

-- Tabla de Gastos de Vehículos
CREATE TABLE gastos_vehiculos (
    id_gasto SERIAL PRIMARY KEY,
    id_vehiculo INTEGER REFERENCES vehiculos(id_vehiculo),
    tipo_gasto VARCHAR(50),
    monto DECIMAL(10, 2),
    fecha DATE
);