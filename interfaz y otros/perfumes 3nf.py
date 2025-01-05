import os

# Ruta donde se guardará el archivo
new_file_path = "D:/Gabriela Fragancias/2024/SQL_Organized_Perfumes3.txt"

# Crear el directorio si no existe
os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

# Contenido del archivo SQL organizado
sql_data = """
-- Tabla Marca
INSERT INTO Marca (id_marca, nombre_marca) VALUES 
(1, 'Adidas'), 
(2, 'Air-Val International'), 
(3, 'Alta Moda');

-- Tabla Perfume
INSERT INTO Perfume (id_perfume, nombre_perfume, id_marca, ano_lanzamiento, perfumero, notas_olfativas, costo, precio_venta_contado, precio_venta_credito, segmento, franja_etaria, ocasion) 
VALUES 
(1, 'Adidas Ice Dive', 1, 2001, 'No Disponible', 'Fresca, acuática', 15.00, 28.00, 30.00, 'Deportivo', '18-30', 'Casual'), 
(2, 'Adidas Team Five Special Edition', 1, 2013, 'Philippe Bousseton', 'Cítricos, aromáticos', 20.00, 32.00, 35.00, 'Deportivo', '18-30', 'Casual'),
(3, 'Oh La La! Agatha Ruiz de la Prada', 2, 2010, 'No Disponible', 'Vibrante, floral', 25.00, 45.00, 50.00, 'Juvenil', '15-30', 'Festivo');

-- Tabla Presentacion
INSERT INTO Presentacion (id_presentacion, id_perfume, codigo_barra, tamano_ml) 
VALUES 
(1, 1, '8411114079707', 50), 
(2, 1, '8411114079708', 100), 
(3, 2, '8411061697290', 50), 
(4, 3, '8411061810606', 100);
"""

# Intentar escribir el archivo
try:
    with open(new_file_path, "w", encoding="utf-8") as new_file:
        new_file.write(sql_data)
    print(f"Archivo guardado correctamente en: {new_file_path}")
except FileNotFoundError:
    print(f"No se puede guardar el archivo en la ruta: {new_file_path}")
