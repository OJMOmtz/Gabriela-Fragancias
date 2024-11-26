-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- Para búsquedas textuales mejoradas

-- Configuración de esquema
CREATE SCHEMA IF NOT EXISTS Gabriela_Fragancias;
SET search_path TO Gabriela_Fragancias, public;
-- Tabla Empresa
CREATE TABLE empresa (
    id_empresa SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    email VARCHAR(100)
);

-- Tabla Usuario
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL
);

-- Tabla de Clientes
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    email VARCHAR(100),
    id_zona INTEGER REFERENCES zona(id_zona)
);

-- Tabla de Productos
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2),
    id_marca INTEGER REFERENCES marcas(id_marca),
    id_perfumista INTEGER REFERENCES perfumistas(id_perfumista)
);

-- Tabla de Vendedores
CREATE TABLE vendedores (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    id_zona INTEGER REFERENCES zona(id_zona)
);

-- Tabla de Inventario por Vendedora
CREATE TABLE inventario_vendedora (
    id_inventario SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER
);

-- Tabla de Ventas
CREATE TABLE ventas (
    id_venta SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    total DECIMAL(10, 2)
);

-- Tabla de Rutas
CREATE TABLE rutas (
    id_ruta SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor)
);

-- Tabla Cédula
CREATE TABLE cedula (
    id_cedula SERIAL PRIMARY KEY,
    numero_cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL
);

-- Tabla AntecedentesJudiciales
CREATE TABLE antecedentes_judiciales (
    id_antecedente SERIAL PRIMARY KEY,
    id_cedula INTEGER REFERENCES cedula(id_cedula),
    descripcion TEXT
);

-- Tabla de RUC
CREATE TABLE ruc (
    id_ruc SERIAL PRIMARY KEY,
    numero_ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(100) NOT NULL
);

-- Tabla Presentacion
CREATE TABLE presentacion (
    id_presentacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de Maletines de Vendedoras
CREATE TABLE maletines_vendedoras (
    id_maletin SERIAL PRIMARY KEY,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    id_presentacion INTEGER REFERENCES presentacion(id_presentacion)
);

-- Tabla Productos de Maletines
CREATE TABLE productos_maletines (
    id_producto_maletin SERIAL PRIMARY KEY,
    id_maletin INTEGER REFERENCES maletines_vendedoras(id_maletin),
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER
);

-- Tabla de Liquidaciones
CREATE TABLE liquidaciones (
    id_liquidacion SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    id_vendedor INTEGER REFERENCES vendedores(id_vendedor),
    total DECIMAL(10, 2)
);

-- Tabla de Vehículos
CREATE TABLE vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    placa VARCHAR(20) UNIQUE NOT NULL
);

-- Tabla de Gastos de Vehículos
CREATE TABLE gastos_vehiculos (
    id_gasto SERIAL PRIMARY KEY,
    id_vehiculo INTEGER REFERENCES vehiculos(id_vehiculo),
    fecha DATE NOT NULL,
    descripcion TEXT,
    monto DECIMAL(10, 2)
);

-- Tabla RutaVenta
CREATE TABLE ruta_venta (
    id_ruta_venta SERIAL PRIMARY KEY,
    id_ruta INTEGER REFERENCES rutas(id_ruta),
    id_venta INTEGER REFERENCES ventas(id_venta)
);

-- Tabla de Tracking GPS
CREATE TABLE tracking_gps (
    id_tracking SERIAL PRIMARY KEY,
    id_vehiculo INTEGER REFERENCES vehiculos(id_vehiculo),
    fecha_hora TIMESTAMP NOT NULL,
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8)
);

-- Tabla de Proveedores
CREATE TABLE proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    email VARCHAR(100)
);

-- Tabla de Compras a Proveedores
CREATE TABLE compras_proveedores (
    id_compra SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    id_proveedor INTEGER REFERENCES proveedores(id_proveedor),
    total DECIMAL(10, 2)
);

-- Tabla de Detalles de Compra
CREATE TABLE detalles_compra (
    id_detalle_compra SERIAL PRIMARY KEY,
    id_compra INTEGER REFERENCES compras_proveedores(id_compra),
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER,
    precio DECIMAL(10, 2)
);

-- Tabla Departamento
CREATE TABLE departamento (
    id_departamento SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla Municipio
CREATE TABLE municipio (
    id_municipio SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_departamento INTEGER REFERENCES departamento(id_departamento)
);

-- Tabla Zona
CREATE TABLE zona (
    id_zona SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_municipio INTEGER REFERENCES municipio(id_municipio)
);

-- Tabla Ubicacion
CREATE TABLE ubicacion (
    id_ubicacion SERIAL PRIMARY KEY,
    latitud DECIMAL(10, 8),
    longitud DECIMAL(11, 8),
    id_zona INTEGER REFERENCES zona(id_zona)
);

-- Tabla de Marcas
CREATE TABLE marcas (
    id_marca SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de Perfumistas
CREATE TABLE perfumistas (
    id_perfumista SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de Notas Olfativas
CREATE TABLE notas_olfativas (
    id_nota SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de relación entre Productos y Notas Olfativas
CREATE TABLE productos_notas_olfativas (
    id_producto_nota SERIAL PRIMARY KEY,
    id_producto INTEGER REFERENCES productos(id_producto),
    id_nota INTEGER REFERENCES notas_olfativas(id_nota)
);

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