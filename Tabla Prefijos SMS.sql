--Tabla Prefijos
CREATE TABLE gf.prefijos (
    id_prefijo SERIAL PRIMARY KEY,
    prefijo VARCHAR(4) UNIQUE NOT NULL,
    descripcion VARCHAR(50)
);

961;HOLA PARAGUAY-VOX;
971;PERSONAL;
972;PERSONAL;
973;PERSONAL;
975;PERSONAL;
976;PERSONAL;
981;TELECEL-TIGO;
982;TELECEL-TIGO;
983;TELECEL-TIGO;
984;TELECEL-TIGO;
985;TELECEL-TIGO;
991;AMX MOVIL CLARO;
992;AMX MOVIL CLARO;
993;AMX MOVIL CLARO;
995;AMX MOVIL CLARO;

INSERT INTO gf.prefijos (prefijo, descripcion) 
VALUES 
    ('+595961', 'HOLA PARAGUAY-VOX'),
    ('+595971', 'PERSONAL'),
    ('+595972', 'PERSONAL'),
    ('+595973', 'PERSONAL'),
    ('+595975', 'PERSONAL'),
    ('+595976', 'PERSONAL'),
    ('+595981', 'TELECEL-TIGO'),
    ('+595982', 'TELECEL-TIGO'),
    ('+595983', 'TELECEL-TIGO'),
    ('+595984', 'TELECEL-TIGO'),
    ('+595985', 'TELECEL-TIGO'),
    ('+595991', 'AMX MOVIL CLARO'),
    ('+595992', 'AMX MOVIL CLARO'),
    ('+595993', 'AMX MOVIL CLARO'),
    ('+595995', 'AMX MOVIL CLARO');

-- Tabla SMS
CREATE TABLE gf.sms (
    id_sms SERIAL PRIMARY KEY,
    destinatario VARCHAR(20),
    enviado BOOLEAN,
    fecha DATE,
    hora TIME,
    modulo VARCHAR(50),
    referencia VARCHAR(100),
    fecha_env DATE,
    id_cliente INTEGER,
    id_mensaje_preestablecido INTEGER REFERENCES gf.mensajes_preestablecidos(id_mensaje)
);

-- Tabla de Mensajes Preestablecidos
CREATE TABLE gf.mensajes_preestablecidos (
    id_mensaje SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    contenido TEXT
);

INSERT INTO gf.mensajes_preestablecidos (tipo, contenido)
VALUES
    ('Cumpleaños', '¡Feliz cumpleaños! Le deseamos un maravilloso día.'),
    ('Pago Retrasado', 'Estimado cliente, le recordamos que tiene un pago retrasado. Por favor, realice el pago lo antes posible.'),
    ('Promoción', '¡No te pierdas nuestra última promoción! Con un descuento especial en todos nuestros productos.');

INSERT INTO gf.sms (destinatario, enviado, fecha, hora, modulo, referencia, fecha_env, id_cliente, id_mensaje_preestablecido)
VALUES
    ('+595981234567', true, '2023-06-01', '10:00:00', 'Cumpleaños', 'Cliente ID: 123', '2023-05-31', 123, 1);
	