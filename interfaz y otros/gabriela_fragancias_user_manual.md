
# Manual de Usuario para el Sistema de Gestión de Gabriela Fragancias

## Índice
1. [Introducción](#introduccion)
2. [Instalación](#instalacion)
3. [Configuración de la Base de Datos](#configuracion-db)
4. [Uso de la Interfaz de Usuario](#uso-interfaz)
5. [Funcionalidades Principales](#funcionalidades)

---

## 1. Introducción <a name="introduccion"></a>
Este sistema de gestión permite a Gabriela Fragancias manejar su base de datos de productos, clientes, pagos y otros componentes críticos. El sistema incluye una interfaz de usuario adaptativa que facilita la gestión de datos y se ajusta a los roles definidos en la empresa.

## 2. Instalación <a name="instalacion"></a>
1. **Requisitos**: PostgreSQL, Node.js, y cualquier otro requisito de la interfaz gráfica.
2. **Instalación de Dependencias**: Ejecute `npm install` en la carpeta de la interfaz.
3. **Base de Datos**: Use el archivo SQL proporcionado para configurar la base de datos.

## 3. Configuración de la Base de Datos <a name="configuracion-db"></a>
Ejecute los siguientes comandos en PostgreSQL para crear las extensiones necesarias:
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```
Luego, importe el archivo SQL incluido para crear las tablas y configuraciones de datos.

## 4. Uso de la Interfaz de Usuario <a name="uso-interfaz"></a>
### Acceso
1. **Inicio de Sesión**: Ingrese su nombre de usuario y contraseña.
2. **Roles**: Las opciones de la interfaz varían según el rol (Administrador, Vendedor, etc.).

## 5. Funcionalidades Principales <a name="funcionalidades"></a>
- **Gestión de Clientes**: Añadir, editar y visualizar información de clientes.
- **Control de Productos**: Crear y actualizar productos.
- **Pagos y Liquidaciones**: Procesar pagos y revisar historial.
- **Estadísticas**: Acceso a reportes visuales y gráficos de ventas.

---

### Notas
Asegúrese de realizar copias de seguridad de la base de datos periódicamente.
