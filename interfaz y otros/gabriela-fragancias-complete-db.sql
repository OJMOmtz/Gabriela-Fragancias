# Preparing to write the improved database structure, UI code, and user manual into a downloadable file.

# Step 1: Defining the improved SQL structure for PostgreSQL
improved_sql_content = """
-- Improved SQL Structure for Gabriela Fragancias Database

-- Enabling necessary extensions for performance and text search
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Setting up the schema
CREATE SCHEMA IF NOT EXISTS gabriela_fragancias;
SET search_path TO gabriela_fragancias, public;

-- Table Roles with indexed fields for better querying
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

-- Users Table with additional indexes for faster authentication and lookup
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
    estado BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}'::jsonb
);

-- Table Permisos with added timestamp for change tracking
CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

-- Relationship Table Roles_Permisos for Role-Permission Mapping
CREATE TABLE roles_permisos (
    rol_id INTEGER REFERENCES roles(id),
    permiso_id INTEGER REFERENCES permisos(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rol_id, permiso_id)
);

-- Example Additional Entities like Company and Customer Tables 
CREATE TABLE empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    ruc VARCHAR(20) UNIQUE,
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes on fields frequently queried
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_roles_nombre ON roles(nombre);
CREATE INDEX idx_clientes_ruc ON clientes(ruc);
"""

# Step 2: Defining the UI code for a web interface
ui_code_content = """
# Interface Code (Flask example with HTML & Bootstrap for Gabriela Fragancias)

# Importing necessary libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/gabriela_fragancias'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Database Models
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    ruc = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)

# Route to show clients
@app.route('/clientes')
def show_clients():
    clients = Cliente.query.all()
    return render_template('clients.html', clients=clients)

# Route to add a client
@app.route('/clientes/add', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        new_client = Cliente(
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            ruc=request.form['ruc'],
            email=request.form['email'],
            telefono=request.form['telefono'],
            direccion=request.form['direccion']
        )
        db.session.add(new_client)
        db.session.commit()
        flash('Client added successfully!')
        return redirect(url_for('show_clients'))
    return render_template('add_client.html')

if __name__ == '__main__':
    app.run(debug=True)
"""

# Step 3: Creating the Markdown manual
manual_content = """
# Manual de Usuario para Gabriela Fragancias

## 1. Introducción
Esta interfaz está diseñada para gestionar la base de datos de Gabriela Fragancias, facilitando la administración de clientes, productos, ventas, y otros elementos clave.

## 2. Acceso a la Interfaz
Para acceder a la interfaz, abra la aplicación Flask mediante el archivo `app.py` y acceda a `http://localhost:5000/clientes`.

## 3. Funcionalidades Principales
- **Gestión de Clientes**: Ver, agregar y actualizar clientes.
- **Gestión de Productos**: Añadir, editar y eliminar productos.

## 4. Uso
1. Acceda al apartado deseado desde el menú de navegación.
2. Complete los formularios para agregar o editar información.
3. Utilice los botones de acción (Guardar, Cancelar) para procesar los datos.

## 5. Resolución de Problemas
- Si encuentra un error de conexión, verifique la configuración de la base de datos en `app.config['SQLALCHEMY_DATABASE_URI']`.
"""

# Saving all content into a single markdown file for download
output_file_path = '/mnt/data/Gabriela_Fragancias_Optimized_Setup.md'
with open(output_file_path, 'w') as output_file:
    output_file.write("# Optimized Database Structure and Interface Code for Gabriela Fragancias\n\n")
    output_file.write("## Improved SQL Structure:\n\n```sql\n")
    output_file.write(improved_sql_content)
    output_file.write("\n```\n\n## UI Code:\n\n```python\n")
    output_file.write(ui_code_content)
    output_file.write("\n```\n\n## User Manual:\n\n")
    output_file.write(manual_content)

output_file_path

-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- Para búsquedas textuales mejoradas

-- Configuración de esquema
CREATE SCHEMA IF NOT EXISTS gabriela_fragancias;
SET search_path TO gabriela_fragancias, public;

-- Tablas base del sistema

-- Tabla Roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

-- Tabla Usuarios
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
    estado BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}'::jsonb
);

-- Tabla Permisos
CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

-- Tabla Roles Permisos
CREATE TABLE roles_permisos (
    rol_id INTEGER REFERENCES roles(id),
    permiso_id INTEGER REFERENCES permisos(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rol_id, permiso_id)
);

-- Tabla Empresa
CREATE TABLE empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla RUC
CREATE TABLE ruc (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    digito_verificador INT NOT NULL,
    razon_social VARCHAR(255),
    tipo VARCHAR(20) CHECK (tipo IN ('Persona', 'Empresa'))
);

-- Tabla Antecedentes_Judiciales
CREATE TABLE antecedentes_judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) REFERENCES personas_cedulas(numero_cedula),
    causa_penal TEXT,
    fecha_causa DATE,
    unidad_procesadora VARCHAR(100),
    juez VARCHAR(100),
    estado_proceso VARCHAR(50),
    fuente VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tablas de negocio
CREATE TABLE zonas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    area GEOGRAPHY(POLYGON, 4326),
    meta_ventas DECIMAL(12,2),
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Vendedores
CREATE TABLE vendedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_ingreso DATE NOT NULL,
    zona_id INTEGER REFERENCES zonas(id),
    comision_porcentaje DECIMAL(5,2) DEFAULT 0,
    meta_mensual DECIMAL(12,2),
	estado BOOLEAN DEFAULT true,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Clientes
