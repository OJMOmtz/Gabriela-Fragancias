-- Tabla de Perfumistas
CREATE TABLE Perfumistas (
    ID_Perfumista INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Nacionalidad VARCHAR(50),
    UNIQUE (Nombre, Apellido)
);

-- Tabla de Notas Olfativas
CREATE TABLE Notas_Olfativas (
    ID_Nota INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(50) NOT NULL,
    Descripcion TEXT,
    UNIQUE (Nombre)
);

-- Tabla de relación entre Productos y Notas Olfativas
CREATE TABLE Producto_Notas (
    ID_Producto INT,
    ID_Nota INT,
    Tipo_Nota ENUM('Alta', 'Media', 'Base'),
    PRIMARY KEY (ID_Producto, ID_Nota, Tipo_Nota),
    FOREIGN KEY (ID_Producto) REFERENCES Productos(ID_Producto),
    FOREIGN KEY (ID_Nota) REFERENCES Notas_Olfativas(ID_Nota)
);

