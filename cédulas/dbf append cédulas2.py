import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
from typing import Optional, Any, Dict, Union
import os
from psycopg2.extras import execute_batch

class DBFLoader:
    def __init__(self):
        self.tables = []
        self.setup_logging()
        self.setup_ui()
        
    def setup_logging(self):
        """Configura el sistema de logging con más detalle para debug"""
        logging.basicConfig(
            filename='dbf_loader.log',
            level=logging.DEBUG,  # Cambiado a DEBUG para más detalle
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)


    def standardize_date(self, date_value: Any) -> Optional[datetime.date]:
        """Manejo mejorado de fechas con múltiples formatos"""
        if date_value is None or (isinstance(date_value, str) and not date_value.strip()):
            return None
            
        try:
            # Si ya es un objeto date
            if isinstance(date_value, datetime.date):
                return date_value
                
            # Si es datetime
            if isinstance(date_value, datetime):
                return date_value.date()
                
            # Si es string
            if isinstance(date_value, str):
                date_str = date_value.strip()
                
                # Intentar varios formatos comunes
                formats_to_try = [
                    '%d/%m/%Y',
                    '%Y%m%d',
                    '%Y-%m-%d',
                    '%d-%m-%Y',
                    '%d.%m.%Y',
                    '%m/%d/%Y'
                ]
                
                for date_format in formats_to_try:
                    try:
                        return datetime.strptime(date_str, date_format).date()
                    except ValueError:
                        continue
                        
            # Si es número (común en DBF)
            if isinstance(date_value, (int, float)):
                date_str = str(int(date_value))
                if len(date_str) == 8:  # Formato YYYYMMDD
                    try:
                        return datetime.strptime(date_str, '%Y%m%d').date()
                    except ValueError:
                        pass
                        
            self.logger.warning(f"Formato de fecha no reconocido: {date_value} ({type(date_value)})")
            self.log_to_ui(f"⚠️ Fecha no reconocida: {date_value}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error procesando fecha {date_value}: {str(e)}")
            self.log_to_ui(f"❌ Error en fecha: {date_value}")
            return None

    def clean_address(self, address: Optional[str]) -> Optional[str]:
        """Limpieza y normalización de direcciones"""
        if address is None:
            return None
            
        if not isinstance(address, str):
            address = str(address)
            
        # Limpieza básica
        address = address.strip()
        
        # Eliminar caracteres no deseados
        address = ''.join(char for char in address if char.isprintable())
        
        # Normalizar espacios múltiples
        address = ' '.join(address.split())
        
        # Validar longitud mínima
        if len(address) < 2:
            return None
            
        return address

