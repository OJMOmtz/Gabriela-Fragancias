# Manual de Usuario - Base de Datos Gabriela Fragancias

## Introducción
Este manual describe la instalación, uso, y mantenimiento de la base de datos para Gabriela Fragancias, así como las consultas y reportes básicos para gestionar clientes, productos, ventas y más.

## Instalación
1. Cargar el archivo SQL `gabriela_fragancias_schema.sql` en su sistema de base de datos PostgreSQL.
2. Crear la base de datos y las tablas ejecutando el archivo SQL.

## Uso Básico de la Interfaz
### Clientes
- **Registro de Cliente:** Añada los detalles del cliente, como nombre, apellido, cédula y datos de contacto.

### Productos
- **Gestión de Productos:** Administre el inventario de productos, incluyendo el stock y el precio.

### Ventas
- **Registrar Ventas:** Añada ventas y detalles, asignando productos a cada cliente.

## Consultas y Reportes
- **Top Productos Vendidos:** Utilice la función `perfume_mas_vendido` para obtener los productos más vendidos en un rango de fechas.
- **Balance de Clientes:** Consulte el saldo restante para cada cliente usando la vista `VW_Balance_Clientes`.

## Mantenimiento
- **Respaldos y Restauración:** Realice respaldos periódicos de la base de datos para asegurar la integridad de la información.
- **Optimización:** Monitoree el rendimiento de la base de datos y ajuste índices según el uso.

**Para más detalles y ejemplos de uso, consulte el archivo completo.**