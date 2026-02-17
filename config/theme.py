"""
Sistema de diseño - Design Tokens.
Soporte para tema OSCURO y CLARO.
Colores, tipografía, espaciados y variables de diseño centralizadas.
"""

import streamlit as st
from dataclasses import dataclass
from typing import Dict


@dataclass
class ColorPalette:
    """Paleta de colores — Tema OSCURO."""
    # Colores principales
    primary: str = '#1383A7'
    primary_dark: str = '#0C4A6E'
    primary_light: str = '#1CA8D4'
    primary_glow: str = 'rgba(19, 131, 167, 0.35)'
    secondary: str = '#104E63'
    tertiary: str = '#104E63'
    quaternary: str = '#0C4A6E'
    accent: str = '#10B981'
    light: str = '#F0FAFE'

    # Colores de estado
    success: str = '#10B981'
    success_light: str = 'rgba(16, 185, 129, 0.12)'
    success_hover: str = '#0EA472'
    warning: str = '#F59E0B'
    warning_dark: str = '#F97316'
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

    # Colores para títulos inline (h2, h3, h4)
    heading_primary: str = '#F0FAFE'
    heading_secondary: str = '#1CA8D4'
    heading_accent: str = '#1CA8D4'

    # Overlay para imágenes de fondo
    hero_overlay: str = 'rgba(0, 0, 0, 0.55)'

    # Texto sobre hero images (siempre blanco)
    hero_title: str = '#FFFFFF'
    hero_subtitle: str = 'rgba(255, 255, 255, 0.85)'

    # Sidebar navigation (tema oscuro)
    nav_bg: str = 'rgba(19, 131, 167, 0.06)'
    nav_border: str = 'rgba(19, 131, 167, 0.12)'
    nav_text: str = 'rgba(240, 250, 254, 0.65)'
    nav_hover: str = 'rgba(19, 131, 167, 0.08)'
    nav_selected_bg: str = 'linear-gradient(135deg, #0C4A6E 0%, #1383A7 100%)'
    nav_selected_text: str = '#FFFFFF'

    # Popover trigger buttons (sidebar)
    popover_btn_bg: str = 'rgba(19, 131, 167, 0.08)'
    popover_btn_border: str = 'rgba(19, 131, 167, 0.18)'
    popover_btn_text: str = '#F0FAFE'
    popover_btn_hover_bg: str = 'rgba(19, 131, 167, 0.15)'
    popover_btn_hover_border: str = '#1383A7'

    # Popover body (menú desplegado)
    popover_body_bg: str = '#0C1B2E'
    popover_body_border: str = 'rgba(19, 131, 167, 0.25)'
    popover_body_shadow: str = '0 8px 30px rgba(0,0,0,0.35), 0 2px 8px rgba(19,131,167,0.10)'

    # Gradientes predefinidos
    gradient_primary: str = 'linear-gradient(135deg, #0C4A6E 0%, #1383A7 100%)'
    gradient_accent: str = 'linear-gradient(135deg, #104E63 0%, #1383A7 100%)'
    gradient_cta: str = 'linear-gradient(135deg, #0C4A6E 0%, #104E63 100%)'
    gradient_surface: str = 'linear-gradient(180deg, rgba(19,131,167,0.08) 0%, rgba(12,74,110,0.04) 100%)'
    gradient_card: str = 'linear-gradient(160deg, rgba(19,131,167,0.10) 0%, rgba(16,78,99,0.06) 60%, rgba(12,74,110,0.03) 100%)'
    gradient_glow: str = 'radial-gradient(ellipse at 50% 0%, rgba(19,131,167,0.15) 0%, transparent 70%)'


