import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
from typing import List, Tuple, Dict
from collections import Counter, defaultdict
import json
import csv
from datetime import datetime

class SQLAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Analizador de Archivos SQL")
        self.root.geometry("1000x700")
        self.table_counts = Counter()
        self.setup_ui()

        # Variables para almacenar datos
        self.sql_content = ""
        self.renamed_sql_content = ""
        self.table_mapping = {}
        self.table_relations = defaultdict(list)
        self.indices = defaultdict(list)
        self.constraints = defaultdict(list)

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, pady=10)

        # Botones
        ttk.Button(
            button_frame, 
            text="Seleccionar Archivo SQL", 
            command=self.analizar_archivo
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="Exportar SQL Renombrado",
            command=self.exportar_sql_renombrado
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame,
            text="Exportar Análisis",
            command=self.exportar_analisis
        ).grid(row=0, column=2, padx=5)

        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Pestañas de análisis
        self.result_text = self.crear_text_area("Análisis General")
        self.indices_text = self.crear_text_area("Índices y Constraints")
        self.relations_text = self.crear_text_area("Relaciones entre Tablas")

    def crear_text_area(self, tab_name: str) -> tk.Text:
        """Crea un área de texto con scrollbar en una nueva pestaña."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=tab_name)

        text_area = tk.Text(frame, height=30, width=100, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_area.yview)

        text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        text_area.config(yscrollcommand=scrollbar.set)

        return text_area

    def generar_nuevo_nombre(self, nombre_original: str) -> str:
        """Genera un nuevo nombre para una tabla si ya existe."""
        base_name = nombre_original.split('.')[-1]  # Maneja casos como schema.tabla
        self.table_counts[base_name] += 1
        if self.table_counts[base_name] > 1:
            base_name = f"{base_name}_{self.table_counts[base_name]}"
        return base_name

    def renombrar_tablas(self, sql_content: str) -> Tuple[str, Dict[str, str]]:
        """Renombra las tablas en el contenido SQL y devuelve el nuevo contenido y el mapeo."""
        modified_content = sql_content
        table_mapping = {}

        # Encuentra todas las definiciones CREATE TABLE
        create_table_pattern = r"CREATE TABLE\s+([\w\.]+)\s*\("
        table_names = re.findall(create_table_pattern, sql_content)

        for original_name in table_names:
            new_name = self.generar_nuevo_nombre(original_name)
            table_mapping[original_name] = new_name

        for original_name, new_name in table_mapping.items():
            modified_content = re.sub(
                fr"\b{re.escape(original_name)}\b",
                new_name,
                modified_content
            )

        return modified_content, table_mapping

    def extraer_tablas(self, content: str) -> List[Tuple[str, str]]:
        """Extrae las definiciones de tablas del contenido SQL."""
        return re.findall(r"CREATE TABLE\s+([\w\.]+)\s*\((.*?)\);", content, re.DOTALL)

    def analizar_columnas(self, table_def: str) -> List[str]:
        """Analiza las columnas de una definición de tabla."""
        columns = []
        for line in table_def.split('\n'):
            line = line.strip()
            if line and not line.startswith(('PRIMARY KEY', 'FOREIGN KEY', 'CONSTRAINT')):
                columns.append(line.rstrip(','))
        return columns

    def analizar_indices(self, content: str):
        """Analiza los índices en el contenido SQL."""
        index_pattern = r"CREATE\s+(?:UNIQUE\s+)?INDEX\s+(\w+)\s+ON\s+(\w+)\s*\((.*?)\)"
        indices = re.findall(index_pattern, content, re.IGNORECASE)

        self.indices_text.delete(1.0, tk.END)
        self.indices_text.insert(tk.END, "=== ÍNDICES ===\n\n")

        for index_name, table_name, columns in indices:
            self.indices[table_name].append({
                'name': index_name,
                'columns': [col.strip() for col in columns.split(',')]
            })
            self.indices_text.insert(tk.END, f"Tabla: {table_name}\n")
            self.indices_text.insert(tk.END, f"  Índice: {index_name}\n")
            self.indices_text.insert(tk.END, f"  Columnas: {columns}\n\n")

    def analizar_constraints(self, content: str):
        """Analiza los constraints en el contenido SQL."""
        table_pattern = r"CREATE TABLE\s+(\w+)\s*\((.*?)\);"
        tables = re.findall(table_pattern, content, re.DOTALL)

        self.indices_text.insert(tk.END, "=== CONSTRAINTS ===\n\n")

        for table_name, table_def in tables:
            pk_pattern = r"PRIMARY KEY\s*\((.*?)\)"
            pk_matches = re.findall(pk_pattern, table_def)

            fk_pattern = r"FOREIGN KEY\s*\((.*?)\)\s*REFERENCES\s*(\w+)\s*\((.*?)\)"
            fk_matches = re.findall(fk_pattern, table_def)

            unique_pattern = r"UNIQUE\s*\((.*?)\)"
            unique_matches = re.findall(unique_pattern, table_def)

            self.constraints[table_name] = {
                'primary_keys': pk_matches,
                'foreign_keys': fk_matches,
                'unique_constraints': unique_matches
            }

            self.indices_text.insert(tk.END, f"Tabla: {table_name}\n")
            if pk_matches:
                self.indices_text.insert(tk.END, f"  Primary Key: {', '.join(pk_matches)}\n")

            for fk_cols, ref_table, ref_cols in fk_matches:
                self.indices_text.insert(tk.END, \
                    f"  Foreign Key: ({fk_cols}) → {ref_table}({ref_cols})\n")

                # Almacenar relaciones
                self.table_relations[table_name].append({
                    'referenced_table': ref_table,
                    'columns': fk_cols,
                    'referenced_columns': ref_cols
                })

            for unique_cols in unique_matches:
                self.indices_text.insert(tk.END, f"  Unique: {unique_cols}\n")

            self.indices_text.insert(tk.END, "\n")

    def analizar_relaciones(self):
        """Analiza y muestra las relaciones entre tablas."""
        self.relations_text.delete(1.0, tk.END)
        self.relations_text.insert(tk.END, "=== RELACIONES ENTRE TABLAS ===\n\n")

        for table, relations in self.table_relations.items():
            self.relations_text.insert(tk.END, f"Tabla: {table}\n")
            for relation in relations:
                self.relations_text.insert(tk.END, \
                    f"  → Referencia: {relation['referenced_table']}\n    Columnas: {relation['columns']} → {relation['referenced_columns']}\n")
            self.relations_text.insert(tk.END, "\n")

    def mostrar_analisis(self, sql_content: str):
        """Muestra el análisis del contenido SQL."""
        self.result_text.delete(1.0, tk.END)

        tables = self.extraer_tablas(sql_content)
        self.result_text.insert(tk.END, "=== TABLAS ENCONTRADAS ===\n\n")

        for table_name, table_def in tables:
            self.result_text.insert(tk.END, f"Tabla: {table_name}\n")
            columns = self.analizar_columnas(table_def)
            for column in columns:
                self.result_text.insert(tk.END, f"  - {column}\n")
            self.result_text.insert(tk.END, "\n")

    def analizar_archivo(self):
        """Analiza el archivo SQL seleccionado."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos SQL", "*.sql"), ("Todos los archivos", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.sql_content = file.read()

            self.renamed_sql_content, self.table_mapping = self.renombrar_tablas(self.sql_content)

            self.mostrar_analisis(self.renamed_sql_content)
            self.analizar_indices(self.renamed_sql_content)
            self.analizar_constraints(self.renamed_sql_content)
            self.analizar_relaciones()

        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo: {str(e)}")

    def exportar_sql_renombrado(self):
        """Exporta el SQL con las tablas renombradas."""
        if not self.renamed_sql_content:
            messagebox.showwarning("Advertencia", "Primero debe analizar un archivo SQL.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".sql",
            filetypes=[("Archivos SQL", "*.sql"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.renamed_sql_content)
                messagebox.showinfo("Éxito", "Archivo SQL renombrado exportado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar el archivo: {str(e)}")

    def exportar_analisis(self):
        """Exporta el análisis completo a diferentes formatos."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"analisis_sql_{timestamp}"

        try:
            with open(f"{base_filename}.txt", 'w', encoding='utf-8') as f:
                f.write(self.result_text.get(1.0, tk.END))
                f.write("\n\nÍNDICES Y CONSTRAINTS\n")
                f.write(self.indices_text.get(1.0, tk.END))
                f.write("\n\nRELACIONES\n")
                f.write(self.relations_text.get(1.0, tk.END))

            with open(f"{base_filename}.json", 'w', encoding='utf-8') as f:
                json.dump({
                    'table_mapping': self.table_mapping,
                    'indices': dict(self.indices),
                    'constraints': dict(self.constraints),
                    'relations': dict(self.table_relations)
                }, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Éxito", "Análisis exportado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar el análisis: {str(e)}")

    def run(self):
        """Inicia la aplicación."""
        self.root.mainloop()

if __name__ == "__main__":
    app = SQLAnalyzer()
    app.run()
