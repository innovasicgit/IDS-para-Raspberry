# Sistema de Diseño - Fase 3

## 📐 Arquitectura del Tema

El sistema de diseño implementado proporciona un enfoque profesional y escalable para la gestión de estilos en la aplicación IDS.

### Estructura de Archivos

```
config/
  └── theme.py          # Design tokens y sistema de tema
frontend/
  ├── style.py          # Estilos globales usando el tema
  ├── layouts/
  │   ├── __init__.py
  │   └── main_layout.py    # Layouts reutilizables
  ├── utils/
  │   ├── __init__.py
  │   └── formatters.py     # Funciones de formateo
  └── components/
      └── *.py          # Componentes usando el tema
```

## 🎨 Design Tokens

### ColorPalette

Sistema de colores semánticos consistente:

```python
from config.theme import theme

# Colores principales
theme.colors.primary      # #4B9FE1 - Color principal
theme.colors.secondary    # #2E5077 - Color secundario
theme.colors.accent       # #F39C12 - Acento

# Estados
theme.colors.success      # #00C853 - Verde éxito
theme.colors.warning      # #FFA726 - Naranja advertencia
theme.colors.error        # #FF5252 - Rojo error
theme.colors.info         # #29B6F6 - Azul info

# Tipos de ataque
theme.colors.normal       # #4CAF50 - Tráfico normal
theme.colors.anomaly      # #FF5252 - Anomalía
theme.colors.ddos_tcp     # #E53935 - DDoS TCP
theme.colors.ddos_udp     # #D32F2F - DDoS UDP
```

### Typography

Sistema tipográfico consistente:

```python
# Familias de fuentes
theme.typography.font_family        # 'Roboto', sans-serif
theme.typography.font_family_mono   # 'Consolas', monospace

# Tamaños
theme.typography.size_xs      # 0.75rem
theme.typography.size_sm      # 0.875rem
theme.typography.size_base    # 1rem
theme.typography.size_lg      # 1.125rem
theme.typography.size_xl      # 1.25rem
theme.typography.size_2xl     # 1.5rem
theme.typography.size_3xl     # 1.875rem
theme.typography.size_4xl     # 2.25rem

# Pesos
theme.typography.weight_normal      # 400
theme.typography.weight_medium      # 500
theme.typography.weight_semibold    # 600
theme.typography.weight_bold        # 700
```

### Spacing

Sistema de espaciado consistente:

```python
theme.spacing.xs      # 0.25rem (4px)
theme.spacing.sm      # 0.5rem  (8px)
theme.spacing.md      # 1rem    (16px)
theme.spacing.lg      # 1.5rem  (24px)
theme.spacing.xl      # 2rem    (32px)
theme.spacing.xxl     # 3rem    (48px)
theme.spacing.xxxl    # 4rem    (64px)
```

### Otros Tokens

```python
# Border Radius
theme.radius.sm       # 0.25rem
theme.radius.md       # 0.5rem
theme.radius.lg       # 1rem
theme.radius.full     # 9999px

# Shadows
theme.shadows.sm      # Sombra pequeña
theme.shadows.md      # Sombra media
theme.shadows.lg      # Sombra grande
theme.shadows.xl      # Sombra extra grande

# Transitions
theme.transitions.fast    # 0.15s
theme.transitions.base    # 0.3s
theme.transitions.slow    # 0.5s
theme.transitions.ease    # ease-in-out
```

## 🛠️ Uso en Componentes

### Ejemplo 1: Card con Tema

```python
import streamlit as st
from config.theme import theme

st.markdown(
    f"""
    <div style="
        background: {theme.colors.surface_variant};
        padding: {theme.spacing.lg};
        border-radius: {theme.radius.lg};
        box-shadow: {theme.shadows.md};
        border: 1px solid {theme.colors.border};
    ">
        <h3 style="color: {theme.colors.text_primary};">
            Título del Card
        </h3>
        <p style="color: {theme.colors.text_secondary};">
            Contenido del card
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
```

