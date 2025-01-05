import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
import os
from psycopg2.extras import execute_batch

class DBFLoader:
    def __init__(self):
        self.tables = []  # List to store selected DBF file paths
        self.setup_logging()
        self.setup_ui()

        # Centralized database configuration
        self.db_config = {
            "host": "localhost",
            "database": "Gabriela_Fragancias",
            "user": "postgres",
            "password": "salmos23",
            "port": 5432,  # Add default port
            "connect_timeout": 3
        }

        self.sexo_mapping = {1: 'F', 2: 'M'}  # Customizable mapping
        self.batch_size = 1000  # Tamaño del lote para inserción en la base de datos

    def setup_logging(self):
        """Configures the logging system"""
        logging.basicConfig(
            filename='dbf_loader.log',
            level=logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_ui(self):
        """Configures the user interface"""
        self.window = tk.Tk()
        self.window.title("Cargador de tablas DBF")
        self.window.geometry("400x300")

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(main_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Cargar datos", command=self.load_data).pack(pady=5, fill=tk.X)

        self.files_listbox = tk.Listbox(main_frame, height=8)
        self.files_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress_bar.pack(pady=5, fill=tk.X)

    def get_db_connection(self) -> tuple:
        """Establishes a connection to the PostgreSQL database"""
        try:
            conn = psycopg2.connect(
                host=self.db_config["host"],
                database=self.db_config["database"],
                user=self.db_config["user"],
                password=self.db_config["password"],
                connect_timeout=self.db_config["connect_timeout"]
            )
            cur = conn.cursor()
            return conn, cur
        except psycopg2.Error as e:
            self.logger.error(f"Error de conexión a la base de datos: {str(e)}")
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            raise

    def safe_str(self, value):
        """Converts any value to a string safely"""
        if value is None:
            return ''
        return str(value).strip()

    def standardize_date(self, date_value):
        """Standardizes different date formats to a datetime.date object"""
        try:
            if date_value is None:
                return None

            if isinstance(date_value, str):
                date_str = date_value.strip()
                if not date_str:
                    return None

                # Try different date formats
                for fmt in ['%Y%m%d', '%d/%m/%Y']:
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except ValueError:
                        continue

            elif isinstance(date_value, (int, float)):
                # Convert number to string and try YYYYMMDD format
                date_str = str(int(date_value))
                if len(date_str) == 8:
                    try:
                        return datetime.strptime(date_str, '%Y%m%d').date()
                    except ValueError:
                        pass

            self.logger.warning(f"Formato de fecha no reconocido: {date_value} ({type(date_value)})")
            return None

        except Exception as e:
            self.logger.warning(f"Error al procesar fecha {date_value}: {str(e)}")
            return None

    def process_record(self, record):
        """Procesa y valida un registro individual"""
        try:
            # Debug logging para ver los campos raw
            self.logger.debug(f"Registro raw: {record}")

            # Procesar campos básicos
            cedula = self.safe_str(record.get('NROCED'))
            nombre = self.safe_str(record.get('NOMBRE'))
            apellido = self.safe_str(record.get('APELLI'))

            # Manejo del campo sexo con validación y mapeo
            sexo_value = record.get('SEXO')
            if sexo_value is not None:
                try:
                    sexo_int = int(sexo_value)
                    sexo = self.sexo_mapping.get(sexo_int, None)
                    if sexo is None:
                        raise ValueError(f"Valor de sexo no válido: {sexo_value}")
                except ValueError:
                    raise ValueError(f"Sexo debe ser un número entero: {sexo_value}")
            else:
                sexo = None

            # Procesar dirección
            direcc = self.safe_str(record.get('DOMICILIO'))

            # Procesar fecha de nacimiento
            fec_nac = self.standardize_date(record.get('FECHANAC'))

            # Log detallado de los campos procesados
            self.logger.debug(f"""
            Campos procesados:
            Cédula: {cedula}
            Nombre: {nombre}
            Apellido: {apellido}
            Sexo: {sexo}
            Fecha Nacimiento: {fec_nac}
            Dirección: {direcc}
            """)

            # Validaciones básicas
            if not cedula or cedula.isspace():
                raise ValueError("Cédula es obligatoria")

            if not cedula.isdigit():
                raise ValueError(f"Cédula debe ser numérica: {cedula}")

            return (cedula, nombre, apellido, sexo, fec_nac, direcc)

        except Exception as e:
            self.logger.warning(f"Error procesando registro {record}: {str(e)}")
            raise

    def load_data(self):
        """Carga los datos de los archivos DBF a PostgreSQL"""
        if not self.tables:
            messagebox.showwarning("Advertencia", "Por favor seleccione archivos DBF primero")
            return

        try:
            conn, cur = self.get_db_connection()
            total_records = 0
            processed_records = 0
            error_records = 0

            # Activar logging detallado temporalmente
            self.logger.setLevel(logging.DEBUG)

            # Primer archivo para verificar estructura
            if self.tables:
                first_table = dbfread.DBF(self.tables[0], lowernames=True)
                self.logger.info(f"Estructura del primer archivo: {first_table.field_names}")

            # Contar registros totales
            for table_path in self.tables:
                table = dbfread.DBF(table_path, lowernames=True)
                total_records += len(list(table))

            self.progress_bar["maximum"] = total_records
        
            # Procesar archivos
            for table_path in self.tables:
                self.logger.info(f"Procesando {table_path}")
                table = dbfread.DBF(table_path, lowernames=True)

                records_to_insert = []

                for record in table:
                    try:
                        processed_record = self.process_record(record)
                        records_to_insert.append(processed_record)
                        processed_records += 1

                        if len(records_to_insert) == self.batch_size:
                            self.insert_records_batch(conn, cur, records_to_insert)
                            records_to_insert = []

                    except Exception as e:
                        error_records += 1
                        self.logger.warning(f"Omitiendo registro inválido: {str(e)}")

                    self.progress_label["text"] = f"Procesando... {processed_records + error_records} de {total_records}"
                    self.progress_bar["value"] = processed_records + error_records
                    self.window.update_idletasks()

            # Insertar registros en batch
            insert_query = """
                INSERT INTO personas (cedula, nombre, apellido, sexo, fec_nac, direcc)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            execute_batch(cur, insert_query, records_to_insert)
            conn.commit()

            # Restaurar nivel de logging original
            self.logger.setLevel(logging.WARNING)

            # Mostrar resumen
            messagebox.showinfo("Carga completa", f"Se procesaron {processed_records} registros.\nSe omitieron {error_records} registros con errores.")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la carga de datos: {str(e)}")
            self.logger.error(f"Error de carga de datos: {str(e)}")

        finally:
            self.progress_label["text"] = ""
            self.progress_bar["value"] = 0
            if conn:
                cur.close()
                conn.close()

    def select_files(self):
        """Abre un diálogo para seleccionar archivos DBF"""
        file_paths = filedialog.askopenfilenames(filetypes=[("DBF Files", "*.dbf")])
        if file_paths:
            self.files_listbox.delete(0, tk.END)
            for file_path in file_paths:
                self.files_listbox.insert(tk.END, os.path.basename(file_path))
            self.tables = file_paths

    def run(self):
        """Inicia la aplicación"""
        self.window.mainloop()

if __name__ == "__main__":
    app = DBFLoader()
    app.run()
