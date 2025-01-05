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

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.window = tk.Tk()
        self.window.title("Cargador de tablas DBF")
        self.window.geometry("600x400")
        
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(main_frame, text="Seleccionar archivos DBF", command=self.select_files).pack(pady=5, fill=tk.X)
        ttk.Button(main_frame, text="Cargar datos", command=self.load_data).pack(pady=5, fill=tk.X)
        
        # Agregar área de log visual
        self.log_text = tk.Text(main_frame, height=10, width=50)
        self.log_text.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.files_listbox = tk.Listbox(main_frame, height=5)
        self.files_listbox.pack(pady=5, fill=tk.X)
        
        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress_bar.pack(pady=5, fill=tk.X)

    def log_to_ui(self, message: str):
        """Agrega mensaje al área de log visual"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.window.update()

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
            
            # Logging detallado
            self.logger.debug(
                f"Registro procesado:\n"
                f"Cédula: {cedula}\n"
                f"Nombre: {nombre}\n"
                f"Apellido: {apellido}\n"
                f"Sexo: {sexo}\n"
                f"Fecha Nac.: {fecha_nac}\n"
                f"Dirección: {direccion}"
            )
            
            return (cedula, nombre, apellido, sexo, fecha_nac, direccion)
            
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
    def standardize_date(self, date_value: Any) -> Optional[datetime.date]:
        """Estandariza diferentes formatos de fecha"""
        try:
            if date_value is None:
                return None
                
            # Si es una fecha ya formateada, retornarla
            if isinstance(date_value, datetime.date):
                return date_value
                
            # Si es datetime, convertirla a date
            if isinstance(date_value, datetime):
                return date_value.date()
                
            # Si es string, intentar varios formatos
            if isinstance(date_value, str):
                date_str = date_value.strip()
                if not date_str:
                    return None
                    
                formats_to_try = [
                    '%d/%m/%Y',
                    '%Y%m%d',
                    '%Y-%m-%d',
                    '%d-%m-%Y'
                ]
                
                for date_format in formats_to_try:
                    try:
                        return datetime.strptime(date_str, date_format).date()
                    except ValueError:
                        continue
                        
            # Si es un número (puede venir como entero en el DBF)
            if isinstance(date_value, (int, float)):
                # Convertir a string y probar formato YYYYMMDD
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

    def process_record(self, record: Dict) -> tuple:
        """Procesa y valida un registro individual"""
        try:
            # Debug logging para ver los campos raw
            self.logger.debug(f"Registro raw: {record}")
            
            # Procesar campos básicos
            cedula = self.safe_str(record.get('cedula'))
            nombre = self.safe_str(record.get('nombre'))
            apellido = self.safe_str(record.get('apellido'))
            sexo = self.safe_str(record.get('sexo'))
            
            # Procesar dirección - verificar diferentes posibles nombres de campo
            direcc = None
            for field in ['direcc', 'direccion', 'direc', 'dir']:
                if field in record:
                    direcc = self.safe_str(record[field])
                    if direcc:
                        break
                        
            # Procesar fecha de nacimiento - verificar diferentes posibles nombres de campo
            fec_nac = None
            for field in ['fec_nac', 'fecha_nac', 'fechanac', 'fnac']:
                if field in record:
                    fec_nac = self.standardize_date(record[field])
                    if fec_nac:
                        break
            
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
                total_records += len(table)
            
            self.progress_bar['maximum'] = total_records
            
            # Procesar los archivos
            for table_path in self.tables:
                try:
                    table = dbfread.DBF(table_path, lowernames=True)
                    self.logger.info(f"Procesando archivo: {table_path}")
                    self.logger.info(f"Campos disponibles: {table.field_names}")
                    
                    records_to_insert = []
                    
                    for record in table:
                        try:
                            processed_record = self.process_record(record)
                            records_to_insert.append(processed_record)
                            processed_records += 1
                            
                            if processed_records % 100 == 0:
                                self.progress_bar['value'] = processed_records
                                self.progress_label.config(
                                    text=f"Procesando: {processed_records}/{total_records} registros"
                                )
                                self.window.update()
                            
                            if len(records_to_insert) >= 1000:
                                execute_batch(cur, """
                                    INSERT INTO Cedulas 
                                    (numero_cedula, nombre, apellido, sexo, fecha_nacimiento, direccion)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (numero_cedula) DO UPDATE 
                                    SET nombre = EXCLUDED.nombre,
                                        apellido = EXCLUDED.apellido,
                                        sexo = EXCLUDED.sexo,
                                        fecha_nacimiento = COALESCE(EXCLUDED.fecha_nacimiento, Cedulas.fecha_nacimiento),
                                        direccion = COALESCE(EXCLUDED.direccion, Cedulas.direccion)
                                """, records_to_insert, page_size=1000)
                                records_to_insert = []
                                conn.commit()
                            
                        except Exception as e:
                            error_records += 1
                            self.logger.warning(f"Error en registro: {str(e)}")
                            continue
                    
                    if records_to_insert:
                        execute_batch(cur, """
                            INSERT INTO Cedulas 
                            (numero_cedula, nombre, apellido, sexo, fecha_nacimiento, direccion)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON CONFLICT (numero_cedula) DO UPDATE 
                            SET nombre = EXCLUDED.nombre,
                                apellido = EXCLUDED.apellido,
                                sexo = EXCLUDED.sexo,
                                fecha_nacimiento = COALESCE(EXCLUDED.fecha_nacimiento, Cedulas.fecha_nacimiento),
                                direccion = COALESCE(EXCLUDED.direccion, Cedulas.direccion)
                        """, records_to_insert, page_size=1000)
                        conn.commit()
                    
                except Exception as e:
                    self.logger.error(f"Error procesando archivo {table_path}: {str(e)}")
                    messagebox.showerror("Error", f"Error al procesar {os.path.basename(table_path)}")
                    continue
            
            # Restaurar nivel de logging
            self.logger.setLevel(logging.INFO)
            
            summary = f"""
            Proceso completado:
            - Total registros procesados: {processed_records}
            - Registros con error: {error_records}
            - Tasa de éxito: {((processed_records - error_records) / processed_records * 100):.2f}%
            """
            
            self.logger.info(summary)
            messagebox.showinfo("Éxito", summary)
            
        except Exception as e:
            self.logger.error(f"Error general: {str(e)}")
            messagebox.showerror("Error", "Ocurrió un error durante la carga")
            
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
            self.progress_label.config(text="Proceso completado")

    def run(self):
        self.window.mainloop()
        
if __name__ == "__main__":
    app = DBFLoader()
    app.run()
    
    