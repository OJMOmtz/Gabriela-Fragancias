-- Tabla Marca
CREATE TABLE Marca (
    id_marca SERIAL PRIMARY KEY,
    nombre_marca VARCHAR(100) NOT NULL,
    ano_fundacion INTEGER,
    sede VARCHAR(100)
);

-- Tabla Perfume
CREATE TABLE Perfume (
    id_perfume SERIAL PRIMARY KEY,
    nombre_perfume VARCHAR(200) NOT NULL,
    id_marca INTEGER REFERENCES Marca(id_marca),
    costo DECIMAL(10, 2),
    precio_venta_credito DECIMAL(10, 2),
    precio_venta_contado DECIMAL(10, 2),
    segmento VARCHAR(50),
    franja_etaria VARCHAR(50),
    ocasion VARCHAR(50),
    ano_lanzamiento INTEGER,
    perfumero VARCHAR(100),
    notas_olfativas TEXT,
    notas_salida TEXT,
    notas_corazon TEXT,
    notas_fondo TEXT,
    intensidad VARCHAR(20),
    concentracion VARCHAR(20),
    duracion VARCHAR(50),
    estilo VARCHAR(50),
    imagen_url VARCHAR(255)
);

-- Tabla Presentacion
CREATE TABLE Presentacion (
    id_presentacion SERIAL PRIMARY KEY,
    id_perfume INTEGER REFERENCES Perfume(id_perfume) ON DELETE CASCADE,
    codigo_barra VARCHAR(50) UNIQUE NOT NULL,
    tamano_ml INTEGER CHECK (tamano_ml > 0),
    imagen_url VARCHAR(255)
);
#Estos datos son relevantes para las tablas de arriba
Marca 	Producto 	Segmento 	Ocasión 	Notas Destacadas 	Intensidad 	Duración 	Estilo 	Concentración 	Imagen
Adidas 	Ice Dive 	Masculino, Juvenil 	Deportivo, Casual 	Menta, Lavanda, Notas Marinas 	Moderada 	4-6 horas 	Fresco, Energético 	EDT
Adidas 	Team Five Special Edition 	Juvenil, Masculino 	Deportivo 	Cítricos, Aromáticos 	Moderada 	4-6 horas 	Fresco, Energético 	EDT
Marca 	Año de Creación 	Perfumero(s) 	Producto Emblemático 	Composición Olfativa 	Público Objetivo 	Descripción Breve 	Presentaciones 	Imagen (URL)
Adidas 	1949 	Varios 	Adidas Moves 	Aromático Fresco 	Deportistas y público joven 	Fragancia energizante, ideal para después de hacer deporte 	30ml, 50ml, 100ml 	URL de la imagen
-- Tabla Marca
INSERT INTO Marca (id_marca, nombre_marca) VALUES (1, 'Adidas');

-- Tabla Perfume
INSERT INTO Perfume (id_perfume, nombre_perfume, id_marca, ano_lanzamiento, perfumero, notas_olfativas, costo, precio_venta_contado, precio_venta_credito, segmento, franja_etaria, ocasion) 
VALUES 
(1, 'Adidas Ice Dive', 1, 2020, 'Alberto Morillas', 'Fresco y deportivo', 15.00, 28.00, 30.00, 'Deportivo', '18-30', 'Casual');

-- Tabla Presentacion
INSERT INTO Presentacion (id_presentacion, id_perfume, codigo_barra, tamano_ml) 
VALUES 
(1, 1, '8411114079707', 50),
(2, 1, '8411114079708', 100);

-- Tabla Cédula
CREATE TABLE Cedula (
    id_cedula SERIAL PRIMARY KEY,
    numero_ci VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT NOT NULL
);

-- Tabla AntecedentesJudiciales
CREATE TABLE AntecedentesJudiciales (
    id_antecedente SERIAL PRIMARY KEY,
    numero_ci VARCHAR(20) REFERENCES Cedula(numero_ci),
    causa_penal TEXT
);

-- Tabla Cliente
CREATE TABLE Cliente (
    id_cliente SERIAL PRIMARY KEY,
	tarjeta VARCHAR(5),
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula_ruc VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) CHECK (email LIKE '%_@_%._%'),
    telefono VARCHAR(20),
    direccion TEXT,
    tipo_pago VARCHAR(20),
    grupo_economico VARCHAR(50),
    sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
    edad INTEGER CHECK (edad >= 18)
);

-- Tabla Vendedor
CREATE TABLE Vendedor (
    id_vendedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cedula VARCHAR(20) UNIQUE,
    telefono VARCHAR(20),
    zona VARCHAR(50)
);
#Estas deben traer datos de distintas tablas que deben unificarse y limpiarse, en algunos casos agregar columnas que faltan.
al crear la sql cédulas hay que considerar estas necesidades de los datos a extraer de las dbf
poli01.pdf
Columna: NROCED, Tipo: N
Columna: APELLI, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: FECHANAC, Tipo: N
Columna: DOMICILIO, Tipo: C

regciv.dbf
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N

cap001.dbf
Columna: CIDCAP, Tipo: N
Columna: ORDEN, Tipo: N
Columna: CAUSA, Tipo: C
Tienes estas tres columnas que nos interesan. En la primera se tiene el número de cédula, en la seguda la orden de captura y en la tercera la causa. En la base de datos cédula, debe conectarse con el número de cédula para obtener el nombre, apellido y dirección. La causa debe aparecer con una alerta para evitar fraudes.

deshabilitados.dbf
Columna: OBS, Tipo: C 
debe aparecer con una alerta para evitar fraudes.
desh_exte.dbf
Columna: DESCRI_EST, Tipo: C
debe aparecer con una alerta para evitar fraudes.
pol_y_mil.dbf
Columna: TIPO, Tipo: C
Columna: GRADO, Tipo: C
debe aparecer  con una alerta para conocer el tipo y grado si es policía o militar
difuntos.dbf
Columna: FEC_DEF, Tipo: D
debe aparecer con una alerta "DIFUNTO" con la fecha de defunción para evitar fraudes.

Estructura de la tabla DBF 'D:\PADRONES\Automotores\cap001.dbf':
Columna: CIDCAP, Tipo: N
Columna: ORDEN, Tipo: N
Columna: CLAVE, Tipo: N
Columna: CAUSA, Tipo: C
Columna: UNIDAD, Tipo: N
Columna: FECNOTA, Tipo: N
Columna: NRONOTA, Tipo: N
Columna: COMPETE, Tipo: N
Columna: TURNO, Tipo: N
Columna: CIRCUN, Tipo: N
Columna: LUGARH, Tipo: C
Columna: JUEZ, Tipo: C
Columna: SECRETA, Tipo: C
Columna: INTERINO, Tipo: N
Columna: FECHAGRA, Tipo: N
Columna: USUARIO, Tipo: C
Columna: HORAGRA, Tipo: N
Columna: ESTADO, Tipo: C
Columna: OBSERVA, Tipo: C
Columna: RADIO, Tipo: C
Columna: FECRADIO, Tipo: N
Columna: UNIDAINF, Tipo: N
Columna: NOBRE, Tipo: C
Columna: GUARDI, Tipo: C
Columna: HORAGUA, Tipo: N
Columna: CREDEN, Tipo: N
Columna: SITU, Tipo: C
Columna: TIPOSE, Tipo: C
Columna: NROSE, Tipo: N

