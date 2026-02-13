"""
Sistema de diseño - Design Tokens.
Colores, tipografía, espaciados y variables de diseño centralizadas.
Paleta: #0C4A6E · #1383A7 · #104E63 · #F0FAFE
Profesional UI/UX con tonalidades claras difuminadas.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ColorPalette:
    """Paleta de colores del sistema — Tema Azul Profundo profesional."""
    # Colores principales
    primary: str = '#1383A7'
    primary_dark: str = '#0C4A6E'
    primary_light: str = '#1CA8D4'
    primary_glow: str = 'rgba(19, 131, 167, 0.35)'
    secondary: str = '#104E63'
    accent: str = '#10B981'
    light: str = '#F0FAFE'

    # Colores de estado
    success: str = '#10B981'
    success_light: str = 'rgba(16, 185, 129, 0.12)'
    success_hover: str = '#0EA472'
    warning: str = '#F59E0B'
    warning_light: str = 'rgba(245, 158, 11, 0.12)'
    warning_hover: str = '#D97706'
    error: str = '#EF4444'
    error_light: str = 'rgba(239, 68, 68, 0.12)'
    error_hover: str = '#DC2626'
    info: str = '#1383A7'

    # Colores semánticos (detección)
    normal: str = '#10B981'
    anomaly: str = '#EF4444'
    ddos_tcp: str = '#EF4444'
    ddos_udp: str = '#F59E0B'
    reconnaissance: str = '#1383A7'

    # Fondos y superficies
    background: str = '#070D1A'
    surface: str = '#0C1B2E'
    surface_elevated: str = '#0F2237'
    surface_overlay: str = 'rgba(19, 131, 167, 0.06)'
    surface_variant: str = 'rgba(19, 131, 167, 0.08)'
    surface_glass: str = 'rgba(12, 74, 110, 0.25)'
    border: str = 'rgba(19, 131, 167, 0.18)'
    border_subtle: str = 'rgba(19, 131, 167, 0.10)'
    border_active: str = 'rgba(19, 131, 167, 0.45)'

    # Textos
    text_primary: str = '#F0FAFE'
    text_secondary: str = 'rgba(240, 250, 254, 0.65)'
    text_disabled: str = 'rgba(240, 250, 254, 0.35)'
    text_on_primary: str = '#FFFFFF'

    # Gradientes predefinidos
    gradient_primary: str = 'linear-gradient(135deg, #0C4A6E 0%, #1383A7 100%)'
    gradient_accent: str = 'linear-gradient(135deg, #104E63 0%, #1383A7 100%)'
    gradient_cta: str = 'linear-gradient(135deg, #0C4A6E 0%, #104E63 100%)'
    gradient_surface: str = 'linear-gradient(180deg, rgba(19,131,167,0.08) 0%, rgba(12,74,110,0.04) 100%)'
    gradient_card: str = 'linear-gradient(160deg, rgba(19,131,167,0.10) 0%, rgba(16,78,99,0.06) 60%, rgba(12,74,110,0.03) 100%)'
    gradient_glow: str = 'radial-gradient(ellipse at 50% 0%, rgba(19,131,167,0.15) 0%, transparent 70%)'


@dataclass
class Typography:
    """Sistema de tipografía."""
    font_family: str = "'Inter', 'Segoe UI', 'Roboto', sans-serif"
    font_family_mono: str = "'Fira Code', 'Consolas', monospace"
    size_xs: str = '0.75rem'
    size_sm: str = '0.875rem'
    size_base: str = '1rem'
    size_lg: str = '1.125rem'
    size_xl: str = '1.25rem'
    size_2xl: str = '1.5rem'
    size_3xl: str = '1.875rem'
    size_4xl: str = '2.25rem'
    weight_light: int = 300
    weight_regular: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700


@dataclass
class Spacing:
    """Sistema de espaciados."""
    xs: str = '0.25rem'
    sm: str = '0.5rem'
    md: str = '1rem'
    lg: str = '1.5rem'
    xl: str = '2rem'
    xxl: str = '3rem'
    xxxl: str = '4rem'


@dataclass
class BorderRadius:
    """Sistema de border radius."""
    none: str = '0'
    sm: str = '0.375rem'
    md: str = '0.625rem'
    lg: str = '0.875rem'
    xl: str = '1.125rem'
    xxl: str = '1.5rem'
    full: str = '9999px'


@dataclass
class Shadows:
    """Sistema de sombras."""
    none: str = 'none'
    sm: str = '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08)'
    md: str = '0 4px 12px rgba(0,0,0,0.15), 0 1px 3px rgba(0,0,0,0.10)'
    lg: str = '0 10px 25px rgba(0,0,0,0.20), 0 4px 10px rgba(0,0,0,0.10)'
    xl: str = '0 20px 40px rgba(0,0,0,0.25), 0 8px 16px rgba(0,0,0,0.10)'
    glow: str = '0 0 20px rgba(19,131,167,0.15), 0 0 40px rgba(19,131,167,0.05)'
    glow_success: str = '0 0 20px rgba(16,185,129,0.15)'
    glow_error: str = '0 0 20px rgba(239,68,68,0.15)'


@dataclass
class Transitions:
    """Sistema de transiciones."""
    fast: str = '150ms'
    base: str = '250ms'
    slow: str = '350ms'
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
        return {
            'Normal': self.colors.normal,
            'Anómalo': self.colors.anomaly,
            'DDOS_TCP': self.colors.ddos_tcp,
            'DDOS_UDP': self.colors.ddos_udp,
            'Reconnaissance': self.colors.reconnaissance,
        }

    def get_chart_colors(self) -> Dict[str, str]:
        return {
            'primary': self.colors.primary,
            'success': self.colors.success,
            'warning': self.colors.warning,
            'error': self.colors.error,
            'background': 'rgba(0,0,0,0)',
            'grid': 'rgba(19, 131, 167, 0.12)',
            'text': self.colors.text_primary,
        }

    def generate_css(self) -> str:
        """Generar variables CSS desde tokens."""
        return f"""
        :root {{
            --color-primary: {self.colors.primary};
            --color-primary-dark: {self.colors.primary_dark};
            --color-primary-light: {self.colors.primary_light};
            --color-secondary: {self.colors.secondary};
            --color-background: {self.colors.background};
            --color-surface: {self.colors.surface};
            --color-text: {self.colors.text_primary};
            --color-text-secondary: {self.colors.text_secondary};
            --color-success: {self.colors.success};
            --color-warning: {self.colors.warning};
            --color-error: {self.colors.error};
            --color-border: {self.colors.border};
            --shadow-glow: {self.shadows.glow};
        }}
        """


# Instancia global
theme = Theme()