CREATE TABLE clientes (
	id SERIAL PRIMARY KEY,
	numero_tarjeta VARCHAR(7) NOT NULL UNIQUE,
	nombre VARCHAR(100) NOT NULL,
	documento VARCHAR(20) UNIQUE NOT NULL,
	tipo_documento VARCHAR(10),
	telefono VARCHAR(20),
	email VARCHAR(100),
	direccion TEXT,
	ubicacion GEOGRAPHY(POINT, 4326),
	zona_id INTEGER REFERENCES zonas(id),
	vendedor_id INTEGER REFERENCES vendedores(id),
	limite_credito DECIMAL(12,2) DEFAULT 0,
	categoria VARCHAR(20) DEFAULT 'REGULAR',
	fecha_registro DATE DEFAULT CURRENT_DATE,
	ultimo_contacto TIMESTAMP,
	estado BOOLEAN DEFAULT true,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Tarjetas
CREATE TABLE tarjetas (
	id_tarjeta SERIAL PRIMARY KEY,
	numero_tarjeta VARCHAR(7) NOT NULL UNIQUE,
	id_cliente INTEGER REFERENCES clientes(id),
	id_vendedor INTEGER REFERENCES vendedores(id),
	total_gs DECIMAL(10, 2) NOT NULL CHECK (total_gs > 0),
	saldo DECIMAL(10, 2) DEFAULT 0 CHECK (saldo >= 0),
	form_pago VARCHAR(20) CHECK (form_pago IN ('SEM', 'QUIN', 'MENS')),
	estado VARCHAR(20) CHECK (estado IN ('activa', 'cancelada')),
	fecha_emision DATE DEFAULT CURRENT_DATE
);

-- Tabla Marcas
CREATE TABLE marcas (
	id_marca SERIAL PRIMARY KEY,
	nombre VARCHAR(100) UNIQUE NOT NULL,
	año_fundacion INT CHECK (año_fundacion > 1900 AND año_fundacion <= EXTRACT(YEAR FROM CURRENT_DATE)),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Productos
CREATE TABLE productos (
	id SERIAL PRIMARY KEY,
	codigo VARCHAR(50) UNIQUE NOT NULL,
	id_marca INTEGER REFERENCES marcas(id_marca),
	nombre VARCHAR(100) NOT NULL,
	descripcion TEXT,
	categoria VARCHAR(50),
	precio_costo DECIMAL(10,2) NOT NULL CHECK (precio_costo >= 0),
	precio_venta DECIMAL(10,2) NOT NULL CHECK (precio_venta >= 0),
	stock_actual INTEGER DEFAULT 0 CHECK (stock_actual >= 0),
	stock_minimo INTEGER DEFAULT 5 CHECK (stock_minimo >= 0),
	stock_maximo INTEGER DEFAULT 100 CHECK (stock_maximo >= stock_minimo),
	fragancia VARCHAR(100),
	volumen_ml INTEGER CHECK (volumen_ml > 0),
	imagen_url VARCHAR(255),
	proveedor VARCHAR(100),
	tiempo_reposicion INTEGER, -- días
	estado BOOLEAN DEFAULT true,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	metadata JSONB DEFAULT '{}'::jsonb
);

-- Tabla Productos Vendidos
CREATE TABLE productos_vendidos (
	id_producto_vendido SERIAL PRIMARY KEY,
	id_tarjeta INTEGER REFERENCES tarjetas(id_tarjeta),
	id_producto INTEGER REFERENCES productos(id),
	cantidad INTEGER CHECK (cantidad > 0),
	precio DECIMAL(10, 2) CHECK (precio > 0),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Maletines
CREATE TABLE maletines (
	id_maletin SERIAL PRIMARY KEY,
	id_vendedor INTEGER REFERENCES vendedores(id),
	fecha_carga DATE DEFAULT CURRENT_DATE,
	estado VARCHAR(20) CHECK (estado IN ('activo', 'devuelto', 'perdido')),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Productos Maletín
CREATE TABLE productos_maletin (
	id_maletin INTEGER REFERENCES maletines(id_maletin),
	id_producto INTEGER REFERENCES productos(id),
	cantidad INTEGER NOT NULL CHECK (cantidad > 0),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id_maletin, id_producto)
);

-- Tabla Liquidaciones
CREATE TABLE liquidaciones (
	id_liquidacion SERIAL PRIMARY KEY,
	id_vendedor INTEGER REFERENCES vendedores(id),
	fecha_liquidacion DATE DEFAULT CURRENT_DATE,
	total_ventas DECIMAL(10, 2) DEFAULT 0,
	comision DECIMAL(10, 2) DEFAULT 0,
	total_pagar DECIMAL(10, 2) DEFAULT 0,
	estado VARCHAR(20) CHECK (estado IN ('pendiente', 'aprobada', 'pagada')),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Ventas
CREATE TABLE ventas (
	id SERIAL PRIMARY KEY,
	numero_factura VARCHAR(20) UNIQUE,
	fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	cliente_id INTEGER REFERENCES clientes(id),
	vendedor_id INTEGER REFERENCES vendedores(id),
	subtotal DECIMAL(10,2) NOT NULL CHECK(subtotal >= 0),
	descuento DECIMAL(10,2) DEFAULT 0 CHECK(descuento >= 0 AND descuento <= subtotal),
	impuesto DECIMAL(10,2) DEFAULT 0 CHECK(impuesto >= 0),
	total DECIMAL(10,2) AS (subtotal - descuento + impuesto), -- Calculado
	forma_pago VARCHAR[20],
	numero_cuotas INT DEFUALT[1],
	estado VARCAHR[20] DEFUALT['pendiente'] ,
	punto_ruta_id INT REFERENCE puntos_ruta[id],
	create_date TIEMPO DEFUALT[CURRENT_TIME],
	update_date TIEMPO DEFUALT[CURRENT_TIME],
	metadata JSONB DEFUALT['{}']::JSONB ,
	CHECK [estado IN ['pendiente','pagada','cancelada','anulada']]
);

-- Tabla Detalles Venta 
CREATE TABLE detalles_venta (
	id SERIAL PRIMARY KEY,
	venta_id INTEGER REFERENCES ventas(id),
	productos_id INTEGER REFERENCES productos(id),
	cantidad INT CHECK(cantidad > 0),
	precio_unitario DECIMAL[10][2] CHECK(precio_unitario >0 ),
	descuento DECIMAL[10][2] DEFUALT[0],
	subtotal AS(cantidad * precio_unitario - descuento),
	create_date TIEMPO DEFUALT[CURRENT_TIME],
	update_date TIEMPO DEFUALT[CURRENT_TIME]
);

-- Tabla Pagos 
CREATE TABLE pagos(
	id SERIAL PRIMARY KEY,
	venta_id INT REFERENCE ventas[id],
	fecha_control TIEMPO DEFUALT[CURRENT_TIME],
	fecha_entrega TIEMPO DEFUALT[CURRENT_TIME],
	monto_entrega DECIMAL[10][2] CHECK(monto_entrega >0 ),
	saldo_restante AS(monto_entrega - total),
	create_date TIEMPO DEFUALT[CURRENT_TIME],
	update_date TIEMPO DEFUALT[CURRENT_TIME]
);

-- Tabla Vehículos
CREATE TABLE vehiculos (
	id SERIAL PRIMARY KEY,
	placa VARCHAR(20) UNIQUE NOT NULL,
	marca VARCHAR(50),
	modelo VARCHAR(50),
	año INTEGER,
	motor VARCHAR(50),
	chassis VARCHAR(50),
	capacidad_kg DECIMAL(10,2),
	vendedor_id INTEGER REFERENCES vendedores(id),
	ultimo_mantenimiento DATE,
	proximo_mantenimiento DATE,
	kilometraje_actual INTEGER DEFAULT 0,
	estado BOOLEAN DEFAULT true,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	historial_mantenimiento JSONB DEFAULT '[]'::jsonb
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

-- Tabla Rutas (para vendedores y manejo de geolocalización)
CREATE TABLE Rutas (
    id_ruta SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedores(id_vendedor),
    nombre_ruta VARCHAR(100) NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    zona VARCHAR(50),
    id_vehiculo INTEGER REFERENCES Vehiculo(id_vehiculo),
	coordenadas GEOGRAPHY(POINT, 4326)  -- Integración con GIS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Tracking GPS
CREATE TABLE tracking_gps (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INT REFERENCES vehiculos(id_vehiculo),
	coordenadas GEOGRAPHY(Point, 4326);
    latitud DECIMAL(9, 6),
    longitud DECIMAL(9, 6),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Proveedores
CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE,
    nombre VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    direccion TEXT, CHARACTER SET utf8mb4;
    telefono VARCHAR(20),
    email VARCHAR(100) CHARACTER SET utf8mb4;
);

-- Tabla de Compras a Proveedores
CREATE TABLE compras_proveedores (
    id_compra SERIAL PRIMARY KEY,
    id_proveedor INT REFERENCES proveedores(id_proveedor),
    fecha_compra DATE DEFAULT CURRENT_DATE,
    total DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Detalles de Compra
CREATE TABLE detalles_compra (
    id_detalle SERIAL PRIMARY KEY,
    id_compra INT REFERENCES compras_proveedores(id_compra),
    id_producto INT REFERENCES productos(id_producto),
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla Departamento
CREATE TABLE Departamento (
    id_departamento SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_departamento VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Municipio
CREATE TABLE Municipio (
    id_municipio SERIAL PRIMARY KEY,
    id_departamento INTEGER REFERENCES Departamento(id_departamento),
    nombre_municipio VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_municipio VARCHAR(10) UNIQUE NOT NULL
);

-- Tabla Zona
CREATE TABLE Zona (
    id_zona SERIAL PRIMARY KEY,
    id_municipio INTEGER REFERENCES Municipio(id_municipio),
    nombre_zona VARCHAR(100) NOT NULL, CHARACTER SET utf8mb4;
    codigo_zona VARCHAR(10) UNIQUE NOT NULL,
    geometria GEOGRAPHY(POLYGON, 4326)
);

-- Tabla Ubicacion
CREATE TABLE Ubicacion (
    id_ubicacion SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Vendedor(id_vendedor),
    fecha_hora TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    coordenadas GEOGRAPHY(POINT, 4326)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL DEFAULT NULL
);

-- Tabla de Equipos (para manejar lectores de códigos, impresoras, etc.)
CREATE TABLE equipos (
    id_equipo SERIAL PRIMARY KEY,
    tipo VARCHAR(50) CHECK (tipo IN ('Lector Código Barras', 'Impresora Ticket', 'Impresora Matricial', 'Impresora Láser', 'Impresora Inyección')),
    marca VARCHAR(50), CHARACTER SET utf8mb4;
    modelo VARCHAR(50), CHARACTER SET utf8mb4;
    fecha_adquisicion DATE
);

-- Tabla Rutas
CREATE TABLE rutas (
	id SERIAL PRIMARY KEY,
	vendedor_id INTEGER REFERENCES vendedores(id),
	vehiculo_id INTEGER REFERENCES vehiculos(id),
	fecha DATE NOT NULL,
	inicio_ruta GEOGRAPHY(POINT, 4326),
	fin_ruta GEOGRAPHY(POINT, 4326),
	distancia_km DECIMAL(10,2),
	tiempo_estimado INTEGER, -- minutos
	tiempo_real INTEGER,
	estado VARCHAR(20) CHECK (estado IN ('planificada', 'en_progreso', 'completada', 'cancelada')),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	metadata JSONB DEFAULT '{}'::jsonb
);

-- Tabla Puntos Ruta
CREATE TABLE puntos_ruta (
	id SERIAL PRIMARY KEY,
	ruta_id INTEGER REFERENCES rutas(id),
	cliente_id INTEGER REFERENCES clientes(id),
	orden INTEGER NOT NULL,
	hora_planificada TIME,
	hora_real TIME,
	ubicacion GEOGRAPHY(POINT, 4326),
	estado VARCHAR(20) CHECK (estado IN ('pendiente', 'visitado', 'no_visitado', 'reprogramado')),
	notas TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Log Actividad 
CREATE TABLE log_actividad(
	id SERIAL PRIMARY KEY,
	usuario_id INT REFERENCE usuarios[id],
	accion VARCAHR[50],
	tabla_afectada VARCAHR[50],
	registro_id INT,
	detalles JSONB,
	ip_address VARCAHR[45],
	create_date TIEMPO DEFUALT[CURRENT_TIME]
);

-- Funciones útiles 
CREATE OR REPLACE FUNCTION actualizar_stock()
RETURNS TRIGGER AS $$
BEGIN 
UPDATE productos SET stock_actual = stock_actual - NEW.cantidad WHERE id = NEW.producto_id; 
RETURN NEW; 
END; $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calcular_comision_vendedor()
RETURNS TRIGGER AS $$
BEGIN 
UPDATE vendedores SET meta_mensual = meta_mensual + NEW.total * (comision_porcentaje / 100)
WHERE id = NEW.vendedor_id; 
RETURN NEW; 
END; $$ LANGUAGE plpgsql;

-- Triggers 
CREATE TRIGGER tr_actualizar_stock AFTER INSERT ON detalles_venta FOR EACH ROW EXECUTE FUNCTION actualizar_stock();
CREATE TRIGGER tr_calcular_comision AFTER INSERT ON ventas FOR EACH ROW EXECUTE FUNCTION calcular_comision_vendedor();

-- Datos iniciales 
INSERT INTO roles (nombre, descripcion)
VALUES ('admin', 'Administrador del sistema'),
('vendedor', 'Vendedor con acceso a clientes y ventas'),
('supervisor', 'Supervisor de ventas'),
('contador', 'Acceso a información financiera'),
('almacen', 'Gestión de inventario');

INSERT INTO permisos (nombre, descripcion)
VALUES ('crear_venta', 'Puede crear nuevas ventas'),
('ver_ventas', 'Puede ver listado de ventas'),
('modificar_venta', 'Puede modificar ventas existentes'),
('eliminar_venta', 'Puede eliminar ventas'),
('ver_reportes', 'Puede ver reportes del sistema'),
('gestionar_usuarios', 'Puede gestionar usuarios'),
('gestionar_productos', 'Puede gestionar productos'),
('ver_estadisticas', 'Puede ver estadísticas del sistema'),
('gestionar_rutas', 'Puede gestionar rutas de venta'),
('gestionar_inventario', 'Puede gestionar inventario');

COMMENT ON TABLE usuarios IS 'Almacena información de usuarios del sistema';
COMMENT ON TABLE ventas IS 'Registro de ventas realizadas';
COMMENT ON TABLE rutas IS 'Planificación de rutas de vendedores';
COMMENT ON TABLE productos IS 'Catálogo de productos disponibles';

-- Vista consolidada de relaciones cliente-tarjeta 
CREATE OR REPLACE VIEW vista_cliente_tarjeta AS 
SELECT pc.numero_cedula, pc.nombre, pc.apellido,c.tarjeta AS numero_tarjeta_cliente,t.numero_tarjeta AS numero_tarjeta_activa,t.saldo,t.forma_pago,t.estado,z.nombre_zona 
FROM personas_cedulas pc JOIN clientes c ON pc.id_persona = c.id_persona LEFT JOIN tarjetas t ON c.tarjeta = t.numero_tarjeta LEFT JOIN zonas z ON t.id_zona = z.id_zona;

-- Vista para control de pagos 
CREATE OR REPLACE VIEW vista_control_pagos AS 
SELECT t.numero_tarjeta,c.nombre,p.fecha_control,p.fecha_entrega,p.monto_entrega,p.saldo_restante 
FROM tarjetas t JOIN clientes c ON t.id_cliente = c.id_cliente JOIN pagos p ON t.id_tarjeta = p.id_tarjeta ORDER BY p.fecha_control;

-- =============================================
-- PERMISOS =====================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO current_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO current_user;

-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- Para búsquedas textuales mejoradas

-- Configuración de esquema
CREATE SCHEMA IF NOT EXISTS gabriela_fragancias;
SET search_path TO gabriela_fragancias, public;

-- Tablas base del sistema
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    rol_id INTEGER REFERENCES roles(id),
    vendedor_id INTEGER,
    ultimo_login TIMESTAMP,
    intentos_fallidos INTEGER DEFAULT 0,
    bloqueado BOOLEAN DEFAULT false,
    fecha_bloqueo TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT true
);

CREATE TABLE roles_permisos (
    rol_id INTEGER REFERENCES roles(id),
    permiso_id INTEGER REFERENCES permisos(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rol_id, permiso_id)
);

-- Tabla Empresa
CREATE TABLE Empresa (
    id_empresa SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
999639|BARRIOS ENCISO, PEDRO|7|BAEP653610X|CANCELADO|
999649|CAMPUZANO DE MORENO, ROSALINA|4|CAMR652481Z|ACTIVO|
999669|BENITEZ ARCE, POLICENA|9|BEAP652670H|CANCELADO|
999709|SOSA PERALTA, IGNACIO DIOSNEL|1|SOPI552150V|SUSPENSION TEMPORAL|
999739|LOPEZ CACERES, NATALIA MARIA|3|LOCN782280D|ACTIVO|
999769|CARDENAS ROJAS, SONIA ELIZABETH|5|CARS661180|ACTIVO|
999829|CHAMORRO ALCARAZ, NELSON ADOLFO|2|CAAN742950P|ACTIVO|
999849|ORTIZ GONZALEZ, HIGINIO LEONARDO|7|OIGH653110M|CANCELADO|
999869|GUERRERO RIVEROS, ANACLETO|1|GURA631170H|SUSPENSION TEMPORAL|
999879|CAÑETE, ALFREDO|9|CAAL6514106|ACTIVO|
999899|PAVON DE FLORES, NORMA BEATRIZ|3|AUGM6726822|CANCELADO|
999929|CUEVAS CENTURION, ANDRES RAUL|9|CUCA670480N|CANCELADO|
-- Tabla RUC
gabriela_fragancias=# \d public.ruc
                                             Tabla ½public.ruc╗
      Columna       |          Tipo          | Ordenamiento | Nulable  |             Por omisi¾n
--------------------+------------------------+--------------+----------+-------------------------------------
 id_ruc             | integer                |              | not null | nextval('ruc_id_ruc_seq'::regclass)
 razon_social       | character varying(255) |              |          |
 digito_verificador | integer                |              | not null |
 ruc                | character varying(20)  |              | not null |
 estado             | character varying(20)  |              |          |
═ndices:
    "ruc_pkey" PRIMARY KEY, btree (id_ruc)
    "ruc_ruc_key" UNIQUE CONSTRAINT, btree (ruc)



-- Tabla Antecedentes_Judiciales
CREATE TABLE Antecedentes_Judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) REFERENCES Personas_Cedulas(numero_cedula),
    causa_penal TEXT,
    fecha_causa DATE,
    unidad_procesadora VARCHAR(100),
    juez VARCHAR(100),
    estado_proceso VARCHAR(50),
    fuente VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tablas de negocio
CREATE TABLE zonas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    area geography(POLYGON, 4326),
    meta_ventas DECIMAL(12,2),
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vendedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_ingreso DATE NOT NULL,
    zona_id INTEGER REFERENCES zonas(id),
    comision_porcentaje DECIMAL(5,2) DEFAULT 0,
    meta_mensual DECIMAL(12,2),
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Actualizar referencia en usuarios
ALTER TABLE usuarios
ADD CONSTRAINT fk_usuarios_vendedores
FOREIGN KEY (vendedor_id) REFERENCES vendedores(id);


CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    numero_tarjeta VARCHAR(7) NOT NULL,	
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE,
    tipo_documento VARCHAR(10),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    ubicacion geography(POINT, 4326),
    zona_id INTEGER REFERENCES zonas(id),
    vendedor_id INTEGER REFERENCES vendedores(id),
    limite_credito DECIMAL(12,2) DEFAULT 0,
    categoria VARCHAR(20) DEFAULT 'REGULAR',
    fecha_registro DATE DEFAULT CURRENT_DATE,
    ultimo_contacto TIMESTAMP,
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    historial_compras JSONB DEFAULT '[]'::jsonb,
    preferencias JSONB DEFAULT '{}'::jsonb
);

-- Tabla Tarjetas (creamos esta tabla primero porque Clientes la referencia)
CREATE TABLE Tarjetas (
    id_tarjeta SERIAL PRIMARY KEY,
    numero_tarjeta VARCHAR(7) NOT NULL,
    id_cliente INTEGER,
    id_vendedor INTEGER REFERENCES Personas_Cedulas(id_persona),
    id_zona INTEGER,
    total_gs DECIMAL(10, 2) NOT NULL CHECK (total_gs > 0),
    saldo DECIMAL(10, 2) DEFAULT 0 CHECK (saldo >= 0),
    forma_pago VARCHAR(20) DEFAULT 'SEM' CHECK (forma_pago IN ('SEM', 'QUIN', 'MENS')),
    estado VARCHAR(20) DEFAULT 'activa' CHECK (estado IN ('activa', 'cancelada')),
    fecha_emision DATE DEFAULT CURRENT_DATE,
    local_laboral VARCHAR(100),
    barrio VARCHAR(100),
    ciudad VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT tarjeta_unique_active UNIQUE (numero_tarjeta, estado)
);

-- Tabla Marcas
CREATE TABLE Marcas (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    año_fundacion INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    id_marca INTEGER REFERENCES Marcas(id_marca),
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50),
    precio_costo DECIMAL(10,2) NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 5,
    stock_maximo INTEGER DEFAULT 100,
    fragancia VARCHAR(100),
    volumen_ml INTEGER,
    imagen_url VARCHAR(255),
    proveedor VARCHAR(100),
    tiempo_reposicion INTEGER, -- días
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE vehiculos (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INTEGER,
    motor VARCHAR(50) NOT NULL,
	chassis VARCHAR(50) NOT NULL,
    capacidad_kg DECIMAL(10,2),
    vendedor_id INTEGER REFERENCES vendedores(id),
    ultimo_mantenimiento DATE,
    proximo_mantenimiento DATE,
    kilometraje_actual INTEGER DEFAULT 0,
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    historial_mantenimiento JSONB DEFAULT '[]'::jsonb
);

CREATE TABLE rutas (
    id SERIAL PRIMARY KEY,
    vendedor_id INTEGER REFERENCES vendedores(id),
    vehiculo_id INTEGER REFERENCES vehiculos(id),
    fecha DATE NOT NULL,
    inicio_ruta geography(POINT, 4326),
    fin_ruta geography(POINT, 4326),
    distancia_km DECIMAL(10,2),
    tiempo_estimado INTEGER, -- minutos
    tiempo_real INTEGER,
    estado VARCHAR(20) DEFAULT 'planificada',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    CHECK (estado IN ('planificada', 'en_progreso', 'completada', 'cancelada'))
);

CREATE TABLE puntos_ruta (
    id SERIAL PRIMARY KEY,
    ruta_id INTEGER REFERENCES rutas(id),
    cliente_id INTEGER REFERENCES clientes(id),
    orden INTEGER NOT NULL,
    hora_planificada TIME,
    hora_real TIME,
    ubicacion geography(POINT, 4326),
    estado VARCHAR(20) DEFAULT 'pendiente',
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (estado IN ('pendiente', 'visitado', 'no_visitado', 'reprogramado'))
);

-- Tabla Productos_Vendidos
CREATE TABLE Productos_Vendidos (
    id_producto_vendido SERIAL PRIMARY KEY,
    id_tarjeta INTEGER REFERENCES Tarjetas(id_tarjeta),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER CHECK (cantidad > 0),
    precio DECIMAL(10, 2) CHECK (precio > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Maletines
CREATE TABLE Maletines (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Personas_Cedulas(id_persona),
    fecha_carga DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(20) DEFAULT 'activo' CHECK (estado IN ('activo', 'devuelto', 'perdido')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Productos_Maletin
CREATE TABLE Productos_Maletin (
    id_maletin INTEGER REFERENCES Maletines(id_maletin),
    id_producto INTEGER REFERENCES Productos(id_producto),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_maletin, id_producto)
);

-- Tabla Liquidaciones
CREATE TABLE Liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES Personas_Cedulas(id_persona),
    fecha_liquidacion DATE DEFAULT CURRENT_DATE,
    total_ventas DECIMAL(10, 2) DEFAULT 0,
    comision DECIMAL(10, 2) DEFAULT 0,
    total_pagar DECIMAL(10, 2) DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'aprobada', 'pagada')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    numero_factura VARCHAR(20) UNIQUE,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cliente_id INTEGER REFERENCES clientes(id),
    vendedor_id INTEGER REFERENCES vendedores(id),
    subtotal DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    impuesto DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    forma_pago VARCHAR(20),
    numero_cuotas INTEGER DEFAULT 1,
    estado VARCHAR(20) DEFAULT 'pendiente',
    punto_ruta_id INTEGER REFERENCES puntos_ruta(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    CHECK (estado IN ('pendiente', 'pagada', 'cancelada', 'anulada'))
);

CREATE TABLE detalles_venta (
    id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES ventas(id),
    producto_id INTEGER REFERENCES productos(id),
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    subtotal DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    venta_id INTEGER REFERENCES ventas(id),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto DECIMAL(10,2) NOT NULL,
    forma_pago VARCHAR(20) NOT NULL,
    numero_comprobante VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'procesado',
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    CHECK (estado IN ('procesado', 'anulado', 'rechazado'))
);

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

-- Tabla de Equipos
CREATE TABLE equipos (
    id_equipo SERIAL PRIMARY KEY,
    tipo VARCHAR(50) CHECK (tipo IN ('Lector Código Barras', 'Impresora Ticket', 'Impresora Matricial', 'Impresora Láser', 'Impresora Inyección')),
    marca VARCHAR(50),
    modelo VARCHAR(50),
    fecha_adquisicion DATE DEFAULT CURRENT_DATE
);

-- Tablas para funcionalidades futuras
CREATE TABLE notificaciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    titulo VARCHAR(100) NOT NULL,
    mensaje TEXT NOT NULL,
    tipo VARCHAR(20),
    leida BOOLEAN DEFAULT false,
    fecha_lectura TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE metas_ventas (
    id SERIAL PRIMARY KEY,
    vendedor_id INTEGER REFERENCES vendedores(id),
    zona_id INTEGER REFERENCES zonas(id),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    monto_objetivo DECIMAL(12,2) NOT NULL,
    monto_alcanzado DECIMAL(12,2) DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'activa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE promociones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    tipo VARCHAR(20),
    descuento DECIMAL(5,2),
    condiciones JSONB,
    estado BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_clientes_documento ON clientes(documento);
CREATE INDEX idx_clientes_zona ON clientes(zona_id);
CREATE INDEX idx_vendedores_zona ON vendedores(zona_id);
CREATE INDEX idx_ventas_cliente ON ventas(cliente_id);
CREATE INDEX idx_ventas_vendedor ON ventas(vendedor_id);
CREATE INDEX idx_ventas_fecha ON ventas(fecha);
CREATE INDEX idx_pagos_venta ON pagos(venta_id);
CREATE INDEX idx_rutas_vendedor ON rutas(vendedor_id);
CREATE INDEX idx_productos_codigo ON productos(codigo);
CREATE INDEX idx_productos_nombre ON productos USING gin(nombre gin_trgm_ops);

-- Índices espaciales
CREATE INDEX idx_zonas_area ON zonas USING GIST(area);
CREATE INDEX idx_clientes_ubicacion ON clientes USING GIST(ubicacion);
CREATE INDEX idx_rutas_inicio ON rutas USING GIST(inicio_ruta);
CREATE INDEX idx_rutas_fin ON rutas USING GIST(fin_ruta);
CREATE INDEX idx_puntos_ruta_ubicacion ON puntos_ruta USING GIST(ubicacion);

CREATE INDEX idx_personas_cedulas_numero_cedula ON Personas_Cedulas(numero_cedula);
CREATE INDEX idx_clientes_tarjeta ON Clientes(tarjeta);
CREATE INDEX idx_tarjetas_numero ON Tarjetas(numero_tarjeta);
CREATE INDEX idx_productos_vendidos_tarjeta ON Productos_Vendidos(id_tarjeta);
CREATE INDEX idx_tarjetas_ubicacion ON Tarjetas(local_laboral, barrio);
CREATE INDEX idx_pagos_fechas ON Pagos(fecha_control, fecha_entrega);
CREATE INDEX idx_rutas_gis ON Rutas USING GIST(coordenadas);
CREATE INDEX idx_zonas_gis ON Zonas USING GIST(geom);

-- Funciones útiles
CREATE OR REPLACE FUNCTION actualizar_stock() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE productos
    SET stock_actual = stock_actual - NEW.cantidad
    WHERE id = NEW.producto_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calcular_comision_vendedor() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE vendedores
    SET meta_mensual = meta_mensual + NEW.total * (comision_porcentaje / 100)
    WHERE id = NEW.vendedor_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER tr_actualizar_stock
AFTER INSERT ON detalles_venta
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock();

CREATE TRIGGER tr_calcular_comision
AFTER INSERT ON ventas
FOR EACH ROW
EXECUTE FUNCTION calcular_comision_vendedor();

-- Datos iniciales
INSERT INTO roles (nombre, descripcion) VALUES
('admin', 'Administrador del sistema'),
('vendedor', 'Vendedor con acceso a clientes y ventas'),
('supervisor', 'Supervisor de ventas'),
('contador', 'Acceso a información financiera'),
('almacen', 'Gestión de inventario');

INSERT INTO permisos (nombre, descripcion) VALUES
('crear_venta', 'Puede crear nuevas ventas'),
('ver_ventas', 'Puede ver listado de ventas'),
('modificar_venta', 'Puede modificar ventas existentes'),
('eliminar_venta', 'Puede eliminar ventas'),
('ver_reportes', 'Puede ver reportes del sistema'),
('gestionar_usuarios', 'Puede gestionar usuarios'),
('gestionar_productos', 'Puede gestionar productos'),
('ver_estadisticas', 'Puede ver estadísticas del sistema'),
('gestionar_rutas', 'Puede gestionar rutas de venta'),
('gestionar_inventario', 'Puede gestionar inventario');

-- Comentarios para documentación
COMMENT ON TABLE usuarios IS 'Almacena información de usuarios del sistema';
COMMENT ON TABLE ventas IS 'Registro de ventas realizadas';
COMMENT ON TABLE rutas IS 'Planificación de rutas de vendedores';
COMMENT ON TABLE productos IS 'Catálogo de productos disponibles';

-- Vista consolidada de relaciones cliente-tarjeta
CREATE OR REPLACE VIEW vista_cliente_tarjeta AS
SELECT 
    pc.numero_cedula,
    pc.nombre,
    pc.apellido,
    c.tarjeta AS numero_tarjeta_cliente,
    t.numero_tarjeta AS numero_tarjeta_activa,
    t.saldo,
    t.forma_pago,
    t.estado,
    z.nombre_zona
FROM Personas_Cedulas pc
JOIN Clientes c ON pc.id_persona = c.id_persona
LEFT JOIN Tarjetas t ON c.tarjeta = t.numero_tarjeta
LEFT JOIN Zonas z ON t.id_zona = z.id_zona;

-- Vista para control de pagos
CREATE OR REPLACE VIEW vista_control_pagos AS
SELECT 
    t.numero_tarjeta,
    c.nombre,
    p.fecha_control,
    p.fecha_entrega,
    p.monto_entrega,
    p.saldo_restante
FROM Tarjetas t
JOIN Clientes c ON t.id_cliente = c.id_cliente
JOIN Pagos p ON t.id_tarjeta = p.id_tarjeta
ORDER BY p.fecha_control;

-- =============================================
-- PERMISOS
-- =============================================

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO current_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO current_user;

Sistema de Base de Datos:

Gestión geoespacial:
Soporte para PostGIS
Almacenamiento de polígonos de zonas de venta
Registro de ubicaciones de clientes
Tracking de rutas de vendedores

Gestión de ventas:
Control de vendedores y sus zonas asignadas
Registro de clientes
Sistema de ventas y pagos
Control de cuotas y estados de pago


Logística:
Gestión de vehículos
Planificación de rutas
Seguimiento de visitas a clientes
Control de stock

Optimización:
Índices espaciales para consultas geográficas eficientes
Índices estándar para relaciones frecuentes
Restricciones para mantener la integridad de datos

Consultas útiles para:
Calcular rutas óptimas por zona
Análisis de ventas por territorio
Seguimiento de pagos de clientes

Tablas para usuarios, roles y permisos
Sistema de sesiones seguro
Registro de actividad (logs)
Roles predefinidos con permisos específicos
Índices para optimizar consultas


Interfaz de Usuario:

Mantiene la estética del diseño original:
Uso de color verde suave de fondo
Logo elegante con la Torre Eiffel
Tipografía IBM Plex Mono para los campos de datos
Diseño de tarjeta estructurado

Incluye todas las secciones importantes:
Información de la empresa
Datos del cliente y producto
Tabla de control de pagos
Sección para firma y documentación

Características funcionales:
Campos de entrada para toda la información necesaria
Tabla de pagos dinámica
Checkboxes para forma de pago
Responsive design

Mejoras sobre el original:
Campos de entrada validados
Mejor legibilidad
Espaciado optimizado
Mantiene la esencia vintage pero con toques modernos

Pantalla de login
Manejo de sesión de usuario
Información del usuario activo
Botón de cierre de sesión
Registro de última actividad

Seguridad:
Almacenamiento seguro de contraseñas (hash)
Control de intentos fallidos
Sistema de bloqueo de cuentas
Tokens de sesión
Registro de IP y User Agent

Características adicionales:
Roles diferentes para distintos niveles de acceso
Sistema de permisos granular
Registro de actividad detallado
Conexión entre usuarios y vendedores

Para implementar completamente el sistema, necesitarías:
Crear un API REST para:
Autenticación
CRUD de usuarios
Gestión de sesiones
Verificación de permisos

Implementar middleware de autenticación
Configurar un sistema de tokens JWT

Integración de seguridad y usabilidad:
Sistema de autenticación robusto pero amigable
Interfaz que mantiene la estética original mientras moderniza la funcionalidad
Base de datos bien estructurada con relaciones claras

Atención al detalle:
Uso consistente de la tipografía IBM Plex Mono
Mantener la identidad visual con la Torre Eiffel
Colores y estilos que reflejan la marca

Funcionalidad empresarial:
Sistema de roles y permisos escalable
Tracking de actividades
Gestión geoespacial para rutas de venta

Para futuros desarrollos, podríamos considerar:
Dashboard administrativo
Sistema de reportes
App móvil para vendedores
Integración con sistemas de mapas
Sistema de notificaciones

-- Índices para optimizar consultas frecuentes
CREATE INDEX idx_productos_marca ON Productos(ID_Marca);
CREATE INDEX idx_ventas_cliente ON Ventas(ID_Cliente);
CREATE INDEX idx_ventas_fecha ON Ventas(Fecha_Venta);
CREATE INDEX idx_inventario_producto ON Inventario(ID_Producto);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_clientes_cedula ON clientes(cedula);
CREATE INDEX idx_clientes_ruc ON clientes(ruc);
CREATE INDEX idx_productos_codigo_barras ON productos(codigo_barras);
CREATE INDEX idx_ventas_fecha ON ventas(fecha_venta);
CREATE INDEX idx_empleados_cargo ON empleados(cargo);
CREATE INDEX idx_cliente_cedula ON Cliente(cedula);

-- Trigger que ejecuta la función al insertar una venta
CREATE TRIGGER tg_actualizar_saldo
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_saldo_cliente();
CREATE OR REPLACE FUNCTION actualizar_stock_producto() 
RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.cantidad > (SELECT stock FROM Productos WHERE id_producto = NEW.id_producto)) THEN
        RAISE EXCEPTION 'No hay suficiente stock para este producto';
    ELSE
        UPDATE Productos 
        SET stock = stock - NEW.cantidad 
        WHERE id_producto = NEW.id_producto;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION actualizar_saldo_cliente() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Clientes 
    SET saldo = saldo - NEW.total
    WHERE id_cliente = NEW.id_cliente;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que ejecuta la función al insertar una venta
CREATE TRIGGER tg_actualizar_stock
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock_producto();

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

-- Trigger para actualizar el stock al vender
CREATE OR REPLACE FUNCTION actualizar_stock() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.cantidad > OLD.stock THEN
        RAISE EXCEPTION 'No hay suficiente stock';
    ELSE
        UPDATE Inventario SET stock = stock - NEW.cantidad WHERE id_presentacion = NEW.id_presentacion;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_stock
AFTER INSERT ON DetalleVenta
FOR EACH ROW EXECUTE FUNCTION actualizar_stock();

CREATE OR REPLACE FUNCTION actualizar_saldo_cliente() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Clientes 
    SET saldo = saldo - NEW.total
    WHERE id_cliente = NEW.id_cliente;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Vistas para reportes comunes
CREATE VIEW VW_Ventas_Por_Cliente AS
SELECT 
    c.ID_Cliente, 
    c.Nombre, 
    c.Apellido, 
    COUNT(v.ID_Venta) AS Total_Ventas, 
    SUM(v.Total) AS Monto_Total
FROM 
    Clientes c
LEFT JOIN 
    Ventas v ON c.ID_Cliente = v.ID_Cliente
GROUP BY 
    c.ID_Cliente;

CREATE VIEW VW_Stock_Productos AS
SELECT 
    p.ID_Producto, 
    p.Nombre, 
    m.Nombre AS Marca, 
    p.Stock, 
    p.Precio_Venta
FROM 
    Productos p
JOIN 
    Marcas m ON p.ID_Marca = m.ID_Marca;

-- Trigger para verificar si un cliente tiene antecedentes judiciales
CREATE OR REPLACE FUNCTION verificar_antecedentes() 
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM AntecedentesJudiciales WHERE cedula = NEW.cedula) THEN
        RAISE NOTICE 'El cliente con cédula % tiene antecedentes judiciales', NEW.cedula;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_verificar_antecedentes
BEFORE INSERT ON Clientes
FOR EACH ROW
EXECUTE FUNCTION verificar_antecedentes();

-- Trigger para actualizar la comisión de las vendedoras tras una venta
CREATE OR REPLACE FUNCTION actualizar_comision_vendedora() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Liquidaciones 
    SET total_ventas = total_ventas + NEW.total,
        comision = comision + (50000 * NEW.cantidad)  -- Comisión por producto
    WHERE id_vendedor = NEW.id_vendedor;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_actualizar_comision
AFTER INSERT ON Ventas
FOR EACH ROW
EXECUTE FUNCTION actualizar_comision_vendedora();

-- Índices faltantes para optimización de consultas
CREATE INDEX idx_rutas_vendedor_fecha ON Rutas(id_vendedor, fecha);
CREATE INDEX idx_pagos_cliente_metodo ON Pagos(id_cliente, metodo_pago);
CREATE INDEX idx_antecedentes_cedula ON AntecedentesJudiciales(cedula);
CREATE INDEX idx_inventario_maletines_producto ON Inventario_Maletines(id_maletin, id_producto);
CREATE INDEX idx_vehiculos_motor_chasis_placa ON Vehiculos(numero_motor, numero_chasis, placa);

-- Trigger para verificar si un cliente tiene antecedentes judiciales

CREATE OR REPLACE FUNCTION verificar_antecedentes() 

RETURNS TRIGGER AS $$

BEGIN

    IF EXISTS (SELECT 1 FROM AntecedentesJudiciales WHERE cedula = NEW.cedula) THEN

        RAISE NOTICE 'El cliente con cédula % tiene antecedentes judiciales', NEW.cedula;

    END IF;

    RETURN NEW;

END;

$$ LANGUAGE plpgsql;


CREATE TRIGGER tg_verificar_antecedentes

BEFORE INSERT ON Clientes

FOR EACH ROW

EXECUTE FUNCTION verificar_antecedentes();


-- Trigger para actualizar la comisión de las vendedoras tras una venta

CREATE OR REPLACE FUNCTION actualizar_comision_vendedora() 

RETURNS TRIGGER AS $$

BEGIN

    UPDATE Liquidaciones 

    SET total_ventas = total_ventas + NEW.total,

        comision = comision + (50000 * NEW.cantidad)  -- Comisión por producto

    WHERE id_vendedor = NEW.id_vendedor;

    RETURN NEW;

END;

$$ LANGUAGE plpgsql;


CREATE TRIGGER tg_actualizar_comision

AFTER INSERT ON Ventas

FOR EACH ROW

EXECUTE FUNCTION actualizar_comision_vendedora();


-- Índices faltantes para optimización de consultas

CREATE INDEX idx_rutas_vendedor_fecha ON Rutas(id_vendedor, fecha);

CREATE INDEX idx_pagos_cliente_metodo ON Pagos(id_cliente, metodo_pago);

CREATE INDEX idx_antecedentes_cedula ON AntecedentesJudiciales(cedula);

CREATE INDEX idx_inventario_maletines_producto ON Inventario_Maletines(id_maletin, id_producto);

CREATE INDEX idx_vehiculos_motor_chasis_placa ON Vehiculos(numero_motor, numero_chasis, placa);

Trigger verificar_antecedentes

    Función: Verifica si un cliente tiene antecedentes judiciales al momento de registrarse.
    Observación: Es una función sencilla y efectiva para su propósito. El uso de RAISE NOTICE es útil para informar sobre la existencia de antecedentes, pero en un entorno productivo, podrías considerar registrar esta información en un log o enviar una notificación a un usuario específico.

Trigger actualizar_comision_vendedora

    Función: Actualiza la comisión de una vendedora cada vez que se registra una nueva venta.
    Observaciones:
        Cálculo de la comisión: La fórmula (50000 * NEW.cantidad) asume que la comisión es fija por producto. Si la comisión varía según el producto o la vendedora, deberías ajustar esta lógica.
        Tabla Liquidaciones: ¿La tabla Liquidaciones se actualiza con cada venta o se utiliza para calcular comisiones periódicamente? Si se actualiza con cada venta, podrías considerar agrupar las ventas por vendedor y periodo para generar un resumen más preciso de las comisiones.
        Concurrencia: Si hay múltiples transacciones simultáneas, este trigger podría generar problemas de concurrencia al actualizar la misma fila en la tabla Liquidaciones. Podrías utilizar transacciones o bloqueos para evitar esto.

Análisis de los Índices

    Función: Los índices mejoran el rendimiento de las consultas al reducir la cantidad de datos que deben ser escaneados.
    Observaciones:
        Selección de columnas: Los índices creados parecen estar bien seleccionados, considerando las columnas más utilizadas en las consultas.
        Cardinalidad: Es importante monitorear la cardinalidad de los índices (cantidad de valores únicos) para asegurar que estén siendo utilizados de manera eficiente.
        Tamaño de la tabla: Si las tablas son muy grandes, podrías considerar crear índices compuestos o particionar las tablas para mejorar el rendimiento.

Sugerencias Adicionales

    Redundancia: Revisa si hay columnas que contienen información redundante. Por ejemplo, si el nombre y apellido del cliente están almacenados tanto en la tabla Clientes como en la tabla Ventas, podrías eliminar esta redundancia para reducir el espacio de almacenamiento y mejorar la integridad de los datos.
    Normalización: Asegúrate de que las tablas estén normalizadas para evitar anomalías de datos y mejorar la integridad.
    Optimización de consultas: Analiza las consultas más frecuentes y utiliza herramientas como EXPLAIN para identificar cuellos de botella y optimizar el rendimiento.
    Pruebas: Realiza pruebas exhaustivas para verificar que los triggers y funciones funcionen correctamente y no introduzcan errores en la base de datos.

Preguntas para Aclarar

    ¿Cuál es la estructura completa de las tablas involucradas (campos, tipos de datos, relaciones)?
    ¿Qué tipo de consultas se realizan con mayor frecuencia?
    ¿Hay algún requisito específico de rendimiento o escalabilidad?
    ¿Se utilizan otras herramientas de base de datos, como vistas o funciones materializadas?

Ejemplo de Optimización del Trigger actualizar_comision_vendedora:
SQL

CREATE OR REPLACE FUNCTION actualizar_comision_vendedora() 
RETURNS TRIGGER AS $$
BEGIN
    -- Utilizar una transacción para garantizar la consistencia de los datos
    BEGIN
        UPDATE Liquidaciones 
        SET total_ventas = total_ventas + NEW.total,
            comision = comision + (SELECT comisión_por_producto FROM Productos WHERE id_producto = NEW.id_producto) * NEW.cantidad
        WHERE id_vendedor = NEW.id_vendedor;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE NOTICE 'Error al actualizar la comisión: %', SQLERRM;
    END;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

Usa el código con precaución.

Este ejemplo muestra cómo calcular la comisión de forma más flexible, utilizando una tabla Productos para obtener la comisión por producto. También incluye una transacción para garantizar la consistencia de los datos en caso de errores.

Espero que estas observaciones y sugerencias te sean útiles. ¡No dudes en hacer más preguntas!
foto de perfil

podrías presentar el código completo con tus mejoras

¡Absolutamente! Basándome en el análisis anterior y las sugerencias proporcionadas, aquí te presento una versión mejorada del código, incorporando las mejoras discutidas y adaptándolo a un escenario más completo:

Consideraciones Adicionales:

    Estructura de tablas: Asumí una estructura de tablas simplificada para este ejemplo. Adapta las tablas y relaciones a tu modelo de datos real.
    Cálculo de comisiones: Se ha introducido una tabla Comisiones para almacenar las comisiones por producto, lo que permite una mayor flexibilidad en el cálculo.
    Logueo de eventos: Se ha agregado un log para registrar los eventos importantes, como la detección de antecedentes judiciales o errores en la actualización de comisiones.
    Manejo de errores: Se han incluido bloques EXCEPTION para manejar errores de manera más robusta.
    Optimizaciones adicionales: Se pueden realizar más optimizaciones dependiendo de la complejidad de tu aplicación y las características del sistema de base de datos.

Código Mejorado:
SQL

-- Tabla para almacenar las comisiones por producto
CREATE TABLE Comisiones (
    id_producto INTEGER,
    comision NUMERIC,
    PRIMARY KEY (id_producto),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- Función para registrar eventos en un log
CREATE OR REPLACE FUNCTION registrar_evento(evento TEXT)
RETURNS VOID AS $$
BEGIN
    INSERT INTO Log (fecha, evento) VALUES (NOW(), evento);
END;
$$ LANGUAGE plpgsql;

-- Trigger para verificar antecedentes judiciales y registrar en el log
CREATE OR REPLACE FUNCTION verificar_antecedentes() 
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM AntecedentesJudiciales WHERE cedula = NEW.cedula) THEN
        RAISE NOTICE 'El cliente con cédula % tiene antecedentes judiciales', NEW.cedula;
        PERFORM registrar_evento('Cliente con antecedentes: ' || NEW.cedula);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar la comisión de las vendedoras tras una venta
CREATE OR REPLACE FUNCTION actualizar_comision_vendedora() 
RETURNS TRIGGER AS $$
BEGIN
    BEGIN
        UPDATE Liquidaciones 
        SET total_ventas = total_ventas + NEW.total,
            comision = comision + (SELECT comision FROM Comisiones WHERE id_producto = NEW.id_producto) * NEW.cantidad
        WHERE id_vendedor = NEW.id_vendedor;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            PERFORM registrar_evento('Error al actualizar comisión: ' || SQLERRM);
    END;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Índices adicionales (adapta según tu esquema)
CREATE INDEX idx_liquidaciones_vendedor ON Liquidaciones(id_vendedor);
CREATE INDEX idx_comisiones_producto ON Comisiones(id_producto);

Usa el código con precaución.

Explicación de los cambios:

    Tabla Comisiones: Esta tabla almacena la comisión por producto, permitiendo una gestión más flexible y escalable de las comisiones.
    Función registrar_evento: Esta función simplifica el registro de eventos en un log, lo que puede ser útil para la auditoría y la resolución de problemas.
    Trigger verificar_antecedentes: Se ha agregado una llamada a registrar_evento para documentar la detección de antecedentes judiciales.
    Trigger actualizar_comision_vendedora: Se utiliza la tabla Comisiones para obtener la comisión por producto y se ha mejorado el manejo de errores con un bloque EXCEPTION.
    Índices adicionales: Se ha agregado un índice en la tabla Liquidaciones para mejorar el rendimiento de las actualizaciones de comisiones.

Consideraciones Futuras:

    Optimización de consultas: Utiliza herramientas como EXPLAIN para identificar consultas lentas y optimizarlas.
    Particionamiento: Si las tablas son muy grandes, considera particionarlas para mejorar el rendimiento de las consultas.
    Materialización de vistas: Si hay consultas que se ejecutan con frecuencia, puedes considerar materializarlas como vistas para mejorar el rendimiento.
    Monitoreo: Implementa un sistema de monitoreo para identificar problemas de rendimiento y detectar anomalías en los datos.

Adaptación a tu Esquema:

    Ajuste de tablas y columnas: Asegúrate de que las tablas y columnas coincidan con tu esquema de base de datos.
    Modificación de funciones y triggers: Adapta las funciones y triggers para que se ajusten a tu lógica de negocio específica.
    Creación de índices: Crea índices en las columnas que se utilizan frecuentemente en las cláusulas WHERE, JOIN y ORDER BY de tus consultas.

Recuerda: Esta es solo una propuesta. La optimización de una base de datos es un proceso iterativo que requiere un profundo conocimiento de tu aplicación y de las características del sistema de base de datos que estás utilizando.

¿Te gustaría profundizar en alguna parte específica del código o explorar otras opciones de optimización?
foto de perfil

excelente, has visto las tablas

¡Absolutamente! Basándome en el código que hemos analizado, puedo inferir una estructura de tablas general para Gabriela Fragancias. Sin embargo, para poder ofrecerte una respuesta más precisa y personalizada, te pediría que me confirmes o corrijas la siguiente estructura:

Posible estructura de tablas:

    Clientes: id_cliente (PK), nombre, apellido, cedula, dirección, teléfono
    Ventas: id_venta (PK), fecha, total, id_cliente (FK), id_vendedor (FK)
    Productos: id_producto (PK), nombre, precio
    Ventas_Detalle: id_venta_detalle (PK), cantidad, id_venta (FK), id_producto (FK)
    Vendedores: id_vendedor (PK), nombre, apellido, comisión_base
    Liquidaciones: id_liquidacion (PK), fecha_inicio, fecha_fin, total_ventas, comision, id_vendedor (FK)
    AntecedentesJudiciales: id_antecedente (PK), descripcion, cedula (FK)
    Rutas: id_ruta (PK), fecha, id_vendedor (FK)
    Pagos: id_pago (PK), fecha, monto, metodo_pago, id_venta (FK)
    Inventario_Maletines: id_inventario_maletin (PK), cantidad, id_maletin (FK), id_producto (FK)
    Maletines: id_maletin (PK), descripcion
    Vehiculos: id_vehiculo (PK), numero_motor, numero_chasis, placa

Relaciones:

    Una venta puede tener muchos productos (relación muchos a muchos a través de Ventas_Detalle).
    Un cliente puede realizar muchas ventas.
    Un vendedor puede realizar muchas ventas y tener muchas rutas.
    Un pago está asociado a una venta.
    Un inventario de maletines contiene varios productos.
