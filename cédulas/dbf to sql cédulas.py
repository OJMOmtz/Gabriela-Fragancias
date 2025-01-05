import dbfread
import psycopg2
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk

def browse_dbf_file():
    global dbf_file
    dbf_file = filedialog.askopenfilename(filetypes=[("DBF Files", "*.dbf")])
    dbf_path_label.config(text=dbf_file)
    load_column_sources()

def load_column_sources():
    if dbf_file:
        dbf = dbfread.DBF(dbf_file, encoding='latin-1')
        source_columns = dbf.fields
        for i, col_src_combo in enumerate(column_sources):
            col_src_combo['values'] = source_columns

def run_migration():
    # Get selected column mappings
    source_columns = [col_src.get() for col_src in column_sources]
    target_columns = column_targets.copy()

    # Check if all column mappings are filled
    if '' in source_columns or '' in target_columns:
        messagebox.showerror("Error", "Por favor, completa todas las columnas de origen y destino.")
        return

    try:
        # Establish connection with the database (adjust parameters according to your configuration)
        conn = psycopg2.connect(
            dbname="Gabriela_Fragancias",
            user="postgres",
            password="salmos23",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # Check if target columns exist in the table
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'Cedulas'")
        valid_columns = [row[0] for row in cur.fetchall()]
        invalid_columns = [col for col in target_columns if col not in valid_columns]

        if invalid_columns:
            messagebox.showerror("Error", f"Las siguientes columnas no existen en la tabla de destino: {', '.join(invalid_columns)}")
            return

        # Read data from DBF file
        for record in dbfread.DBF(dbf_file, encoding='latin-1'):
            # Insert into SQL table
            cur.execute(f"""
                INSERT INTO Cedulas ({', '.join(target_columns)})
                VALUES ({', '.join(['%s'] * len(target_columns))})
            """, [record[src_col] for src_col in source_columns])

        # Commit changes and close connection
        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("Éxito", "La migración se ha completado con éxito.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante la migración:\n{str(e)}")

# Create main window
root = Tk()
root.title("DBF a PostgreSQL")

# DBF file selection
dbf_path_label = Label(root, text="Selecciona un archivo DBF...")
dbf_path_label.pack()
browse_button = Button(root, text="Buscar archivo DBF", command=browse_dbf_file)
browse_button.pack()

# Column mapping
column_frame = Frame(root)
column_frame.pack(pady=10)

column_sources = []
column_targets = []

for i, col_tgt in enumerate(["numero_cedula", "nombre", "apellido", "sexo", "fecha_nacimiento", "lugar_nacimiento", "direccion"]):
    Label(column_frame, text=f"Columna de origen {i+1}").grid(row=i, column=0)
    col_src_combo = ttk.Combobox(column_frame)
    col_src_combo.grid(row=i, column=1)
    column_sources.append(col_src_combo)

    Label(column_frame, text=f"Columna de destino {i+1}").grid(row=i, column=2)
    col_tgt_label = Label(column_frame, text=col_tgt)
    col_tgt_label.grid(row=i, column=3)
    column_targets.append(col_tgt)

# Run migration button
run_button = Button(root, text="Ejecutar migración", command=run_migration)
run_button.pack()

root.mainloop()
