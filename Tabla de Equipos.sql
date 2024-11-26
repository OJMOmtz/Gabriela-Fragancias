-- Tabla de Equipos (para manejar lectores de códigos, impresoras, etc.)
CREATE TABLE equipos (
    id_equipo SERIAL PRIMARY KEY,
    tipo VARCHAR(50) CHECK (tipo IN ('Lector Código Barras', 'Impresora Ticket', 'Impresora Matricial', 'Impresora Láser', 'Impresora Inyección')),
    marca VARCHAR(50), CHARACTER SET utf8mb4;
    modelo VARCHAR(50), CHARACTER SET utf8mb4;
    fecha_adquisicion DATE
);