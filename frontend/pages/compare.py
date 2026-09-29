"""
Página de comparación de modelos.
Permite ejecutar múltiples modelos sobre el mismo dataset y comparar resultados.
"""

import sys
import os
# Agregar ruta raíz al PYTHONPATH para acceder a metricas.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import streamlit as st
from config.theme import get_current_theme
from config.i18n import t
from pathlib import Path
import base64
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from collections import Counter

from backend.model_utils import load_model, dict_predict
from backend.predict import predecir
from backend.notifications import (
    ALERT_ATTACK_THRESHOLD,
    ALERT_SUSPICIOUS_THRESHOLD,
    get_alert_level_from_anomaly_percentage,
)
from backend.constants import (
    KMEANS_TXT_PATH,
    MODEL_PATHS,
    MODEL_TYPE_BY_ID,
    SUPERVISED_MODEL_PATHS,
    UNSUPERVISED_MODEL_PATHS,
)
import metricas


def show_compare_page():
    """Página principal de comparación de modelos."""

    theme = get_current_theme()
    c = theme.colors

    # helper base64
    # subir un nivel extra para llegar al directorio de la raíz donde está
    # la carpeta `img` (frontend/pages -> frontend -> raíz)
    img_dir = Path(__file__).parent.parent.parent / "img"
    def _b64(fname):
        p = img_dir / fname
        if not p.exists():
            return None
        ext = p.suffix.lstrip('.')
        data = base64.b64encode(p.read_bytes()).decode()
        return f"data:image/{ext};base64,{data}"

    img5_b64 = _b64("img5.jpg") or ""

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
            background: url('{img5_b64}') center center / cover no-repeat;
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
            <h1 style="margin: 0 0 0.5rem 0; color: {c.hero_title}; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">{t('compare_models')}</h1>
            <p style="margin: 0; font-size: 1.1rem; color: {c.hero_subtitle}; text-shadow: 0 1px 5px rgba(0,0,0,0.3);">
                {t('compare_subtitle')}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==================== ¿QUÉ ES Y PARA QUÉ SIRVE? ====================
    with st.expander(t("compare_help_title"), expanded=False):
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
            <li><strong style="color: {c.heading_secondary};">No supervisados → Internas</strong> — Evalúan la calidad de clusters sin etiquetas
            (Silhouette, Calinski-Harabasz, Davies-Bouldin).</li>
            <li><strong style="color: {c.heading_secondary};">Supervisados → Externas</strong> — Comparan contra etiquetas reales
            (Matriz de confusión, Accuracy, Precision, Recall, F1, ROC AUC).</li>
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
        model_options = list(UNSUPERVISED_MODEL_PATHS.keys()) + list(SUPERVISED_MODEL_PATHS.keys())
        default_models = ['IForest', 'OCSVM', 'KMEANS']

        def _fmt_model(opt):
            model_group = MODEL_TYPE_BY_ID.get(opt, "No supervisados")
            return f"{model_group} | {opt}"

        selected_models = st.multiselect(
            t('models_to_compare'),
            model_options,
            default=default_models,
            format_func=_fmt_model,
            help=t('models_to_compare_help')
        )

        # Info sobre los modelos seleccionados
        if selected_models:
            model_descriptions = {
                'IForest': '🌲 **IForest** — Aísla anomalías con árboles aleatorios.',
                'OCSVM': '🔵 **OCSVM** — Frontera alrededor del tráfico normal.',
                'KMEANS': '🟠 **KMEANS** — Agrupa tráfico por similitud.',
                'AUTOENCODER': '🔴 **Autoencoder** — Red neuronal multiclase.',
                'DecisionTree': '🌳 **Decision Tree** — Clasificador supervisado basado en reglas.',
                'ExtraTrees': '🌲 **Extra Trees** — Ensamble supervisado de árboles extremadamente aleatorios.',
                'RandomForest': '🌴 **Random Forest** — Ensamble supervisado robusto de árboles.',
            }
            desc_text = " | ".join([model_descriptions.get(m, m) for m in selected_models])
            st.caption(desc_text)

    with cfg_col2:
        selected_supervised = [m for m in selected_models if m in SUPERVISED_MODEL_PATHS]
        selected_unsupervised = [m for m in selected_models if m in UNSUPERVISED_MODEL_PATHS]
        st.markdown(f"**{t('automatic_metrics')}**")
        st.caption(f"{t('unsupervised')}: {t('internal_metrics')} ({len(selected_unsupervised)})")
        st.caption(f"{t('supervised')}: {t('external_metrics')} ({len(selected_supervised)})")

        if selected_supervised:
            if 'supervised_attack_threshold' not in st.session_state:
                st.session_state['supervised_attack_threshold'] = 0.70
            attack_thr = st.slider(
                t('attack_threshold'),
                min_value=0.05,
                max_value=0.95,
                value=float(st.session_state.get('supervised_attack_threshold', 0.70)),
                step=0.01,
                help=t('attack_threshold_help')
            )
            st.session_state['supervised_attack_threshold'] = float(attack_thr)
            st.caption(f"Umbral activo: {attack_thr:.2f}")

        true_label_col = None
        if selected_supervised:
            if data_source is not None:
                posibles = metricas.candidate_label_columns(data_source)
                if posibles:
                    true_label_col = st.selectbox(
                        t('real_labels_column'),
                        posibles,
                        help=t('real_labels_help')
                    )
                else:
                    st.info(t('no_valid_label_columns'))
            else:
                st.info(t('load_labeled_data'))

    # Validación visual
    st.markdown("")
    if len(selected_models) < 2:
        st.warning(t('select_two_models'))

    # Botón de comparación
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col2:
        comparar = st.button(
            t('run_comparison'),
            use_container_width=True,
            type="primary",
            disabled=(data_source is None or len(selected_models) < 1)
        )

    if comparar:
        _run_comparison(data_source, selected_models, true_label_col)


