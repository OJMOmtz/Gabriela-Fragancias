import os
import pandas as pd
from dbfread import DBF
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from io import StringIO
import sys

def get_column_type_from_dtype(dtype):
    """Convertir dtype de pandas a tipo SQL."""
    dtype_str = str(dtype)
    if 'int' in dtype_str:
        return 'INTEGER'
    elif 'float' in dtype_str:
        return 'NUMERIC'
    elif 'datetime' in dtype_str:
        return 'TIMESTAMP'
    elif 'bool' in dtype_str:
        return 'BOOLEAN'
    else:
        return 'VARCHAR(255)'

def get_column_type(field_type, field_length):
    """Convertir tipo DBF a tipo SQL."""
    type_mapping = {
        'C': lambda length: f"VARCHAR({length})",
        'N': lambda length: f"NUMERIC({length})",
        'L': lambda _: "BOOLEAN",
        'D': lambda _: "DATE",
        'T': lambda _: "TIMESTAMP",
        'F': lambda length: f"NUMERIC({length})",
        'B': lambda _: "BLOB",
        'M': lambda _: "TEXT",
        'G': lambda _: "BLOB",
        'P': lambda _: "BLOB",
        'Y': lambda _: "DECIMAL(10,4)"
    }
    
    return type_mapping.get(field_type, lambda x: "VARCHAR(255)")(field_length)

def capture_pandas_info():
    """Capturar la salida de df.info() en un string."""
    buffer = StringIO()
    sys.stdout = buffer
    return buffer, sys.stdout

def analyze_dbf_file(file_path):
    """Analizar estructura de archivo DBF."""
    try:
        table = DBF(file_path, encoding='latin-1')
        columns = []
        
        for field in table.fields:
            columns.append({
                "Nombre": field.name,
                "Tipo": get_column_type(field.type, field.length),
                "Longitud": field.length,
                "Decimales": field.decimal_count if hasattr(field, 'decimal_count') else None
            })
        
        structure = {
            "Tipo": "DBF",
            "Columnas": columns,
            "Total_Filas": len(table),
            "Tamaño_Bytes": os.path.getsize(file_path),
            "Tamaño_MB": round(os.path.getsize(file_path) / (1024 * 1024), 2),
            "Encoding": table.encoding
        }
        return structure
    except Exception as e:
        print(f"Error al analizar el archivo DBF {file_path}: {str(e)}")
        return None

def analyze_csv_file(file_path):
    """Analizar estructura de archivo CSV."""
    try:
        df = pd.read_csv(file_path, encoding='iso-8859-1', on_bad_lines='skip')
        columns = []
        
        for col_name, dtype in df.dtypes.items():
            null_count = df[col_name].isna().sum()
            unique_count = df[col_name].nunique()
            
            columns.append({
                "Nombre": col_name,
                "Tipo": get_column_type_from_dtype(dtype),
                "Valores_Nulos": int(null_count),
                "Valores_Unicos": int(unique_count),
                "Muestra": str(df[col_name].head(3).tolist())
            })
        
        structure = {
            "Tipo": "CSV",
            "Columnas": columns,
            "Total_Filas": len(df),
            "Total_Columnas": len(df.columns),
            "Tamaño_Bytes": os.path.getsize(file_path),
            "Tamaño_MB": round(os.path.getsize(file_path) / (1024 * 1024), 2),
            "Memoria_Uso_MB": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
        }
        return structure
    except Exception as e:
        print(f"Error al analizar el archivo CSV {file_path}: {str(e)}")
        return None

