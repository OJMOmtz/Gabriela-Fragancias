import pandas as pd
import psycopg2
from datetime import datetime
import os
from typing import Dict, Any, List
import logging
import chardet

# Configurar logging más detallado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_cedulas.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class CedulasETL:
    def __init__(self):
        self.db_params = {
            "dbname": "Gabriela_Fragancias",
            "user": "postgres",
            "password": "salmos23",
            "host": "localhost"
        }
        
        # Mapeo específico de columnas para cada archivo
        self.column_patterns = {
            'CÉDULAS-2024-1_ISO-8859-1.csv': {
                'numero_cedula': 0,
                'nombre': 1,
                'apellido': 2,
                'fecha_nacimiento': 4,
                'direccion': 5
            },
            'pad_col_2017_1_w1252.csv': {
                'numero_cedula': 0,
                'nombre': 1,
                'apellido': 2,
                'fecha_nacimiento': 3,
                'sexo': 4,
                'direccion': 5,
                'id_distrito': 6,
                'id_dpto': 7,
                
            },
            'regciv_2021_ISO-8859-1.csv': {
                'numero_cedula': 0,
                'nombre': 1,
                'apellido': 2,
                'fecha_nacimiento': 3,
                'sexo': 4
            }
        }

    def detect_encoding(self, filepath: str) -> str:
        """Detectar la codificación del archivo."""
        with open(filepath, 'rb') as file:
            raw = file.read()
            result = chardet.detect(raw)
            return result['encoding']

    def connect_db(self):
        """Establecer conexión con la base de datos."""
        try:
            conn = psycopg2.connect(**self.db_params)
            return conn
        except Exception as e:
            logging.error(f"Error conectando a la base de datos: {e}")
            raise

    def clean_text(self, text: Any) -> str:
        """Limpiar y normalizar texto."""
        if pd.isna(text) or text is None:
            return None
        text = str(text).strip().upper()
        return text if text else None

    def parse_date(self, date_val: Any) -> str:
        """Convertir diferentes formatos de fecha a ISO."""
        if pd.isna(date_val) or date_val is None:
            return None
            
        try:
            if isinstance(date_val, str):
                # Manejar formatos comunes
                date_val = date_val.replace('/', '-')
                for fmt in ['%d-%m-%Y', '%Y-%m-%d', '%Y%m%d']:
                    try:
                        return datetime.strptime(date_val, fmt).strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            elif isinstance(date_val, (int, float)):
                # Convertir fecha numérica YYYYMMDD
                date_str = str(int(date_val))
                if len(date_str) == 8:
                    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
                
        except Exception as e:
            logging.warning(f"Error parseando fecha {date_val}: {e}")
        return None

    def normalize_gender(self, gender: Any) -> str:
        """Normalizar género a M/F."""
        if pd.isna(gender) or gender is None:
            return None
        gender = str(gender).upper().strip()
        return 'M' if gender in ['M', '2', 'MASCULINO'] else 'F' if gender in ['F', '1', 'FEMENINO'] else None

    def process_file(self, filepath: str) -> pd.DataFrame:
        """Procesar un archivo CSV."""
        try:
            filename = os.path.basename(filepath)
            logging.info(f"Procesando archivo: {filename}")
            
            # Detectar codificación
            encoding = self.detect_encoding(filepath)
            logging.info(f"Codificación detectada: {encoding}")

            # Leer primeras líneas para logging
            with open(filepath, 'r', encoding=encoding) as f:
                header = f.readline()
                logging.debug(f"Primera línea del archivo: {header}")

            # Determinar el separador
            separator = '\t' if '\t' in header else ','
            logging.info(f"Separador detectado: {separator}")

            # Leer el archivo
            try:
                df = pd.read_csv(filepath, encoding=encoding, sep=separator, dtype=str)
            except Exception as e:
                logging.error(f"Error leyendo archivo {filepath}: {str(e)}")
                return pd.DataFrame()
            
            # Crear DataFrame limpio
            clean_data = pd.DataFrame()

            # Obtener mapeo específico para este archivo
            column_map = self.column_patterns.get(filename, {})
            
            if column_map:
                logging.info(f"Usando mapeo específico para {filename}")
                for target_col, source_col in column_map.items():
                    if isinstance(source_col, int):
                        value = df.iloc[:, source_col]
                    else:
                        value = df[source_col]
                    
                    if target_col == 'fecha_nacimiento':
                        clean_data[target_col] = value.apply(self.parse_date)
                    elif target_col == 'sexo':
                        clean_data[target_col] = value.apply(self.normalize_gender)
                    else:
                        clean_data[target_col] = value.apply(self.clean_text)
            else:
                logging.info("Usando detección automática de columnas")
                # Intenta encontrar columnas por nombres comunes
                for col in df.columns:
                    col_lower = str(col).lower()
                    if 'cedul' in col_lower:
                        clean_data['numero_cedula'] = df[col].apply(self.clean_text)
                    elif 'nombre' in col_lower and 'apellido' not in col_lower:
                        clean_data['nombre'] = df[col].apply(self.clean_text)
                    elif 'apellido' in col_lower:
                        clean_data['apellido'] = df[col].apply(self.clean_text)
                    elif any(x in col_lower for x in ['sex', 'gen']):
                        clean_data['sexo'] = df[col].apply(self.normalize_gender)
                    elif any(x in col_lower for x in ['nac', 'fec']):
                        clean_data['fecha_nacimiento'] = df[col].apply(self.parse_date)
                    elif 'dir' in col_lower:
                        clean_data['direccion'] = df[col].apply(self.clean_text)

            # Validar datos requeridos
            if 'numero_cedula' not in clean_data.columns:
                logging.error(f"No se encontró columna de número de cédula en {filename}")
                return pd.DataFrame()

            # Filtrar registros válidos
            clean_data = clean_data[clean_data['numero_cedula'].notna()]
            
            logging.info(f"Registros válidos encontrados en {filename}: {len(clean_data)}")
            return clean_data

        except Exception as e:
            logging.error(f"Error procesando archivo {filepath}: {str(e)}")
            return pd.DataFrame()
        
        # Filtrar y corregir líneas con un número incorrecto de campos
        expected_fields = 7  # Ajustar según el número de campos esperado
        bad_lines = []
        
        for i, row in df.iterrows():
            if len(row) != expected_fields:
                bad_lines.append(i)
                logging.warning(f"Línea {i+2} en {filename} tiene {len(row)} campos, se esperaban {expected_fields}")
        
        # Eliminar líneas problemáticas
        df.drop(bad_lines, inplace=True)
        
    def bulk_insert(self, df: pd.DataFrame, table: str) -> int:
        """Insertar datos usando COPY."""
        if df.empty:
            return 0
            
        conn = self.connect_db()
        try:
            # Crear archivo temporal
            temp_file = 'temp_cedulas.csv'
            df.to_csv(temp_file, index=False, sep='\t', na_rep='\\N')
            
            cursor = conn.cursor()
            
            # Logging de la estructura de datos a insertar
            logging.debug(f"Columnas a insertar: {','.join(df.columns)}")
            logging.debug(f"Primera fila: {df.iloc[0].to_dict()}")
            
            with open(temp_file, 'r') as f:
                cursor.copy_expert(f"""
                    COPY {table} ({','.join(df.columns)})
                    FROM STDIN
                    WITH (FORMAT CSV, DELIMITER E'\t', NULL '\\N', HEADER TRUE)
                """, f)
            
            inserted = cursor.rowcount
            conn.commit()
            logging.info(f"Registros insertados: {inserted}")
            return inserted
            
        except Exception as e:
            conn.rollback()
            logging.error(f"Error en inserción: {str(e)}")
            return 0
        finally:
            conn.close()
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def run(self, directory: str) -> Dict[str, int]:
        """Ejecutar ETL para todos los archivos en el directorio."""
        results = {}
        total_processed = 0
        
        # Procesar todos los archivos CSV
        for filename in os.listdir(directory):
            if filename.lower().endswith('.csv'):
                filepath = os.path.join(directory, filename)
                try:
                    logging.info(f"\n{'='*50}\nProcesando {filename}")
                    
                    # Procesar archivo
                    df = self.process_file(filepath)
                    
                    # Insertar datos
                    inserted = self.bulk_insert(df, 'gf.cedulas')
                    
                    results[filename] = inserted
                    total_processed += inserted
                    
                    logging.info(f"Procesado {filename}: {inserted} registros insertados")
                    
                except Exception as e:
                    logging.error(f"Error procesando {filename}: {str(e)}")
                    results[filename] = 0
                    
        return results

if __name__ == "__main__":
    # Ejecutar ETL
    etl = CedulasETL()
    directory = "D:/PADRONES/csvs/Cédulas"  # Ajustar al directorio correcto
    
    try:
        results = etl.run(directory)
        
        # Mostrar resultados
        print("\nResultados del ETL:")
        print("-" * 50)
        for filename, count in results.items():
            print(f"{filename}: {count:,} registros")
        print("-" * 50)
        print(f"Total registros procesados: {sum(results.values()):,}")
        
    except Exception as e:
        print(f"Error ejecutando ETL: {e}")
        logging.error(f"Error en ejecución principal: {e}")