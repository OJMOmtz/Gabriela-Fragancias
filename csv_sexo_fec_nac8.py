# Lee el archivo CSV y escribe en un nuevo archivo CSV con las columnas reordenadas
with open(r'D:\PADRONES\csvs\.idea\CÉDULAS-2024-1_ISO-8859-1.csv', 'r', encoding='ISO-8859-1') as file_in:
    with open(r'D:\PADRONES\csvs\.idea\CÉDULAS-2024-1_ISO-8859-1_nuevo.csv', 'w', encoding='ISO-8859-1') as file_out:
        header = file_in.readline().strip().split(';')
        indice_fecha = header.index('fecha_nacimiento')
        indice_sexo = header.index('sexo')
        header[indice_sexo], header[indice_fecha] = header[indice_fecha], header[indice_sexo]
        file_out.write(';'.join(header) + '\n')
        
        for line in file_in:
            try:
                values = line.strip().split(';')
                values[indice_sexo], values[indice_fecha] = values[indice_fecha], values[indice_sexo]
                file_out.write(';'.join(values) + '\n')
            except:
                pass
