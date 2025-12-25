import os
import re
from datetime import datetime
from pathlib import Path
from fpdf import FPDF

# Definir ruta base absoluta
BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = BASE_DIR / "reports"

class PDFReport(FPDF):
    def header(self):
        # Encabezado simple
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'BELFORT RISK REPORT', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def footer(self):
        # Pie de página con número
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def clean_markdown_symbols(text):
    """Limpia el texto de Markdown para que se vea bien en PDF plano."""
    # Eliminar negritas **texto**
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Eliminar itálicas *texto*
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Eliminar encabezados ###
    text = re.sub(r'#+\s', '', text)
    # Eliminar links [texto](url)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    return text

def save_risk_report(topic: str, content: str):
    """
    Genera y guarda un reporte formal en formatos Markdown (.md) y PDF.
    """
    # 1. Preparar nombres y rutas
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    safe_topic = topic.replace(" ", "_").replace("/", "-")
    filename_base = f"{timestamp}_{safe_topic}"
    
    md_path = REPORTS_DIR / f"{filename_base}.md"
    pdf_path = REPORTS_DIR / f"{filename_base}.pdf"

    # Asegurar que la carpeta existe
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # 2. Guardar versión Markdown (Para referencia técnica)
    header_md = f"# BELFORT RISK REPORT\n**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n**Tema:** {topic}\n\n---\n\n"
    full_md_content = header_md + content
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(full_md_content)

    # 3. Guardar versión PDF (Para enviar a gerencia)
    try:
        pdf = PDFReport()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Metadatos del PDF
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 10, f"Tema: {topic}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        # Limpieza de contenido para PDF
        clean_content = clean_markdown_symbols(content)
        
        # Manejo básico de caracteres latinos (tildes, ñ)
        # fpdf2 a veces prefiere latin-1 para fuentes estándar
        try:
            clean_content = clean_content.encode('latin-1', 'replace').decode('latin-1')
        except:
            pass # Si falla, usa el string original
            
        pdf.multi_cell(0, 5, clean_content)
        
        pdf.output(str(pdf_path))
        
        return f"✅ REPORTE GENERADO:\n- PDF: {pdf_path}\n- MD: {md_path}"

    except Exception as e:
        return f"⚠️ Reporte guardado solo como MD. Error en PDF: {str(e)}"