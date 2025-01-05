def create_table(self, cursor):
    """Crear la tabla si no existe."""
    cursor.execute("""
        DROP TABLE IF EXISTS gf.cedulas;
        
        CREATE TABLE gf.cedulas (
            numero_cedula VARCHAR(20) PRIMARY KEY,
            nombre VARCHAR(100),
            apellido VARCHAR(100),
            sexo CHAR(1),
            fecha_nacimiento DATE,
            lugar_nacimiento VARCHAR(100),
            direccion VARCHAR(200),
            id_barrio INTEGER,
            id_distrito INTEGER,
            id_dpto INTEGER,
            zona VARCHAR(50),
            fecha_defuncion DATE,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX idx_cedulas_nombre ON gf.cedulas(nombre);
        CREATE INDEX idx_cedulas_apellido ON gf.cedulas(apellido);
    """)

def process_files(self):
    """Procesar archivos DBF y cargar a PostgreSQL."""
    if not self.files_selected:
        messagebox.showerror("Error", "No se han seleccionado archivos")
        return

    try:
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            total_files = len(self.files_selected)
            self.progress['maximum'] = total_files
            records_processed = 0
            self.processing_cancelled = False

            for i, file_path in enumerate(self.files_selected):
                if self.processing_cancelled:
                    break
                    
                try:
                    # Leer archivo DBF directamente
                    table = dbfread.DBF(file_path)
                    
                    # Obtener mapeo para este archivo
                    file_mapping = self.mappings[file_path]
                    
                    # Procesar registros
                    batch_data = []
                    for record in table:
                        if self.processing_cancelled:
                            break
                            
                        transformed_record = {}
                        
                        # Mapear y transformar cada columna
                        for pg_col, combo in file_mapping.items():
                            dbf_col = combo.get()
                            if not dbf_col:
                                continue

                            value = record.get(dbf_col)

                            # Transformaciones específicas
                            if pg_col == 'fecha_nacimiento':
                                value = self.transform_date(value)
                            elif pg_col in ['nombre', 'apellido', 'lugar_nacimiento']:
                                value = self.clean_text(value)
                            elif pg_col == 'sexo':
                                value = self.transform_sex(value)
                            elif pg_col == 'numero_cedula':
                                # Asegurar que la cédula sea string y tenga el formato correcto
                                try:
                                    if value is not None:
                                        value = str(int(value)).zfill(8)  # Rellenar con ceros a la izquierda
                                except (ValueError, TypeError):
                                    value = None
                                    logging.warning(f"Valor de cédula inválido: {value}")

                            transformed_record[pg_col] = value

                        if transformed_record.get('numero_cedula'):
                            batch_data.append(transformed_record)
                            records_processed += 1

                        # Procesar en lotes de 1000 registros
                        if len(batch_data) >= 1000:
                            self._insert_batch(cursor, batch_data)
                            batch_data = []

                    # Insertar registros restantes
                    if batch_data:
                        self._insert_batch(cursor, batch_data)

                    conn.commit()
                    self.progress['value'] = i + 1
                    self.progress_label['text'] = f"Procesando... {i+1}/{total_files}"
                    self.root.update_idletasks()
                    
                except Exception as e:
                    logging.error(f"Error procesando archivo {file_path}: {str(e)}")
                    messagebox.showerror("Error", 
                                       f"Error procesando archivo {os.path.basename(file_path)}: {str(e)}")

            if not self.processing_cancelled:
                self.progress_label['text'] = f"¡Proceso completado! {records_processed} registros procesados"
                messagebox.showinfo("Éxito", 
                                  f"ETL completado exitosamente\n"
                                  f"Archivos procesados: {total_files}\n"
                                  f"Registros procesados: {records_processed}")

    except Exception as e:
        logging.error(f"Error durante el procesamiento: {str(e)}")
        messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")
