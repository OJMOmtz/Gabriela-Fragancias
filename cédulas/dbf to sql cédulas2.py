import subprocess
import psycopg2
from tkinter import *
from tkinter import messagebox

def table_exists(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')")
    return cur.fetchone()[0]

def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE ruc (
        ruc_id SERIAL PRIMARY KEY, -- This automatically creates a unique constraint
        numero_ruc VARCHAR(20) UNIQUE NOT NULL,
        razon_social VARCHAR(255),
        digito_verificador VARCHAR(255) NOT NULL,
        ruc VARCHAR(20) UNIQUE,
        estado VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def run_copy_table():
    source_db = "Brisa_Assistance"
    source_table = "empresas_ruc"
    target_db = "Gabriela_Fragancias"
    target_table = "ruc"

    try:
        # Connect to target database
        conn = psycopg2.connect(
            dbname=target_db,
            user="postgres",
            password="salmos23",
            host="localhost",
            port="5432"
        )

        # Check if target table exists, create it if not
        if not table_exists(conn, target_table):
            create_table(conn)

        conn.close()

        # Export table from source database
        subprocess.run(f"pg_dump -U postgres -t {source_table} {source_db} > temp_table.sql", shell=True, env={"PGPASSWORD": "salmos23"})

        # Import table into target database
        subprocess.run(f"psql -U postgres -d {target_db} -f temp_table.sql", shell=True, env={"PGPASSWORD": "salmos23"})

        messagebox.showinfo("Éxito", "La tabla se ha copiado con éxito.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error durante la copia de la tabla:\n{str(e)}")

# Create main window
root = Tk()
root.title("Copiar tabla PostgreSQL")

# Run copy table button
run_button = Button(root, text="Copiar tabla", command=run_copy_table)
run_button.pack()

root.mainloop()