def analyze_file(file_path):
    """Analizar archivo según su extensión."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".dbf":
        return analyze_dbf_file(file_path)
    elif ext == ".csv" or ext == ".txt":
        return analyze_csv_file(file_path)
    else:
        return None

class AnalysisResults:
    def __init__(self):
        self.results = {}
    
    def add_result(self, file_path, structure):
        self.results[file_path] = structure
    
    def save_to_file(self, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            for file_path, structure in self.results.items():
                f.write(f"\nArchivo: {file_path}\n")
                f.write("=" * 80 + "\n")
                
                if structure:
                    for key, value in structure.items():
                        if key == "Columnas":
                            f.write("\nColumnas:\n")
                            for col in value:
                                f.write(f"  - {col['Nombre']}: {col['Tipo']}\n")
                                for k, v in col.items():
                                    if k not in ['Nombre', 'Tipo']:
                                        f.write(f"    {k}: {v}\n")
                        else:
                            f.write(f"{key}: {value}\n")
                f.write("\n")

class FileAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Estructuras de Archivos")
        self.root.geometry("800x600")
        
        self.directory_path = tk.StringVar()
        self.include_subdirs_var = tk.BooleanVar()
        self.results = AnalysisResults()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuración del directorio
        directory_frame = ttk.LabelFrame(main_frame, text="Selección de directorio", padding="5")
        directory_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(directory_frame, text="Directorio:").grid(row=0, column=0, padx=5)
        ttk.Entry(directory_frame, textvariable=self.directory_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(directory_frame, text="Examinar", command=self.browse_directory).grid(row=0, column=2, padx=5)
        
        ttk.Checkbutton(directory_frame, text="Incluir subdirectorios", 
                       variable=self.include_subdirs_var).grid(row=1, column=1, pady=5)
        
        # Área de progreso
        self.progress_frame = ttk.LabelFrame(main_frame, text="Progreso", padding="5")
        self.progress_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.progress_label = ttk.Label(self.progress_frame, text="")
        self.progress_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=300, mode='determinate')
        self.progress_bar.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.process_button = ttk.Button(button_frame, text="Procesar", 
                                       command=self.start_processing)
        self.process_button.grid(row=0, column=0, padx=5)
        
        self.save_button = ttk.Button(button_frame, text="Guardar", 
                                    command=self.save_results, state="disabled")
        self.save_button.grid(row=0, column=1, padx=5)
        
        ttk.Button(button_frame, text="Salir", 
                  command=self.root.quit).grid(row=0, column=2, padx=5)
        
        # Área de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="5")
        result_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.result_text = tk.Text(result_frame, height=15, width=80)
        self.result_text.grid(row=0, column=0, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", 
                                command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
    
    def browse_directory(self):
        path = filedialog.askdirectory(title="Selecciona un directorio")
        if path:
            self.directory_path.set(path)
    
    def start_processing(self):
        if not self.directory_path.get():
            messagebox.showwarning("Advertencia", "Por favor, seleccione un directorio.")
            return
        
        self.process_button.config(state="disabled")
        self.save_button.config(state="disabled")
        self.result_text.delete(1.0, tk.END)
        self.progress_bar['value'] = 0
        
        thread = threading.Thread(target=self.process_files)
        thread.daemon = True
        thread.start()
    
    def process_files(self):
        try:
            directory = self.directory_path.get()
            include_subdirs = self.include_subdirs_var.get()
            
            files_to_process = []
            for root, _, files in os.walk(directory):
                if not include_subdirs and root != directory:
                    continue
                
                for file in files:
                    if file.lower().endswith(('.dbf', '.csv', '.txt')):
                        files_to_process.append(os.path.join(root, file))
            
            total_files = len(files_to_process)
            self.progress_bar['maximum'] = total_files
            
            for i, file_path in enumerate(files_to_process, 1):
                self.progress_label.config(text=f"Procesando {i}/{total_files}: {os.path.basename(file_path)}")
                structure = analyze_file(file_path)
                
                if structure:
                    self.results.add_result(file_path, structure)
                    self.update_result_text(file_path, structure)
                
                self.progress_bar['value'] = i
                self.root.update_idletasks()
            
            self.progress_label.config(text="Análisis completado")
            self.save_button.config(state="normal")
            self.process_button.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")
            self.process_button.config(state="normal")
    
    def update_result_text(self, file_path, structure):
        self.result_text.insert(tk.END, f"\nArchivo: {file_path}\n")
        self.result_text.insert(tk.END, "=" * 80 + "\n")
        
        for key, value in structure.items():
            if key == "Columnas":
                self.result_text.insert(tk.END, "\nColumnas:\n")
                for col in value:
                    self.result_text.insert(tk.END, f"  - {col['Nombre']}: {col['Tipo']}\n")
            else:
                self.result_text.insert(tk.END, f"{key}: {value}\n")
        
        self.result_text.see(tk.END)
    
    def save_results(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.results.save_to_file(file_path)
            messagebox.showinfo("Éxito", "Resultados guardados exitosamente")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileAnalyzerGUI(root)
    root.mainloop()