Estructura de la tabla DBF 'D:\PADRONES\Automotores\poli01.dbf':
Columna: NROCED, Tipo: N
Columna: NROPRO, Tipo: N
Columna: APELLI, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: IC, Tipo: C
Columna: ESTADO, Tipo: N
Columna: FECHANAC, Tipo: N
Columna: SEXO, Tipo: N
Columna: PROFESION, Tipo: N
Columna: LUGNAC, Tipo: C
Columna: NACIO, Tipo: N
Columna: NOMPAD, Tipo: C
Columna: NOMMAD, Tipo: C
Columna: NOMCONJ, Tipo: C
Columna: DOMICILIO, Tipo: C
Columna: NROPROPEN, Tipo: N
Columna: UBICACION, Tipo: N
Columna: USUARIO, Tipo: C
Columna: FECHAGRA, Tipo: N
Columna: SITUACION, Tipo: N
Columna: FECHAIMP, Tipo: N

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\deshabilitados.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: OBS, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\desh_exte.dbf':
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FECHA_NACI, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: NACIONALID, Tipo: N
Columna: DESCRI_EST, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\difuntos.dbf':
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_DEF, Tipo: D

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\extranjeros.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INS, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: NACIONAL, Tipo: C
Columna: DIRECCION, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\interdictos.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FECINS, Tipo: C
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\menores.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INS, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: DES_MENOR, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\nacionalidades.dbf':
Columna: ID_NACION, Tipo: N
Columna: DES_NACION, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\part.dbf':
Columna: CODIGO, Tipo: N
Columna: ANIO, Tipo: N
Columna: CRUZAR, Tipo: L
Columna: NOMBRE, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: SIGLAS, Tipo: C
Columna: CERTIFICA, Tipo: L
Columna: PRI_ENTRE, Tipo: D
Columna: SEG_ENTRE, Tipo: D
Columna: RUTA, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: EXTERIOR, Tipo: C
Columna: VIEJO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Consulta Padron 2013\data\pol_y_mil.dbf':
Columna: TIPO, Tipo: C
Columna: GRADO, Tipo: C
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FECINS, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\deshabilitados.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FEC_INSCRI, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: OBS, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\desh_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: SECUENCIA, Tipo: N
Columna: FECHA_HABI, Tipo: D
Columna: FECHA_INGR, Tipo: D
Columna: MOTIVO, Tipo: C
Columna: COD_DESHAB, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\difuntos.dbf':
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: FEC_DEF, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: TIPO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: ID_TIPOREG, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\inhabilitados.dbf':
Columna: ID_INHABIL, Tipo: N
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_DEFUNC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: SERIE_BOLE, Tipo: N
Columna: DIRECCION, Tipo: C
Columna: LUGNAC, Tipo: C
Columna: BARRIO, Tipo: C
Columna: FECHA_EST, Tipo: D
Columna: DESCRI_EST, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: ID_TIPOREG, Tipo: N
Columna: TIPO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\interdictos.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FECINS, Tipo: C
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\menores.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FEC_INSCRI, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: DIRECCION, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\part.dbf':
Columna: CODIGO, Tipo: N
Columna: ANIO, Tipo: N
Columna: CRUZAR, Tipo: L
Columna: NOMBRE, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: SIGLAS, Tipo: C
Columna: CERTIFICA, Tipo: L
Columna: PRI_ENTRE, Tipo: D
Columna: SEG_ENTRE, Tipo: D
Columna: RUTA, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: EXTERIOR, Tipo: C
Columna: VIEJO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\pol_y_mil.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FECINS, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\regciv.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: ID_INTERNO, Tipo: N
Columna: NACIONAL, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: ESTATUS, Tipo: C
Columna: NAC, Tipo: N

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc)\data\regciv_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: APE2, Tipo: C
Columna: NOM2, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc) 31-08\data\deshabilitados.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FEC_INSCRI, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: OBS, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc) 31-08\data\difuntos.dbf':
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: FEC_DEF, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc) 31-08\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FEC_INSCRI, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc) 31-08\data\interdictos.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FECINS, Tipo: C
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc) 31-08\data\menores.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FEC_INSCRI, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: DIRECCION, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc) 31-08\data\part.dbf':
Columna: LISTA, Tipo: N
Columna: COD, Tipo: C
Columna: DESCRIP, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: AFILS, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc) 31-08\data\pol_y_mil.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FECINS, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2010 (rcp2008.dbc) 31-08\data\regciv.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: ID_INTERNO, Tipo: N
Columna: NACIONAL, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: ESTATUS, Tipo: C
Columna: NAC, Tipo: N

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\deshabilitados.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: OBS, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\desh_exte.dbf':
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FECHA_NACI, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: NACIONALID, Tipo: N
Columna: DESCRI_EST, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\difuntos.dbf':
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_DEF, Tipo: D

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\extranjeros.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INS, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: NACIONAL, Tipo: C
Columna: DIRECCION, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\interdictos.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FECINS, Tipo: C
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\menores.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INS, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: DES_MENOR, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\nacionalidades.dbf':
Columna: ID_NACION, Tipo: N
Columna: DES_NACION, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\part.dbf':
Columna: CODIGO, Tipo: N
Columna: ANIO, Tipo: N
Columna: CRUZAR, Tipo: L
Columna: NOMBRE, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: SIGLAS, Tipo: C
Columna: CERTIFICA, Tipo: L
Columna: PRI_ENTRE, Tipo: D
Columna: SEG_ENTRE, Tipo: D
Columna: RUTA, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: EXTERIOR, Tipo: C
Columna: VIEJO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\pol_y_mil.dbf':
Columna: TIPO, Tipo: C
Columna: GRADO, Tipo: C
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FECINS, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\regciv.dbf':
Columna: DEPART, Tipo: I
Columna: DISTRITO, Tipo: I
Columna: ZONA, Tipo: I
Columna: LOCAL, Tipo: I
Columna: MESA, Tipo: I
Columna: ORDEN, Tipo: I
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: FEC_NAC, Tipo: D

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)\data\regciv_exte.dbf':
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: DEPART_ULT, Tipo: N
Columna: DISTRI_ULT, Tipo: N
Columna: BARRIO, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: DES_MENOR, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\deshabilitados.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: OBS, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\desh_exte.dbf':
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FECHA_NACI, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: NACIONALID, Tipo: N
Columna: DESCRI_EST, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\difuntos.dbf':
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_DEF, Tipo: D

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\extranjeros.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INS, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: NACIONAL, Tipo: C
Columna: DIRECCION, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\interdictos.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FECINS, Tipo: C
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\menores.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INS, Tipo: D
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: DES_MENOR, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\nacionalidades.dbf':
Columna: ID_NACION, Tipo: N
Columna: DES_NACION, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\part.dbf':
Columna: CODIGO, Tipo: N
Columna: ANIO, Tipo: N
Columna: CRUZAR, Tipo: L
Columna: NOMBRE, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: SIGLAS, Tipo: C
Columna: CERTIFICA, Tipo: L
Columna: PRI_ENTRE, Tipo: D
Columna: SEG_ENTRE, Tipo: D
Columna: RUTA, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: EXTERIOR, Tipo: C
Columna: VIEJO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2013 Generales (rcp2008.dbc)-\data\pol_y_mil.dbf':
Columna: TIPO, Tipo: C
Columna: GRADO, Tipo: C
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FECINS, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2015 (rcp2008.dbc)\data\desh_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: SECUENCIA, Tipo: N
Columna: FECHA_HABI, Tipo: D
Columna: FECHA_INGR, Tipo: D
Columna: MOTIVO, Tipo: C
Columna: COD_DESHAB, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2015 (rcp2008.dbc)\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: TIPO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: ID_TIPOREG, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2015 (rcp2008.dbc)\data\inhabilitados.dbf':
Columna: ID_INHABIL, Tipo: N
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_DEFUNC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: SERIE_BOLE, Tipo: N
Columna: DIRECCION, Tipo: C
Columna: LUGNAC, Tipo: C
Columna: BARRIO, Tipo: C
Columna: FECHA_EST, Tipo: D
Columna: DESCRI_EST, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: ID_TIPOREG, Tipo: N
Columna: TIPO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2015 (rcp2008.dbc)\data\part.dbf':
Columna: CODIGO, Tipo: N
Columna: ANIO, Tipo: N
Columna: CRUZAR, Tipo: L
Columna: NOMBRE, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: SIGLAS, Tipo: C
Columna: CERTIFICA, Tipo: L
Columna: PRI_ENTRE, Tipo: D
Columna: SEG_ENTRE, Tipo: D
Columna: RUTA, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: EXTERIOR, Tipo: C
Columna: VIEJO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2015 (rcp2008.dbc)\data\regciv.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: TIPO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: COD_VOTO, Tipo: N
Columna: DES_VOTO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2015 (rcp2008.dbc)\data\regciv_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: APE2, Tipo: C
Columna: NOM2, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2017 HC (datos.dbc)\mas_pda.dbf':
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: NUMERO_CED, Tipo: N
Columna: CODIGO_SEC, Tipo: N
Columna: SLOCAL, Tipo: N
Columna: APELLIDO, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: FECHA_NACI, Tipo: D
Columna: COD_DPTO, Tipo: N
Columna: COD_DIST, Tipo: N
Columna: DIRECCION, Tipo: C
Columna: NUMERO_CAS, Tipo: C
Columna: CODIGO_SEX, Tipo: N
Columna: FECHA_AFIL, Tipo: D
Columna: DEP_05, Tipo: N
Columna: DIS_05, Tipo: N
Columna: ZON_05, Tipo: N
Columna: LOC_05, Tipo: N
Columna: PARTIDO, Tipo: C
Columna: KEY_DDS, Tipo: C
Columna: KEY_DD, Tipo: C
Columna: KEY_DDZ, Tipo: C
Columna: KEY_DDZL, Tipo: C
Columna: VOTO, Tipo: C
Columna: VOTO1, Tipo: C
Columna: VOTO2, Tipo: C
Columna: VOTO3, Tipo: C
Columna: VOTO4, Tipo: C
Columna: VOTO5, Tipo: C
Columna: CED_APE, Tipo: C
Columna: SEC_LOC, Tipo: N
Columna: OK, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2017 pre ANR (datos.dbc)\mas_pda.dbf':
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: NUMERO_CED, Tipo: N
Columna: APELLIDO, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: FECHA_NACI, Tipo: D
Columna: COD_DPTO, Tipo: N
Columna: COD_DIST, Tipo: N
Columna: CODIGO_SEC, Tipo: N
Columna: SLOCAL, Tipo: N
Columna: DIRECCION, Tipo: C
Columna: NUMERO_CAS, Tipo: C
Columna: CODIGO_SEX, Tipo: N
Columna: FECHA_AFIL, Tipo: D
Columna: HABILITADO, Tipo: N
Columna: PAIS_05, Tipo: N
Columna: CIUDAD_05, Tipo: N
Columna: KEY_DDS, Tipo: C
Columna: KEY_DD, Tipo: C
Columna: KEY_PC, Tipo: C
Columna: KEY_DDZ, Tipo: C
Columna: KEY_DDZL, Tipo: C
Columna: VOTO1, Tipo: C
Columna: VOTO2, Tipo: C
Columna: VOTO3, Tipo: C
Columna: VOTO4, Tipo: C
Columna: VOTO5, Tipo: C
Columna: FECHA_INSC, Tipo: D
Columna: PARTIDO, Tipo: C
Columna: DEP_05, Tipo: N
Columna: DIS_05, Tipo: N
Columna: ZON_05, Tipo: N
Columna: LOC_05, Tipo: N
Columna: ZONA_RCP, Tipo: N
Columna: LOCAL_RCP, Tipo: N
Columna: RCP, Tipo: C
Columna: CEDULA_REA, Tipo: N
Columna: NRO_TALON_, Tipo: N
Columna: NRO_BOLETA, Tipo: N
Columna: ANT_FEC_IN, Tipo: D
Columna: NRO_CASA, Tipo: N
Columna: VOTO, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2018 (rcp2008.dbc)\data\desh_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: SECUENCIA, Tipo: N
Columna: FECHA_HABI, Tipo: D
Columna: FECHA_INGR, Tipo: D
Columna: MOTIVO, Tipo: C
Columna: COD_DESHAB, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2018 (rcp2008.dbc)\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: TIPO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: ID_TIPOREG, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2018 (rcp2008.dbc)\data\inhabilitados.dbf':
Columna: ID_INHABIL, Tipo: N
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_DEFUNC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: SERIE_BOLE, Tipo: N
Columna: DIRECCION, Tipo: C
Columna: LUGNAC, Tipo: C
Columna: BARRIO, Tipo: C
Columna: FECHA_EST, Tipo: D
Columna: DESCRI_EST, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: ID_TIPOREG, Tipo: N
Columna: TIPO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2018 (rcp2008.dbc)\data\part.dbf':
Columna: CODIGO, Tipo: N
Columna: ANIO, Tipo: N
Columna: CRUZAR, Tipo: L
Columna: NOMBRE, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: SIGLAS, Tipo: C
Columna: CERTIFICA, Tipo: L
Columna: PRI_ENTRE, Tipo: D
Columna: SEG_ENTRE, Tipo: D
Columna: RUTA, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: EXTERIOR, Tipo: C
Columna: VIEJO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2018 (rcp2008.dbc)\data\regciv.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: TIPO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: COD_VOTO, Tipo: N
Columna: DES_VOTO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2018 (rcp2008.dbc)\data\regciv_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: APE2, Tipo: C
Columna: NOM2, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2020 (rcp2008.dbc)\data\desh_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: SECUENCIA, Tipo: N
Columna: FECHA_HABI, Tipo: D
Columna: FECHA_INGR, Tipo: D
Columna: MOTIVO, Tipo: C
Columna: COD_DESHAB, Tipo: N
Columna: APE2, Tipo: C
Columna: NOM2, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2020 (rcp2008.dbc)\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: TIPO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: ID_TIPOREG, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2020 (rcp2008.dbc)\data\inhabilitados.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_DEFUNC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: SERIE_BOLE, Tipo: N
Columna: DIRECCION, Tipo: C
Columna: LUGNAC, Tipo: C
Columna: BARRIO, Tipo: C
Columna: FECHA_EST, Tipo: D
Columna: DESCRI_EST, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: ID_TIPOREG, Tipo: N
Columna: TIPO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2020 (rcp2008.dbc)\data\part.dbf':
Columna: CODIGO, Tipo: N
Columna: ANIO, Tipo: N
Columna: CRUZAR, Tipo: L
Columna: NOMBRE, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: SIGLAS, Tipo: C
Columna: CERTIFICA, Tipo: L
Columna: PRI_ENTRE, Tipo: D
Columna: SEG_ENTRE, Tipo: D
Columna: RUTA, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: EXTERIOR, Tipo: C
Columna: VIEJO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2020 (rcp2008.dbc)\data\regciv.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: TIPO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2020 (rcp2008.dbc)\data\regciv_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021\data\desh_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: SECUENCIA, Tipo: N
Columna: FECHA_HABI, Tipo: D
Columna: FECHA_INGR, Tipo: D
Columna: MOTIVO, Tipo: C
Columna: COD_DESHAB, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: TIPO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: ID_TIPOREG, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021\data\inhabilitados.dbf':
Columna: ID_INHABIL, Tipo: N
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_DEFUNC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: SERIE_BOLE, Tipo: N
Columna: DIRECCION, Tipo: C
Columna: LUGNAC, Tipo: C
Columna: BARRIO, Tipo: C
Columna: FECHA_EST, Tipo: D
Columna: DESCRI_EST, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: ID_TIPOREG, Tipo: N
Columna: TIPO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021\data\part.dbf':
Columna: CODIGO, Tipo: N
Columna: ANIO, Tipo: N
Columna: CRUZAR, Tipo: L
Columna: NOMBRE, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: SIGLAS, Tipo: C
Columna: CERTIFICA, Tipo: L
Columna: PRI_ENTRE, Tipo: D
Columna: SEG_ENTRE, Tipo: D
Columna: RUTA, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: EXTERIOR, Tipo: C
Columna: VIEJO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021\data\regciv.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: TIPO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: COD_VOTO, Tipo: N
Columna: DES_VOTO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021\data\regciv_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: APE2, Tipo: C
Columna: NOM2, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021 (rcp2008.dbc)\regciv.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: TIPO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: COD_VOTO, Tipo: N
Columna: DES_VOTO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021 (rcp2008.dbc)\data\desh_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: SECUENCIA, Tipo: N
Columna: FECHA_HABI, Tipo: D
Columna: FECHA_INGR, Tipo: D
Columna: MOTIVO, Tipo: C
Columna: COD_DESHAB, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021 (rcp2008.dbc)\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: TIPO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: ID_TIPOREG, Tipo: N
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021 (rcp2008.dbc)\data\inhabilitados.dbf':
Columna: ID_INHABIL, Tipo: N
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_DEFUNC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: SERIE_BOLE, Tipo: N
Columna: DIRECCION, Tipo: C
Columna: LUGNAC, Tipo: C
Columna: BARRIO, Tipo: C
Columna: FECHA_EST, Tipo: D
Columna: DESCRI_EST, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: ID_TIPOREG, Tipo: N
Columna: TIPO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021 (rcp2008.dbc)\data\nacionalidades.dbf':
Columna: ID_NACION, Tipo: N
Columna: DES_NACION, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021 (rcp2008.dbc)\data\part.dbf':
Columna: CODIGO, Tipo: N
Columna: ANIO, Tipo: N
Columna: CRUZAR, Tipo: L
Columna: NOMBRE, Tipo: C
Columna: ESPARTIDO, Tipo: L
Columna: SIGLAS, Tipo: C
Columna: CERTIFICA, Tipo: L
Columna: PRI_ENTRE, Tipo: D
Columna: SEG_ENTRE, Tipo: D
Columna: RUTA, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: EXTERIOR, Tipo: C
Columna: VIEJO, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021 (rcp2008.dbc)\data\regciv.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: N
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: FEC_INSCRI, Tipo: D
Columna: TIPO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: COD_VOTO, Tipo: N
Columna: DES_VOTO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021 (rcp2008.dbc)\data\regciv_exte.dbf':
Columna: IDENTIFICA, Tipo: N
Columna: ANO, Tipo: N
Columna: PAIS, Tipo: N
Columna: CIUDAD, Tipo: N
Columna: TIPO, Tipo: C
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: SERIE_BOLE, Tipo: N
Columna: CEDULA, Tipo: N
Columna: FEC_INSCRI, Tipo: D
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: D
Columna: BARRIO, Tipo: C
Columna: SEXO, Tipo: C
Columna: ID_NACION, Tipo: N
Columna: DIRECC, Tipo: C
Columna: APE2, Tipo: C
Columna: NOM2, Tipo: C
Columna: PART, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: _NullFlags, Tipo: 0

