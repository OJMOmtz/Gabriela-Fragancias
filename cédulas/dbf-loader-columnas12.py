import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
from psycopg2.extras import execute_batch
import configparser
import time

class CedulasLoader:
    def __init__(self):
        self.tables = []
        self.config = self.load_config()
        self.setup_logging()
        self.setup_ui()
        self.start_time = None
        self.failure_reasons = {}

    def load_config(self):
        """Carga la configuración de conexión desde database.ini"""
        config = configparser.ConfigParser()
        config.read('database.ini')
        return config['postgresql']

    def setup_logging(self):
        """Configura el sistema de logging."""
        logging.basicConfig(
            filename='cedulas_loader.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_ui(self):
        """Configura la interfaz gráfica de usuario."""
        self.window = tk.Tk()
        self.window.title("Cargador de Cédulas")
        self.window.geometry("600x400")

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(main_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Cargar datos", command=self.load_data).pack(pady=5, fill=tk.X)

        self.log_text = tk.Text(main_frame, height=10, width=50)
        self.log_text.pack(pady=5, fill=tk.BOTH, expand=True)

        self.files_listbox = tk.Listbox(main_frame, height=5)
        self.files_listbox.pack(pady=5, fill=tk.X)

        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress_bar.pack(pady=5, fill=tk.X)

    def log_to_ui(self, message: str):
        """Muestra mensajes en la interfaz gráfica."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.window.update()

    def get_db_connection(self):
        """Establece la conexión con la base de datos PostgreSQL."""
        try:
            conn = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['dbname'],
                user=self.config['user'],
                password=self.config['password']
            )
            cur = conn.cursor()
            cur.execute("SET search_path TO gf;")
            self.logger.info("Conexión establecida con la base de datos")
            return conn, cur
        except psycopg2.Error as e:
            self.logger.error(f"Error conectándose a la base de datos: {e}")
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            raise

    def process_record(self, record):
        """Procesa y valida un registro antes de insertarlo en la base de datos."""
        try:
            def safe_str(value):
                return str(value).strip() if value is not None else ''

            cedula = safe_str(record.get('cedula', ''))
            if not cedula.isdigit():
                reason = "Cédula inválida"
                self.failure_reasons[reason] = self.failure_reasons.get(reason, 0) + 1
                self.logger.warning(f"{reason}: {record}")
                return None

            nombre = safe_str(record.get('nombre', ''))
            apellido = safe_str(record.get('apellido', ''))
            fecha_nac = self.standardize_date(record.get('fec_nac'))
            if fecha_nac is None:
                reason = "Fecha de nacimiento inválida"
                self.failure_reasons[reason] = self.failure_reasons.get(reason, 0) + 1
                self.logger.warning(f"{reason}: {record} (usando NULL)")

            sexo = safe_str(record.get('sexo', '')).upper()[:1]
            direccion = self.clean_address(record.get('direcc', ''))

            id_distrito = safe_str(record.get('id_distrito', ''))
            id_dpto = safe_str(record.get('id_dpto', ''))
            zona = safe_str(record.get('zona', ''))
            lugar_nacimiento = safe_str(record.get('lug_nac', ''))
            fecha_defuncion = self.standardize_date(record.get('fecha_defuncion'))

            return (
                cedula, nombre, apellido, fecha_nac, sexo, direccion,
                id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
            )
        except Exception as e:
            reason = f"Error procesando registro: {e}"
            self.failure_reasons[reason] = self.failure_reasons.get(reason, 0) + 1
            self.logger.error(f"{reason}: {record}")
            return None

    def standardize_date(self, date_value):
        """Convierte diferentes formatos de fecha a un estándar."""
        try:
            if isinstance(date_value, int):
                # Asume formato AAAAMMDD para fechas numéricas
                date_value = str(date_value)
                if len(date_value) == 8:
                    return datetime.strptime(date_value, '%Y%m%d').date()
            if isinstance(date_value, str):
                return datetime.strptime(date_value, '%Y-%m-%d').date()
            return date_value
        except (ValueError, TypeError):
            self.logger.warning(f"Fecha inválida: {date_value}")
            return None

    def clean_address(self, address):
        """Limpia y valida una dirección."""
        if not address or not isinstance(address, str):
            return None
        address = ' '.join(address.split())
        return address if len(address) > 2 else None

    def load_data(self):
        """Carga los datos desde los archivos seleccionados a la base de datos."""
        if not self.tables:
            messagebox.showwarning("Advertencia", "Por favor seleccione archivos primero")
            return

        conn, cur = self.get_db_connection()
        total_records = 0
        processed_records = 0
        failed_records = []
        self.start_time = time.time()

        try:
            for table_path in self.tables:
                table = dbfread.DBF(table_path, lowernames=True)
                total_records = len(table)
                records_to_insert = []

                for record in table:
                    processed_record = self.process_record(record)
                    if processed_record:
                        records_to_insert.append(processed_record)
                    else:
                        failed_records.append(record)

                    if len(records_to_insert) >= 5000:  # Aumentamos el tamaño del lote
                        self.insert_records(cur, records_to_insert)
                        records_to_insert = []

                    processed_records += 1
                    self.update_progress(processed_records, total_records)

                if records_to_insert:
                    self.insert_records(cur, records_to_insert)

            conn.commit()
            self.generate_failure_report(failed_records)
            messagebox.showinfo("Éxito", f"Datos cargados exitosamente. Total registros: {processed_records}, Fallidos: {len(failed_records)}")
        except Exception as e:
            self.logger.error(f"Error general: {e}")
            conn.rollback()
            messagebox.showerror("Error", "Ocurrió un error durante la carga")
        finally:
            cur.close()
            conn.close()

    def insert_records(self, cur, records):
        """Inserta registros en la tabla cedulas."""
        try:
            execute_batch(cur, """
                INSERT INTO gf.cedulas (
                    numero_cedula, nombre, apellido, fecha_nacimiento, sexo, direccion,
                    id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (numero_cedula) DO UPDATE SET
                    nombre = EXCLUDED.nombre,
                    apellido = EXCLUDED.apellido,
                    fecha_nacimiento = EXCLUDED.fecha_nacimiento,
                    sexo = EXCLUDED.sexo,
                    direccion = EXCLUDED.direccion,
                    id_distrito = EXCLUDED.id_distrito,
                    id_dpto = EXCLUDED.id_dpto,
                    zona = EXCLUDED.zona,
                    lugar_nacimiento = EXCLUDED.lugar_nacimiento,
                    fecha_defuncion = EXCLUDED.fecha_defuncion
            """, records, page_size=5000)
        except psycopg2.Error as e:
            self.logger.error(f"Error insertando registros: {e}")
            cur.execute("ROLLBACK;")  # Asegura un rollback en caso de fallo
            self.logger.info("Transacción revertida, reintentando con lotes más pequeños")
            self.retry_insertion(cur, records)

    def retry_insertion(self, cur, records):
        """Divide registros en lotes más pequeños en caso de error."""
        batch_size = 100  # Tamaño más pequeño para intentar resolver errores
        for i in range(0, len(records), batch_size):
            try:
                batch = records[i:i + batch_size]
                execute_batch(cur, """
                    INSERT INTO gf.cedulas (
                        numero_cedula, nombre, apellido, fecha_nacimiento, sexo, direccion,
                        id_distrito, id_dpto, zona, lugar_nacimiento, fecha_defuncion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (numero_cedula) DO UPDATE SET
                        nombre = EXCLUDED.nombre,
                        apellido = EXCLUDED.apellido,
                        fecha_nacimiento = EXCLUDED.fecha_nacimiento,
                        sexo = EXCLUDED.sexo,
                        direccion = EXCLUDED.direccion,
                        id_distrito = EXCLUDED.id_distrito,
                        id_dpto = EXCLUDED.id_dpto,
                        zona = EXCLUDED.zona,
                        lugar_nacimiento = EXCLUDED.lugar_nacimiento,
                        fecha_defuncion = EXCLUDED.fecha_defuncion
                """, batch, page_size=batch_size)
                cur.connection.commit()
            except psycopg2.Error as e:
                self.logger.error(f"Error en lote reducido: {e}")
                cur.execute("ROLLBACK;")

    def update_progress(self, processed_records, total_records):
        """Actualiza la barra de progreso en la interfaz gráfica."""
        elapsed_time = time.time() - self.start_time
        records_per_second = processed_records / elapsed_time if elapsed_time > 0 else 0
        remaining_records = total_records - processed_records
        estimated_remaining_time = remaining_records / records_per_second if records_per_second > 0 else 0

        hours, rem = divmod(estimated_remaining_time, 3600)
        minutes, seconds = divmod(rem, 60)

        self.progress_bar['value'] = (processed_records / total_records) * 100
        progress_text = (
            f"Progreso: {processed_records}/{total_records} | Velocidad: {records_per_second:.2f} reg/s | "
            f"Tiempo restante: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        )
        self.progress_label['text'] = progress_text
        self.logger.info(progress_text)
        self.window.update()

    def generate_failure_report(self, failed_records):
        """Genera un informe detallado de los registros fallidos y sus razones."""
        with open('failed_records.log', 'w', encoding='utf-8') as f:
            for record in failed_records:
                f.write(f"{record}\n")

        with open('failure_reasons.log', 'w', encoding='utf-8') as f:
            for reason, count in self.failure_reasons.items():
                f.write(f"{reason}: {count}\n")

    def select_files(self):
        """Selecciona archivos DBF para procesar."""
        file_paths = filedialog.askopenfilenames(filetypes=[("Archivos DBF", "*.dbf")])
        self.tables = list(file_paths)
        self.files_listbox.delete(0, tk.END)
        for file_path in file_paths:
            self.files_listbox.insert(tk.END, file_path)

    def run(self):
        """Ejecuta la aplicación gráfica."""
        self.window.mainloop()

if __name__ == "__main__":
    app = CedulasLoader()
    app.run()
