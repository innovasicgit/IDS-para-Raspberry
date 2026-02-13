"""
Página de comparación de modelos.
Permite ejecutar múltiples modelos sobre el mismo dataset y comparar resultados.
"""

import streamlit as st
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
    st.title('📊 Comparar Modelos')
    st.markdown(
        """
        <div style="background: linear-gradient(160deg, rgba(19,131,167,0.08) 0%, rgba(12,74,110,0.04) 100%); padding: 1rem 1.2rem; border-radius: 14px; margin: .6rem 0 1rem 0; border: 1px solid rgba(19,131,167,0.12);">
        <p style="margin:0; font-size: .95rem; line-height:1.5; color: rgba(240,250,254,0.75);">
        • Seleccione uno o varios modelos para ejecutar la misma predicción sobre un único conjunto de datos (última captura o un CSV).<br/>
        • <strong style="color: #1CA8D4;">Internas</strong>: calcula Silhouette, Calinski y Davies sobre las representaciones del pipeline si hay ≥2 clases predichas.<br/>
        • <strong style="color: #1CA8D4;">Externas</strong>: requiere una columna con etiquetas reales; para modelos multiclase (KMEANS/Autoencoder) se resume a <em>Normal</em> vs <em>Ataque</em> para AUC/ROC.<br/>
        • El gráfico "Normal vs Ataques" suma todas las categorías de ataque (p. ej., DDoS_TCP/UDP, Reconnaissance).
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Selección de origen de datos
    data_source = _select_data_source()
    
    # Selección de modelos y métricas
    selected_models = st.multiselect(
        'Seleccione modelos', 
        ['IForest', 'OCSVM', 'KMEANS', 'AUTOENCODER'], 
        default=['IForest','OCSVM','KMEANS']
    )
    
    metric_compare = st.selectbox(
        'Métricas de validación', 
        ['Internas', 'Externas', 'Ninguna'], 
        help='Internas: Silhouette, Calinski, Davies. Externas: requiere columna de etiquetas reales.'
    )

    true_label_col = None
    if metric_compare == 'Externas':
        if data_source is not None:
            posibles = data_source.columns.tolist()
            true_label_col = st.selectbox('Columna de etiquetas reales (0/1 o multiclase)', posibles)
        else:
            st.info('Cargue datos con etiquetas reales para métricas externas.')

    # Botón de comparación
    if st.button('🚀 Comparar'):
        _run_comparison(data_source, selected_models, metric_compare, true_label_col)


def _select_data_source():
    """Seleccionar origen de datos (captura o CSV)."""
    src_cols = st.columns(2, gap="medium")
    data_source = None
    
    if 'data' in st.session_state and st.session_state.data is not None:
        with src_cols[0]:
            usar_captura = st.checkbox('Usar datos de la última captura', value=True)
        if usar_captura:
            data_source = st.session_state.data.copy()
    
    if data_source is None:
        with src_cols[1]:
            uploaded_cmp = st.file_uploader('Cargar CSV para comparar', type='csv', key='csv_compare')
        if uploaded_cmp is not None:
            data_source = pd.read_csv(uploaded_cmp)
            st.success('Datos cargados para comparar.')
        else:
            st.info('Cargue un CSV o use la última captura para habilitar la comparación.')
    
    return data_source


def _prep_df(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocesar DataFrame para predicción."""
    lista = ['ip_ttl','tos','ip_flags_rb','ip_flags_df','ip_flags_mf']
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
    for opt in selected_models:
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
        fila = {'Modelo': opt, **conteos, 'Tiempo (s)': float(pred_time)}
        
        # Métricas internas
        if metric_compare == 'Internas':
            if y is not None and len(np.unique(y)) >= 2:
                try:
                    s, c, d = metricas.metrica_internas(pd.DataFrame(pp3), y)
                    fila.update({'Silhouette': float(s), 'Calinski': float(c), 'Davies': float(d)})
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
                
                # Binarizar predicciones si es multiclase
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

                # Matriz de confusión
                cm = confusion_matrix(y_true, y_bin)
                fila.update({'MatrizConfusion': cm})

                # ROC AUC si ambos son binarios
                if np.unique(y_true).size == 2 and np.unique(y_bin).size == 2:
                    try:
                        aucv = roc_auc_score(y_true, y_bin)
                        fila.update({'ROC_AUC': float(aucv)})
                    except Exception:
                        pass
            except Exception:
                pass
        
        filas.append(fila)

    if not filas:
        st.info('Sin resultados para mostrar.')
        return

    # Mostrar resultados
    _display_results(filas, metric_compare)


def _display_results(filas, metric_compare):
    """Mostrar resultados de la comparación."""
    res_df = pd.DataFrame(filas)
    
    # Columnas base a mostrar
    cols = ['Modelo', 'Normal', 'Anómalo', 'DDOS_TCP', 'DDOS_UDP', 'Reconnaissance', 'Tiempo (s)']
    
    # Agregar columnas de métricas si existen en el DataFrame
    if metric_compare == 'Internas':
        for col in ['Silhouette', 'Calinski', 'Davies']:
            if col in res_df.columns:
                cols.append(col)
    
    if metric_compare == 'Externas':
        if 'ROC_AUC' in res_df.columns:
            cols.append('ROC_AUC')
    
    # Filtrar solo las columnas que existen
    cols_disponibles = [c for c in cols if c in res_df.columns]
    
    st.markdown('### 📋 Resumen')
    st.dataframe(res_df[cols_disponibles], use_container_width=True)

    # Matrices de confusión
    if metric_compare == 'Externas':
        st.markdown('### 🧮 Matrices de Confusión')
        for _, row in res_df.iterrows():
            if 'MatrizConfusion' in row and row['MatrizConfusion'] is not None:
                st.write(f"Modelo: {row['Modelo']}")
                st.dataframe(pd.DataFrame(row['MatrizConfusion']), use_container_width=True)

    # Gráfico Normal vs Ataques
    st.markdown('### 📊 Normal vs Ataques')
    modelos = res_df['Modelo'].values
    normales = res_df['Normal'].fillna(0).values
    
    # Sumar todas las categorías de ataques disponibles
    ataques = np.zeros(len(res_df))
    for col in ['Anómalo', 'DDOS_TCP', 'DDOS_UDP', 'Reconnaissance']:
        if col in res_df.columns:
            ataques += res_df[col].fillna(0).values
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Normal', x=modelos, y=normales, marker_color='#10B981'))
    fig.add_trace(go.Bar(name='Ataques', x=modelos, y=ataques, marker_color='#EF4444'))
    fig.update_layout(
        barmode='group', 
        title='Normal vs Ataques por modelo', 
        title_x=0.5,
        xaxis_title='Modelo',
        yaxis_title='Cantidad de predicciones',
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de tiempos
    if 'Tiempo (s)' in res_df.columns:
        st.markdown('### ⏱️ Tiempos de predicción por modelo')
        figt = go.Figure(data=[go.Bar(x=res_df['Modelo'], y=res_df['Tiempo (s)'], marker_color='#1383A7')])
        figt.update_layout(title='Tiempo de predicción (s)', title_x=0.5)
        st.plotly_chart(figt, use_container_width=True)
