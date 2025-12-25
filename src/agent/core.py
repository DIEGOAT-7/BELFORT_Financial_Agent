import os
import google.generativeai as genai
from dotenv import load_dotenv

# Importamos nuestras herramientas modulares
from src.tools.db_tools import execute_sql_query, get_db_schema
from src.tools.market_tools import get_market_data
from src.tools.report_tools import save_risk_report



# Cargar variables de entorno (.env)
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("No se encontró GOOGLE_API_KEY en el archivo .env")

genai.configure(api_key=API_KEY)

def initialize_agent():
    """Configura y devuelve la sesión de chat de BELFORT."""
    
    # 1. Preparar Herramientas
    tools_list = [execute_sql_query, get_market_data, save_risk_report]
    
    # 2. Obtener Esquema actualizado
    db_schema = get_db_schema()
    
    # 3. Prompt del Sistema (La personalidad de Belfort)
    system_instruction = f"""
    Eres BELFORT, un Agente de Inteligencia Financiera de élite.
    
    TUS CAPACIDADES:
    1. Consultar la cartera interna del usuario (DB SQL). Esquema: {db_schema}
    2. Consultar el mercado real en vivo (Yahoo Finance).
    
    TU MODUS OPERANDI:
    - Eres agresivo con los datos pero conservador con el riesgo.
    - Piensa paso a paso: ¿Necesito datos internos? ¿Datos externos? ¿Ambos?
    - Si encuentras un ticker en la DB (ej: 'AAPL'), verifica su precio actual en el mercado para calcular valor real.
    - Responde siempre en formato Markdown bien estructurado.
    - Si fallas en una query SQL, corrígela tú mismo e intenta de nuevo.
    - Si el usuario pide guardar un análisis, usa la herramienta 'save_risk_report'.
    """
    
    # 4. Inicializar Modelo
    model = genai.GenerativeModel(
        model_name='gemini-flash-latest',
        tools=tools_list,
        system_instruction=system_instruction
    )
    
    return model.start_chat(enable_automatic_function_calling=True)