Estructura de la tabla DBF 'D:\PADRONES\Padrón 2021 ANR (datos.dbc)\mas_pda.dbf':
Columna: MESA, Tipo: N
Columna: ORDEN, Tipo: N
Columna: NUMERO_CED, Tipo: N
Columna: CODIGO_SEC, Tipo: N
Columna: SEC_ANT, Tipo: N
Columna: SLOCAL, Tipo: N
Columna: APELLIDO, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: FECHA_NACI, Tipo: D
Columna: COD_DPTO, Tipo: N
Columna: COD_DIST, Tipo: N
Columna: WESTA, Tipo: N
Columna: DIRECCION, Tipo: C
Columna: NUMERO_CAS, Tipo: C
Columna: CODIGO_SEX, Tipo: N
Columna: FECHA_AFIL, Tipo: D
Columna: PARTIDO, Tipo: C
Columna: DEP_RCP, Tipo: N
Columna: DIS_RCP, Tipo: N
Columna: ZON_RCP, Tipo: N
Columna: LOC_RCP, Tipo: N
Columna: INSC_RCP, Tipo: D
Columna: TALON_RCP, Tipo: N
Columna: BOLET_RCP, Tipo: N
Columna: VOTO1, Tipo: C
Columna: VOTO2, Tipo: C
Columna: VOTO3, Tipo: C
Columna: VOTO4, Tipo: C
Columna: VOTO5, Tipo: C
Columna: SEC_LOC, Tipo: N
Columna: KEY_DDS, Tipo: C
Columna: KEYDD, Tipo: C
Columna: KEYDDZ, Tipo: C
Columna: KEYDDZL, Tipo: C
Columna: CED_APE, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón UNACE (rcp2008.dbc)\data\deshabilitados.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FEC_INSCRI, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C
Columna: OBS, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón UNACE (rcp2008.dbc)\data\difuntos.dbf':
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: FEC_DEF, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón UNACE (rcp2008.dbc)\data\dobles.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FEC_INSCRI, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón UNACE (rcp2008.dbc)\data\interdictos.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FECINS, Tipo: C
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón UNACE (rcp2008.dbc)\data\menores.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FEC_INS, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón UNACE (rcp2008.dbc)\data\part.dbf':
Columna: LISTA, Tipo: N
Columna: COD, Tipo: C
Columna: DESCRIP, Tipo: C
Columna: SIGLAS, Tipo: C
Columna: AFILS, Tipo: N

Estructura de la tabla DBF 'D:\PADRONES\Padrón UNACE (rcp2008.dbc)\data\pol_y_mil.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: CEDULA, Tipo: C
Columna: FECINS, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: SEXO, Tipo: C
Columna: NACIONAL, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\Padrón UNACE (rcp2008.dbc)\data\regciv.dbf':
Columna: DEPART, Tipo: N
Columna: DISTRITO, Tipo: N
Columna: ZONA, Tipo: N
Columna: LOCAL, Tipo: N
Columna: TALON, Tipo: N
Columna: BOLETA, Tipo: N
Columna: FEC_INSCRI, Tipo: C
Columna: CEDULA, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: SEXO, Tipo: C
Columna: FEC_NAC, Tipo: N
Columna: NACIONAL, Tipo: C

#Los datos de RUC pueden ir a una tabla RUC aparte si es más práctico
Estructura de la tabla DBF 'D:\PADRONES\RUC\RUC.dbf':
Columna: ID_RUC, Tipo: N
Columna: RUCDIGITO, Tipo: C
Columna: RAZON, Tipo: C

Estructura de la tabla DBF 'D:\PADRONES\RUC\RUC2017.dbf':
Columna: ID_RUC, Tipo: N
Columna: RUCDIGITO, Tipo: C
Columna: RAZON, Tipo: C
Columna: DIGITO, Tipo: C

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc 1.csv':
<class 'pandas.core.frame.DataFrame'>
Index: 65534 entries, 1;1000060-7;BENITEZ CENTURION to 65534;5635210-7;BENITEZ MARTINEZ
Data columns (total 1 columns):
 #   Column                  Non-Null Count  Dtype 
---  ------                  --------------  ----- 
 0   id_ruc;rucdigito;razon  65534 non-null  object
dtypes: object(1)
memory usage: 1024.0+ KB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc0.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 172875 entries, 0 to 172874
Data columns (total 2 columns):
 #   Column                                  Non-Null Count   Dtype 
---  ------                                  --------------   ----- 
 0   1000000;CAÑETE GONZALEZ                 172875 non-null  object
 1    JUANA DEL CARMEN;3;CAGJ761720E;ACTIVO  160283 non-null  object
dtypes: object(2)
memory usage: 2.6+ MB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc1.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 173054 entries, 0 to 173053
Data columns (total 2 columns):
 #   Column                         Non-Null Count   Dtype 
---  ------                         --------------   ----- 
 0   1000001;CHIR DE LOPEZ          173054 non-null  object
 1    RAQUEL;1;CIAR6422903;ACTIVO;  160490 non-null  object
dtypes: object(2)
memory usage: 2.6+ MB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc2.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 174094 entries, 0 to 174093
Data columns (total 2 columns):
 #   Column                             Non-Null Count   Dtype 
---  ------                             --------------   ----- 
 0   1000012;PEÑA INSAURRALDE           174094 non-null  object
 1    LELI GLADYS;7;PEIL632000O;ACTIVO  161521 non-null  object
dtypes: object(2)
memory usage: 2.7+ MB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc3.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 173757 entries, 0 to 173756
Data columns (total 2 columns):
 #   Column                                Non-Null Count   Dtype 