@dataclass
class LightColorPalette(ColorPalette):
    """Paleta de colores — Tema CLARO."""
    # Colores principales
    primary: str = '#048BA8'
    primary_dark: str = '#0C4A6E'
    primary_light: str = '#1383A7'
    primary_glow: str = 'rgba(4, 139, 168, 0.25)'
    secondary: str = '#104E63'
    tertiary: str = '#048BA8'
    quaternary: str = '#0C4A6E'
    accent: str = '#0EA472'
    light: str = '#F0FAFE'

    # Colores de estado
    success: str = '#059669'
    success_light: str = 'rgba(5, 150, 105, 0.10)'
    success_hover: str = '#047857'
    warning: str = '#D97706'
    warning_dark: str = '#B45309'
    warning_light: str = 'rgba(217, 119, 6, 0.10)'
    warning_hover: str = '#B45309'
    error: str = '#DC2626'
    error_light: str = 'rgba(220, 38, 38, 0.08)'
    error_hover: str = '#B91C1C'
    info: str = '#048BA8'

    # Colores semánticos (detección)
    normal: str = '#059669'
    anomaly: str = '#DC2626'
    ddos_tcp: str = '#DC2626'
    ddos_udp: str = '#D97706'
    reconnaissance: str = '#048BA8'

    # Fondos y superficies
    background: str = '#F0FAFE'
    surface: str = '#FFFFFF'
    surface_elevated: str = '#F8FCFE'
    surface_overlay: str = 'rgba(4, 139, 168, 0.04)'
    surface_variant: str = 'rgba(4, 139, 168, 0.06)'
    surface_glass: str = 'rgba(255, 255, 255, 0.85)'
    border: str = 'rgba(4, 139, 168, 0.20)'
    border_subtle: str = 'rgba(4, 139, 168, 0.10)'
    border_active: str = 'rgba(4, 139, 168, 0.40)'

    # Textos
    text_primary: str = '#0C1B2E'
    text_secondary: str = 'rgba(12, 27, 46, 0.65)'
    text_disabled: str = 'rgba(12, 27, 46, 0.35)'
    text_on_primary: str = '#FFFFFF'

    # Colores para títulos inline
    heading_primary: str = '#0C1B2E'
    heading_secondary: str = '#048BA8'
    heading_accent: str = '#104E63'

    # Overlay para imágenes de fondo
    hero_overlay: str = 'rgba(0, 0, 0, 0.50)'

    # Texto sobre hero images (siempre blanco)
    hero_title: str = '#FFFFFF'
    hero_subtitle: str = 'rgba(255, 255, 255, 0.90)'

    # Sidebar navigation (tema claro) — colores sólidos y visibles
    nav_bg: str = '#E3F4F9'
    nav_border: str = '#B8DDE8'
    nav_text: str = '#1A4A5C'
    nav_hover: str = '#D0EBF3'
    nav_selected_bg: str = 'linear-gradient(135deg, #048BA8 0%, #0C4A6E 100%)'
    nav_selected_text: str = '#FFFFFF'

    # Popover trigger buttons (sidebar) — mismos colores que nav
    popover_btn_bg: str = '#E3F4F9'
    popover_btn_border: str = '#B8DDE8'
    popover_btn_text: str = '#0C4A6E'
    popover_btn_hover_bg: str = '#D0EBF3'
    popover_btn_hover_border: str = '#048BA8'

    # Popover body (menú desplegado)
    popover_body_bg: str = '#FFFFFF'
    popover_body_border: str = '#B8DDE8'
    popover_body_shadow: str = '0 8px 30px rgba(4, 139, 168, 0.15), 0 2px 8px rgba(0,0,0,0.08)'

    # Gradientes predefinidos
    gradient_primary: str = 'linear-gradient(135deg, #048BA8 0%, #0C4A6E 100%)'
    gradient_accent: str = 'linear-gradient(135deg, #104E63 0%, #048BA8 100%)'
    gradient_cta: str = 'linear-gradient(135deg, #048BA8 0%, #104E63 100%)'
    gradient_surface: str = 'linear-gradient(180deg, rgba(4,139,168,0.06) 0%, rgba(4,139,168,0.02) 100%)'
    gradient_card: str = 'linear-gradient(160deg, rgba(4,139,168,0.06) 0%, rgba(16,78,99,0.03) 60%, rgba(12,74,110,0.01) 100%)'
    gradient_glow: str = 'radial-gradient(ellipse at 50% 0%, rgba(4,139,168,0.08) 0%, transparent 70%)'


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
    """Sistema de sombras — Tema oscuro."""
    none: str = 'none'
    sm: str = '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08)'
    md: str = '0 4px 12px rgba(0,0,0,0.15), 0 1px 3px rgba(0,0,0,0.10)'
    lg: str = '0 10px 25px rgba(0,0,0,0.20), 0 4px 10px rgba(0,0,0,0.10)'
    xl: str = '0 20px 40px rgba(0,0,0,0.25), 0 8px 16px rgba(0,0,0,0.10)'
    glow: str = '0 0 20px rgba(19,131,167,0.15), 0 0 40px rgba(19,131,167,0.05)'
    glow_success: str = '0 0 20px rgba(16,185,129,0.15)'
    glow_error: str = '0 0 20px rgba(239,68,68,0.15)'


