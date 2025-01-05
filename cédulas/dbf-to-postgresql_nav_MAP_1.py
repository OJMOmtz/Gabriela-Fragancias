import os
import tkinter as tk
from tkinter import filedialog, messagebox
from dbfread import DBF
import psycopg2
from psycopg2 import sql

# Configuración de la conexión a PostgreSQL
DB_CONFIG = {
    'dbname': 'Gabriela_Fragancias',
    'user': 'postgres',
    'password': 'salmos23',
    'host': 'localhost',
    'port': 5432
}

def conectar_postgresql():
    """Establece una conexión a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a PostgreSQL: {e}")
        return None

def seleccionar_archivo_dbf():
    """Abre un cuadro de diálogo para seleccionar un archivo DBF."""
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo DBF",
        filetypes=[("Archivos DBF", "*.dbf")]
    )
    return file_path

def cargar_datos_dbf(file_path):
    """Carga los datos desde un archivo DBF."""
    try:
        table = DBF(file_path, load=True, encoding='latin-1')
        return [record for record in table]
    except Exception as e:
        messagebox.showerror("Error al cargar DBF", f"No se pudo leer el archivo DBF: {e}")
        return None

def insertar_datos_postgresql(data, table_name):
    """Inserta los datos del DBF en PostgreSQL."""
    conn = conectar_postgresql()
    if not conn:
        return

    try:
        with conn.cursor() as cursor:
            # Asumimos que las claves del primer registro son los nombres de las columnas
            columns = data[0].keys()
            query = sql.SQL(
                "INSERT INTO {table} ({fields}) VALUES ({placeholders})"
            ).format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
                placeholders=sql.SQL(", ").join(sql.Placeholder() * len(columns))
            )

            # Inserta cada fila
            for record in data:
                cursor.execute(query, list(record.values()))

        conn.commit()
        messagebox.showinfo("Éxito", f"Se insertaron {len(data)} registros en la tabla '{table_name}' correctamente.")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error al insertar datos", f"Ocurrió un error al insertar datos: {e}")
    finally:
        conn.close()

def main():
    """Función principal para ejecutar el programa."""
    # Crear ventana principal
    root = tk.Tk()
    root.title("Importar DBF a PostgreSQL")
    root.geometry("400x200")

    def ejecutar_importacion():
        file_path = seleccionar_archivo_dbf()
        if not file_path:
            return

        data = cargar_datos_dbf(file_path)
        if not data:
            return

        table_name = table_name_entry.get().strip()
        if not table_name:
            messagebox.showerror("Error", "Debe especificar el nombre de la tabla en PostgreSQL.")
            return

        insertar_datos_postgresql(data, table_name)

    # Elementos de la interfaz gráfica
    tk.Label(root, text="Nombre de la tabla en PostgreSQL:").pack(pady=10)
    table_name_entry = tk.Entry(root, width=30)
    table_name_entry.pack(pady=5)

    tk.Button(root, text="Seleccionar DBF e Importar", command=ejecutar_importacion).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