---  ------                                --------------   ----- 
 0   1000063;ZACARIAS MONNIN               173757 non-null  object
 1    RUBEN GUSTAVO;1;ZAMR653640V;ACTIVO;  161177 non-null  object
dtypes: object(2)
memory usage: 2.7+ MB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc4.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 173436 entries, 0 to 173435
Data columns (total 2 columns):
 #   Column                                               Non-Null Count   Dtype 
---  ------                                               --------------   ----- 
 0   1000004;MOLINA DE TROCHE                             173436 non-null  object
 1    SANDRA ELIZABETH;6;MOTS763530\;SUSPENSION TEMPORAL  160815 non-null  object
dtypes: object(2)
memory usage: 2.6+ MB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc5.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 173568 entries, 0 to 173567
Data columns (total 2 columns):
 #   Column                            Non-Null Count   Dtype 
---  ------                            --------------   ----- 
 0   1000025;MIZUMOTO                  173568 non-null  object
 1    TAKASHI;9;MITA662560Q;CANCELADO  160990 non-null  object
dtypes: object(2)
memory usage: 2.6+ MB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc6.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 173244 entries, 0 to 173243
Data columns (total 2 columns):
 #   Column                              Non-Null Count   Dtype 
---  ------                              --------------   ----- 
 0   1000006;VILLASANTTI  ACOSTA         173244 non-null  object
 1    MAURICIO;2;VIAM6519216;CANCELADO;  160701 non-null  object
dtypes: object(2)
memory usage: 2.6+ MB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc7.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 172862 entries, 0 to 172861
Data columns (total 2 columns):
 #   Column                          Non-Null Count   Dtype 
---  ------                          --------------   ----- 
 0   1000007;ROMERO GOMEZ            172862 non-null  object
 1    ALFREDO;0;ROGA652940D;ACTIVO;  160272 non-null  object
dtypes: object(2)
memory usage: 2.6+ MB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc8.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 172789 entries, 0 to 172788
Data columns (total 2 columns):
 #   Column                                         Non-Null Count   Dtype 
---  ------                                         --------------   ----- 
 0   1000018;TRINIDAD                               172789 non-null  object
 1    SEBASTIAN;6;TISE651860P;SUSPENSION TEMPORAL;  160209 non-null  object
dtypes: object(2)
memory usage: 2.6+ MB
None

Estructura del archivo CSV 'D:\PADRONES\RUC\ruc9.csv':
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 173157 entries, 0 to 173156
Data columns (total 2 columns):
 #   Column                                   Non-Null Count   Dtype 
---  ------                                   --------------   ----- 
 0   1000009;GONZALEZ FERNANDEZ               173157 non-null  object
 1    ROBERTO TRIGIDIO;7;GOFR651540U;ACTIVO;  160586 non-null  object
dtypes: object(2)
memory usage: 2.6+ MB
None

-- Tabla Venta
CREATE TABLE Venta (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES Cliente(id_cliente) ON DELETE CASCADE,
    id_vendedor INTEGER REFERENCES Vendedor(id_vendedor) ON DELETE CASCADE,
    fecha_venta TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2),
    estado VARCHAR(20) CHECK (estado IN ('pendiente', 'pagado', 'cancelado')),
    entrega_inmediata BOOLEAN DEFAULT TRUE
);
-- Tabla DetalleVenta
CREATE TABLE DetalleVenta (
    id_detalle_venta SERIAL PRIMARY KEY,
    id_venta INTEGER REFERENCES Venta(id_venta) ON DELETE CASCADE,
    id_presentacion INTEGER REFERENCES Presentacion(id_presentacion) ON DELETE CASCADE,
    cantidad INTEGER CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2),
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED
);
-- Tabla Vehiculo
CREATE TABLE Vehiculo (
    id_vehiculo SERIAL PRIMARY KEY,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    placa VARCHAR(20) UNIQUE,
    ano INTEGER
);
-- Tabla RutaVenta
CREATE TABLE RutaVenta (
   id_ruta SERIAL PRIMARY KEY,
   id_vehiculo INTEGER REFERENCES Vehiculo(id_vehiculo),
   fecha DATE
);
-- Tabla GastoVehiculo
CREATE TABLE GastoVehiculo (
   id_gasto SERIAL PRIMARY KEY,
   tipo_gasto VARCHAR(50),
   monto DECIMAL(10, 2),
   fecha DATE
);

Estructura de la tabla DBF 'D:\PADRONES\SATI\DATOS\cedauto.dbf':
Columna: CED_TIPO, Tipo: C
Columna: CED_SITU, Tipo: C
Columna: CED_NROCED, Tipo: N
Columna: CED_FECHAG, Tipo: D
Columna: CED_VTO, Tipo: C
Columna: CED_FECHAE, Tipo: C
Columna: CED_NOMBRE, Tipo: C
Columna: CED_APELLI, Tipo: C
Columna: CED_NOMAPE, Tipo: C
Columna: CED_DOCTIT, Tipo: C
Columna: CED_DIRECC, Tipo: C
Columna: CED_LOCALI, Tipo: C
Columna: CED_DEPTO, Tipo: C
Columna: CED_CHAPA, Tipo: C
Columna: CED_MARCA, Tipo: C
Columna: CED_MODELO, Tipo: C
Columna: CED_TIPOVE, Tipo: C
Columna: CED_A_OMOD, Tipo: N
Columna: CED_CHASSI, Tipo: C
Columna: CED_MOTOR, Tipo: C
Columna: CED_COLOR, Tipo: C
Columna: OBSER, Tipo: N

Estructura de la tabla DBF 'D:\PADRONES\SATI\DATOS\provisorios.dbf':
Columna: NROENT, Tipo: C
Columna: FECHAENT, Tipo: C
Columna: OFICINAREG, Tipo: C
Columna: DOCUMENTO, Tipo: C
Columna: SITUACION, Tipo: C
Columna: NOMBRE, Tipo: C
Columna: APELLIDO, Tipo: C
Columna: MARCA, Tipo: C
Columna: MODELO, Tipo: C
Columna: CHASSIS, Tipo: C
Columna: TIPO, Tipo: C
Columna: COLOR, Tipo: C
Columna: MATRICULA, Tipo: C
Columna: NROHOJA, Tipo: C
Columna: NROSTICKER, Tipo: C
Columna: FECHAIMP, Tipo: C

#Estas tablas contienen datos de vehículos

-- Tabla Inventario
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    ubicacion VARCHAR(50),
    id_presentacion INTEGER REFERENCES Presentacion(id_presentacion) ON DELETE CASCADE,
    stock INTEGER CHECK (stock >= 0)
);

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

#esta es la base de datos anterior en FireBird
Estructura de la tabla Firebird 'SIS':
Columna: 1, Tipo: AI                             
Columna: 2, Tipo: AI                             
Columna: 3, Tipo: AI                             
Columna: 4, Tipo: AI                             
Columna: 5, Tipo: AI                             
Columna: 6, Tipo: AI                             
Columna: 7, Tipo: AI                             
Columna: 8, Tipo: AI                             
Columna: 9, Tipo: AI                             
Columna: 10, Tipo: AI                             
Columna: PRODUCTO, Tipo: DESCRIPCION_CORTO              

Estructura de la tabla Firebird 'UCTABRIGHTS':
Columna: UCKEY, Tipo: RDB$8                          
Columna: UCCOMPNAME, Tipo: RDB$7                          
Columna: UCMODULE, Tipo: RDB$6                          
Columna: UCIDUSER, Tipo: RDB$5                          

Estructura de la tabla Firebird 'CLIENTE':
Columna: IMAGEN, Tipo: PICTURE                        
Columna: ACTIVO, Tipo: ENTERO                         
Columna: EMAIL, Tipo: NOMBRE_LARGO                   
Columna: AI_CLIENTE, Tipo: ENTERO                         
Columna: APELLIDO, Tipo: DESCRIPTION_LARGE              
Columna: DIRECCION, Tipo: DESCRIPTION_LARGE              
Columna: ID_CIUDAD, Tipo: AI                             
Columna: ID_GRUPO_CLIENTE, Tipo: AI                             
Columna: MEMO, Tipo: MEMO                           
Columna: ORDEN_VISITA, Tipo: AI                             
Columna: OBSERVACION, Tipo: MEMO                           
Columna: NOMBRE, Tipo: DESCRIPTION_SHORT              
Columna: TELEFONO, Tipo: DESCRIPTION_SHORT              
Columna: RUC, Tipo: DESCRIPTION_SHORT              
Columna: BARRIO, Tipo: DESCRIPTION_SHORT              
Columna: CONTACTO, Tipo: DESCRIPTION_SHORT              
Columna: CONTACTO2, Tipo: DESCRIPTION_SHORT              
Columna: DOCUMENTO_1, Tipo: DESCRIPTION_SHORT              
Columna: DOCUMENTO_2, Tipo: DESCRIPTION_SHORT              
Columna: CELULAR, Tipo: DESCRIPTION_SHORT              
Columna: TELEFONO_1, Tipo: DESCRIPTION_SHORT              
Columna: TELEFONO_2, Tipo: DESCRIPTION_SHORT              
Columna: CALIFICACION, Tipo: NOMBRE_CORTO                   
Columna: RECIBIRPEDIDO, Tipo: SI_NO_NO                       
Columna: LATITUD, Tipo: DESCRIPTION_SHORT              
Columna: LONGITUD, Tipo: DESCRIPTION_SHORT              
Columna: FECHA_NACIMIENTO, Tipo: FECHA                          
Columna: DIRECCIONTRABAJO, Tipo: MEMO                           
Columna: ID_VENDEDOR, Tipo: ENTERO                         
Columna: LUGARTRABAJO, Tipo: DESCRIPTION_LARGE              
Columna: LATITUD1, Tipo: DESCRIPTION_SHORT              
Columna: LONGITUD1, Tipo: DESCRIPTION_SHORT              
Columna: FEC_NAC, Tipo: RDB$2381                       

Estructura de la tabla Firebird 'CIUDAD':
Columna: CODIGOAREA, Tipo: CODIGO_AREA                    
Columna: ID_CIUDAD, Tipo: AI                             
Columna: ID_PAIS, Tipo: AI                             
Columna: NOMBRE, Tipo: DESCRIPTION_SHORT              

Estructura de la tabla Firebird 'UCTABRIGHTSEX':
Columna: UCKEY, Tipo: RDB$13                         
Columna: UCFORMNAME, Tipo: RDB$12                         
Columna: UCCOMPNAME, Tipo: RDB$11                         
Columna: UCMODULE, Tipo: RDB$10                         
Columna: UCIDUSER, Tipo: RDB$9                          

