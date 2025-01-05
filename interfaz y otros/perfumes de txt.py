import os

# Ruta del archivo fuente (archivo base)
file_path = "D:/Gabriela Fragancias/2024/Perfumes en 3NF.txt"

# Ruta donde se guardará el archivo SQL generado
new_file_path = "D:/Gabriela Fragancias/2024/SQL_Organized_Perfumes3.txt"

# Crear el directorio si no existe
os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

# Inicializar las listas para almacenar los datos extraídos
marcas = set()  # Evitar duplicados
perfumes = []
presentaciones = []

# Función para limpiar los datos y remover texto no deseado
def limpiar_texto(texto):
    texto = texto.replace("\n", " ").replace("", " ").strip()  # Remover saltos de línea y caracteres no deseados
    texto = " ".join(texto.split())  # Eliminar espacios dobles o más
    return texto

# Leer el archivo base y filtrar los datos relevantes
try:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = limpiar_texto(line)
            # Asumir que los datos útiles están separados por comas en un formato conocido
            # formato: código_barra, marca, perfume, tamaño_ml, costo, precio, sexo, tipo
            if ',' in line:  # Procesar solo líneas que parecen tener datos útiles
                columns = line.split(",")
                
                if len(columns) >= 8:  # Asegurar que hay suficientes columnas
                    codigo_barra = columns[0].strip()
                    marca = columns[1].strip()
                    perfume = columns[2].strip()
                    tamano_ml = columns[3].strip()
                    costo = columns[4].strip()
                    precio = columns[5].strip()
                    sexo = columns[6].strip()
                    tipo = columns[7].strip()

                    # Almacenar datos únicos para marca
                    marcas.add(marca)

                    # Guardar el perfume y sus detalles
                    perfumes.append((marca, perfume, costo, precio, sexo, tipo))

                    # Guardar la presentación
                    presentaciones.append((perfume, codigo_barra, tamano_ml))

    print("Datos extraídos correctamente del archivo base.")

except FileNotFoundError:
    print(f"No se encuentra el archivo base en la ruta: {file_path}")

# Generar las inserciones SQL
sql_output = []

# Insertar marcas
sql_output.append("-- Tabla Marca")
for i, marca in enumerate(marcas, start=1):
    sql_output.append(f"INSERT INTO Marca (id_marca, nombre_marca) VALUES ({i}, '{marca}');")

# Insertar perfumes
sql_output.append("\n-- Tabla Perfume")
for i, (marca, perfume, costo, precio, sexo, tipo) in enumerate(perfumes, start=1):
    sql_output.append(f"INSERT INTO Perfume (id_perfume, nombre_perfume, costo, precio_venta_contado, segmento, franja_etaria, ocasion) "
                      f"VALUES ({i}, '{perfume}', {costo}, {precio}, '{tipo}', '{sexo}', '');")

# Insertar presentaciones
sql_output.append("\n-- Tabla Presentacion")
for i, (perfume, codigo_barra, tamano_ml) in enumerate(presentaciones, start=1):
    sql_output.append(f"INSERT INTO Presentacion (id_presentacion, codigo_barra, tamano_ml) "
                      f"VALUES ({i}, '{codigo_barra}', {tamano_ml});")

# Guardar las inserciones SQL en el archivo
try:
    with open(new_file_path, "w", encoding="utf-8") as new_file:
        new_file.write("\n".join(sql_output))
    print(f"Archivo SQL generado y guardado correctamente en: {new_file_path}")

except FileNotFoundError:
    print(f"No se puede guardar el archivo en la ruta: {new_file_path}")