### Ejemplo 2: Layouts Reutilizables

```python
from frontend.layouts import create_page_header, create_info_card

# Header consistente
create_page_header(
    "Dashboard Principal",
    subtitle="Sistema de Detección de Intrusiones",
    icon="🛡️"
)

# Card informativo
create_info_card(
    "Información",
    "Este es un mensaje informativo importante",
    variant="info"
)
```

### Ejemplo 3: Formatters

```python
from frontend.utils import (
    format_number,
    format_percentage,
    format_bytes,
    format_attack_name
)

# Formatear números
total_packets = 1234567
st.metric("Paquetes", format_number(total_packets))  # "1.234.567"

# Formatear porcentajes
accuracy = 0.9534
st.write(format_percentage(accuracy))  # "95.3%"

# Formatear bytes
file_size = 1536000
st.write(format_bytes(file_size))  # "1.46 MB"

# Formatear nombres de ataque
attack = "ddos_tcp"
st.write(format_attack_name(attack))  # "DDoS TCP"
```

## 📊 Charts con Tema

El tema proporciona colores consistentes para gráficos:

```python
from config.theme import theme

# Obtener mapa de colores para gráficos
color_map = theme.get_color_map()

# Crear gráfico de Plotly con colores del tema
import plotly.graph_objects as go

fig = go.Figure(data=[
    go.Bar(
        x=['Normal', 'Anomalía'],
        y=[100, 50],
        marker_color=[color_map['Normal'], color_map['Anomalía']]
    )
])

# Aplicar configuración del tema
chart_colors = theme.get_chart_colors()
fig.update_layout(
    plot_bgcolor=chart_colors['plot_bgcolor'],
    paper_bgcolor=chart_colors['paper_bgcolor'],
    font_color=chart_colors['font_color']
)
```

## 🎭 Estados Especiales

### Loading State

```python
from frontend.layouts import create_loading_state

with create_loading_state("Procesando datos..."):
    # Operación larga
    process_data()
```

### Empty State

```python
from frontend.layouts import create_empty_state

if not data:
    create_empty_state(
        "No hay datos disponibles",
        "Sube un archivo CSV o inicia una captura",
        icon="📭"
    )
```

## ✅ Beneficios

1. **Consistencia Visual**: Todos los componentes usan los mismos colores, espaciados y tipografía
2. **Mantenibilidad**: Cambios en el tema se reflejan automáticamente en toda la app
3. **Escalabilidad**: Fácil agregar nuevos componentes siguiendo el sistema
4. **Profesionalismo**: Diseño coherente y pulido
5. **Dark/Light Theme**: Base preparada para múltiples temas

## 🚀 Próximos Pasos

1. Aplicar tema a componentes restantes (charts.py, data_uploader.py, sidebar.py)
2. Implementar animaciones usando `theme.transitions`
3. Crear variantes de tema (dark mode, high contrast)
4. Agregar más layouts reutilizables
5. Documentar componentes con Storybook-style

## 📝 Convenciones

### Nomenclatura de Colores

- `primary`, `secondary`, `accent`: Colores de marca
- `success`, `warning`, `error`, `info`: Estados
- `text_primary`, `text_secondary`: Texto
- `surface`, `background`: Fondos
- `border`, `divider`: Separadores

### Espaciado

Usar múltiplos de 4px siguiendo la escala del tema:
- `xs` (4px): Espacios muy pequeños
- `sm` (8px): Espacios pequeños
- `md` (16px): Espaciado base
- `lg` (24px): Espacios grandes
- `xl` (32px): Espacios muy grandes

### Componentes

Todos los componentes deben:
1. Importar `theme` de `config.theme`
2. Usar tokens del tema en lugar de valores hardcodeados
3. Incluir docstrings con tipos
4. Ser reutilizables y composables