Estructura de la tabla Firebird 'EMPRESA_CLAVE':
Columna: FECHA, Tipo: RDB$2155                       
Columna: ID_EMPRESA, Tipo: AI                             
Columna: PRODUCTO, Tipo: DESCRIPCION_CORTO              
Columna: CLAVE, Tipo: DESCRIPCION_CORTO              

Estructura de la tabla Firebird 'UCTABUSERSLOGGED':
Columna: UCDATA, Tipo: RDB$18                         
Columna: UCMACHINENAME, Tipo: RDB$17                         
Columna: UCAPPLICATIONID, Tipo: RDB$16                         
Columna: UCIDUSER, Tipo: RDB$15                         
Columna: UCIDLOGON, Tipo: RDB$14                         

Estructura de la tabla Firebird 'EMPRESA':
Columna: PAGARE, Tipo: PICTURE                        
Columna: IMAGEN, Tipo: PICTURE                        
Columna: PUERTO_SERVIDOR, Tipo: ENTERO                         
Columna: CONTRASE_EMAIL, Tipo: DESCRIPCION_MEDIO              
Columna: DIRECCION, Tipo: DIRECION                       
Columna: LINEA1, Tipo: DIRECION                       
Columna: LINEA2, Tipo: DIRECION                       
Columna: IDEOLOGIA, Tipo: DIRECION                       
Columna: NOMBRE_SERVIDOR, Tipo: DESCRIPTION_LARGE              
Columna: MAXIMO_ITEMS_COMPRA, Tipo: AI                             
Columna: MAXIMO_ITEMS_SALIDA, Tipo: AI                             
Columna: MAXIMO_ITEMS_ENTRADA, Tipo: AI                             
Columna: MAXIMO_ITEMS_TRANFERENCIA, Tipo: ENTERO                         
Columna: PROMOCION_LINEA2, Tipo: MEMO                           
Columna: PROMOCION_LINEA, Tipo: MEMO                           
Columna: ID_EMPRESA, Tipo: AI                             
Columna: RAZON, Tipo: DESCRIPTION_LARGE              
Columna: ID_CIUDAD, Tipo: AI                             
Columna: EMAIL, Tipo: DESCRIPTION_LARGE              
Columna: WEB, Tipo: DESCRIPTION_LARGE              
Columna: REGISTRO, Tipo: DESCRIPTION_LARGE              
Columna: MAXIMO_ITEMS_VENTA, Tipo: ENTERO                         
Columna: ID_LENGUAJE, Tipo: ENTERO_CORTO                   
Columna: GUARDAR_EVENTOSS, Tipo: YES_NO                         
Columna: CAN_INSER_INCOM, Tipo: YES_NO                         
Columna: COMPROBAR_DO_CLI, Tipo: YES_NO                         
Columna: COMPROBAR_BA_PRO, Tipo: YES_NO                         
Columna: PANTALLA_MODAL, Tipo: YES_NO                         
Columna: PERMITIR_AUTO_CARGA, Tipo: YES_NO                         
Columna: TELEFONO1, Tipo: DESCRIPTION_SHORT              
Columna: TELEFONO2, Tipo: DESCRIPTION_SHORT              
Columna: FAX1, Tipo: DESCRIPTION_SHORT              
Columna: FAX2, Tipo: DESCRIPTION_SHORT              
Columna: NOMBRE, Tipo: DESCRIPTION_SHORT              
Columna: MEMBRETE_HACIENDA, Tipo: YES_NO                         
Columna: OFRECER_PROMOCION, Tipo: NO_YES_YES                     
Columna: EMAILDESALDOBIENVENIDA, Tipo: SI_NO_NO                       
Columna: CONTROLARSTOCK, Tipo: SI_NO_NO                       

Estructura de la tabla Firebird 'UCTABUSERS':
Columna: UCEMAIL, Tipo: RDB$40                         
Columna: UCLOGIN, Tipo: RDB$35                         
Columna: UCUSERNAME, Tipo: RDB$26                         
Columna: UCKEY, Tipo: RDB$44                         
Columna: UCPROFILE, Tipo: RDB$43                         
Columna: UCPRIVILEGED, Tipo: RDB$41                         
Columna: UCUSERDAYSSUN, Tipo: RDB$39                         
Columna: UCUSEREXPIRED, Tipo: RDB$38                         
Columna: UCPASSWORD, Tipo: RDB$36                         
Columna: UCIDUSER, Tipo: RDB$19                         
Columna: UCPASSEXPIRED, Tipo: RDB$37                         
Columna: UCTYPEREC, Tipo: RDB$42                         

Estructura de la tabla Firebird 'VENDEDOR':
Columna: PORCENTAJE_VENTA, Tipo: NUMERO                         
Columna: FECHA_NACIMIENTO, Tipo: RDB$509                        
Columna: DIRECCION, Tipo: DESCRIPTION_LARGE              
Columna: EMAIL, Tipo: DESCRIPTION_LARGE              
Columna: ID_VENDEDOR, Tipo: AI                             
Columna: ACTIVO, Tipo: YES_NO                         
Columna: RUC, Tipo: DESCRIPTION_SHORT              
Columna: TELEFONO, Tipo: DESCRIPTION_SHORT              
Columna: APELLIDO_MATERNO, Tipo: DESCRIPTION_SHORT              
Columna: APELLIDO_PATERNO, Tipo: DESCRIPTION_SHORT              
Columna: NOMBRE, Tipo: DESCRIPTION_SHORT              
Columna: ID_USUARIO, Tipo: ENTERO                         
Columna: CLAVEACCESO, Tipo: NOMBRE_CORTO                   

Estructura de la tabla Firebird 'CUENTA_CLIENTE':
Columna: CREDITO, Tipo: NUMERO                         
Columna: DEBITO, Tipo: NUMERO                         
Columna: ID_COBRANZA_DETALLE, Tipo: ENTERO                         
Columna: REFERENCIA, Tipo: NUMERO_MEDIO                   
Columna: VENCIMIENTO, Tipo: DATE                           
Columna: ID_CUENTA_CLIENTE, Tipo: NUMERO_MEDIO                   
Columna: ID_COMPROBANTE, Tipo: NUMERO_MEDIO                   
Columna: FECHA, Tipo: DATE                           
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: ID_PERSONAL, Tipo: AI                             
Columna: NRO, Tipo: NOMBRE_CORTO                   
Columna: DESCRIPCION, Tipo: DESCRIPTION_SHORT              
Columna: DE_HASTA, Tipo: ALIAS                          
Columna: ID_VENTA, Tipo: ENTERO                         
Columna: ID_FORMA_PAGO, Tipo: ENTERO                         
Columna: ID_METO_PAGO, Tipo: ENTERO                         

Estructura de la tabla Firebird 'PAIS':
Columna: AREA_CODIGO, Tipo: CODIGO_AREA                    
Columna: ID_PAIS, Tipo: AI                             
Columna: NOMBRE, Tipo: DESCRIPTION_SHORT              
Columna: NACIONALIDAD, Tipo: DESCRIPTION_SHORT              

Estructura de la tabla Firebird 'GRUPO_CLIENTE':
Columna: ID_GRUPO_CLIENTE, Tipo: AI                             
Columna: DESCRIPCION, Tipo: DESCRIPTION_SHORT              
Columna: ID_VENDEDOR, Tipo: ENTERO                         

Estructura de la tabla Firebird 'FIB$DATASETS_INFO':
Columna: CONDITIONS, Tipo: RDB$5606                       
Columna: REFRESH_SQL, Tipo: RDB$5602                       
Columna: DELETE_SQL, Tipo: RDB$5601                       
Columna: INSERT_SQL, Tipo: RDB$5600                       
Columna: UPDATE_SQL, Tipo: RDB$5599                       
Columna: SELECT_SQL, Tipo: RDB$5598                       
Columna: FIB$VERSION, Tipo: RDB$5607                       
Columna: DS_ID, Tipo: RDB$5596                       
Columna: UPDATE_ONLY_MODIFIED_FIELDS, Tipo: FIB$BOOLEAN                    
Columna: UPDATE_TABLE_NAME, Tipo: RDB$5605                       
Columna: KEY_FIELD, Tipo: RDB$5604                       
Columna: NAME_GENERATOR, Tipo: RDB$5603                       
Columna: DESCRIPTION, Tipo: RDB$5597                       

Estructura de la tabla Firebird 'EMAIL_PENDIENTES':
Columna: ADJUNTO, Tipo: MEMO_CORTO                     
Columna: ID_EMAIL_PENDIENTES, Tipo: ENTERO                         
Columna: EMAIL, Tipo: DESCRIPTION_LARGE              
Columna: ASUNTO, Tipo: DESCRIPTION_LARGE              
Columna: CONTENIDO, Tipo: MEMO                           
Columna: ENVIADO, Tipo: YES_NO                         

Estructura de la tabla Firebird 'PRODUCTO':
Columna: PRECIO_COSTO, Tipo: NUMERO                         
Columna: PESO, Tipo: NUMERO                         
Columna: PRECIO3, Tipo: NUMERO                         
Columna: PRECIO2, Tipo: NUMERO                         
Columna: PRECIO1, Tipo: NUMERO                         
Columna: ID_PRODUCTO, Tipo: ENTERO                         
Columna: OFERTAR, Tipo: SI_NO_NO                       
Columna: CODIGO_BARRAS, Tipo: NOMBRE_CORTO                   
Columna: DESCRIPCION, Tipo: NOMBRE_CORTO                   
Columna: ID_TIPO_PRODUCTO, Tipo: ENTERO                         
Columna: ID_MARCA_PRODUCTO, Tipo: ENTERO                         
Columna: ID_PRODUCTO_SEXO, Tipo: ENTERO                         

Estructura de la tabla Firebird 'MOVIMIENTO':
Columna: FECHA, Tipo: FECHA                          
Columna: ID_VENDEDOR, Tipo: ENTERO                         
Columna: ID_MOVIMIENTO, Tipo: ENTERO                         
Columna: ENVIADO, Tipo: SI_NO_NO                       
Columna: ENTREGADO, Tipo: SI_NO_NO                       

Estructura de la tabla Firebird 'MOVIMIENTO_DETALLE':
Columna: PESO, Tipo: NUMERO                         
Columna: PRECIO3, Tipo: NUMERO                         
Columna: PRECIO2, Tipo: NUMERO                         
Columna: PRECIO1, Tipo: NUMERO                         
Columna: CANT_DEVUELTO, Tipo: ENTERO                         
Columna: CANTIDAD, Tipo: ENTERO                         
Columna: ID_PRODUCTO, Tipo: ENTERO                         
Columna: ID_MOVIMIENTO, Tipo: ENTERO                         
Columna: ID_MOVIMIENTO_DETALLE, Tipo: ENTERO                         
Columna: CODIGO_BARRAS, Tipo: NOMBRE_CORTO                   
Columna: DEVUELTO, Tipo: SI_NO_NO                       

