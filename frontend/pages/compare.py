"""
Página de comparación de modelos.
Permite ejecutar múltiples modelos sobre el mismo dataset y comparar resultados.
"""

import streamlit as st
from config.theme import get_current_theme
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from collections import Counter

from backend.model_utils import load_model, dict_predict, pred_threshold
from backend.predict import predecir
from backend.constants import (
    IFOREST_MODEL_PATHS,
    OCSVM_MODEL_PATH,
    KMEANS_MODEL_PATHS,
    AUTOENCODER_MODEL_PATH,
    KMEANS_TXT_PATH
)
import metricas


def show_compare_page():
    """Página principal de comparación de modelos."""

    t = get_current_theme()
    c = t.colors

    # URL de imagen estática (servida por Streamlit static serving)
    img5_url = "app/static/img5.jpg"

    # ==================== HEADER ====================
    st.markdown(f"""
    <style>
        .compare-hero {{
            position: relative;
            padding: 2.5rem 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 1.5rem;
            overflow: hidden;
            background: url('{img5_url}') center center / cover no-repeat;
        }}
        .compare-hero::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: {c.hero_overlay};
            border-radius: 15px;
            z-index: 1;
        }}
        .compare-hero-content {{
            position: relative;
            z-index: 2;
        }}
    </style>
    <div class="compare-hero">
        <div class="compare-hero-content">
            <h1 style="margin: 0 0 0.5rem 0; color: {c.hero_title}; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">📊 Comparar Modelos</h1>
            <p style="margin: 0; font-size: 1.1rem; color: {c.hero_subtitle}; text-shadow: 0 1px 5px rgba(0,0,0,0.3);">
                Ejecuta varios modelos de IA sobre el mismo dataset y compara su rendimiento lado a lado
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==================== ¿QUÉ ES Y PARA QUÉ SIRVE? ====================
    with st.expander("💡 ¿Qué es esta página y cómo funciona?", expanded=False):
        st.markdown(f"""
        <div style="line-height: 1.8; font-size: 0.95rem;">

        <h4 style="color: {c.heading_secondary}; margin-top: 0;">🎯 ¿Para qué sirve?</h4>
        <p>Esta herramienta te permite <strong>evaluar y comparar</strong> el rendimiento de los distintos modelos de detección de intrusos
        que tiene el sistema. Así puedes determinar <strong>cuál modelo es más efectivo</strong> para detectar amenazas en tu red IoT.</p>

        <h4 style="color: {c.heading_secondary};">📋 ¿Cómo funciona? (3 pasos)</h4>
        <table style="width: 100%; border-collapse: separate; border-spacing: 0 8px; table-layout: fixed;">
            <tr>
                <td style="background: rgba(16,185,129,0.1); padding: 12px; border-radius: 8px; text-align: center; width: 33%;">
                    <strong style="font-size: 1.5rem;">1️⃣</strong><br/>
                    <strong style="color: {c.success};">Cargar datos</strong><br/>
                    <span style="font-size: 0.85rem;">Usa tu última captura de red o sube un CSV con tráfico de red</span>
                </td>
                <td style="background: rgba(19,131,167,0.1); padding: 12px; border-radius: 8px; text-align: center; width: 33%;">
                    <strong style="font-size: 1.5rem;">2️⃣</strong><br/>
                    <strong style="color: {c.heading_secondary};">Seleccionar modelos</strong><br/>
                    <span style="font-size: 0.85rem;">Elige 2 o más modelos de IA para comparar sus resultados</span>
                </td>
                <td style="background: rgba(245,158,11,0.1); padding: 12px; border-radius: 8px; text-align: center; width: 33%;">
                    <strong style="font-size: 1.5rem;">3️⃣</strong><br/>
                    <strong style="color: {c.warning};">Analizar resultados</strong><br/>
                    <span style="font-size: 0.85rem;">Revisa gráficas, métricas y recomendaciones automáticas</span>
                </td>
            </tr>
        </table>

        <h4 style="color: {c.heading_secondary}; margin-top: 1rem;">📊 Tipos de métricas disponibles</h4>
        <ul>
            <li><strong style="color: {c.heading_secondary};">Internas</strong> — Evalúan la calidad de los clusters sin datos de referencia
            (Silhouette, Calinski-Harabasz, Davies-Bouldin). Útil cuando <em>no tienes etiquetas reales</em>.</li>
            <li><strong style="color: {c.heading_secondary};">Externas</strong> — Comparan las predicciones contra etiquetas reales conocidas
            (Matriz de confusión, ROC AUC). Útil cuando <em>sí sabes cuáles son ataques reales</em>.</li>
            <li><strong style="color: {c.heading_secondary};">Ninguna</strong> — Solo muestra conteos de detección y tiempos de ejecución.</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ==================== CONFIGURACIÓN ====================
    st.markdown(f"""
    <h3 style="color: {c.heading_primary}; margin: 0 0 1rem 0;">⚙️ Configuración del análisis</h3>
    """, unsafe_allow_html=True)

    # Origen de datos
    data_source = _select_data_source()

    st.markdown("")

    # Selección de modelos y métricas en 2 columnas
    cfg_col1, cfg_col2 = st.columns([3, 2], gap="large")

    with cfg_col1:
        selected_models = st.multiselect(
            '🤖 Modelos a comparar',
            ['IForest', 'OCSVM', 'KMEANS', 'AUTOENCODER'],
            default=['IForest', 'OCSVM', 'KMEANS'],
            help='Selecciona 2 o más modelos para una comparación efectiva.'
        )

        # Info sobre los modelos seleccionados
        if selected_models:
            model_descriptions = {
                'IForest': '🌲 **IForest** — Aísla anomalías con árboles aleatorios.',
                'OCSVM': '🔵 **OCSVM** — Frontera alrededor del tráfico normal.',
                'KMEANS': '🟠 **KMEANS** — Agrupa tráfico por similitud.',
                'AUTOENCODER': '🔴 **Autoencoder** — Red neuronal multiclase.',
            }
            desc_text = " | ".join([model_descriptions.get(m, m) for m in selected_models])
            st.caption(desc_text)

    with cfg_col2:
        metric_compare = st.selectbox(
            '📏 Métricas de validación',
            ['Internas', 'Externas', 'Ninguna'],
            help='Internas: evalúan calidad de clusters. Externas: requieren etiquetas reales.'
        )

        true_label_col = None
        if metric_compare == 'Externas':
            if data_source is not None:
                posibles = data_source.columns.tolist()
                true_label_col = st.selectbox(
                    '🏷️ Columna de etiquetas reales',
                    posibles,
                    help='Selecciona la columna que contiene las clasificaciones reales (0=Normal, 1=Ataque).'
                )
            else:
                st.info('�� Carga datos con etiquetas reales para métricas externas.')

    # Validación visual
    st.markdown("")
    if len(selected_models) < 2:
        st.warning('⚠️ Selecciona al menos **2 modelos** para realizar una comparación significativa.')

    # Botón de comparación
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        comparar = st.button(
            '🚀 Ejecutar Comparación',
            use_container_width=True,
            type="primary",
            disabled=(data_source is None or len(selected_models) < 1)
        )

    if comparar:
        _run_comparison(data_source, selected_models, metric_compare, true_label_col)


def _select_data_source():
    """Seleccionar origen de datos (captura o CSV)."""
    t = get_current_theme()
    c = t.colors
    src_col1, src_col2 = st.columns(2, gap="medium")
    data_source = None

    has_capture = 'data' in st.session_state and st.session_state.data is not None

    with src_col1:
        st.markdown(f"""
        <div style="background: rgba(16,185,129,0.06); padding: 0.8rem 1rem; border-radius: 10px;
                    border: 1px solid rgba(16,185,129,0.15); margin-bottom: 0.5rem;">
            <p style="margin: 0; font-size: 0.9rem; color: rgba(240,250,254,0.6);">
                📡 <strong style="color: {c.success};">Última captura de red</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        if has_capture:
            usar_captura = st.checkbox('Usar datos de la última captura', value=True)
            if usar_captura:
                data_source = st.session_state.data.copy()
                n_rows = len(data_source)
                st.caption(f"✅ {n_rows:,} registros disponibles")
        else:
            st.caption("⚪ No hay captura disponible. Ve al Panel de Control para capturar tráfico.")

    with src_col2:
        st.markdown(f"""
        <div style="background: rgba(19,131,167,0.06); padding: 0.8rem 1rem; border-radius: 10px;
                    border: 1px solid rgba(19,131,167,0.15); margin-bottom: 0.5rem;">
            <p style="margin: 0; font-size: 0.9rem; color: rgba(240,250,254,0.6);">
                📄 <strong style="color: {c.heading_secondary};">Subir archivo CSV</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        if data_source is None:
            uploaded_cmp = st.file_uploader('Cargar CSV para comparar', type='csv', key='csv_compare', label_visibility='collapsed')
            if uploaded_cmp is not None:
                data_source = pd.read_csv(uploaded_cmp)
                st.caption(f"✅ {len(data_source):,} registros cargados desde CSV")
        else:
            st.caption("⚪ Usando datos de captura (desmarca arriba para subir CSV)")

    if data_source is None:
        st.info('📂 Carga un archivo CSV o realiza una captura en el Panel de Control para comenzar.')

    return data_source


def _prep_df(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocesar DataFrame para predicción."""
    lista = ['ip_ttl', 'tos', 'ip_flags_rb', 'ip_flags_df', 'ip_flags_mf']
    df = df.copy()
    if set(lista).issubset(set(df.columns)):
        df[lista] = df[lista].astype('str')
        df.ip_ttl = df.ip_ttl.str.replace(',', '.')
        df.tos = df.tos.str.replace(',', '.')
        df.ip_flags_rb = df.ip_flags_rb.str_replace(',', '.') if hasattr(df.ip_flags_rb, 'str_replace') else df.ip_flags_rb.str.replace(',', '.')
        df.ip_flags_df = df.ip_flags_df.str.replace(',', '.')
        df.ip_flags_mf = df.ip_flags_mf.str.replace(',', '.')
    return df.replace('', np.nan).fillna(0)


def _load_model_path(opt: str):
    """Obtener ruta del modelo según opción."""
    return {
        'IForest': IFOREST_MODEL_PATHS,
        'OCSVM': OCSVM_MODEL_PATH,
        'KMEANS': KMEANS_MODEL_PATHS,
        'AUTOENCODER': AUTOENCODER_MODEL_PATH,
    }.get(opt)


def _predict(opt: str, model, df: pd.DataFrame):
    """Ejecutar predicción según tipo de modelo."""
    try:
        if opt == 'IForest':
            scores = model.decision_function(df)
            y = pred_threshold(scores, -0.10)['Pred'].values
            pp3 = model[0].transform(df)
        elif opt == 'OCSVM':
            scores = model.decision_function(df)
            thr = np.percentile(scores, 100 * 0.45)
            y = np.where(scores >= thr, 0, 1)
            pp3 = model[0].transform(df)
        elif opt == 'KMEANS':
            y = model.predict(df)
            pp3 = model[0].transform(df)
        elif opt == 'AUTOENCODER':
            y = model.predict(df)
            pp3 = model[0].transform(df)
        else:
            return None, None
        return pp3, y
    except Exception:
        return None, None


def _counts(opt: str, y):
    """Contar predicciones por categoría."""
    if y is None:
        return {'Normal': 0, 'Anómalo': 0, 'DDOS_TCP': 0, 'DDOS_UDP': 0, 'Reconnaissance': 0}

    if opt in ['KMEANS']:
        path2 = KMEANS_TXT_PATH
        mapping = dict_predict(path2)
        etiquetas = [mapping.get(int(c), 'Desconocido') for c in y]
        c = Counter(etiquetas)
        return {
            'Normal': int(c.get('Normal', 0)),
            'Anómalo': int(c.get('Anómalo', 0)),
            'DDOS_TCP': int(c.get('DDoS_TCP', 0)),
            'DDOS_UDP': int(c.get('DDoS_UDP', 0)),
            'Reconnaissance': int(c.get('Reconnaissance', 0)),
        }

    if opt == 'AUTOENCODER':
        return {
            'Normal': int(np.count_nonzero(y == 0)),
            'Anómalo': 0,
            'DDOS_TCP': int(np.count_nonzero(y == 1)),
            'DDOS_UDP': int(np.count_nonzero(y == 3)),
            'Reconnaissance': int(np.count_nonzero(y == 2)),
        }

    normales = int((y == 0).sum())
    anomalos = int((y == 1).sum())
    return {'Normal': normales, 'Anómalo': anomalos, 'DDOS_TCP': 0, 'DDOS_UDP': 0, 'Reconnaissance': 0}


def _run_comparison(data_source, selected_models, metric_compare, true_label_col):
    """Ejecutar comparación de modelos."""
    if data_source is None:
        st.warning('⚠ Cargue datos o use la última captura antes de comparar.')
        return

    dfp = _prep_df(data_source)
    y_true = None
    if metric_compare == 'Externas' and true_label_col is not None and true_label_col in data_source.columns:
        y_true = data_source[true_label_col].values

    filas = []
    progress_bar = st.progress(0, text="Ejecutando modelos...")

    for i, opt in enumerate(selected_models):
        progress_bar.progress((i) / len(selected_models), text=f"🔄 Analizando modelo **{opt}**...")

        path = _load_model_path(opt)
        if path is None:
            st.error(f'Ruta no definida para {opt}')
            continue

        model = load_model(path)
        if model is None:
            st.error(f'No se pudo cargar el modelo {opt}')
            continue

        t0 = time.time()
        pp3, y = _predict(opt, model, dfp)
        pred_time = time.time() - t0
        conteos = _counts(opt, y)
        fila = {'Modelo': opt, **conteos, 'Tiempo (s)': round(float(pred_time), 4)}

        # Métricas internas
        if metric_compare == 'Internas':
            if y is not None and len(np.unique(y)) >= 2:
                try:
                    s, c, d = metricas.metrica_internas(pd.DataFrame(pp3), y)
                    fila.update({'Silhouette': round(float(s), 4), 'Calinski': round(float(c), 2), 'Davies': round(float(d), 4)})
                except Exception as e:
                    st.warning(f"No se pudieron calcular métricas internas para {opt}: {str(e)}")
                    fila.update({'Silhouette': None, 'Calinski': None, 'Davies': None})
            else:
                st.info(f"Métricas internas no disponibles para {opt} (requiere ≥2 clases)")
                fila.update({'Silhouette': None, 'Calinski': None, 'Davies': None})

        # Métricas externas
        if metric_compare == 'Externas' and y_true is not None and y is not None and len(y_true) == len(y):
            try:
                from sklearn.metrics import confusion_matrix, roc_auc_score

                y_bin = None
                if opt in ['KMEANS']:
                    path2 = KMEANS_TXT_PATH
                    mapping = dict_predict(path2)
                    etiquetas = np.array([mapping.get(int(c), 'Desconocido') for c in y])
                    y_bin = (etiquetas != 'Normal').astype(int)
                elif opt == 'AUTOENCODER':
                    y_bin = (y != 0).astype(int)
                else:
                    y_bin = y.astype(int)

                cm = confusion_matrix(y_true, y_bin)
                fila.update({'MatrizConfusion': cm})

                if np.unique(y_true).size == 2 and np.unique(y_bin).size == 2:
                    try:
                        aucv = roc_auc_score(y_true, y_bin)
                        fila.update({'ROC_AUC': round(float(aucv), 4)})
                    except Exception:
                        pass
            except Exception:
                pass

        filas.append(fila)

    progress_bar.progress(1.0, text="✅ Análisis completado")
    time.sleep(0.5)
    progress_bar.empty()

    if not filas:
        st.info('Sin resultados para mostrar.')
        return

    _display_results(filas, metric_compare)


def _generate_normal_vs_attacks_insight(res_df, normales, ataques):
    """Generar explicación inteligente para la gráfica Normal vs Ataques."""
    t = get_current_theme()
    c = t.colors
    insights = []

    for i, modelo in enumerate(res_df['Modelo'].values):
        n = normales[i]
        a = ataques[i]
        t = n + a
        if t == 0:
            continue

        pct_ataque = (a / t) * 100

        if pct_ataque == 0:
            estado = "🟢"
            color = c.success
            msg = f"no detectó amenazas. Todo el tráfico fue clasificado como normal."
        elif pct_ataque < 5:
            estado = "🟢"
            color = c.success
            msg = f"detectó un nivel mínimo de anomalías ({pct_ataque:.1f}%). La red se encuentra en buen estado."
        elif pct_ataque < 20:
            estado = "🟡"
            color = c.warning
            msg = f"detectó un {pct_ataque:.1f}% de tráfico anómalo. Se recomienda revisar los patrones detectados."
        elif pct_ataque < 50:
            estado = "🟠"
            color = c.warning_dark
            msg = f"detectó un {pct_ataque:.1f}% de posibles ataques. Se requiere atención inmediata."
        else:
            estado = "🔴"
            color = c.error
            msg = f"clasificó el {pct_ataque:.1f}% del tráfico como ataques. Situación crítica que requiere acción urgente."

        insights.append(f'<p style="margin: 4px 0;"><strong style="color: {color};">{estado} {modelo}</strong>: {msg} '
                        f'<span style="color: rgba(240,250,254,0.5);">({int(n):,} normales / {int(a):,} ataques)</span></p>')

    # Análisis de consenso entre modelos
    if len(res_df) >= 2:
        pcts = [(ataques[i] / (normales[i] + ataques[i])) * 100 if (normales[i] + ataques[i]) > 0 else 0
                for i in range(len(res_df))]
        avg_pct = np.mean(pcts)
        std_pct = np.std(pcts)

        if std_pct < 5:
            consenso = f'<p style="margin: 8px 0 0 0;"><strong style="color: {c.heading_secondary};">📊 Consenso:</strong> Los modelos <strong>coinciden</strong> en sus detecciones (desviación del {std_pct:.1f}%). Promedio de ataques: {avg_pct:.1f}%.</p>'
        elif std_pct < 15:
            consenso = f'<p style="margin: 8px 0 0 0;"><strong style="color: {c.warning};">📊 Consenso parcial:</strong> Los modelos muestran diferencias moderadas (desviación del {std_pct:.1f}%). Promedio de ataques: {avg_pct:.1f}%. Considera usar el modelo más conservador.</p>'
        else:
            consenso = f'<p style="margin: 8px 0 0 0;"><strong style="color: {c.error};">📊 Sin consenso:</strong> Los modelos difieren significativamente (desviación del {std_pct:.1f}%). Promedio de ataques: {avg_pct:.1f}%. Se recomienda análisis más profundo.</p>'
        insights.append(consenso)

    return "\n".join(insights)


def _generate_time_insight(res_df):
    """Generar explicación inteligente para la gráfica de tiempos."""
    t = get_current_theme()
    c = t.colors
    if 'Tiempo (s)' not in res_df.columns or len(res_df) == 0:
        return ""

    tiempos = res_df[['Modelo', 'Tiempo (s)']].copy()
    fastest = tiempos.loc[tiempos['Tiempo (s)'].idxmin()]
    slowest = tiempos.loc[tiempos['Tiempo (s)'].idxmax()]

    insights = []

    insights.append(f'<p style="margin: 4px 0;"><strong style="color: {c.success};">⚡ Más rápido:</strong> '
                    f'<strong>{fastest["Modelo"]}</strong> con {fastest["Tiempo (s)"]:.4f} segundos.</p>')

    if len(res_df) > 1:
        insights.append(f'<p style="margin: 4px 0;"><strong style="color: {c.warning};">🐢 Más lento:</strong> '
                        f'<strong>{slowest["Modelo"]}</strong> con {slowest["Tiempo (s)"]:.4f} segundos.</p>')

        if fastest["Tiempo (s)"] > 0:
            factor = slowest["Tiempo (s)"] / fastest["Tiempo (s)"]
            insights.append(f'<p style="margin: 4px 0;"><strong style="color: {c.heading_secondary};">�� Diferencia:</strong> '
                            f'{fastest["Modelo"]} es <strong>{factor:.1f}x más rápido</strong> que {slowest["Modelo"]}.</p>')

    avg_time = tiempos['Tiempo (s)'].mean()
    if avg_time < 1:
        rec = "Todos los modelos son suficientemente rápidos para análisis en tiempo real."
        rec_color = c.success
    elif avg_time < 5:
        rec = "Los tiempos son aceptables para análisis periódico. Para tiempo real, prefiere los modelos más rápidos."
        rec_color = c.warning
    else:
        rec = "Los tiempos son elevados. Considera reducir el volumen de datos o usar solo los modelos más rápidos."
        rec_color = c.error

    insights.append(f'<p style="margin: 8px 0 0 0;"><strong style="color: {rec_color};">💡 Recomendación:</strong> {rec}</p>')

    return "\n".join(insights)


def _display_results(filas, metric_compare):
    """Mostrar resultados de la comparación."""
    t = get_current_theme()
    c = t.colors
    res_df = pd.DataFrame(filas)

    st.markdown("---")
    st.markdown(f"""
    <h2 style="text-align: center; color: {c.heading_primary}; margin: 1rem 0 1.5rem 0;">
        📈 Resultados del Análisis
    </h2>
    """, unsafe_allow_html=True)

    # ==================== MÉTRICAS RÁPIDAS (KPIs) ====================
    total_paquetes = int(res_df['Normal'].fillna(0).sum() + res_df['Anómalo'].fillna(0).sum() +
                         res_df['DDOS_TCP'].fillna(0).sum() + res_df['DDOS_UDP'].fillna(0).sum() +
                         res_df['Reconnaissance'].fillna(0).sum())
    num_modelos = len(res_df)
    avg_time = res_df['Tiempo (s)'].mean() if 'Tiempo (s)' in res_df.columns else 0

    normales_total = res_df['Normal'].fillna(0).sum()
    ataques_total = total_paquetes - normales_total
    pct_ataques = (ataques_total / total_paquetes * 100) if total_paquetes > 0 else 0

    kpi_cols = st.columns(4, gap="medium")
    with kpi_cols[0]:
        st.metric("🤖 Modelos evaluados", f"{num_modelos}")
    with kpi_cols[1]:
        st.metric("📦 Predicciones totales", f"{total_paquetes // num_modelos:,}" if num_modelos > 0 else "0")
    with kpi_cols[2]:
        delta_color = "normal" if pct_ataques < 10 else "inverse"
        st.metric("🚨 Amenazas (promedio)", f"{pct_ataques:.1f}%",
                   delta=f"{'Bajo' if pct_ataques < 10 else 'Medio' if pct_ataques < 30 else 'Alto'} riesgo",
                   delta_color=delta_color)
    with kpi_cols[3]:
        st.metric("⏱️ Tiempo promedio", f"{avg_time:.3f}s")

    st.markdown("")

    # ==================== TABLA RESUMEN ====================
    st.markdown(f"""
    <div style="background: rgba(19,131,167,0.06); padding: 1rem 1.2rem; border-radius: 12px;
                border: 1px solid rgba(19,131,167,0.15); margin-bottom: 0.5rem;">
        <h3 style="margin: 0 0 0.3rem 0; color: {c.heading_primary}; font-size: 1.1rem;">📋 Tabla comparativa detallada</h3>
        <p style="margin: 0; font-size: 0.85rem; color: rgba(240,250,254,0.5);">
            Cada fila muestra cuántos paquetes clasificó cada modelo como Normal, Anómalo o tipo de ataque específico.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cols = ['Modelo', 'Normal', 'Anómalo', 'DDOS_TCP', 'DDOS_UDP', 'Reconnaissance', 'Tiempo (s)']

    if metric_compare == 'Internas':
        for col in ['Silhouette', 'Calinski', 'Davies']:
            if col in res_df.columns:
                cols.append(col)

    if metric_compare == 'Externas':
        if 'ROC_AUC' in res_df.columns:
            cols.append('ROC_AUC')

    cols_disponibles = [c for c in cols if c in res_df.columns]
    st.dataframe(res_df[cols_disponibles], use_container_width=True, hide_index=True)

    # Explicación de métricas internas
    if metric_compare == 'Internas' and any(c in res_df.columns for c in ['Silhouette', 'Calinski', 'Davies']):
        with st.expander("📖 ¿Qué significan estas métricas?"):
            st.markdown(f"""
            | Métrica | Qué mide | Valor ideal |
            |---------|----------|-------------|
            | **Silhouette** | Qué tan bien separados están los grupos (clusters). | Cercano a **1.0** (mejor) |
            | **Calinski-Harabasz** | Relación entre la dispersión entre clusters y dentro de clusters. | **Mayor es mejor** |
            | **Davies-Bouldin** | Similitud promedio entre clusters. | Cercano a **0** (mejor) |

            **En resumen:** Un buen modelo tiene Silhouette alto, Calinski alto y Davies bajo.
            """)

    st.markdown("")

    # ==================== MATRICES DE CONFUSIÓN ====================
    if metric_compare == 'Externas':
        has_cm = any('MatrizConfusion' in f and f['MatrizConfusion'] is not None for f in filas)
        if has_cm:
            st.markdown(f"""
            <div style="background: rgba(245,158,11,0.06); padding: 1rem 1.2rem; border-radius: 12px;
                        border: 1px solid rgba(245,158,11,0.15); margin-bottom: 0.5rem;">
                <h3 style="margin: 0 0 0.3rem 0; color: {c.heading_primary}; font-size: 1.1rem;">🧮 Matrices de Confusión</h3>
                <p style="margin: 0; font-size: 0.85rem; color: rgba(240,250,254,0.5);">
                    Comparan las predicciones del modelo vs las etiquetas reales. La diagonal principal (↘) muestra aciertos.
                </p>
            </div>
            """, unsafe_allow_html=True)

            cm_cols = st.columns(len(filas), gap="medium")
            for idx, fila in enumerate(filas):
                if 'MatrizConfusion' in fila and fila['MatrizConfusion'] is not None:
                    with cm_cols[idx]:
                        st.markdown(f"**{fila['Modelo']}**")
                        cm_df = pd.DataFrame(
                            fila['MatrizConfusion'],
                            columns=['Pred: Normal', 'Pred: Ataque'],
                            index=['Real: Normal', 'Real: Ataque']
                        )
                        st.dataframe(cm_df, use_container_width=True)
            st.markdown("")

    # ==================== GRÁFICAS LADO A LADO ====================
    chart_col1, chart_col2 = st.columns(2, gap="large")

    # --- Gráfico Normal vs Ataques ---
    with chart_col1:
        st.markdown(f"""
        <div style="background: rgba(19,131,167,0.06); padding: 1rem 1.2rem; border-radius: 12px;
                    border: 1px solid rgba(19,131,167,0.15); margin-bottom: 0.5rem;">
            <h3 style="margin: 0 0 0.3rem 0; color: {c.heading_primary}; font-size: 1.1rem;">📊 Normal vs Ataques</h3>
            <p style="margin: 0; font-size: 0.85rem; color: rgba(240,250,254,0.5);">
                Cuántos paquetes clasificó cada modelo como tráfico legítimo vs amenazas detectadas.
            </p>
        </div>
        """, unsafe_allow_html=True)

        modelos = res_df['Modelo'].values
        normales = res_df['Normal'].fillna(0).values

        ataques = np.zeros(len(res_df))
        for col in ['Anómalo', 'DDOS_TCP', 'DDOS_UDP', 'Reconnaissance']:
            if col in res_df.columns:
                ataques += res_df[col].fillna(0).values

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Normal', x=modelos, y=normales,
            marker_color=c.success,
            text=[f'{int(v):,}' for v in normales],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            name='Ataques', x=modelos, y=ataques,
            marker_color=c.error,
            text=[f'{int(v):,}' for v in ataques],
            textposition='auto'
        ))
        fig.update_layout(
            barmode='group',
            xaxis_title='Modelo',
            yaxis_title='Paquetes',
            template='plotly_dark',
            height=400,
            margin=dict(t=20, b=40, l=50, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)

        # Insight inteligente
        insight_nva = _generate_normal_vs_attacks_insight(res_df, normales, ataques)
        if insight_nva:
            st.markdown(f"""
            <div style="background: rgba(19,131,167,0.05); padding: 0.8rem 1rem; border-radius: 10px;
                        border-left: 3px solid {c.primary}; font-size: 0.88rem; line-height: 1.6;
                        overflow-wrap: break-word; word-break: break-word; max-width: 100%; box-sizing: border-box;">
                <strong style="color: {c.heading_secondary};">🔍 Análisis automático:</strong><br/>
                {insight_nva}
            </div>
            """, unsafe_allow_html=True)

    # --- Gráfico de Tiempos ---
    with chart_col2:
        st.markdown(f"""
        <div style="background: rgba(19,131,167,0.06); padding: 1rem 1.2rem; border-radius: 12px;
                    border: 1px solid rgba(19,131,167,0.15); margin-bottom: 0.5rem;">
            <h3 style="margin: 0 0 0.3rem 0; color: {c.heading_primary}; font-size: 1.1rem;">⏱️ Tiempos de predicción</h3>
            <p style="margin: 0; font-size: 0.85rem; color: rgba(240,250,254,0.5);">
                Cuánto tardó cada modelo en analizar todos los paquetes. Menor es mejor.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if 'Tiempo (s)' in res_df.columns:
            tiempos = res_df['Tiempo (s)'].values
            max_t = max(tiempos) if max(tiempos) > 0 else 1
            colors = []
            for t in tiempos:
                ratio = t / max_t
                if ratio < 0.4:
                    colors.append(c.success)
                elif ratio < 0.7:
                    colors.append(c.warning)
                else:
                    colors.append(c.error)

            figt = go.Figure(data=[go.Bar(
                x=res_df['Modelo'], y=res_df['Tiempo (s)'],
                marker_color=colors,
                text=[f'{v:.4f}s' for v in tiempos],
                textposition='auto'
            )])
            figt.update_layout(
                xaxis_title='Modelo',
                yaxis_title='Segundos',
                template='plotly_dark',
                height=400,
                margin=dict(t=20, b=40, l=50, r=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(figt, use_container_width=True)

            # Insight inteligente
            insight_time = _generate_time_insight(res_df)
            if insight_time:
                st.markdown(f"""
                <div style="background: rgba(19,131,167,0.05); padding: 0.8rem 1rem; border-radius: 10px;
                            border-left: 3px solid {c.primary}; font-size: 0.88rem; line-height: 1.6;
                            overflow-wrap: break-word; word-break: break-word; max-width: 100%; box-sizing: border-box;">
                    <strong style="color: {c.heading_secondary};">🔍 Análisis automático:</strong><br/>
                    {insight_time}
                </div>
                """, unsafe_allow_html=True)

    # ==================== DESGLOSE DE ATAQUES ====================
    attack_cols = ['DDOS_TCP', 'DDOS_UDP', 'Reconnaissance']
    has_attack_detail = any(res_df[col].fillna(0).sum() > 0 for col in attack_cols if col in res_df.columns)

    if has_attack_detail:
        st.markdown("")
        st.markdown(f"""
        <div style="background: rgba(239,68,68,0.06); padding: 1rem 1.2rem; border-radius: 12px;
                    border: 1px solid rgba(239,68,68,0.15); margin-bottom: 0.5rem;">
            <h3 style="margin: 0 0 0.3rem 0; color: {c.heading_primary}; font-size: 1.1rem;">🎯 Desglose por tipo de ataque</h3>
            <p style="margin: 0; font-size: 0.85rem; color: rgba(240,250,254,0.5);">
                Detalle de los tipos de ataques detectados por los modelos multiclase (KMEANS y Autoencoder).
            </p>
        </div>
        """, unsafe_allow_html=True)

        fig_detail = go.Figure()
        attack_colors = {'DDOS_TCP': c.error, 'DDOS_UDP': c.warning, 'Reconnaissance': c.primary}
        attack_labels = {'DDOS_TCP': 'DDoS TCP', 'DDOS_UDP': 'DDoS UDP', 'Reconnaissance': 'Reconnaissance'}

        for col in attack_cols:
            if col in res_df.columns and res_df[col].fillna(0).sum() > 0:
                fig_detail.add_trace(go.Bar(
                    name=attack_labels.get(col, col),
                    x=res_df['Modelo'], y=res_df[col].fillna(0),
                    marker_color=attack_colors.get(col, c.primary),
                    text=[f'{int(v):,}' for v in res_df[col].fillna(0).values],
                    textposition='auto'
                ))

        fig_detail.update_layout(
            barmode='group',
            xaxis_title='Modelo',
            yaxis_title='Paquetes detectados',
            template='plotly_dark',
            height=350,
            margin=dict(t=20, b=40, l=50, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_detail, use_container_width=True)

        # Insight de ataques
        dominant_attack = None
        max_attack_count = 0
        for col in attack_cols:
            if col in res_df.columns:
                total_col = res_df[col].fillna(0).sum()
                if total_col > max_attack_count:
                    max_attack_count = total_col
                    dominant_attack = attack_labels.get(col, col)

        if dominant_attack and max_attack_count > 0:
            attack_count_str = f"{int(max_attack_count):,}"
            attack_recommendation = 'Revisa las reglas de firewall para mitigar este tipo de ataque.' if max_attack_count > 10 else 'Nivel bajo, mantén monitoreo regular.'
            st.markdown(f"""
            <div style="background: rgba(239,68,68,0.05); padding: 0.8rem 1rem; border-radius: 10px;
                        border-left: 3px solid {c.error}; font-size: 0.88rem; line-height: 1.6;
                        overflow-wrap: break-word; word-break: break-word; max-width: 100%; box-sizing: border-box;">
                <strong style="color: {c.error};">⚠️ Ataque predominante:</strong>
                <strong>{dominant_attack}</strong> con {attack_count_str} detecciones totales.
                {attack_recommendation}
            </div>
            """, unsafe_allow_html=True)
