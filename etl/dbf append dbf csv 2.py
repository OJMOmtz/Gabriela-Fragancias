import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from dbfread import DBF
import pandas as pd
import threading

def browse_dbf_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("DBF Files", "*.dbf")])
    if file_paths:
        dbf_path_label.config(text=", ".join(file_paths))
        update_column_sources(file_paths[0])

def update_column_sources(file_path):
    if file_path:
        dbf = DBF(file_path, char_decode_errors='ignore')
        columns = dbf.field_names
        for col_src_combo in column_sources:
            col_src_combo.config(values=columns)

def migration_thread():
    file_paths = dbf_path_label.cget("text").split(", ")
    if file_paths:
        dfs = []
        progress_step = 100 // len(file_paths)
        progress_bar['value'] = 0
        for file_path in file_paths:
            dbf = DBF(file_path, char_decode_errors='ignore')
            df = pd.DataFrame(iter(dbf))
            dfs.append(df)
            progress_bar['value'] += progress_step
            progress_bar.update()
        combined_df = pd.concat(dfs)
        column_mapping = {}
        for col_src_combo, col_tgt in zip(column_sources, column_targets):
            column_mapping[col_src_combo.get()] = col_tgt
        combined_df = combined_df.rename(columns=column_mapping)
        combined_df = combined_df.drop_duplicates()
        output_csv = 'migrated.csv'
        combined_df.to_csv(output_csv, index=False)
        progress_bar['value'] = 100
        print(f"Datos migrados y guardados en {output_csv}")

def run_migration():
    migration_thread_obj = threading.Thread(target=migration_thread)
    migration_thread_obj.start()

root = tk.Tk()
root.title("DBF Migration Tool")

# DBF file selection
dbf_path_label = ttk.Label(root, text="Selecciona archivos DBF...")
dbf_path_label.pack()
browse_button = ttk.Button(root, text="Buscar archivos DBF", command=browse_dbf_files)
browse_button.pack()

# Column mapping
column_frame = ttk.Frame(root)
column_frame.pack(pady=10)

column_sources = []
column_targets = []

for i, col_tgt in enumerate(["numero_cedula", "nombre", "apellido", "sexo", "fecha_nacimiento", "lugar_nacimiento", "direccion"]):
    ttk.Label(column_frame, text=f"Columna de origen {i+1}").grid(row=i, column=0)
    col_src_combo = ttk.Combobox(column_frame)
    col_src_combo.grid(row=i, column=1)
    column_sources.append(col_src_combo)

    ttk.Label(column_frame, text=f"Columna de destino {i+1}").grid(row=i, column=2)
    col_tgt_label = ttk.Label(column_frame, text=col_tgt)
    col_tgt_label.grid(row=i, column=3)
    column_targets.append(col_tgt)

# Progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.pack(pady=10)

# Run migration button
run_button = ttk.Button(root, text="Ejecutar migración", command=run_migration)
run_button.pack()

root.mainloop()