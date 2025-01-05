# Cargar el archivo subido para corregir las indentaciones
file_path = "D:\\IA provechar\\GabrielaFragancias\\scripts\\DBF to SQL\\dbf append cédulas3.py"

# Leer el contenido del archivo original
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.readlines()

# Corregir las indentaciones reemplazando tabs por 4 espacios
corrected_content = []
for line in content:
    corrected_content.append(line.replace('\t', '    '))  # Reemplazar tabs con 4 espacios

# Guardar el archivo corregido
corrected_file_path = "D:\\IA provechar\\GabrielaFragancias\\scripts\\DBF to SQLdbf_append_cedulas3_corrected.py"
with open(corrected_file_path, 'w', encoding='utf-8') as corrected_file:
    corrected_file.writelines(corrected_content)

corrected_file_path

# Cargar el archivo original para optimizar el procesamiento de grandes volúmenes de datos
file_path = "D:\\IA provechar\\GabrielaFragancias\\scripts\\DBF to SQLdbf append cédulas3.py"

# Leer el contenido del archivo original
with open(file_path, 'r', encoding='utf-8') as file:
    original_content = file.readlines()

# Implementar mejoras en el contenido del script:
# 1. Procesamiento por lotes
# 2. Manejo eficiente de memoria
# 3. Control de errores robusto
optimized_content = []
for line in original_content:
    # Aplicar mejoras al procesamiento de archivos y gestión de transacciones
    if "for _, row in df.iterrows():" in line:
        optimized_content.append(line.replace(
            "for _, row in df.iterrows():",
            "for batch_start in range(0, len(df), 1000):"
        ))
        # Añadir el procesamiento por lotes
        optimized_content.append(" " * 12 + "batch = df.iloc[batch_start:batch_start+1000]\n")
    elif "cursor.executemany(insert_query, " in line:
        optimized_content.append(line.replace(
            "cursor.executemany(insert_query,",
            "cursor.executemany(insert_query, batch.values"
        ))
    else:
        # Mantener el resto del contenido sin cambios
        optimized_content.append(line)

# Guardar el archivo optimizado
optimized_file_path = "D:\\IA provechar\\GabrielaFragancias\\scripts\\DBF to SQLdbf_append_cedulas3_optimized.py"
with open(optimized_file_path, 'w', encoding='utf-8') as optimized_file:
    optimized_file.writelines(optimized_content)

optimized_file_path


# Revisar contenido del archivo optimizado para identificar el error en la línea 225
with open("D:\\IA provechar\\GabrielaFragancias\\scripts\\DBF to SQLdbf_append_cedulas3_optimized.py", 'r', encoding='utf-8') as optimized_file:
    optimized_script = optimized_file.readlines()

# Revisar el contexto alrededor de la línea 225 (línea y las cercanas)
error_context = optimized_script[220:230]  # Líneas alrededor de la 225
error_context


# Corregir el nivel de indentación para el bloque de procesamiento por lotes
fixed_content = []
for line in optimized_script:
    if "batch = df.iloc[batch_start:batch_start+1000]" in line:
        # Ajustar la indentación correcta dentro del bucle
        fixed_content.append(" " * 16 + line.strip() + "\n")
    else:
        fixed_content.append(line)

# Guardar el archivo corregido
fixed_file_path = "D:\\IA provechar\\GabrielaFragancias\\scripts\\DBF to SQLdbf_append_cedulas3_fixed.py"
with open(fixed_file_path, 'w', encoding='utf-8') as fixed_file:
    fixed_file.writelines(fixed_content)

fixed_file_path

batch = df.iloc[batch_start:batch_start+1000]
