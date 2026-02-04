"""
Sistema de diseño - Design Tokens.
Colores, tipografía, espaciados y variables de diseño centralizadas.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ColorPalette:
    """Paleta de colores del sistema."""
    # Colores principales
    primary: str = '#4B9FE1'
    secondary: str = '#42A5F5'
    accent: str = '#00C853'
    
    # Colores de estado
    success: str = '#00C853'
    warning: str = '#FFA726'
    error: str = '#FF5252'
    info: str = '#4B9FE1'
    
    # Colores semánticos
    normal: str = '#00C853'
    anomaly: str = '#FF5252'
    ddos_tcp: str = '#FF5252'
    ddos_udp: str = '#FFA726'
    reconnaissance: str = '#42A5F5'
    
    # Grises
    background: str = '#0E1117'
    surface: str = '#262730'
    surface_variant: str = 'rgba(255,255,255,0.06)'
    border: str = 'rgba(255,255,255,0.2)'
    
    # Textos
    text_primary: str = '#FAFAFA'
    text_secondary: str = 'rgba(255,255,255,0.7)'
    text_disabled: str = 'rgba(255,255,255,0.5)'


@dataclass
class Typography:
    """Sistema de tipografía."""
    # Familias
    font_family: str = "'Inter', 'Segoe UI', 'Roboto', sans-serif"
    font_family_mono: str = "'Fira Code', 'Consolas', monospace"
    
    # Tamaños (rem)
    size_xs: str = '0.75rem'    # 12px
    size_sm: str = '0.875rem'   # 14px
    size_base: str = '1rem'     # 16px
    size_lg: str = '1.125rem'   # 18px
    size_xl: str = '1.25rem'    # 20px
    size_2xl: str = '1.5rem'    # 24px
    size_3xl: str = '1.875rem'  # 30px
    size_4xl: str = '2.25rem'   # 36px
    
    # Pesos
    weight_light: int = 300
    weight_regular: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700


@dataclass
class Spacing:
    """Sistema de espaciados."""
    # Espaciado base: 4px
    xs: str = '0.25rem'   # 4px
    sm: str = '0.5rem'    # 8px
    md: str = '1rem'      # 16px
    lg: str = '1.5rem'    # 24px
    xl: str = '2rem'      # 32px
    xxl: str = '3rem'     # 48px
    xxxl: str = '4rem'    # 64px


@dataclass
class BorderRadius:
    """Sistema de border radius."""
    none: str = '0'
    sm: str = '0.25rem'   # 4px
    md: str = '0.5rem'    # 8px
    lg: str = '0.75rem'   # 12px
    xl: str = '1rem'      # 16px
    full: str = '9999px'


@dataclass
class Shadows:
    """Sistema de sombras."""
    none: str = 'none'
    sm: str = '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
    md: str = '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
    lg: str = '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
    xl: str = '0 20px 25px -5px rgba(0, 0, 0, 0.1)'


@dataclass
class Transitions:
    """Sistema de transiciones."""
    fast: str = '150ms'
    base: str = '200ms'
    slow: str = '300ms'
    ease: str = 'cubic-bezier(0.4, 0.0, 0.2, 1)'


class Theme:
    """Tema principal de la aplicación."""
    
    def __init__(self):
        self.colors = ColorPalette()
        self.typography = Typography()
        self.spacing = Spacing()
        self.radius = BorderRadius()
        self.shadows = Shadows()
        self.transitions = Transitions()
    
    def get_color_map(self) -> Dict[str, str]:
        """Obtener mapa de colores para gráficos."""
        return {
            'Normal': self.colors.normal,
            'Anómalo': self.colors.anomaly,
            'DDOS_TCP': self.colors.ddos_tcp,
            'DDOS_UDP': self.colors.ddos_udp,
            'Reconnaissance': self.colors.reconnaissance,
        }
    
    def get_chart_colors(self) -> Dict[str, str]:
        """Colores para gráficos Plotly."""
        return {
            'primary': self.colors.primary,
            'success': self.colors.success,
            'warning': self.colors.warning,
            'error': self.colors.error,
            'background': 'rgba(0,0,0,0)',
            'grid': 'rgba(255,255,255,0.1)',
            'text': self.colors.text_primary,
        }
    
    def generate_css(self) -> str:
        """Generar CSS con variables del tema."""
        return f"""
        :root {{
            /* Colores */
            --color-primary: {self.colors.primary};
            --color-success: {self.colors.success};
            --color-warning: {self.colors.warning};
            --color-error: {self.colors.error};
            --color-info: {self.colors.info};
            
            /* Backgrounds */
            --bg-primary: {self.colors.background};
            --bg-surface: {self.colors.surface};
            --bg-surface-variant: {self.colors.surface_variant};
            
            /* Textos */
            --text-primary: {self.colors.text_primary};
            --text-secondary: {self.colors.text_secondary};
            
            /* Tipografía */
            --font-family: {self.typography.font_family};
            --font-size-base: {self.typography.size_base};
            
            /* Espaciado */
            --spacing-sm: {self.spacing.sm};
            --spacing-md: {self.spacing.md};
            --spacing-lg: {self.spacing.lg};
            
            /* Border Radius */
            --radius-md: {self.radius.md};
            --radius-lg: {self.radius.lg};
            
            /* Transiciones */
            --transition-base: {self.transitions.base};
        }}
        """


# Instancia global del tema
theme = Theme()
