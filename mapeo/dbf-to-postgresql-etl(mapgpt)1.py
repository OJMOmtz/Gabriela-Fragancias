import os
import psycopg2
from dbfread import DBF
from tkinter import Tk, filedialog

def select_dbf_file():
    """Open a file dialog to select a DBF file."""
    Tk().withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a DBF File",
        filetypes=[("DBF Files", "*.dbf")]
    )
    return file_path

def connect_to_postgresql():
    """Establish a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="Gabriela_Fragancias",
            user="postgres",
            password="salmos23",
            port=5432
        )
        return connection
    except Exception as e:
        print("Error connecting to PostgreSQL:", e)
        return None

def insert_data_from_dbf(file_path, connection, table_name):
    """Insert data from the DBF file into the specified PostgreSQL table."""
    try:
        # Open the DBF file
        dbf_table = DBF(file_path, encoding='latin1')  # Adjust encoding if needed
        
        # Get column names from DBF
        dbf_columns = dbf_table.field_names

        # Create the SQL INSERT query template
        placeholders = ', '.join(["%s"] * len(dbf_columns))
        columns = ', '.join(dbf_columns)
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Insert rows
        with connection.cursor() as cursor:
            for record in dbf_table:
                values = [record[col] for col in dbf_columns]
                cursor.execute(query, values)

        # Commit changes
        connection.commit()
        print(f"Data from {os.path.basename(file_path)} successfully inserted into {table_name}.")
    except Exception as e:
        print("Error during data insertion:", e)
        connection.rollback()

def main():
    """Main function to orchestrate the DBF to PostgreSQL process."""
    print("Select the DBF file to import.")
    dbf_file = select_dbf_file()

    if not dbf_file:
        print("No file selected. Exiting.")
        return

    # Connect to PostgreSQL
    connection = connect_to_postgresql()
    if not connection:
        print("Failed to connect to the database. Exiting.")
        return

    # Specify the target PostgreSQL table
    table_name = "your_table_name"  # Update this to your target table

    # Insert data
    insert_data_from_dbf(dbf_file, connection, table_name)

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()
