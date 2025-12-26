import google.generativeai as genai
import os
from dotenv import load_dotenv

# Cargar entorno
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: No se encontró la API KEY en .env")
else:
    print(f"Usando API Key que empieza por: {api_key[:5]}...")
    genai.configure(api_key=api_key)

    print("\nConsultando modelos disponibles en Google AI Studio...")
    try:
        found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Disponible: {m.name}")
                found = True
        
        if not found:
            print("No se encontraron modelos compatibles con 'generateContent'.")
            
    except Exception as e:
        print(f"\n Error de conexión: {e}")
        