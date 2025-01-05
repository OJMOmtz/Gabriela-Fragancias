import tkinter as tk
from tkinter import filedialog
import csv
import dbf
from datetime import datetime
import struct

def is_valid_date(date_string):
    try:
        if '/' in date_string:
            if len(date_string.split('/')[0]) == 4:
                anio, mes, dia = map(int, date_string.split('/'))
            else:
                dia, mes, anio = map(int, date_string.split('/'))
        else:
            if len(date_string) == 8:
                anio, mes, dia = int(date_string[:4]), int(date_string[4:6]), int(date_string[6:8])
            else:
                return False
        
        datetime(anio, mes, dia)
        return True
    except ValueError:
        return False

def convert_csv_to_dbf(csv_file, dbf_file):
    # Leer el archivo CSV con codificación UTF-8
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        
        # Crear el archivo DBF
        table = dbf.Table(
            dbf_file,
            [
                'CEDULA C(10)',
                'NOMBRE C(50)',
                'APELLIDO C(50)',
                'FEC_NAC D',
                'DIRECC C(100)'
            ],
            codepage='cp1252'  # Especificar la página de códigos Latin-1
        )
        table.open(mode=dbf.READ_WRITE)

        # Recorrer las filas del CSV y escribirlas en el DBF
        for row in reader:
            cedula = row['CEDULA'].replace('.', '')[:10]  # Eliminar separadores de miles
            nombre = row['NOMBRE'][:50].encode('cp1252', errors='replace').decode('cp1252')
            apellido = row['APELLIDO'][:50].encode('cp1252', errors='replace').decode('cp1252')
            
            fecha_raw = row['FEC_NAC']
            if not is_valid_date(fecha_raw):
                print(f"Skipping invalid date: {fecha_raw}")
                continue  # Skip the current row and move to the next one
            
            if '/' in fecha_raw:
                if len(fecha_raw.split('/')[0]) == 4:
                    anio, mes, dia = map(int, fecha_raw.split('/'))
                else:
                    dia, mes, anio = map(int, fecha_raw.split('/'))
            else:
                anio, mes, dia = int(fecha_raw[:4]), int(fecha_raw[4:6]), int(fecha_raw[6:8])
            
            fec_nac = datetime(anio, mes, dia)         
            except (ValueError, IndexError) as e:
                print(f"Error processing date '{fecha_raw}': {str(e)}")
                continue  # Skip the current row and move to the next one
            
            direcc = (row['DIRECC'] or '')[:100].encode('cp1252', errors='replace').decode('cp1252')
            
            table.append((cedula, nombre, apellido, fec_nac, direcc))
        
        # Cerrar el archivo DBF
        table.close()
       
def update_character(string, fielddef, memo, input_decoder, encoder):
    "Updates data with the given string"
    string = encoder(string.strip())[0]  # Codificar la cadena utilizando UTF-8
    if len(string) > fielddef.length:
        if memo:
            string = string[:fielddef.length - 10]  # 10 for the memo reference
            memo_string = string + '\x00'  # for update_log
            memo_fields = memo.get_memo_fields()
            if memo_fields:
                field_num = memo_fields[0]
            else:
                field_num = memo.next_memo_field()
            memo_data = array('B', input_decoder(string)[0] + '\x1a')
            block, offset = memo.add_memo(field_num, memo_data)
            string = string[:fielddef.length - 10] + struct.pack('<l', block)[0:4] + struct.pack('<l', offset)[0:4]
        else:
            string = string[:fielddef.length]
    return array('B', string) + array('B', '\x00' * (fielddef.length - len(string)))
        
def browse_csv():
    csv_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    csv_entry.delete(0, tk.END)
    csv_entry.insert(tk.END, csv_file)

def browse_dbf():
    dbf_file = filedialog.asksaveasfilename(defaultextension=".dbf", filetypes=[("DBF Files", "*.dbf")])
    dbf_entry.delete(0, tk.END)
    dbf_entry.insert(tk.END, dbf_file)

def convert():
    csv_file = csv_entry.get()
    dbf_file = dbf_entry.get()
    convert_csv_to_dbf(csv_file, dbf_file)
    status_label.config(text="Conversión completada!")

# Crear la ventana principal
window = tk.Tk()
window.title("CSV a DBF")

# Entrada para el archivo CSV
csv_label = tk.Label(window, text="Archivo CSV:")
csv_label.pack()
csv_entry = tk.Entry(window, width=50)
csv_entry.pack()
csv_button = tk.Button(window, text="Buscar", command=browse_csv)
csv_button.pack()

# Entrada para el archivo DBF
dbf_label = tk.Label(window, text="Archivo DBF:")
dbf_label.pack()
dbf_entry = tk.Entry(window, width=50)
dbf_entry.pack()
dbf_button = tk.Button(window, text="Guardar como", command=browse_dbf)
dbf_button.pack()

# Botón para iniciar la conversión
convert_button = tk.Button(window, text="Convertir", command=convert)
convert_button.pack()

# Etiqueta para mostrar el estado
status_label = tk.Label(window, text="")
status_label.pack()

# Iniciar la ventana
window.mainloop()