Estructura de la tabla Firebird 'RECIBO_CLIENTE':
Columna: COMISION, Tipo: NUMERO                         
Columna: TOTAL, Tipo: NUMERO                         
Columna: ID_GRUPO, Tipo: ENTERO                         
Columna: COMENTARIO, Tipo: DIRECION                       
Columna: FECHA, Tipo: RDB$510                        
Columna: ID_USUARIO, Tipo: ENTERO                         
Columna: ID_VENDEDOR, Tipo: ENTERO                         
Columna: ID_COBRANZA, Tipo: ENTERO                         
Columna: GUARDADO, Tipo: YES_NO                         
Columna: ANA_ITEMS_CLIENTES, Tipo: ENTERO                         
Columna: ANA_ITEMS_CLIENTES_COBRADO, Tipo: ENTERO                         
Columna: TOTALACOBRAR, Tipo: NUMERO                         

Estructura de la tabla Firebird 'RECIBO_CLIENTE_DETALLE':
Columna: COMSION, Tipo: NUMERO                         
Columna: MONTO, Tipo: NUMERO                         
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: ID_COBRANZA, Tipo: ENTERO                         
Columna: ID_COBRANZA_DETALLE, Tipo: ENTERO                         
Columna: NRORECIBO, Tipo: ENTERO                         

Estructura de la tabla Firebird 'VENTA':
Columna: ID_VENTA, Tipo: ENTERO                         
Columna: ID_VENDEDOR, Tipo: ENTERO                         
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: FECHA, Tipo: DATE                           
Columna: ID_FORMA_PAGO, Tipo: ENTERO                         
Columna: NRO_PAGARE, Tipo: ENTERO                         
Columna: COMENTARIO, Tipo: DESCRIPTION_LARGE              
Columna: METODOPAGO, Tipo: DESCRIPCION_MEDIO              
Columna: ANULADO, Tipo: SI_NO_NO                       
Columna: ID_USUARIO, Tipo: ENTERO                         

Estructura de la tabla Firebird 'PEDIDO':
Columna: ID_PEDIDO, Tipo: ENTERO                         
Columna: FECHA, Tipo: DATE                           
Columna: ID_VENDEDOR, Tipo: ENTERO                         
Columna: CANTIDAD, Tipo: NUMERO                         
Columna: PRODUCTO, Tipo: DESCRIPCION_MEDIO              
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: ENTREGADO, Tipo: SI_NO_NO                       

Estructura de la tabla Firebird 'PREVENTA':
Columna: IDPREVENTA, Tipo: ENTERO                         
Columna: IDVENDEDOR, Tipo: ENTERO                         
Columna: FECHA, Tipo: DATE                           
Columna: CANTIDAD, Tipo: NUMERO                         
Columna: PRECIO, Tipo: NUMERO                         
Columna: ENTREGA, Tipo: NUMERO                         
Columna: CUOTA, Tipo: NUMERO                         
Columna: FORMADEPAGO, Tipo: ENTERO                         
Columna: NROCEDULA, Tipo: DESCRIPCION_CORTO              
Columna: NOMBRE, Tipo: DESCRIPTION_SHORT              
Columna: APELLIDO, Tipo: DESCRIPTION_SHORT              
Columna: CELULAR, Tipo: DESCRIPTION_SHORT              
Columna: PRODUCTO, Tipo: DESCRIPCION_MEDIO              
Columna: ID_VENTA, Tipo: ENTERO                         

Estructura de la tabla Firebird 'ALMACEN_MOVI':
Columna: ID_ALMACEN_MO, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: DESCRIPTION_LARGE              
Columna: FECHA, Tipo: RDB$461                        
Columna: NATU, Tipo: AI                             
Columna: GUARDADO, Tipo: YES_NO                         

Estructura de la tabla Firebird 'ALMACEN_MOVI_D':
Columna: ID_DETALLE, Tipo: ENTERO                         
Columna: ID_ALMACEN_MO, Tipo: NUMERO_MEDIO                   
Columna: ID_PRODUCTO, Tipo: AI                             
Columna: CANTIDAD, Tipo: NUMERO                         
Columna: PRECIO, Tipo: NUMERO                         
Columna: SALIDA, Tipo: NUMERO                         

Estructura de la tabla Firebird 'VENTA_FICHAS':
Columna: ID_VENTA_FICHAS, Tipo: ENTERO                         
Columna: ID_VENTA1, Tipo: ENTERO                         
Columna: ACTIVA, Tipo: SI_NO_NO                       
Columna: ID_VENTA2, Tipo: ENTERO                         
Columna: ID_VENTA3, Tipo: ENTERO                         
Columna: ID_VENTA4, Tipo: ENTERO                         
Columna: FECHA, Tipo: DATE                           

Estructura de la tabla Firebird 'CUENTA_CLIENTE_1':
Columna: ID_CUENTA_CLIENTE, Tipo: NUMERO_MEDIO                   
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: ID_COMPROBANTE, Tipo: NUMERO_MEDIO                   
Columna: NRO, Tipo: NOMBRE_CORTO                   
Columna: FECHA, Tipo: RDB$681                        
Columna: DESCRIPCION, Tipo: DESCRIPTION_SHORT              
Columna: CREDITO, Tipo: NUMERO                         
Columna: DEBITO, Tipo: NUMERO                         
Columna: VENCIMIENTO, Tipo: RDB$682                        
Columna: REFERENCIA, Tipo: NUMERO_MEDIO                   
Columna: ID_PERSONAL, Tipo: AI                             
Columna: DE_HASTA, Tipo: ALIAS                          
Columna: ID_COBRANZA_DETALLE, Tipo: ENTERO                         
Columna: ID_VENTA, Tipo: ENTERO                         

Estructura de la tabla Firebird 'VENTAMAYO':
Columna: ID_VENTAMAYO, Tipo: ENTERO                         
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: ID_USUARIO, Tipo: ENTERO                         
Columna: ID_VENDEDOR, Tipo: ENTERO                         
Columna: FECHA, Tipo: FECHA                          
Columna: NROCOMPROBANTE, Tipo: ALIAS                          
Columna: CONFIRMADO, Tipo: SI_NO_NO                       
Columna: IMPRESO, Tipo: SI_NO_NO                       
Columna: TOTAL, Tipo: NUMERO                         
Columna: COSTO, Tipo: NUMERO                         
Columna: GANANCIA, Tipo: NUMERO                         
Columna: CONTADO, Tipo: SI_NO_NO                       
Columna: ID_PRECIO, Tipo: ENTERO                         

Estructura de la tabla Firebird 'VENTAD':
Columna: ID_VENTAD, Tipo: ENTERO                         
Columna: ID_VENTA, Tipo: ENTERO                         
Columna: ID_PRODUCTO, Tipo: ENTERO                         
Columna: CANTIDAD, Tipo: NUMERO                         
Columna: PRECIO, Tipo: NUMERO                         
Columna: COSTO, Tipo: NUMERO                         

Estructura de la tabla Firebird 'CALIFICACION':
Columna: ID_CALIFICACION, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: NOMBRE_CORTO                   
Columna: DESDE, Tipo: ENTERO                         
Columna: HASTA, Tipo: ENTERO                         
Columna: SIMBOLO, Tipo: ALIAS                          

Estructura de la tabla Firebird 'CLIENTE_SEGUI':
Columna: ID_CLIENTE_SEGUI, Tipo: ENTERO                         
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: ID_USUARIO, Tipo: ENTERO                         
Columna: FECHA, Tipo: FECHA                          
Columna: HORA, Tipo: HORA                           
Columna: OBSERVACION, Tipo: DESCRIPTION_LARGE              
Columna: LATITUD, Tipo: DESCRIPCION_CORTO              
Columna: LONGITUD, Tipo: DESCRIPCION_CORTO              

Estructura de la tabla Firebird 'TIPO_PRECIO':
Columna: ID_TIPO_PRECIO, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: ALIAS                          

Estructura de la tabla Firebird 'METO_PAGO':
Columna: ID_METO_PAGO, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: NOMBRE_CORTO                   

Estructura de la tabla Firebird 'VENTAAUX':
Columna: ID_VENTAAUX, Tipo: ENTERO                         
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: ID_VENDEDOR, Tipo: ENTERO                         
Columna: ID_PRODUCTO, Tipo: ENTERO                         
Columna: DESCRIPCIONPRO, Tipo: NOMBRE_LARGO                   
Columna: SALDOACTUAL, Tipo: NUMERO                         
Columna: PAGOS, Tipo: NUMERO                         
Columna: MONTOCUOTA, Tipo: NUMERO                         
Columna: ID_FORMA_PAGO, Tipo: ENTERO                         
Columna: FECHA, Tipo: FECHA                          
Columna: FORMA, Tipo: ALIAS                          
Columna: NROPAGARE, Tipo: ALIAS                          

Estructura de la tabla Firebird 'PRODUCTO_PRECIO_PROVE':
Columna: ID_PRODUCTO_PRECIO_PROVE, Tipo: ENTERO                         
Columna: ID_PRODUCTO, Tipo: ENTERO                         
Columna: ID_PROVEEDOR, Tipo: ENTERO                         
Columna: PRECIO, Tipo: NUMERO                         
Columna: FECHA, Tipo: RDB$2005                       
Columna: ID_USUARIO, Tipo: ENTERO                         

Estructura de la tabla Firebird 'PROVEEDOR':
Columna: ID_PROVEEDOR, Tipo: ENTERO                         
Columna: RUC, Tipo: ALIAS                          
Columna: RAZONSOCIAL, Tipo: NOMBRE_LARGO                   
Columna: TELEFONO, Tipo: NOMBRE_CORTO                   
Columna: CELULAR, Tipo: NOMBRE_CORTO                   
Columna: DIRECCION, Tipo: MEMO                           
Columna: CONTACTO, Tipo: NOMBRE_CORTO                   
Columna: CONTACTO_DATOS, Tipo: DESCRIPCION_CORTO              

Estructura de la tabla Firebird 'COMPRAD':
Columna: ID_COMPRAD, Tipo: ENTERO                         
Columna: ID_COMPRA, Tipo: ENTERO                         
Columna: ID_PRODUCTO, Tipo: NUMERO                         
Columna: CANTIDAD, Tipo: NUMERO                         
Columna: PRECIO, Tipo: NUMERO                         