@dataclass
class LightShadows(Shadows):
    """Sombras para tema claro."""
    sm: str = '0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)'
    md: str = '0 4px 12px rgba(0,0,0,0.08), 0 1px 3px rgba(0,0,0,0.05)'
    lg: str = '0 10px 25px rgba(0,0,0,0.10), 0 4px 10px rgba(0,0,0,0.05)'
    xl: str = '0 20px 40px rgba(0,0,0,0.12), 0 8px 16px rgba(0,0,0,0.05)'
    glow: str = '0 0 20px rgba(4,139,168,0.10), 0 0 40px rgba(4,139,168,0.03)'
    glow_success: str = '0 0 20px rgba(5,150,105,0.10)'
    glow_error: str = '0 0 20px rgba(220,38,38,0.10)'


@dataclass
class Transitions:
    """Sistema de transiciones."""
    fast: str = '150ms'
    base: str = '250ms'
    slow: str = '350ms'
    ease: str = 'cubic-bezier(0.4, 0.0, 0.2, 1)'


class Theme:
    """Tema principal con soporte claro/oscuro."""

    def __init__(self, mode: str = "dark"):
        self.mode = mode
        if mode == "light":
            self.colors = LightColorPalette()
            self.shadows = LightShadows()
        else:
            self.colors = ColorPalette()
            self.shadows = Shadows()
        self.typography = Typography()
        self.spacing = Spacing()
        self.radius = BorderRadius()
        self.transitions = Transitions()

    @property
    def is_dark(self) -> bool:
        return self.mode == "dark"

    @property
    def is_light(self) -> bool:
        return self.mode == "light"

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
            'grid': f'rgba(19, 131, 167, {"0.12" if self.is_dark else "0.08"})',
            'text': self.colors.text_primary,
        }

    def get_plotly_layout(self) -> dict:
        """Layout de Plotly según el tema."""
        return {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': self.colors.text_primary},
            'xaxis': {
                'gridcolor': self.get_chart_colors()['grid'],
                'zerolinecolor': self.get_chart_colors()['grid'],
            },
            'yaxis': {
                'gridcolor': self.get_chart_colors()['grid'],
                'zerolinecolor': self.get_chart_colors()['grid'],
            },
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


def get_current_theme() -> Theme:
    """
    Obtiene el tema actual basado en session_state.
    Usar esta función en TODOS los archivos que necesiten colores dinámicos.
    """
    mode = st.session_state.get("theme_mode", "dark")
    return Theme(mode=mode)


def get_theme_by_mode(mode: str) -> Theme:
    """Obtiene un tema por modo (para funciones cacheadas que no acceden a session_state)."""
    return Theme(mode=mode)


# Instancia global (se usa en style.py para CSS base)
theme = Theme(mode="dark")
