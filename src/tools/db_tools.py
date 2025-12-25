import sqlite3
import pandas as pd
from pathlib import Path

# Definimos la ruta absoluta para evitar errores de "file not found"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "institutional_radar.db"

def get_db_schema():
    """Extrae el esquema (CREATE TABLE) de la base de datos para contexto del LLM."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return "\n".join([t[0] for t in tables if t[0] is not None])
    except Exception as e:
        return f"Error leyendo esquema: {e}"

def execute_sql_query(query: str):
    """
    Ejecuta una consulta SQL SELECT en la base de datos de riesgo.
    Input: query (str) - La consulta SQL.
    Output: JSON string con los resultados.
    """
    # Limpieza básica de seguridad
    if not query.strip().upper().startswith("SELECT"):
        return "Error: Por seguridad, BELFORT solo permite consultas de lectura (SELECT)."

    try:
        conn = sqlite3.connect(DB_PATH)
        # Usamos pandas para facilitar la conversión a dict/json
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return "La consulta se ejecutó correctamente pero no devolvió resultados."
            
        return df.to_json(orient="records")
    except Exception as e:
        return f"Error ejecutando SQL: {str(e)}"