def process_record(self, record: Dict) -> Optional[tuple]:
    """Procesamiento mejorado de registros con logging detallado"""
    try:
        # Debug del registro completo
        self.logger.debug(f"Procesando registro: {record}")
        
        # Obtener y validar cédula
        cedula = self.safe_str(record.get('cedula', record.get('ci', record.get('nro_doc', ''))))
        if not cedula or not cedula.isdigit():
            self.logger.warning(f"Cédula inválida: {cedula}")
            self.log_to_ui(f"⚠️ Cédula inválida: {cedula}")
            return None
        
        # Procesar nombre y apellido
        nombre = self.safe_str(record.get('nombre', record.get('nombres', '')))
        apellido = self.safe_str(record.get('apellido', record.get('apellidos', '')))
        
        # Procesar sexo
        sexo = self.safe_str(record.get('sexo', record.get('genero', '')))
        if sexo:
            sexo = sexo.upper()[:1]  # Tomar solo la primera letra en mayúscula
        
        # Procesar fecha de nacimiento
        fecha_nac = None
        for field in ['fec_nac', 'fecha_nac', 'fechanac', 'fnac', 'nacimiento']:
            if field in record:
                fecha_nac = self.standardize_date(record[field])
                if fecha_nac:
                    break
        
        # Procesar dirección
        direccion = None
        for field in ['direcc', 'direccion', 'direc', 'dir', 'domicilio']:
            if field in record:
                direccion = self.clean_address(record[field])
                if direccion:
                    break
        
        # Procesar lugar de nacimiento
        lugar_nac = self.safe_str(record.get('lugar_nac', record.get('lugnac', '')))
        
        # Procesar departamento
        id_dpto = self.safe_str(record.get('id_dpto', record.get('depart', '')))
        
        # Procesar distrito
        id_distrito = self.safe_str(record.get('id_distrito', record.get('distrito', '')))
        
        # Procesar fecha de defunción
        fecha_defunc = None
        for field in ['fec_defunc', 'fecha_defunc', 'fechadefunc']:
            if field in record:
                fecha_defunc = self.standardize_date(record[field])
                if fecha_defunc:
                    break
        
        # Logging detallado
        self.logger.debug(
            f"Registro procesado:\n"
            f"Cédula: {cedula}\n"
            f"Nombre: {nombre}\n"
            f"Apellido: {apellido}\n"
            f"Sexo: {sexo}\n"
            f"Fecha Nac.: {fecha_nac}\n"
            f"Dirección: {direccion}\n"
            f"Lugar Nac.: {lugar_nac}\n"
            f"Dpto: {id_dpto}\n"
            f"Distrito: {id_distrito}\n"
            f"Fecha Defunc.: {fecha_defunc}"
        )
        
        return (cedula, nombre, apellido, sexo, fecha_nac, direccion, lugar_nac, id_dpto, id_distrito, fecha_defunc)
        
    except Exception as e:
        self.logger.error(f"Error procesando registro: {str(e)}")
        self.log_to_ui(f"❌ Error en registro: {str(e)}")
        return None

    def safe_str(self, value: Any) -> str:
        """Conversión segura a string con limpieza mejorada"""
        if value is None:
            return ''
        
        # Convertir a string y limpiar
        value = str(value).strip()
        
        # Eliminar caracteres no imprimibles
        value = ''.join(char for char in value if char.isprintable())
        
        # Normalizar espacios
        value = ' '.join(value.split())
        
        return value

    # ... [resto del código igual, incluyendo select_files, get_db_connection, load_data y run]
    def create_widgets(self):
        # Frame principal con scrollbar
        main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame para archivos
        files_frame = ttk.LabelFrame(scrollable_frame, text="Archivos DBF", padding="5")
        files_frame.pack(fill="x", padx=5, pady=5)

        # Botón selección de archivos
        ttk.Button(files_frame, text="Seleccionar archivos DBF", 
                  command=self.select_files).pack(pady=5)

        # Lista de archivos
        self.files_listbox = tk.Listbox(files_frame, width=100, height=5)
        self.files_listbox.pack(pady=5)

        # Frame para mapeo
        self.mapping_frame = ttk.LabelFrame(scrollable_frame, text="Mapeo de columnas", padding="5")
        self.mapping_frame.pack(fill="x", padx=5, pady=5)

        # Barra de progreso
        progress_frame = ttk.Frame(scrollable_frame)
        progress_frame.pack(fill="x", padx=5, pady=5)

        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(pady=5)

        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack(pady=5)

        self.total_label = ttk.Label(progress_frame, text="Total registros procesados: 0")
        self.total_label.pack(pady=5)

        # Botón procesar
        ttk.Button(scrollable_frame, text="Procesar", 
                  command=self.process_files).pack(pady=10)

        # Configurar el layout del scroll
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_dbf_columns(self, file_path: str) -> List[str]:
        """Obtener las columnas de un archivo DBF."""
        try:
            table = dbf.Table(file_path)
            table.open()
            columns = table.field_names
            table.close()
            return columns
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo {os.path.basename(file_path)}: {str(e)}")
            return []

    def select_files(self):
        """Seleccionar archivos DBF y mostrar opciones de mapeo."""
        files = filedialog.askopenfilenames(filetypes=[("DBF files", "*.dbf")])
        if not files:
            return

        self.files_selected = list(files)
        self.files_listbox.delete(0, tk.END)
        
        # Limpiar frame de mapeo
        for widget in self.mapping_frame.winfo_children():
            widget.destroy()

        # Mostrar archivos seleccionados y crear mapeo para cada uno
        for file_path in self.files_selected:
            file_name = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, file_path)
            
            # Crear frame para el archivo
            file_frame = ttk.LabelFrame(self.mapping_frame, text=file_name, padding="5")
            file_frame.pack(fill="x", padx=5, pady=5)

            # Obtener columnas del archivo DBF
            dbf_columns = self.get_dbf_columns(file_path)
            
            # Crear mapeo para cada columna PostgreSQL
            self.mappings[file_path] = {}
            
            # Grid para organizar los combobox
            for i, pg_col in enumerate(self.pg_columns):
                row = i // 3
                col = i % 3
                
                # Frame para cada mapeo
                mapping_pair = ttk.Frame(file_frame)
                mapping_pair.grid(row=row, column=col, padx=5, pady=2)
                
                ttk.Label(mapping_pair, text=f"{pg_col}:").pack(side="left")
                combo = ttk.Combobox(mapping_pair, values=[''] + dbf_columns, width=20)
                combo.pack(side="left", padx=2)
                
                # Autoseleccionar si hay coincidencia exacta o similar
                for dbf_col in dbf_columns:
                    if dbf_col.lower() in pg_col.lower() or pg_col.lower() in dbf_col.lower():
                        combo.set(dbf_col)
                        break
                
                self.mappings[file_path][pg_col] = combo