Estructura de la tabla Firebird 'COMPRA':
Columna: ID_COMPRA, Tipo: ENTERO                         
Columna: ID_USUARIO, Tipo: ENTERO                         
Columna: ID_PROVEEDOR, Tipo: ENTERO                         
Columna: FECHA, Tipo: FECHA                          
Columna: NRO_FACTURA, Tipo: ALIAS                          
Columna: RECIBIDO, Tipo: SI_NO_NO                       
Columna: CONTADO, Tipo: SI_NO_NO                       

Estructura de la tabla Firebird 'PRODUCTO_TIPO':
Columna: ID_TIPO_PRODUCTO, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: NOMBRE_CORTO                   

Estructura de la tabla Firebird 'UCTABPERFIL':
Columna: ID_CONFIGURACION, Tipo: ENTERO                         
Columna: ID_USUARIO, Tipo: ENTERO                         
Columna: FORM, Tipo: DESCRIPTION_LARGE              
Columna: GRILLA, Tipo: NOMBRE_CORTO                   
Columna: CAMPO, Tipo: NOMBRE_LARGO                   
Columna: VISIBLE, Tipo: SI_NO_NO                       
Columna: ANCHO, Tipo: ENTERO                         
Columna: POSICION, Tipo: ENTERO                         

Estructura de la tabla Firebird 'PRODUCTO_MARCA':
Columna: ID_MARCA_PRODUCTO, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: NOMBRE_CORTO                   

Estructura de la tabla Firebird 'CLIENTE_NOTA_CREDITO_D':
Columna: ID_NOTA_CREDITO_D, Tipo: ENTERO                         
Columna: ID_CLIENTE_NOTA_CREDITO, Tipo: ENTERO                         
Columna: ID_PRODUCTO, Tipo: ENTERO                         
Columna: CANTIDAD, Tipo: NUMERO                         
Columna: PRECIO, Tipo: NUMERO                         
Columna: COSTO, Tipo: NUMERO                         

Estructura de la tabla Firebird 'COBRANZAMOVILOBSERVACION':
Columna: ID_COBRANZAMOVILOBSERVACION, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: DESCRIPCION_MEDIO              

Estructura de la tabla Firebird 'VENTAMADE':
Columna: COSTO, Tipo: NUMERO                         
Columna: ID_VENTAMADE, Tipo: ENTERO                         
Columna: ID_VENTAMAYO, Tipo: ENTERO                         
Columna: ID_PRODUCTO, Tipo: ENTERO                         
Columna: CANTIDAD, Tipo: NUMERO                         
Columna: UNITARIO, Tipo: NUMERO                         
Columna: DESCONTADO, Tipo: SI_NO_NO                       

Estructura de la tabla Firebird 'CLIENTE_NOTA_CREDITO':
Columna: ID_CLIENTE_NOTA_CREDITO, Tipo: ENTERO                         
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: FECHA, Tipo: RDB$2272                       
Columna: ID_USUARIO, Tipo: ENTERO                         
Columna: COMENTARIO, Tipo: MEMO                           
Columna: GUARDADO, Tipo: SI_NO_NO                       
Columna: ACREDITADO, Tipo: SI_NO_NO                       
Columna: NRO_COMPROBANTE, Tipo: ENTERO                         

Estructura de la tabla Firebird 'CLIENTE_LLAMADA':
Columna: ID_CLIENTE_LLAMADA, Tipo: ENTERO                         
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: FECHA, Tipo: DATE                           
Columna: HORA, Tipo: HORA                           
Columna: ID_MOTIVO_LLAMADA, Tipo: ENTERO                         
Columna: MEMO, Tipo: MEMO                           
Columna: AGENDAR, Tipo: SI_NO_NO                       
Columna: AGENDAR_FECHA, Tipo: DATE                           
Columna: TERMINADO, Tipo: SI_NO_NO                       
Columna: NUMERO, Tipo: ALIAS                          
Columna: ARCHIVO, Tipo: PICTURE                        
Columna: ID_USUARIO, Tipo: ENTERO                         

Estructura de la tabla Firebird 'PRODUCTO_SEXO':
Columna: ID_PRODUCTO_SEXO, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: DESCRIPCION_CORTO              

Estructura de la tabla Firebird 'FORMA_PAGO':
Columna: ID_FORMA_PAGO, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: NOMBRE_CORTO                   

Estructura de la tabla Firebird 'EVENTO':
Columna: IDUSER, Tipo: RDB$2377                       
Columna: MSG, Tipo: RDB$2378                       
Columna: DATA, Tipo: RDB$2379                       
Columna: NIVEL, Tipo: RDB$2380                       

Estructura de la tabla Firebird 'COBRANZAMOVIL':
Columna: ID_COBRANZAMOVIL, Tipo: ENTERO                         
Columna: ID_USUARIO, Tipo: ENTERO                         
Columna: ID_VENDEDOR, Tipo: ENTERO                         
Columna: FECHA, Tipo: RDB$2298                       
Columna: ID_GRUPO_CLIENTE, Tipo: ENTERO                         
Columna: CERRADO, Tipo: SI_NO_NO                       
Columna: APLICADO, Tipo: SI_NO_NO                       
Columna: PASS, Tipo: ALIAS                          
Columna: MONTOACOBRAR, Tipo: NUMERO                         
Columna: CANTIDADCLIENTE, Tipo: ENTERO                         
Columna: META, Tipo: NUMERO                         

Estructura de la tabla Firebird 'COBRANZAMOVILD':
Columna: ID_COBRANZAMOVILD, Tipo: ENTERO                         
Columna: ID_COBRANZAMOVIL, Tipo: ENTERO                         
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: CUOTASVENCIDA, Tipo: ENTERO                         
Columna: MONTOSVENCIDO, Tipo: NUMERO                         
Columna: MONTOPAGADO, Tipo: NUMERO                         
Columna: NRORECIBO, Tipo: ALIAS                          
Columna: COBRO_LATITUD, Tipo: DESCRIPTION_SHORT              
Columna: COBRO_LONGITUD, Tipo: DESCRIPTION_SHORT              
Columna: ID_COBRANZAMOVILOBSERVACION, Tipo: ENTERO                         
Columna: PASS, Tipo: ALIAS                          
Columna: FECHAULTIMOPAGO, Tipo: FECHA                          
Columna: METODODEPAGO, Tipo: DESCRIPTION_LARGE              
Columna: HORA, Tipo: HORA                           
Columna: SALDOACTUAL, Tipo: NUMERO                         
Columna: ID_COBRANZA_DETALLE, Tipo: ENTERO                         
Columna: VENDEDORA, Tipo: DESCRIPTION_LARGE              
Columna: MONTOCUOTA, Tipo: NUMERO                         
Columna: NRO_COMPROBANTE, Tipo: NOMBRE_CORTO                   

Estructura de la tabla Firebird 'MOTIVO_LLAMADA':
Columna: ID_MOTIVO_LLAMADA, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: NOMBRE_CORTO                   

Estructura de la tabla Firebird 'CEDULA2001':
Columna: ID_CEDULA2001, Tipo: NUMERO_REAL                    
Columna: FECHA_NACIMIENTO, Tipo: NOMBRE                         
Columna: NOMBRE, Tipo: NOMBRE                         
Columna: APELLIDO, Tipo: NOMBRE                         
Columna: DIRECCION, Tipo: DIRECCION                      

Estructura de la tabla Firebird 'PADRON':
Columna: ID_PADRON, Tipo: NUMERO_REAL                    
Columna: depar, Tipo: NOMBRE_LARGO                   
Columna: distri, Tipo: NOMBRE_LARGO                   
Columna: nro_ced, Tipo: NOMBRE_LARGO                   
Columna: cedula, Tipo: NOMBRE_LARGO                   
Columna: nombre, Tipo: NOMBRE_LARGO                   
Columna: apellido, Tipo: NOMBRE_LARGO                   
Columna: zona, Tipo: NOMBRE_LARGO                   
Columna: locali, Tipo: NOMBRE_LARGO                   

Estructura de la tabla Firebird 'UCTABRIGHTS':
Columna: UCIDUSER, Tipo: RDB$29                         
Columna: UCMODULE, Tipo: RDB$30                         
Columna: UCCOMPNAME, Tipo: RDB$31                         
Columna: UCKEY, Tipo: RDB$32                         

Estructura de la tabla Firebird 'PRODUCTO':
Columna: BARRAS, Tipo: NOMBRE                         
Columna: DESCRIPCION, Tipo: NOMBRE_LARGO                   
Columna: MARCA, Tipo: NOMBRE_CORTO                   
Columna: GRUPO, Tipo: NOMBRE_CORTO                   
Columna: SESION, Tipo: NOMBRE_CORTO                   
Columna: FAMILIA, Tipo: NOMBRE_CORTO                   
Columna: PRECIO, Tipo: NUMERO                         
Columna: IMAGEN, Tipo: FOTO                           

Estructura de la tabla Firebird 'RUC':
Columna: ID_RUC, Tipo: NUMERO_REAL                    
Columna: RUCDIGITO, Tipo: NOMBRE                         
Columna: RAZON, Tipo: DIRECCION                      

Estructura de la tabla Firebird 'UCTABRIGHTSEX':
Columna: UCIDUSER, Tipo: RDB$33                         
Columna: UCMODULE, Tipo: RDB$34                         
Columna: UCCOMPNAME, Tipo: RDB$35                         
Columna: UCFORMNAME, Tipo: RDB$36                         
Columna: UCKEY, Tipo: RDB$37                         

Estructura de la tabla Firebird 'UCTABUSERS':
Columna: UCIDUSER, Tipo: RDB$38                         
Columna: UCUSERNAME, Tipo: RDB$39                         
Columna: UCLOGIN, Tipo: RDB$40                         
Columna: UCPASSWORD, Tipo: RDB$41                         
Columna: UCPASSEXPIRED, Tipo: RDB$42                         
Columna: UCUSEREXPIRED, Tipo: RDB$43                         
Columna: UCUSERDAYSSUN, Tipo: RDB$44                         
Columna: UCEMAIL, Tipo: RDB$45                         
Columna: UCPRIVILEGED, Tipo: RDB$46                         
Columna: UCTYPEREC, Tipo: RDB$47                         
Columna: UCPROFILE, Tipo: RDB$48                         
Columna: UCKEY, Tipo: RDB$49                         

Estructura de la tabla Firebird 'RUC2017':
Columna: ID_RUC, Tipo: NUMERO_REAL                    
Columna: RUCDIGITO, Tipo: NOMBRE                         
Columna: RAZON, Tipo: DIRECCION                      
Columna: DIGITO, Tipo: NOMBRE                         

