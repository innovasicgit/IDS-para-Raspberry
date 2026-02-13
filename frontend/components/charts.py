"""
Componentes de gráficos reutilizables usando Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Dict, Optional


def create_pie_chart(labels: List[str], values: List[int], title: str = "Distribución") -> go.Figure:
    """
    Crear gráfico de pastel con colores predefinidos.
    
    Args:
        labels: Lista de etiquetas
        values: Lista de valores
        title: Título del gráfico
        
    Returns:
        Figura de Plotly
    """
    color_map = {
        'Normal': '#10B981',
        'Anómalo': '#EF4444',
        'DDOS_TCP': '#EF4444',
        'DDOS_UDP': '#F59E0B',
        'Reconnaissance': '#1383A7'
    }
    
    fig = px.pie(
        names=labels,
        values=values,
        color=labels,
        color_discrete_map=color_map,
        title=title
    )
    fig.update_traces(textinfo='percent+label')
    return fig


def create_bar_chart(
    labels: List[str], 
    values: List[int], 
    title: str = "Distribución de Detecciones",
    color_normal: str = '#10B981',
    color_attack: str = '#EF4444'
) -> go.Figure:
    """
    Crear gráfico de barras con colores según tipo (Normal vs Ataque).
    
    Args:
        labels: Lista de etiquetas
        values: Lista de valores
        title: Título del gráfico
        color_normal: Color para 'Normal'
        color_attack: Color para otros (ataques)
        
    Returns:
        Figura de Plotly
    """
    bar_colors = [
        color_normal if str(lbl).lower() == 'normal' else color_attack 
        for lbl in labels
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            x=labels, 
            y=values, 
            text=values, 
            textposition='auto', 
            marker_color=bar_colors
        )
    ])
    fig.update_layout(title=title, title_x=0.5)
    return fig


def create_histogram(
    data: np.ndarray, 
    title: str = "Distribución",
    threshold: Optional[float] = None,
    nbins: int = 30
) -> go.Figure:
    """
    Crear histograma con línea de umbral opcional.
    
    Args:
        data: Datos para el histograma
        title: Título del gráfico
        threshold: Valor del umbral (opcional)
        nbins: Número de bins
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data, 
        nbinsx=nbins, 
        marker_color='#1383A7', 
        name='Distribución'
    ))
    
    if threshold is not None:
        fig.add_shape(
            type='line', 
            x0=threshold, x1=threshold, 
            y0=0, y1=1, 
            xref='x', yref='paper', 
            line=dict(color='#EF4444', width=2)
        )
        fig.add_annotation(
            x=threshold, y=1, 
            yref='paper', 
            text=f"Umbral={threshold:.3f}", 
            showarrow=True, 
            arrowhead=1
        )
    
    fig.update_layout(title=title, title_x=0.5)
    return fig


def create_traffic_pattern_chart(
    traffic_data: np.ndarray,
    window: int = 20,
    anomaly_indices: Optional[np.ndarray] = None
) -> go.Figure:
    """
    Crear gráfico de patrón de tráfico con techo/suelo y anomalías.
    
    Args:
        traffic_data: Serie de datos de tráfico
        window: Tamaño de ventana para rolling calculations
        anomaly_indices: Índices de anomalías detectadas
        
    Returns:
        Figura de Plotly
    """
    import pandas as pd
    
    # Calcular techo y suelo
    traffic_series = pd.Series(traffic_data)
    ceiling = traffic_series.rolling(window=window).max()
    floor = traffic_series.rolling(window=window).min()
    
    fig = go.Figure()

    # Línea principal de tráfico
    fig.add_trace(go.Scatter(
        x=list(range(len(traffic_data))),
        y=traffic_data,
        mode='lines',
        name='Tráfico',
        line=dict(color='#1383A7', width=1)
    ))

    # Línea de techo
    fig.add_trace(go.Scatter(
        x=list(range(len(ceiling))),
        y=ceiling,
        mode='lines',
        name='Techo',
        line=dict(color='#10B981', width=2, dash='dash')
    ))

    # Línea de suelo
    fig.add_trace(go.Scatter(
        x=list(range(len(floor))),
        y=floor,
        mode='lines',
        name='Suelo',
        line=dict(color='#F59E0B', width=2, dash='dash')
    ))

    # Puntos de anomalías
    if anomaly_indices is not None and len(anomaly_indices) > 0:
        fig.add_trace(go.Scatter(
            x=anomaly_indices,
            y=traffic_data[anomaly_indices],
            mode='markers',
            name='Anomalías',
            marker=dict(color='#EF4444', size=8, symbol='circle')
        ))

    # Layout
    fig.update_layout(
        title="Patrón de Tráfico y Detección de Anomalías",
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F0FAFE'),
        showlegend=True,
        legend=dict(
            yanchor="top", y=0.99,
            xanchor="left", x=0.01,
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(t=50, l=50, r=50, b=50),
        xaxis=dict(
            title="Muestras",
            showgrid=False,
            showline=True,
            linecolor='rgba(19, 131, 167, 0.3)'
        ),
        yaxis=dict(
            title="Intensidad de Tráfico",
            showgrid=True,
            gridcolor='rgba(19, 131, 167, 0.10)',
            zeroline=False
        )
    )
    
    return fig


def create_comparison_bar_chart(
    models: List[str],
    normal_counts: List[int],
    attack_counts: List[int]
) -> go.Figure:
    """
    Crear gráfico de barras agrupadas para comparación de modelos.
    
    Args:
        models: Lista de nombres de modelos
        normal_counts: Conteos de predicciones normales
        attack_counts: Conteos de predicciones de ataques
        
    Returns:
        Figura de Plotly
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Normal', 
        x=models, 
        y=normal_counts, 
        marker_color='#10B981'
    ))
    fig.add_trace(go.Bar(
        name='Ataques', 
        x=models, 
        y=attack_counts, 
        marker_color='#EF4444'
    ))
    fig.update_layout(
        barmode='group', 
        title='Normal vs Ataques por modelo', 
        title_x=0.5
    )
    return fig
