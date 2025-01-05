# Let's process the data from the provided text file to organize it into a CSV format with the required columns: 
# Marca, Producto, Código de barras, Peso, Tipo (DT, EDP, Desodorante), Costo, Precio.

import csv

# Raw data extracted from the file
data = "Lista Gabriel Fragancias.txt"

# Process and organize the data
rows = []
lines = data.splitlines()

for line in lines:
    parts = line.split('\t')
    if len(parts) == 5:
        marca, producto, peso, costo, precio = parts
        codigo = ''
        tipo = 'EDT' if 'EDT' in producto else 'EDP' if 'EDP' in producto else 'EDC' if 'EDC' in producto else ''
    elif len(parts) == 4:
        marca, producto, peso, costo = parts
        codigo = ''
        precio = costo
        tipo = 'EDT' if 'EDT' in producto else 'EDP' if 'EDP' in producto else 'EDC' if 'EDC' in producto else ''
    elif len(parts) == 3:
        marca, producto, peso = parts
        codigo = ''
        costo = ''
        precio = ''
        tipo = 'EDT' if 'EDT' in producto else 'EDP' if 'EDP' in producto else 'EDC' if 'EDC' in producto else ''
    else:
        continue

    rows.append([marca.strip(), producto.strip(), codigo.strip(), peso.strip(), tipo.strip(), costo.strip(), precio.strip()])

# Write to CSV
output_file = "/mnt/data/perfume_data.csv"

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Marca', 'Producto', 'Código de barras', 'Peso', 'Tipo', 'Costo', 'Precio'])
    writer.writerows(rows)

output_file