Estructura de la tabla Firebird 'USER':
Columna: ID, Tipo: ID                             
Columna: RAZON, Tipo: NOMBRE                         
Columna: CONTRASENA, Tipo: NOMBRE                         

Estructura de la tabla Firebird 'FIB$FIELDS_INFO':
Columna: TABLE_NAME, Tipo: RDB$22                         
Columna: FIELD_NAME, Tipo: RDB$23                         
Columna: DISPLAY_LABEL, Tipo: RDB$24                         
Columna: VISIBLE, Tipo: FIB$BOOLEAN                    
Columna: DISPLAY_FORMAT, Tipo: RDB$25                         
Columna: EDIT_FORMAT, Tipo: RDB$26                         
Columna: TRIGGERED, Tipo: FIB$BOOLEAN                    
Columna: DISPLAY_WIDTH, Tipo: RDB$27                         
Columna: FIB$VERSION, Tipo: RDB$28                         

Estructura de la tabla Firebird 'EMPRESA':
Columna: NOMBRE, Tipo: RDB$1                          
Columna: UBICACION, Tipo: RDB$2                          
Columna: IP, Tipo: RDB$5                          

Estructura de la tabla Firebird 'CONFIGURACION':
Columna: INI_DIRECCION, Tipo: RDB$4                          

Estructura de la tabla Firebird 'COPIA_SEGURIDAD':
Columna: HORA_BACK, Tipo: HORA                           
Columna: SERVIDOR, Tipo: NOMBRE_CORTO                   
Columna: BACK_DESTINO, Tipo: NOMBRE_LARGO                   
Columna: NOMBRE_BD, Tipo: NOMBRE_LARGO                   
Columna: ID_COPIA, Tipo: ID                             

Estructura de la tabla Firebird 'FIB$FIELDS_INFO':
Columna: FIB$VERSION, Tipo: RDB$12                         
Columna: DISPLAY_WIDTH, Tipo: RDB$11                         
Columna: TRIGGERED, Tipo: FIB$BOOLEAN                    
Columna: VISIBLE, Tipo: FIB$BOOLEAN                    
Columna: EDIT_FORMAT, Tipo: RDB$10                         
Columna: DISPLAY_FORMAT, Tipo: RDB$9                          
Columna: DISPLAY_LABEL, Tipo: RDB$8                          
Columna: FIELD_NAME, Tipo: RDB$7                          
Columna: TABLE_NAME, Tipo: RDB$6                          

Estructura de la tabla Firebird 'EMPRESA_EMAIL':
Columna: ID_EMPRESA, Tipo: ID                             
Columna: RAZON, Tipo: NOMBRE                         
Columna: DIRECCION, Tipo: DIRECCION                      
Columna: EMAIL, Tipo: NOMBRE                         
Columna: NOMBRE_SERVIDOR, Tipo: NOMBRE                         
Columna: PUERTO_SERVIDOR, Tipo: ID                             
Columna: CONTRASE_EMAIL, Tipo: NOMBRE                         

Estructura de la tabla Firebird 'GRUPO_ENVIO':
Columna: ID_GRUPO_ENVIO, Tipo: ID                             
Columna: DESCRIPCION, Tipo: DIRECCION                      

Estructura de la tabla Firebird 'CONFI_MENSAJE':
Columna: ID_CONFIGURACION, Tipo: ENTERO                         
Columna: ID_CALIFICACION, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: NOMBRE                         
Columna: UBICACION_SONIDO, Tipo: NOMBRE_LARGO                   

Estructura de la tabla Firebird 'REPMAN_REPORTS':
Columna: REPORT_NAME, Tipo: RDB$3                          
Columna: REPORT, Tipo: RDB$13                         
Columna: REPORT_GROUP, Tipo: RDB$14                         
Columna: USER_FLAG, Tipo: RDB$15                         

Estructura de la tabla Firebird 'GRUPO_ENVIO_D':
Columna: ID_GRUPO_ENVIO_D, Tipo: ID                             
Columna: ID_GRUPO_ENVIO, Tipo: ID                             
Columna: ID_CLIENTE, Tipo: ENTERO                         

Estructura de la tabla Firebird 'REPMAN_GROUPS':
Columna: GROUP_CODE, Tipo: RDB$16                         
Columna: GROUP_NAME, Tipo: RDB$17                         
Columna: PARENT_GROUP, Tipo: RDB$18                         

Estructura de la tabla Firebird 'IMAGEN_PRODUCTO':
Columna: ID_IMAGEN_PRODUCTO, Tipo: ENTERO                         
Columna: FECHA, Tipo: FECHA                          
Columna: IMAGEN, Tipo: IMAGEN                         
Columna: ID_PRODUCTO, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: DESCRIPCION                    

Estructura de la tabla Firebird 'IMAGEN_CLIENTE':
Columna: ID_IMAGEN_CLIENTE, Tipo: ENTERO                         
Columna: ID_CLIENTE, Tipo: ENTERO                         
Columna: FECHA, Tipo: FECHA                          
Columna: DESCRIPCION, Tipo: DESCRIPCION                    
Columna: IMAGEN, Tipo: IMAGEN                         
Columna: ID_USUARIO, Tipo: ENTERO                         

Estructura de la tabla Firebird 'IMAGEN_FINANCIERO':
Columna: ID_IMAGEN_FINANCIERO, Tipo: ENTERO                         
Columna: ID_OPERACION_FINANCIERO, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: DESCRIPCION                    
Columna: IMAGEN, Tipo: IMAGEN                         

Estructura de la tabla Firebird 'REPMAN_REPORTS':
Columna: REPORT, Tipo: RDB$2                          
Columna: REPORT_NAME, Tipo: RDB$1                          
Columna: REPORT_GROUP, Tipo: RDB$3                          
Columna: USER_FLAG, Tipo: RDB$4                          

Estructura de la tabla Firebird 'REPMAN_GROUPS':
Columna: GROUP_CODE, Tipo: RDB$5                          
Columna: PARENT_GROUP, Tipo: RDB$7                          
Columna: GROUP_NAME, Tipo: RDB$6                          

Estructura de la tabla Firebird 'CONFIGURACION':
Columna: ID_CONFIGURACION, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: DESCRIPCION                    
Columna: ACTIVO, Tipo: SI_NO_SI                       
Columna: ID_TIPO_CONEXION, Tipo: ENTERO                         
Columna: PROTOCOLO, Tipo: ENTERO                         
Columna: PARAMETROCONEXION, Tipo: DESCRIPCION                    
Columna: CONEXIONPING, Tipo: DESCRIPCION                    
Columna: INTERVALOAGOTADO, Tipo: ENTERO                         
Columna: INTERVALOENVIO, Tipo: ENTERO                         
Columna: INVERVALOREINTENTO, Tipo: ENTERO                         
Columna: VALIDEZMENSAJE, Tipo: ENTERO                         
Columna: CONCATENARSMS, Tipo: ENTERO                         

Estructura de la tabla Firebird 'TIPO_CONEXION':
Columna: ID_TIPO_CONEXION, Tipo: ENTERO                         
Columna: DESCRIPCION, Tipo: DESCRIPCION                    

Estructura de la tabla Firebird 'SMS':
Columna: ID_SMS, Tipo: ENTERO                         
Columna: DESTINATARIO, Tipo: NUMERODESTINATARIO             
Columna: MENSAJE, Tipo: MENSAJE                        
Columna: ENVIADO, Tipo: SI_NO_SI                       
Columna: FECHA, Tipo: FECHA                          
Columna: HORA, Tipo: HORA                           
Columna: MODULO, Tipo: ENTERO                         
Columna: REFERENCIA, Tipo: ENTERO                         
Columna: FECHAENVIADO, Tipo: FECHA                          
Columna: ID_CLIENTE, Tipo: ENTERO                         

Estructura de la tabla Firebird 'UCTABRIGHTS':
Columna: UCIDUSER, Tipo: RDB$1                          
Columna: UCMODULE, Tipo: RDB$2                          
Columna: UCCOMPNAME, Tipo: RDB$3                          
Columna: UCKEY, Tipo: RDB$4                          

Estructura de la tabla Firebird 'UCTABRIGHTSEX':
Columna: UCIDUSER, Tipo: RDB$5                          
Columna: UCMODULE, Tipo: RDB$6                          
Columna: UCCOMPNAME, Tipo: RDB$7                          
Columna: UCFORMNAME, Tipo: RDB$8                          
Columna: UCKEY, Tipo: RDB$9                          

Estructura de la tabla Firebird 'UCTABUSERS':
Columna: UCIDUSER, Tipo: RDB$10                         
Columna: UCUSERNAME, Tipo: RDB$11                         
Columna: UCLOGIN, Tipo: RDB$12                         
Columna: UCPASSWORD, Tipo: RDB$13                         
Columna: UCPASSEXPIRED, Tipo: RDB$14                         
Columna: UCUSEREXPIRED, Tipo: RDB$15                         
Columna: UCUSERDAYSSUN, Tipo: RDB$16                         
Columna: UCEMAIL, Tipo: RDB$17                         
Columna: UCPRIVILEGED, Tipo: RDB$18                         
Columna: UCTYPEREC, Tipo: RDB$19                         
Columna: UCPROFILE, Tipo: RDB$20                         
Columna: UCKEY, Tipo: RDB$21                         

Estructura de la tabla Firebird 'EMAIL':
Columna: ID_EMAIL, Tipo: ENTERO                         
Columna: EMAIL, Tipo: DESCRIPCION                    
Columna: ASUNTO, Tipo: DESCRIPCION                    
Columna: ADJUNTO, Tipo: IMAGEN                         
Columna: CONTENIDO, Tipo: MENSAJE                        
Columna: ENVIADO, Tipo: SI_NO_SI                       
Columna: FECHA, Tipo: FECHA                          
Columna: HORA, Tipo: HORA                           
Columna: MODULO, Tipo: ENTERO                         
Columna: REFERENCIA, Tipo: ENTERO                         

Estructura de la tabla Firebird 'ALDO':
Columna: NUM_ALDO, Tipo: DESCRIPCION                    

Estructura de la tabla Firebird 'SMS_ENTRADA':
Columna: ID_SMS_ENTRADA, Tipo: ENTERO                         
Columna: REMITENTE, Tipo: NUMERODESTINATARIO             
Columna: MENSAJE, Tipo: MENSAJE                        
Columna: LEIDO, Tipo: SI_NO_SI                       
Columna: FECHA, Tipo: FECHA                          
Columna: HORA, Tipo: HORA                           
Columna: ID_CLIENTE, Tipo: ENTERO