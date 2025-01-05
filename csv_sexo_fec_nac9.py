import pandas as pd

def analizar_csv(archivo):
    errores = []
    datos_correctos = []
    
    with open(archivo, 'r', encoding='ISO-8859-1') as f:
        for i, linea in enumerate(f):
            campos = linea.strip().split(',')
            if len(campos) != 6:
                errores.append((i+1, "Número de campos incorrecto"))
            # Aquí puedes agregar más validaciones según tus necesidades
            else:
                datos_correctos.append(campos)

    # Crear DataFrame con los datos correctos
    df = pd.DataFrame(datos_correctos, columns=["numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion"])

    # Reordenar columnas
    df = df[["numero_cedula", "nombre", "apellido", "fecha_nacimiento", "sexo", "direccion"]]

    return df, errores

# Llamar a la función con el nombre de tu archivo
archivo = r"D:\PADRONES\csvs\.idea\CÉDULAS-2024-1_ISO-8859-1.csv"
df, errores = analizar_csv(archivo)

# Imprimir los errores
if errores:
    print("Se encontraron los siguientes errores:")
    for error in errores:
        print(f"Línea {error[0]}: {error[1]}")

# Guardar el DataFrame corregido
df.to_csv("datos_corregidos.csv", index=False, sep=",")