def transform_date(self, date_value):
    """Transformar diferentes formatos de fecha a fecha PostgreSQL."""
    if pd.isna(date_value):
        return None
            
    try:
        if isinstance(date_value, (int, float)):
            # Convertir fecha numérica (YYYYMMDD)
            date_str = str(int(date_value))
            if len(date_str) == 8:
                return datetime.strptime(date_str, '%Y%m%d').date()
        elif isinstance(date_value, str):
            # Intentar varios formatos comunes
            for fmt in ('%Y%m%d', '%d/%m/%Y', '%Y-%m-%d'):
                try:
                    return datetime.strptime(date_value, fmt).date()
                except ValueError:
                    continue
        elif isinstance(date_value, datetime):
            return date_value.date()
                
    except Exception as e:
        print(f"Error transformando fecha {date_value}: {str(e)}")
    return None

    def clean_text(self, text):
        """Limpiar y normalizar texto."""
        if pd.isna(text):
            return None
        text = str(text).strip()
        text = re.sub(r'\s+', ' ', text)
        text = text.upper()  # Normalizar a mayúsculas
        return text if text else None

    def transform_sex(self, sex_value):
        """Normalizar valor de sexo a M/F."""
        if pd.isna(sex_value):
            return None
        sex_value = str(sex_value).upper().strip()
        if sex_value in ['M', '1', 'MASCULINO']:
            return 'M'
        elif sex_value in ['F', '2', 'FEMENINO']:
            return 'F'
        return None

    def process_files(self):
        """Procesar los archivos DBF seleccionados y cargar a PostgreSQL."""
        if not self.files_selected:
            messagebox.showerror("Error", "No se han seleccionado archivos")
            return

        try:
            # Configuración de conexión PostgreSQL
            conn = psycopg2.connect(
                dbname="Gabriela_Fragancias",
                user="postgres",
                password="salmos23",
                host="localhost"
            )
            cursor = conn.cursor()

            total_files = len(self.files_selected)
            self.progress['maximum'] = total_files
            records_processed = 0

            for i, file_path in enumerate(self.files_selected):
                file_name = os.path.basename(file_path)
                self.progress_label['text'] = f"Procesando {file_name}..."

                # Leer archivo DBF
                table = dbf.Table(file_path)
                table.open()
                
                # Convertir a DataFrame para proceso más eficiente
                df = pd.DataFrame(list(table))
                table.close()

                # Obtener mapeo para este archivo
                file_mapping = self.mappings[file_path]

                # Aplicar transformaciones
                transformed_data = []
                for _, row in df.iterrows():
                    record = {}

                    # Mapear y transformar cada columna
                    for pg_col, combo in file_mapping.items():
                        dbf_col = combo.get()
                        if not dbf_col:
                            continue

                        value = row.get(dbf_col)

                        # Aplicar transformaciones específicas
                        if pg_col == 'fecha_nacimiento':
                            value = self.transform_date(value)
                        elif pg_col in ['nombre', 'apellido']:
                            value = self.clean_text(value)
                        elif pg_col == 'sexo':
                            value = self.transform_sex(value)
                        elif pg_col == 'numero_cedula':
                            value = str(value).strip() if value else None

                        record[pg_col] = value

                    if record.get('numero_cedula'):  # Solo insertar si hay número de cédula
                        transformed_data.append(record)
                        records_processed += 1

                # Insertar datos transformados
                if transformed_data:
                    columns = transformed_data[0].keys()
                    values_template = ','.join(['%s'] * len(columns))
                    insert_query = f"""
                        INSERT INTO Cedulas ({','.join(columns)})
                        VALUES ({values_template})
                        ON CONFLICT (numero_cedula) 
                        DO UPDATE SET
                            {','.join(f"{col} = EXCLUDED.{col}" for col in columns if col != 'numero_cedula')}
                    """

                    cursor.executemany(insert_query, 
                                     [tuple(record.values()) for record in transformed_data])

                conn.commit()
                self.progress['value'] = i + 1
                self.root.update_idletasks()

            cursor.close()
            conn.close()

            self.progress_label['text'] = f"¡Proceso completado! {records_processed} registros procesados"
            self.total_label['text'] = f"Total registros procesados: {self.total_records}"
            messagebox.showinfo("Éxito", 
                              f"ETL completado exitosamente\nArchivos procesados: {total_files}\n"
                              f"Registros procesados: {records_processed}")

        except Exception as e:
            messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    app = DBFLoader()
    app.run()
