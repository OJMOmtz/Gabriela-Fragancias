import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import psycopg2
from datetime import datetime
import dbfread
import logging
import csv
import os
from psycopg2.extras import execute_batch
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
import io
import time
from collections import defaultdict

class DBFLoader:
    # ... (código existente sin cambios) ...

    def process_file_worker(self, file_path):
        """Procesa un archivo DBF, CSV o TXT y envía los registros a la cola de procesamiento"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            total_records = 0
            processed_records = []
            
            if file_ext == '.dbf':
                # Procesar archivo DBF
                table = dbfread.DBF(file_path, encoding='latin1')
                total_records = len(table)
                records = table
            elif file_ext in ['.csv', '.txt']:
                # Procesar archivo CSV/TXT
                with open(file_path, 'r', encoding='latin1') as f:
                    # Contar total de líneas
                    total_records = sum(1 for _ in f)
                    f.seek(0)  # Volver al inicio del archivo
                    
                    # Detectar el delimitador
                    dialect = csv.Sniffer().sniff(f.read(1024))
                    f.seek(0)  # Volver al inicio nuevamente
                    
                    reader = csv.DictReader(f, dialect=dialect)
                    records = list(reader)
            else:
                raise ValueError(f"Formato de archivo no soportado: {file_ext}")

            # Actualizar la barra de progreso con el total de registros
            self.window.after(0, lambda: self.update_progress_label(f"Procesando {os.path.basename(file_path)}..."))
            
            # Procesar registros en chunks
            chunk = []
            for i, record in enumerate(records):
                chunk.append(record)
                
                if len(chunk) >= self.batch_size:
                    # Procesar chunk y obtener registros válidos
                    valid_records, chunk_duplicates = self.process_chunk(chunk)
                    
                    # Enviar registros válidos a la cola
                    if valid_records:
                        self.queue.put(valid_records)
                    
                    # Actualizar progreso
                    progress = (i + 1) / total_records * 100
                    self.window.after(0, lambda p=progress: self.update_progress(p))
                    
                    chunk = []
            
            # Procesar el último chunk si existe
            if chunk:
                valid_records, chunk_duplicates = self.process_chunk(chunk)
                if valid_records:
                    self.queue.put(valid_records)
            
            self.logger.info(f"Archivo {os.path.basename(file_path)} procesado exitosamente")
            
        except Exception as e:
            self.logger.error(f"Error procesando archivo {file_path}: {str(e)}")
            raise

    def update_progress_label(self, text):
        """Actualiza el texto de la etiqueta de progreso"""
        self.progress_label.config(text=text)

    def update_progress(self, value):
        """Actualiza la barra de progreso"""
        self.progress_bar['value'] = value

    # ... (resto del código existente sin cambios) ...

if __name__ == "__main__":
    app = DBFLoader()
    app.run()
