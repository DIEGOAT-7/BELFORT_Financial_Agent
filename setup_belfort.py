import os
from pathlib import Path

# Nombre del Proyecto
PROJECT_NAME = "BELFORT_Financial_Agent"

# Estructura de carpetas profesional
STRUCTURE = [
    "data/raw",              # Datos crudos (csv, json)
    "data/processed",        # Datos limpios o la DB SQLite final
    "notebooks",             # Para tus experimentos y pruebas rápidas (Jupyter)
    "src/agent",             # Lógica del cerebro de Gemini
    "src/tools",             # Scripts de herramientas (SQL connector, Yahoo Finance)
    "src/api",               # El servidor FastAPI
    "src/pipelines",         # Scripts de ETL o automatización de datos
    "config",                # Archivos .yaml con prompts y configuraciones
    "tests",                 # Pruebas unitarias (Pytest)
    "docker",                # Dockerfile y configs de despliegue
    "docs",                  # Documentación del proyecto
]

# Archivos iniciales para crear
FILES = {
    "README.md": f"# {PROJECT_NAME}\n\nAgente de IA para Riesgo Financiero.\n",
    ".env": "GOOGLE_API_KEY=tu_api_key_aqui\nDB_PATH=data/processed/institutional_radar.db",
    "requirements.txt": "fastapi\nuvicorn\ngoogle-generativeai\nsqlalchemy\npydantic\npython-dotenv\nyfinance\ntyper\nrich\n",
    "config/agents.yaml": "# Configuración de roles y prompts del sistema\n",
    "src/__init__.py": "",
    "main.py": "# Punto de entrada de la aplicación (Entrypoint)\n",
    ".gitignore": "__pycache__/\n*.env\n.DS_Store\nvenv/\ndata/\n!data/.gitkeep\n"
}

def create_structure():
    base_path = Path.cwd() / PROJECT_NAME
    
    # 1. Crear Directorios
    print(f" Iniciando protocolo de construcción para: {PROJECT_NAME}")
    
    if not base_path.exists():
        base_path.mkdir()
        print(f"Directorio raíz creado: {PROJECT_NAME}")
    
    for folder in STRUCTURE:
        folder_path = base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        # Crear un .gitkeep para que git suba carpetas vacías
        (folder_path / ".gitkeep").touch()
        print(f"Carpeta creada: {folder}")

    # 2. Crear Archivos Base
    for file_name, content in FILES.items():
        file_path = base_path / file_name
        if not file_path.exists():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Archivo creado: {file_name}")
        else:
            print(f"El archivo ya existe: {file_name}")

    print("\n BELFORT está listo. Estructura desplegada correctamente.")
    print(f" cd {PROJECT_NAME}")

if __name__ == "__main__":
    create_structure()