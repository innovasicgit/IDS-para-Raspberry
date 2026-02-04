"""
Página principal del dashboard - Panel de Control de Detección.
"""

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import matplotlib.pyplot as plt
from collections import Counter
import psutil

from backend.constants import (
    IFOREST_MODEL_PATHS,
    OCSVM_MODEL_PATH,
    KMEANS_MODEL_PATHS,
    AUTOENCODER_MODEL_PATH,
    KMEANS_TXT_PATH,
)
from backend.model_utils import load_model, dict_predict, pred_threshold
from backend.capture_utils import (
    build_tshark_command,
    capturing_packets,
    type_packet,
    packet_df,
)
from backend.predict import predecir, mostrar_metricas
from frontend.pdf_report import generar_reporte_pdf, DESCRIPCIONES_AMENAZAS
import metricas

def show_dashboard_page():
    """Página principal del dashboard."""
    st.title('🎯 Panel de Control de Detección')

    # Inicializa el flag una sola vez
    if 'prediccion_realizada' not in st.session_state:
        st.session_state['prediccion_realizada'] = False

    # Estado para captura automática
    if 'auto_capture' not in st.session_state:
        st.session_state.auto_capture = {
            'active': False,
            'is_capturing': False,
            'stop_requested': False,
            'interval_sec': 300,
            'packets_per_capture': 100,
            'duration_sec': 0,  # 0 = sin límite por tiempo
            'next_run_ts': None,
            'last_cycle_result': None,
        }

    # Diseño responsivo: columnas se adaptan al tamaño de pantalla
    # En móvil, las columnas se apilan verticalmente automáticamente
    col1, col2 = st.columns([1, 2], gap="medium")

    # Columna derecha: bienvenida o resumen tras predicción
    with col2:
        if 'prediccion_realizada' not in st.session_state or not st.session_state['prediccion_realizada']:
            st.markdown("## 👋 Bienvenido al Panel IDS")
            st.info("Aquí verás el resumen y visualización de los resultados una vez realices una predicción. Selecciona el modelo y las opciones en el panel de la izquierda, luego captura paquetes y realiza la predicción.")
        else:
            st.markdown("## 📄 Resumen de la Predicción")
            resumen = st.session_state['resumen_prediccion']
            st.success(resumen['texto'])
            
            # Gráficas: Pie y Barras
            col_graf1, col_graf2 = st.columns(2, gap="medium")
            with col_graf1:
                pie_fig = px.pie(
                    names=resumen['labels'],
                    values=resumen['values'],
                    color=resumen['labels'],
                    color_discrete_map={
                        'Normal': '#00C853',
                        'Anómalo': '#FF5252',
                        'DDOS_TCP': '#FF5252',
                        'DDOS_UDP': '#FFA726',
                        'Reconnaissance': '#42A5F5'
                    },
                    title="Distribución porcentual"
                )
                pie_fig.update_traces(textinfo='percent+label')
                st.plotly_chart(pie_fig, use_container_width=True)
            
            with col_graf2:
                # Gráfica de barras
                bar_colors = [('#00C853' if (str(lbl).lower() == 'normal') else '#FF5252') for lbl in resumen['labels']]
                fig_bar = go.Figure(data=[go.Bar(x=resumen['labels'], y=resumen['values'], text=resumen['values'], textposition='auto', marker_color=bar_colors)])
                fig_bar.update_layout(title='Distribución de Detecciones', title_x=0.5)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Mostrar paquetes capturados
            with st.expander("📊 Ver Paquetes Capturados"):
                if 'data_prediccion' in st.session_state:
                    st.dataframe(st.session_state['data_prediccion'], use_container_width=True)
            
            # Diagnóstico OCSVM
            if st.session_state.get('model_option_used') == 'OCSVM' and 'scores' in st.session_state:
                scores = st.session_state['scores']
                if isinstance(scores, (np.ndarray, list)) and len(scores) > 0:
                    try:
                        thr = None
                        if not st.session_state.get('ocsvm_use_sign', True):
                            pct = float(st.session_state.get('ocsvm_percentile', 0.45))
                            thr = np.percentile(scores, 100 * pct)
                        hist_fig = go.Figure()
                        hist_fig.add_trace(go.Histogram(x=scores, nbinsx=30, marker_color='#4B9FE1', name='decision_function'))
                        if thr is not None:
                            hist_fig.add_shape(type='line', x0=thr, x1=thr, y0=0, y1=1, xref='x', yref='paper', line=dict(color='#FF5252', width=2))
                            hist_fig.add_annotation(x=thr, y=1, yref='paper', text=f"Umbral={thr:.3f}", showarrow=True, arrowhead=1)
                        hist_fig.update_layout(title='OCSVM: distribución de decision_function', title_x=0.5)
                        st.plotly_chart(hist_fig, use_container_width=True)
                    except Exception:
                        pass
            
            # Métricas Internas
            if st.session_state.get('metric_option_used') == 'Internas' and 'y_pred' in st.session_state and 'pp3' in st.session_state:
                y_pred = st.session_state['y_pred']
                pp3 = st.session_state['pp3']
                unique_labels = np.unique(y_pred)
                if len(unique_labels) >= 2:
                    silhouette, calinski, davies = metricas.metrica_internas(pp3, y_pred)
                    mostrar_metricas(silhouette, calinski, davies)
                else:
                    st.info("Las métricas internas requieren al menos dos clases en la predicción.")
            
            # Métricas de Rendimiento
            if 'metricas_rendimiento' in st.session_state:
                st.markdown("### ⚙️ Métricas de Rendimiento")
                met = st.session_state['metricas_rendimiento']
                met_cols = st.columns(4, gap="small")
                with met_cols[0]:
                    st.metric("⏱️ Tiempo (s)", f"{met['tiempo']:.2f}")
                with met_cols[1]:
                    st.metric("🖥️ % CPU", f"{met['cpu']:.2f}%")
                with met_cols[2]:
                    st.metric("💾 % Memoria", f"{met['memoria']:.2f}%")
                with met_cols[3]:
                    st.metric("📀 % Disco", f"{met['disco']:.2f}%")
    
    # Interfaz Usuario Panel de Control
    with col1:
        st.markdown("### 🖥 Panel de Control")
        model_option = st.selectbox(
            "📌 Seleccione el modelo de detección",
            ('IForest','OCSVM','KMEANS','AUTOENCODER'),
            help="Cada modelo utiliza diferentes técnicas para detectar anomalías"
        )
        metric_option = st.selectbox(
            "📌 Seleccione el tipo de metrica",
            ('Externas', 'Internas'),
            help="Cada modelo utiliza diferentes técnicas para detectar anomalías"
        )

        # Pestañas justo debajo del formulario (Automática por defecto, Manual)
        tab_auto, tab_manual = st.tabs(["🚀 Captura automática", "🖐️ Captura manual"])

        # ---------------- Captura automática (en pestaña) ----------------
        with tab_auto:
            st.title("⚙️ Captura automática")
            col_auto_a, col_auto_b = st.columns(2, gap="medium")
            with col_auto_a:
                _default_dur_min = max(1, int(st.session_state.auto_capture['duration_sec'] // 60))
                _val_dur_min = st.number_input(
                    'Duración de captura (minutos)', min_value=1, max_value=1440, value=_default_dur_min, step=1,
                    help='La captura automática finalizará cuando se cumpla este tiempo'
                )
                st.session_state.auto_capture['duration_sec'] = int(_val_dur_min * 60)
            with col_auto_b:
                _default_minutes = max(1, int(st.session_state.auto_capture['interval_sec'] // 60))
                _val_minutes = st.number_input(
                    'Intervalo entre capturas (minutos)', min_value=1, max_value=1440, value=_default_minutes, step=1,
                    help='Pausa (en minutos) entre el fin de una captura y el inicio de la siguiente'
                )
                st.session_state.auto_capture['interval_sec'] = int(_val_minutes * 60)
                auto_status = '🟢 Activa' if st.session_state.auto_capture['active'] else '🔴 Detenida'
                st.metric('Estado', auto_status)

            col_btn_a, col_btn_b = st.columns(2, gap="small")
            with col_btn_a:
                if st.button('▶️ Iniciar automática', use_container_width=True, disabled=st.session_state.auto_capture['active']):
                    st.session_state.auto_capture['active'] = True
                    st.session_state.auto_capture['stop_requested'] = False
                    # Ejecutar inmediatamente la primera
                    st.session_state.auto_capture['next_run_ts'] = time.time()
                    st.rerun()
            with col_btn_b:
                if st.button('⏹️ Detener automática', use_container_width=True, disabled=not st.session_state.auto_capture['active']):
                    st.session_state.auto_capture['stop_requested'] = True
                    st.session_state.auto_capture['active'] = False
                    st.session_state.auto_capture['next_run_ts'] = None

            # Countdown/estado próximo ciclo
            if st.session_state.auto_capture['active'] and not st.session_state.auto_capture['is_capturing']:
                if st.session_state.auto_capture['next_run_ts'] is not None:
                    remaining = max(0, int(st.session_state.auto_capture['next_run_ts'] - time.time()))
                    if remaining > 0:
                        m, s = divmod(remaining, 60)
                        st.info(f"⏳ Próxima captura en {m:02d}:{s:02d} min:s")
                        # Refrescar para avanzar el conteo
                        time.sleep(1)
                        st.rerun()
        
        
        # Comando y utilidades de captura desde backend.capture_utils
        comm_arg = build_tshark_command()
        
        # Función para guardar los paquetes en CSV
        def save_packet_csv(df, path):
            df.to_csv(path, index=False)
            st.success(f"✅ Archivo guardado en {path}")
            
        # Auxiliar: ejecutar predicción y mostrar resultado (manual/automática)
        def run_prediction_on_data(data_df):
            try:
                model = None
                if model_option == 'IForest':
                    model = load_model(IFOREST_MODEL_PATHS)
                elif model_option == 'OCSVM':
                    model = load_model(OCSVM_MODEL_PATH)
                elif model_option == 'KMEANS':
                    model = load_model(KMEANS_MODEL_PATHS)
                elif model_option == 'AUTOENCODER':
                    model = load_model(AUTOENCODER_MODEL_PATH)
                if model is None:
                    st.error('No se pudo cargar el modelo seleccionado')
                    return

                lista = ['ip_ttl','tos','ip_flags_rb','ip_flags_df','ip_flags_mf']
                if set(lista).issubset(set(data_df.columns)):
                    data_df[lista] = data_df[lista].astype('str')
                    data_df.ip_ttl = data_df.ip_ttl.str.replace(',','.')
                    data_df.tos = data_df.tos.str.replace(',','.')
                    data_df.ip_flags_rb = data_df.ip_flags_rb.str.replace(',','.')
                    data_df.ip_flags_df = data_df.ip_flags_df.str.replace(',','.')
                    data_df.ip_flags_mf = data_df.ip_flags_mf.str.replace(',','.')
                
                # Limpiar valores vacíos y NaN
                data_df = data_df.replace('', np.nan).fillna(0)
                
                # Convertir todas las columnas numéricas a float, reemplazando errores con 0
                for col in data_df.columns:
                    try:
                        data_df[col] = pd.to_numeric(data_df[col], errors='coerce').fillna(0)
                    except:
                        pass

                start_time = time.time()
                cpu_usage = psutil.cpu_percent(1)
                mem_usage = psutil.virtual_memory().percent
                disco2 = psutil.disk_usage('/')

                pp3, y_pred, scores = predecir(model, data_df, model_option)
                if pp3 is None or y_pred is None:
                    st.error('Error en la predicción')
                    return

                # Conteos y etiquetas
                if model_option == 'KMEANS':
                    path2 = KMEANS_TXT_PATH
                    dict_pred = dict_predict(path2)
                    etiquetas = [dict_pred.get(int(c), 'Desconocido') for c in y_pred]
                    conteo = Counter(etiquetas)
                    normal_count = conteo.get('Normal',0)
                    ddos_tcp_count = conteo.get('DDoS_TCP',0)
                    ddos_udp_count = conteo.get('DDoS_UDP',0)
                    reconnaissance_count = conteo.get('Reconnaissance',0)
                    total = normal_count + ddos_tcp_count + ddos_udp_count + reconnaissance_count
                    labels = ['Normal','DDOS_TCP','DDOS_UDP','Reconnaissance']
                    values = [normal_count, ddos_tcp_count, ddos_udp_count, reconnaissance_count]
                    resumen_text = f"Se analizaron {total} paquetes. Normal: {normal_count}, DDOS_TCP: {ddos_tcp_count}, DDOS_UDP: {ddos_udp_count}, Reconnaissance: {reconnaissance_count}."
                elif model_option=='AUTOENCODER':
                    normal_count = int(np.count_nonzero(y_pred == 0))
                    ddos_tcp_count = int(np.count_nonzero(y_pred == 1))
                    reconnaissance_count = int(np.count_nonzero(y_pred == 2))
                    ddos_udp_count = int(np.count_nonzero(y_pred == 3))
                    total = normal_count + ddos_tcp_count + ddos_udp_count + reconnaissance_count
                    labels = ['Normal','DDOS_TCP','DDOS_UDP','Reconnaissance']
                    values = [normal_count, ddos_tcp_count, ddos_udp_count, reconnaissance_count]
                    resumen_text = f"Se analizaron {total} paquetes. Normal: {normal_count}, DDOS_TCP: {ddos_tcp_count}, DDOS_UDP: {ddos_udp_count}, Reconnaissance: {reconnaissance_count}."
                else:
                    n_normales = int((y_pred == 0).sum())
                    n_anomalos = int((y_pred == 1).sum())
                    total = n_normales + n_anomalos
                    labels = ['Normal','Anómalo']
                    values = [n_normales, n_anomalos]
                    resumen_text = f"Se analizaron {total} paquetes. Normales: {n_normales}, Anómalos: {n_anomalos}."

                # Guardar estado completo para el panel derecho (col2)
                tiempo_total = time.time() - start_time
                st.session_state['prediccion_realizada'] = True
                st.session_state['resumen_prediccion'] = {'texto': resumen_text, 'labels': labels, 'values': values}
                st.session_state['data_prediccion'] = data_df
                st.session_state['y_pred'] = y_pred
                st.session_state['scores'] = scores
                st.session_state['pp3'] = pp3
                st.session_state['model_option_used'] = model_option
                st.session_state['metric_option_used'] = metric_option
                st.session_state['metricas_rendimiento'] = {
                    'tiempo': tiempo_total,
                    'cpu': cpu_usage,
                    'memoria': mem_usage,
                    'disco': disco2[3]
                }

                st.success("✅ Predicción completada. Revisa los resultados en el panel de la derecha →")
                st.rerun()  # Refrescar para mostrar resultados en col2

            except Exception as e:
                st.error(f"❌ Error en la predicción: {str(e)}")

        # Streamlit UI (contenido de pestañas)
        data = None  # Inicializamos el DataFrame

        # ---------------- Pestaña: Captura manual ----------------
        with tab_manual:
            st.title("🖐️ Captura manual")

            # Parámetros manuales
            col_man_a, col_man_b = st.columns(2, gap="medium")
            with col_man_a:
                manual_packets = st.number_input('Paquetes a capturar (manual)', min_value=10, max_value=50000, value=100, step=10)
            with col_man_b:
                manual_duration_min = st.number_input('Duración máx. (min) (manual)', min_value=0, max_value=1440, value=0, step=1)
            manual_duration = int(manual_duration_min * 60)
           
            if st.button("🚀 Iniciar Captura", key="btn_manual_capture"):
                process = capturing_packets(comm_arg)
                st.write("📡 Capturando paquetes...")

                # Inicializamos el DataFrame
                captured_data = None
                progress_bar = st.progress(0, text="Capturando paquetes...")
                total_packets = manual_packets
                start_ts = time.time()

                i = 0
                while i < total_packets:
                    # Parar por tiempo si está configurado
                    if manual_duration and (time.time() - start_ts) >= manual_duration:
                        break
                    packet_str = process.stdout.readline().strip()
                    if packet_str:
                        packet_list = packet_str.split("\t")
                        type_packet_data = type_packet(packet_list)
                        captured_data = packet_df(type_packet_data, captured_data)
                        i += 1
                        progress_bar.progress(i / total_packets, text=f"Paquetes capturados: {i}/{total_packets}")

                try:
                    process.terminate()
                except Exception:
                    pass
                progress_bar.empty()
                st.success("✅ Captura finalizada.")

                # Mostrar el DataFrame capturado y permitir guardar
                if captured_data is not None and list(captured_data.columns) != ['value']:
                    st.write("📊 *Paquetes capturados:*")
                    st.dataframe(captured_data, use_container_width=True)
                    st.session_state.data = captured_data
                    st.success("Datos capturados listos para predicción")
                    if st.button("💾 Guardar en CSV"):
                        save_packet_csv(captured_data, "captura_paquetes.csv")

        # ---------------- Pestaña: Captura automática ----------------
        with tab_auto:
            # Ejecución automática si está activa y toca ciclo
            if st.session_state.auto_capture['active'] and not st.session_state.auto_capture['is_capturing']:
                due = st.session_state.auto_capture['next_run_ts'] is not None and time.time() >= st.session_state.auto_capture['next_run_ts']
                if due:
                    st.session_state.auto_capture['is_capturing'] = True
                    st.info('🚀 Ejecutando captura automática...')
                    process = capturing_packets(comm_arg)

                    captured_data = None
                    duration_sec = int(st.session_state.auto_capture['duration_sec'])
                    if duration_sec <= 0:
                        duration_sec = 60
                    start_ts = time.time()
                    end_ts = start_ts + duration_sec
                    prog = st.progress(0, text='Capturando (automática)...')
                    while time.time() < end_ts:
                        if st.session_state.auto_capture['stop_requested']:
                            break
                        packet_str = process.stdout.readline().strip()
                        if packet_str:
                            packet_list = packet_str.split('\t')
                            type_packet_data = type_packet(packet_list)
                            captured_data = packet_df(type_packet_data, captured_data)
                        elapsed = time.time() - start_ts
                        frac = min(1.0, elapsed / duration_sec)
                        prog.progress(frac, text=f"Tiempo transcurrido: {int(elapsed)}s / {duration_sec}s")
                    try:
                        process.terminate()
                    except Exception:
                        pass
                    prog.empty()

                    if st.session_state.auto_capture['stop_requested']:
                        st.warning('⏹️ Captura automática detenida por el usuario.')
                        st.session_state.auto_capture['active'] = False
                        st.session_state.auto_capture['is_capturing'] = False
                        st.session_state.auto_capture['next_run_ts'] = None
                    else:
                        if captured_data is not None and list(captured_data.columns) != ['value']:
                            st.success('✅ Captura automática finalizada. Ejecutando predicción...')
                            st.session_state.data = captured_data
                            run_prediction_on_data(captured_data)
                        # Programar siguiente ciclo y relanzar el countdown
                        st.session_state.auto_capture['next_run_ts'] = time.time() + int(st.session_state.auto_capture['interval_sec'])
                        st.session_state.auto_capture['is_capturing'] = False
                        st.rerun()

        # Sección de carga de archivo CSV
        uploaded_file = None  # Evita UnboundLocalError si no se usa el cargador
        with st.container():
            st.markdown("### 📊 Cargar Datos para Predicción")
            
            # Si hay datos capturados, mostrar mensaje
            if 'data' in st.session_state and st.session_state.data is not None:
                st.info("✅ Usando datos de la captura de paquetes")
                data = st.session_state.data
                st.markdown('<div class="notification" style="background-color: #4CAF50; color: white;">✅ Datos capturados listos para predicción</div>', unsafe_allow_html=True)
            else:
                # De lo contrario, mostrar el cargador de archivo CSV
                uploaded_file = st.file_uploader(
                    "📂 Cargar archivo CSV",
                    type="csv",
                    help="Cargue sus datos de red en formato CSV",
                    key="csv_uploader_1"
                )
                
                if uploaded_file is not None:
                    try:
                        data = pd.read_csv(uploaded_file)
                        if data.empty or data.shape[1] == 0:
                            st.error("❌ El archivo CSV está vacío o no contiene columnas válidas.")
                            data = None
                        else:
                            st.markdown('<div class="notification" style="background-color: #4CAF50; color: white;">✅ Datos cargados exitosamente</div>', unsafe_allow_html=True)
                            
                            with st.expander("📊 Vista previa de datos"):
                                st.dataframe(data.head(), use_container_width=True)
                                st.info(f"Dimensiones del dataset: {data.shape[0]} filas, {data.shape[1]} columnas")
                    except pd.errors.EmptyDataError:
                        st.error("❌ El archivo CSV está vacío o no tiene columnas válidas.")
                        data = None
                    except Exception as e:
                        st.error(f"❌ Error al cargar el archivo: {str(e)}")
                        data = None
                else:
                    data = None

        if st.button('🚀 Realizar Predicción', key='predict'):
            if data is not None:
                run_prediction_on_data(data)
            else:
                st.warning("⚠ Por favor capture paquetes o cargue un archivo CSV antes de realizar la predicción.")

        # Descargar reporte PDF de la última predicción
        st.markdown("### 📄 Descargar Reporte PDF")
        if st.session_state.get('prediccion_realizada') and 'resumen_prediccion' in st.session_state:
            resumen = st.session_state['resumen_prediccion']
            # Crear gráfica de barras solo para el PDF (no afecta la UI de torta)
            fig_bar, ax = plt.subplots(figsize=(6, 3.5))
            bar_colors = [('#00C853' if (str(lbl).lower() == 'normal') else '#FF5252') for lbl in resumen['labels']]
            ax.bar(resumen['labels'], resumen['values'], color=bar_colors)
            ax.set_title('Distribución de Detecciones')
            ax.set_ylabel('Cantidad')
            for i, v in enumerate(resumen['values']):
                ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontsize=10)
            plt.tight_layout()

            pdf_bytes = generar_reporte_pdf(
                resumen=resumen['texto'],
                labels=resumen['labels'],
                values=resumen['values'],
                descripcion_amenazas=DESCRIPCIONES_AMENAZAS,
                fig=fig_bar
            )
            st.download_button(
                label="📄 Descargar reporte PDF",
                data=pdf_bytes,
                file_name="reporte_prediccion_IDS.pdf",
                mime="application/pdf"
            )
            plt.close(fig_bar)
        else:
            st.warning("⚠ Primero debes capturar tráfico o hacer una predicción antes de descargar el reporte.") 
        
    
    # Mostrar visualización de tráfico solo si hay datos cargados
    if data is not None:
        st.markdown("### 📈 Patrón de Tráfico y Anomalías")
        
        try:
            # Seleccionar solo columnas numéricas para calcular el patrón de tráfico
            numeric_data = data.select_dtypes(include=[np.number])
            
            if numeric_data.empty:
                st.warning("⚠️ No hay datos numéricos para visualizar el patrón de tráfico")
            else:
                # Calculate traffic metrics
                traffic_data = numeric_data.mean(axis=1)
                
                # Calculate ceiling and floor
                window = 20
                ceiling = traffic_data.rolling(window=window).max()
                floor = traffic_data.rolling(window=window).min()
                
                # Create traffic pattern figure
                fig_traffic = go.Figure()

                # Add main traffic line
                fig_traffic.add_trace(go.Scatter(
                    x=list(range(len(traffic_data))),
                    y=traffic_data,
                    mode='lines',
                    name='Tráfico',
                    line=dict(color='#4B9FE1', width=1)
                ))

                # Add ceiling line
                fig_traffic.add_trace(go.Scatter(
                    x=list(range(len(ceiling))),
                    y=ceiling,
                    mode='lines',
                    name='Techo',
                    line=dict(color='#00C853', width=2, dash='dash')
                ))

                # Add floor line
                fig_traffic.add_trace(go.Scatter(
                    x=list(range(len(floor))),
                    y=floor,
                    mode='lines',
                    name='Suelo',
                    line=dict(color='#FFA726', width=2, dash='dash')
                ))

                # Update layout
                fig_traffic.update_layout(
                    title="Patrón de Tráfico y Detección de Anomalías",
                    title_x=0.5,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    showlegend=True,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01,
                        bgcolor="rgba(0,0,0,0)"
                    ),
                    margin=dict(t=50, l=50, r=50, b=50),
                    xaxis=dict(
                        title="Muestras",
                        showgrid=False,
                        showline=True,
                        linecolor='rgba(255,255,255,0.2)'
                    ),
                    yaxis=dict(
                        title="Intensidad de Tráfico",
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.1)',
                        zeroline=False
                    )
                )

                st.plotly_chart(fig_traffic, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error al generar visualización de tráfico: {str(e)}")

