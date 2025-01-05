-- Roles de usuario
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

-- Usuarios del sistema
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    rol_id INTEGER REFERENCES roles(id),
    vendedor_id INTEGER REFERENCES vendedores(id),
    ultimo_login TIMESTAMP,
    intentos_fallidos INTEGER DEFAULT 0,
    bloqueado BOOLEAN DEFAULT false,
    fecha_bloqueo TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

-- Sesiones de usuario
CREATE TABLE sesiones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    estado BOOLEAN DEFAULT true
);

-- Permisos
CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

-- Relación roles-permisos
CREATE TABLE roles_permisos (
    rol_id INTEGER REFERENCES roles(id),
    permiso_id INTEGER REFERENCES permisos(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rol_id, permiso_id)
);

-- Registro de actividad
CREATE TABLE log_actividad (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    accion VARCHAR(50) NOT NULL,
    tabla_afectada VARCHAR(50),
    registro_id INTEGER,
    detalles JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_sesiones_token ON sesiones(token);
CREATE INDEX idx_log_actividad_usuario ON log_actividad(usuario_id);

-- Insertar roles básicos
INSERT INTO roles (nombre, descripcion) VALUES
('admin', 'Administrador del sistema'),
('vendedor', 'Vendedor con acceso a clientes y ventas'),
('supervisor', 'Supervisor de ventas'),
('contador', 'Acceso a información financiera');

-- Insertar permisos básicos
INSERT INTO permisos (nombre, descripcion) VALUES
('crear_venta', 'Puede crear nuevas ventas'),
('ver_ventas', 'Puede ver listado de ventas'),
('modificar_venta', 'Puede modificar ventas existentes'),
('eliminar_venta', 'Puede eliminar ventas'),
('ver_reportes', 'Puede ver reportes del sistema'),
('gestionar_usuarios', 'Puede gestionar usuarios'),
('gestionar_productos', 'Puede gestionar productos'),
('ver_estadisticas', 'Puede ver estadísticas del sistema');

-- Asignar permisos básicos a roles
INSERT INTO roles_permisos (rol_id, permiso_id)
SELECT r.id, p.id
FROM roles r
CROSS JOIN permisos p
WHERE r.nombre = 'admin';

INSERT INTO roles_permisos (rol_id, permiso_id)
SELECT r.id, p.id
FROM roles r
CROSS JOIN permisos p
WHERE r.nombre = 'vendedor' 
AND p.nombre IN ('crear_venta', 'ver_ventas', 'modificar_venta');
