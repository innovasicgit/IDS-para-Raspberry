import io
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os
import unicodedata


def _find_system_font():
    """Buscar una fuente TrueType común en el sistema."""
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def _ensure_unicode_font(pdf):
    """Registrar y devolver el nombre de una fuente Unicode si está disponible.

    Si no se encuentra ninguna fuente, devuelve None.
    """
    font_path = _find_system_font()
    if font_path:
        # Usamos el nombre 'DejaVu' como alias local independientemente de la ruta real
        try:
            pdf.add_font('DejaVu', '', font_path, uni=True)
            pdf.add_font('DejaVu', 'B', font_path, uni=True)
            pdf.add_font('DejaVu', 'I', font_path, uni=True)
            return 'DejaVu'
        except Exception:
            return None
    return None

# Función para crear el PDF del reporte de predicción
def generar_reporte_pdf(resumen, labels, values, descripcion_amenazas, fig=None, logo_path=None):
    """
    resumen: texto resumen de la predicción
    labels: lista de etiquetas de clases
    values: lista de conteos por clase
    descripcion_amenazas: dict {clase: descripcion}
    fig: matplotlib.figure (opcional, para incluir gráfica de barras)
    logo_path: ruta a imagen del logo (opcional)
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Intentar registrar y usar una fuente TrueType Unicode (DejaVu u otra)
    font_name = _ensure_unicode_font(pdf)
    _normalize_fallback = False
    if font_name:
        # fuente registrada correctamente
        pass
    else:
        # Sin fuente Unicode disponible; usaremos Arial pero normalizaremos textos
        font_name = 'Arial'
        _normalize_fallback = True

    def _normalize_for_ascii(s: str) -> str:
        if s is None:
            return s
        # Reemplazar guiones y espacios no rompibles comunes por sus equivalentes ASCII
        replacements = {
            '\u2011': '-',  # non-breaking hyphen
            '\u2013': '-',  # en dash
            '\u2014': '-',  # em dash
            '\u2012': '-',  # figure dash
            '\u00A0': ' ',  # no-break space
        }
        for k, v in replacements.items():
            s = s.replace(k, v)
        # Como último recurso, normalizar compatibilidad y eliminar caracteres no imprimibles
        s = unicodedata.normalize('NFKC', s)
        return s

    # Encabezado con logo (si disponible)
    resolved_logo = None
    if logo_path and os.path.exists(logo_path):
        resolved_logo = logo_path
    else:
        # Intento de ruta relativa: ../img/logo.png (desde frontend/)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        candidate = os.path.join(base_dir, 'img', 'logo.png')
        if os.path.exists(candidate):
            resolved_logo = candidate
    if resolved_logo:
        try:
            pdf.image(resolved_logo, x=12, y=10, w=30)
            pdf.ln(20)  # margen bajo el logo
        except Exception:
            pass

    # Título
    pdf.set_font(font_name, 'B', 18)
    pdf.cell(0, 15, _normalize_for_ascii("Reporte de Predicción IDS") if _normalize_fallback else "Reporte de Predicción IDS", ln=True, align='C')
    pdf.set_font(font_name, '', 12)
    fecha_txt = f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    pdf.cell(0, 10, _normalize_for_ascii(fecha_txt) if _normalize_fallback else fecha_txt, ln=True, align='R')
    pdf.ln(5)

    # Descripción breve
    pdf.set_font(font_name, '', 12)
    pdf.multi_cell(0, 10, _normalize_for_ascii(resumen) if _normalize_fallback else resumen)
    pdf.ln(5)

    # Gráfica de barras
    if fig is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            fig.savefig(tmpfile.name, bbox_inches='tight')
            pdf.image(tmpfile.name, x=30, w=150)
            os.unlink(tmpfile.name)
        pdf.ln(5)

    # Tabla de resultados
    pdf.set_font(font_name, 'B', 12)
    pdf.cell(0, 10, _normalize_for_ascii("Resumen de Resultados:") if _normalize_fallback else "Resumen de Resultados:", ln=True)
    pdf.set_font(font_name, '', 12)
    for label, value in zip(labels, values):
        line = f"{label}: {value}"
        pdf.cell(0, 8, _normalize_for_ascii(line) if _normalize_fallback else line, ln=True)
    pdf.ln(5)

    # Descripción de amenazas
    pdf.set_font(font_name, 'B', 12)
    pdf.cell(0, 10, _normalize_for_ascii("Descripción de Amenazas:") if _normalize_fallback else "Descripción de Amenazas:", ln=True)
    pdf.set_font(font_name, '', 12)
    for label in labels:
        desc = descripcion_amenazas.get(label, "Sin descripción disponible.")
        text_block = f"{label}: {desc}"
        pdf.multi_cell(0, 8, _normalize_for_ascii(text_block) if _normalize_fallback else text_block)
        pdf.ln(1)

    # Pie de página
    pdf.set_y(-30)
    pdf.set_font(font_name, 'I', 10)
    footer = "Sistema de Detección de Anomalías IoT - Innovasic UCC"
    pdf.cell(0, 10, _normalize_for_ascii(footer) if _normalize_fallback else footer, 0, 0, 'C')

    # Salida en memoria como bytes (compatibles con Streamlit)
    pdf_buf = pdf.output(dest='S')
    if isinstance(pdf_buf, (bytes, bytearray)):
        return io.BytesIO(pdf_buf)
    # Compatibilidad con posibles str en versiones antiguas
    return io.BytesIO(str(pdf_buf).encode('latin1'))

# Diccionario ejemplo de descripciones de amenazas
DESCRIPCIONES_AMENAZAS = {
    'Normal': (
        'Tráfico habitual sin indicios de riesgo. Recomendación: mantener el '
        'monitoreo regular para detectar cambios o picos inusuales.'
    ),
    'Anómalo': (
        'Actividad fuera de patrón que puede ser fallo de configuración o intento '
        'de ataque. Recomendación: revisar equipos/servicios recientes y registros.'
    ),
    'DDOS_TCP': (
        'Múltiples conexiones TCP intentan saturar un servicio. Medidas: activar '
        'SYN cookies, límites por IP y cerrar puertos innecesarios.'
    ),
    'DDOS_UDP': (
        'Alto volumen de tráfico UDP hacia puertos abiertos. Medidas: limitar UDP, '
        'permitir solo puertos necesarios y aplicar filtrado con el proveedor.'
    ),
    'Reconnaissance': (
        'Escaneos para descubrir servicios y debilidades. Medidas: ocultar '
        'servicios, reglas anti‑scan y revisar logs de seguridad.'
    ),
}