def _select_data_source():
    """Seleccionar origen de datos (captura o CSV)."""
    theme = get_current_theme()
    c = theme.colors
    src_col1, src_col2 = st.columns(2, gap="medium")
    data_source = None

    has_capture = 'data' in st.session_state and st.session_state.data is not None

    with src_col1:
        st.markdown(f"""
        <div style="background: rgba(16,185,129,0.06); padding: 0.8rem 1rem; border-radius: 10px;
                    border: 1px solid rgba(16,185,129,0.15); margin-bottom: 0.5rem;">
            <p style="margin: 0; font-size: 0.9rem; color: rgba(240,250,254,0.6);">
                {t('last_capture')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        if has_capture:
            usar_captura = st.checkbox(t('use_last_capture'), value=True)
            if usar_captura:
                data_source = st.session_state.data.copy()
                n_rows = len(data_source)
                st.caption(t('records_available', count=n_rows))
        else:
            st.caption(t('no_capture_available'))

    with src_col2:
        st.markdown(f"""
        <div style="background: rgba(19,131,167,0.06); padding: 0.8rem 1rem; border-radius: 10px;
                    border: 1px solid rgba(19,131,167,0.15); margin-bottom: 0.5rem;">
            <p style="margin: 0; font-size: 0.9rem; color: rgba(240,250,254,0.6);">
                {t('upload_csv')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        if data_source is None:
            uploaded_cmp = st.file_uploader(t('load_csv_compare'), type='csv', key='csv_compare', label_visibility='collapsed')
            if uploaded_cmp is not None:
                data_source = pd.read_csv(uploaded_cmp)
                st.caption(t('records_loaded_csv', count=len(data_source)))
        else:
            st.caption(t('using_capture_uncheck'))

    if data_source is None:
        st.info(t('load_csv_or_capture'))

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
    return MODEL_PATHS.get(opt)


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

    if opt in SUPERVISED_MODEL_PATHS:
        y_bin = metricas.to_binary_attack_labels(y)
        normales = int((y_bin == 0).sum())
        anomalos = int((y_bin == 1).sum())
        return {'Normal': normales, 'Anómalo': anomalos, 'DDOS_TCP': 0, 'DDOS_UDP': 0, 'Reconnaissance': 0}

    normales = int((y == 0).sum())
    anomalos = int((y == 1).sum())
    return {'Normal': normales, 'Anómalo': anomalos, 'DDOS_TCP': 0, 'DDOS_UDP': 0, 'Reconnaissance': 0}


def _run_comparison(data_source, selected_models, true_label_col):
    """Ejecutar comparación de modelos."""
    if data_source is None:
        st.warning(t('load_data_before_compare'))
        return

    y_true = None
    df_features = data_source.copy()
    if true_label_col is not None and true_label_col in df_features.columns:
        y_true = df_features[true_label_col].values
        df_features = df_features.drop(columns=[true_label_col], errors='ignore')

    dfp = _prep_df(df_features)

    filas = []
    progress_bar = st.progress(0, text=t('running_models'))

    for i, opt in enumerate(selected_models):
        progress_bar.progress((i) / len(selected_models), text=t('analyzing_model', model=opt))

        path = _load_model_path(opt)
        if path is None:
            st.error(t('model_path_missing', model=opt))
            continue

        model = load_model(path)
        if model is None:
            st.error(t('model_load_failed', model=opt))
            continue

        t0 = time.time()
        pp3, y, scores = predecir(model, dfp, opt)
        pred_time = time.time() - t0
        conteos = _counts(opt, y)
        fila = {'Modelo': opt, **conteos, 'Tiempo (s)': round(float(pred_time), 4)}
        model_type = MODEL_TYPE_BY_ID.get(opt, "No supervisados")
        fila['Tipo'] = model_type

        # Métricas internas para no supervisados.
        if model_type == 'No supervisados':
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

        # Métricas externas para supervisados.
        if model_type == 'Supervisados' and y_true is not None and y is not None and len(y_true) == len(y):
            try:
                if np.unique(metricas.to_binary_attack_labels(y_true)).size < 2:
                    st.info(f"{opt}: las etiquetas reales solo contienen una clase tras la normalización binaria; se omiten métricas externas.")
                else:
                    fila.update(metricas.metricas_externas(y_true, y, y_score=scores))
            except Exception as e:
                st.warning(f"No se pudieron calcular métricas externas para {opt}: {str(e)}")

        if model_type == 'Supervisados' and y_true is None:
            st.info(f"{opt}: sin columna de etiquetas reales; se omiten métricas externas.")

        filas.append(fila)

    progress_bar.progress(1.0, text=t('analysis_completed'))
    time.sleep(0.5)
    progress_bar.empty()

    if not filas:
        st.info(t('no_results'))
        return

    _display_results(filas)


def _generate_normal_vs_attacks_insight(res_df, normales, ataques):
    """Generar explicación inteligente para la gráfica Normal vs Ataques."""
    theme = get_current_theme()
    c = theme.colors
    insights = []

    for i, modelo in enumerate(res_df['Modelo'].values):
        n = normales[i]
        a = ataques[i]
        t = n + a
        if t == 0:
            continue

        pct_ataque = (a / t) * 100

        alert_level = get_alert_level_from_anomaly_percentage(pct_ataque)
        if alert_level == 'normal':
            estado = "🟢"
            color = c.success
            msg = (
                f"detectó un {pct_ataque:.1f}% de tráfico anómalo. "
                f"Este nivel está dentro del margen normal (<{ALERT_SUSPICIOUS_THRESHOLD:.0f}%)."
            )
        elif alert_level == 'suspicious':
            estado = "🟠"
            color = c.warning_dark
            msg = (
                f"detectó un {pct_ataque:.1f}% de posibles ataques. "
                f"Nivel sospechoso ({ALERT_SUSPICIOUS_THRESHOLD:.0f}% a {ALERT_ATTACK_THRESHOLD:.0f}%)."
            )
        else:
            estado = "🔴"
            color = c.error
            msg = (
                f"clasificó el {pct_ataque:.1f}% del tráfico como ataques. "
                f"Situación crítica (≥{ALERT_ATTACK_THRESHOLD:.0f}%) que requiere acción urgente."
            )

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
    theme = get_current_theme()
    c = theme.colors
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


def _display_results(filas):
    """Mostrar resultados de la comparación."""
    theme = get_current_theme()
    c = theme.colors
    res_df = pd.DataFrame(filas)

    # CSS crítico: prevenir que los resultados expandan la página horizontalmente
    st.markdown("""
    <style>
        /* Fix: prevenir resize loop en resultados de comparación */
        [data-testid="stMainBlockContainer"] {
            overflow-x: hidden !important;
            max-width: 100% !important;
        }
        [data-testid="stHorizontalBlock"] {
            overflow: hidden !important;
            max-width: 100% !important;
            flex-wrap: nowrap !important;
        }
        [data-testid="stColumn"] {
            overflow: hidden !important;
            min-width: 0 !important;
        }
        /* Plotly: forzar 100% del ancho de su columna con CSS puro */
        [data-testid="stPlotlyChart"] {
            width: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }
        [data-testid="stPlotlyChart"] > div {
            width: 100% !important;
            max-width: 100% !important;
        }
        [data-testid="stPlotlyChart"] > div > div {
            width: 100% !important;
            max-width: 100% !important;
        }
        .js-plotly-plot {
            width: 100% !important;
            max-width: 100% !important;
        }
        .plotly .main-svg {
            max-width: 100% !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <h2 style="text-align: center; color: {c.heading_primary}; margin: 1rem 0 1.5rem 0;">
        {t('analysis_results')}
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
        st.metric(t('evaluated_models'), f"{num_modelos}")
    with kpi_cols[1]:
        st.metric(t('total_predictions'), f"{total_paquetes // num_modelos:,}" if num_modelos > 0 else "0")
    with kpi_cols[2]:
        alert_level = get_alert_level_from_anomaly_percentage(pct_ataques)
        if alert_level == 'normal':
            delta_text = t('low_risk')
            delta_color = 'normal'
        elif alert_level == 'suspicious':
            delta_text = t('medium_risk')
            delta_color = 'off'
        else:
            delta_text = t('high_risk')
            delta_color = 'inverse'
        st.metric(t('average_threats'), f"{pct_ataques:.1f}%",
                   delta=delta_text,
                   delta_color=delta_color)
    with kpi_cols[3]:
        st.metric(t('average_time'), f"{avg_time:.3f}s")

    st.markdown("")

    # ==================== TABLA RESUMEN ====================
    st.markdown(f"""
    <div style="background: rgba(19,131,167,0.06); padding: 1rem 1.2rem; border-radius: 12px;
                border: 1px solid rgba(19,131,167,0.15); margin-bottom: 0.5rem;">
        <h3 style="margin: 0 0 0.3rem 0; color: {c.heading_primary}; font-size: 1.1rem;">{t('comparison_table')}</h3>
        <p style="margin: 0; font-size: 0.85rem; color: rgba(240,250,254,0.5);">
            {t('comparison_table_help')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    cols = ['Modelo', 'Normal', 'Anómalo', 'DDOS_TCP', 'DDOS_UDP', 'Reconnaissance', 'Tiempo (s)']

    if 'Tipo' in res_df.columns:
        cols.append('Tipo')
    for col in ['Silhouette', 'Calinski', 'Davies', 'Accuracy', 'Precision', 'Recall', 'F1', 'ROC_AUC']:
        if col in res_df.columns:
            cols.append(col)

    cols_disponibles = [c for c in cols if c in res_df.columns]
    st.dataframe(res_df[cols_disponibles], use_container_width=True, hide_index=True)

    # Explicación de métricas internas
    if any(c in res_df.columns for c in ['Silhouette', 'Calinski', 'Davies']):
        with st.expander(t('metric_meanings')):
            st.markdown(f"""
            | Métrica | Qué mide | Valor ideal |
            |---------|----------|-------------|
            | **Silhouette** | Qué tan bien separados están los grupos (clusters). | Cercano a **1.0** (mejor) |
            | **Calinski-Harabasz** | Relación entre la dispersión entre clusters y dentro de clusters. | **Mayor es mejor** |
            | **Davies-Bouldin** | Similitud promedio entre clusters. | Cercano a **0** (mejor) |

            Para modelos supervisados, además se muestran: **Accuracy, Precision, Recall, F1 y ROC AUC**.

            **En resumen:** Un buen modelo tiene Silhouette alto, Calinski alto y Davies bajo.
            """)

    st.markdown("")

    # ==================== MATRICES DE CONFUSIÓN ====================
    has_cm = any('MatrizConfusion' in f and f['MatrizConfusion'] is not None for f in filas)
    if has_cm:
        st.markdown(f"""
        <div style="background: rgba(245,158,11,0.06); padding: 1rem 1.2rem; border-radius: 12px;
                    border: 1px solid rgba(245,158,11,0.15); margin-bottom: 0.5rem;">
            <h3 style="margin: 0 0 0.3rem 0; color: {c.heading_primary}; font-size: 1.1rem;">{t('confusion_matrices')}</h3>
            <p style="margin: 0; font-size: 0.85rem; color: rgba(240,250,254,0.5);">
                {t('confusion_matrices_help')}
            </p>
        </div>
        """, unsafe_allow_html=True)

        filas_cm = [f for f in filas if f.get('MatrizConfusion') is not None]
        cm_cols = st.columns(len(filas_cm), gap="medium")
        for idx, fila in enumerate(filas_cm):
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
        st.plotly_chart(fig, use_container_width=False, config={'displayModeBar': False, 'responsive': True})

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
            st.plotly_chart(figt, use_container_width=False, config={'displayModeBar': False, 'responsive': True})

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
        st.plotly_chart(fig_detail, use_container_width=False, config={'displayModeBar': False, 'responsive': True})

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
