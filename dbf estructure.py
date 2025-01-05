import geopandas as gpd
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from dbfread import DBF
import hashlib

def browse_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(tk.END, directory)

def analyze_files():
    directory = directory_entry.get()
    include_subdirs = include_subdirs_var.get()

    if not directory:
        status_label.config(text="Por favor, selecciona un directorio.")
        return

    progress_bar["maximum"] = len(os.listdir(directory))
    progress_bar["value"] = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_size = os.path.getsize(file_path)
            md5_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            
            if filename.endswith(".dbf"):
                try:
                    dbf = DBF(file_path, lowernames=True)
                    print(f"File: {file_path}")
                    print(f"Size: {file_size} bytes")
                    print(f"MD5: {md5_hash}")
                    print(f"Number of records: {len(dbf)}")
                    print("Columns:")
                    for field in dbf.fields:
                        print(f"  - {field.name}")
                        print(f"    Type: {field.type}")
                        print(f"    Length: {field.length}")
                        if hasattr(field, 'decimal'):
                            print(f"    Decimal: {field.decimal}")
                    print("\n")
                except Exception as e:
                    print(f"Error reading file: {filename}")
                    print(f"Error message: {str(e)}")
                    print("\n")
            
            progress_label.config(text=f"Procesando: {filename}")
            progress_bar["value"] += 1
            progress_bar.update()
            window.update()  # Actualiza la ventana para evitar que se paralice

        if not include_subdirs:
            break

    status_label.config(text="¡Análisis completado!", font=("IBM Plex Mono", 14, "bold"))

# Create the main window
window = tk.Tk()
window.title("Análisis de Estructura de Archivos")

# Create and pack the widgets
directory_label = tk.Label(window, text="Directorio:")
directory_label.pack()

directory_frame = tk.Frame(window)
directory_entry = tk.Entry(directory_frame, width=50)
directory_entry.pack(side=tk.LEFT)

browse_button = tk.Button(directory_frame, text="Explorar", command=browse_directory)
browse_button.pack(side=tk.LEFT)
directory_frame.pack()

include_subdirs_var = tk.BooleanVar()
include_subdirs_check = tk.Checkbutton(window, text="Incluir subdirectorios", variable=include_subdirs_var)
include_subdirs_check.pack()

analyze_button = tk.Button(window, text="Analizar", command=analyze_files)
analyze_button.pack()

progress_label = tk.Label(window, text="")
progress_label.pack()

progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
progress_bar.pack()

status_label = tk.Label(window, text="")
status_label.pack()

# Start the main event loop
window.mainloop()