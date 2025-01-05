import csv
from datetime import datetime
import pandas as pd

def clean_csv(input_file, output_file):
    """
    Limpia un archivo CSV manejando múltiples formatos de fecha,
    separadores de miles y campos vacíos.
    
    Args:
        input_file (str): Ruta del archivo CSV de entrada
        output_file (str): Ruta del archivo CSV de salida
    """
    def clean_date(date_str):
        if not date_str or pd.isna(date_str):
            return ''
        try:
            # Para formato YYYYMMDD
            if len(str(date_str).strip()) == 8 and '/' not in str(date_str):
                date_str = str(date_str).strip()
                return f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:]}"
            # Para formato DD/MM/YYYY
            elif '/' in str(date_str):
                day, month, year = map(int, date_str.split('/'))
                return f"{year:04d}/{month:02d}/{day:02d}"
            return ''
        except (ValueError, AttributeError):
            return ''

    def clean_number(number_str):
        if not number_str or pd.isna(number_str):
            return ''
        # Elimina puntos de los números
        return str(number_str).replace('.', '')

    def clean_address(addr):
        if not addr or pd.isna(addr):
            return ''
        # Reemplaza múltiples guiones por uno solo y limpia espacios
        cleaned = ' - '.join(part.strip() for part in addr.split('-') if part.strip())
        return cleaned

    try:
        # Leer el CSV con pandas para mejor manejo de datos faltantes
        df = pd.read_csv(input_file, sep=';', encoding='utf-8')
        
        # Limpiar cada columna según su tipo
        if 'CEDULA' in df.columns:
            df['CEDULA'] = df['CEDULA'].apply(clean_number)
        
        if 'FEC_NAC' in df.columns:
            df['FEC_NAC'] = df['FEC_NAC'].apply(clean_date)
        
        if 'DIRECC' in df.columns:
            df['DIRECC'] = df['DIRECC'].apply(clean_address)
        
        # Rellenar valores nulos con string vacío
        df = df.fillna('')
        
        # Guardar el archivo limpio
        df.to_csv(output_file, sep=';', index=False, encoding='utf-8')
        
        return True, "Archivo limpiado exitosamente"
        
    except Exception as e:
        return False, f"Error al procesar el archivo: {str(e)}"

# Ejemplo de uso
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog, messagebox
    
    def browse_input():
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filename)
    
    def browse_output():
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        output_entry.delete(0, tk.END)
        output_entry.insert(0, filename)
    
    def process_file():
        input_file = input_entry.get()
        output_file = output_entry.get()
        
        if not input_file or not output_file:
            messagebox.showerror("Error", "Por favor seleccione archivos de entrada y salida")
            return
            
        success, message = clean_csv(input_file, output_file)
        if success:
            messagebox.showinfo("Éxito", message)
        else:
            messagebox.showerror("Error", message)
    
    # Crear ventana
    root = tk.Tk()
    root.title("Limpiador de CSV")
    
    # Entrada
    tk.Label(root, text="Archivo de entrada:").pack(pady=5)
    input_entry = tk.Entry(root, width=50)
    input_entry.pack(pady=5)
    tk.Button(root, text="Examinar", command=browse_input).pack()
    
    # Salida
    tk.Label(root, text="Archivo de salida:").pack(pady=5)
    output_entry = tk.Entry(root, width=50)
    output_entry.pack(pady=5)
    tk.Button(root, text="Examinar", command=browse_output).pack()
    
    # Botón procesar
    tk.Button(root, text="Procesar", command=process_file).pack(pady=20)
    
    root.mainloop()
