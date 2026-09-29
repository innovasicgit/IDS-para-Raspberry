"""
Página de inicio del Sistema IDS para IoT.
Página principal con información del sistema, características y guía de uso.
"""

import streamlit as st
from config.theme import get_current_theme
from config.i18n import t
from pathlib import Path
import base64


def show_home_page():
    """Mostrar página de inicio con información del sistema."""

    theme = get_current_theme()
    c = theme.colors

    # Rutas a imágenes + helpers para base64
    # el directorio `img` está situado en la raíz del proyecto; desde aquí
    # basta con subir dos niveles: `frontend` -> raíz.
    img_dir = Path(__file__).parent.parent / "img"
    def _b64(fname):
        p = img_dir / fname
        if not p.exists():
            return None
        ext = p.suffix.lstrip('.')
        data = base64.b64encode(p.read_bytes()).decode()
        return f"data:image/{ext};base64,{data}"

    # background images (hero y CTA). Usa la mano/escudo para hero, otra para CTA
    hero_b64 = _b64("img4.png") or ""
    cta_b64 = _b64("img1.jpg") or ""

    # Hero banner: rectángulo con imagen de fondo embebida en base64
    # Utiliza la imagen seleccionada para cubrirlo y un overlay semitransparente
    st.markdown(f"""
    <style>
        .home-hero {{
            position: relative;
            padding: 60px 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 20px 0;
            overflow: hidden;
            background: url('{hero_b64}') center center / cover no-repeat;
        }}
        .home-hero::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: {c.hero_overlay};
            z-index: 1;
        }}
        .home-hero-content {{
            position: relative;
            z-index: 2;
        }}
    </style>
    <div class="home-hero">
        <div class="home-hero-content">
            <h1 style="margin: 0; color: {c.hero_title}; font-size: 3rem;">{t("ids_title")}</h1>
            <p style="margin-top: 0.5rem; color: {c.hero_subtitle}; font-size: 1.2rem;">{t("ids_subtitle")}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Cards de características principales
    st.markdown("<br>", unsafe_allow_html=True)
    col_feat1, col_feat2, col_feat3 = st.columns(3, gap="medium")
    with col_feat1:
        st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: {c.surface_variant}; border-radius: 15px; min-height: 180px; display: flex; flex-direction: column; justify-content: center; border: 1px solid {c.border};">
            <h1 style="margin: 0; font-size: 3em;">⚡</h1>
            <p style="margin: 15px 0 5px 0; font-size: 1.3em;"><strong>{t("real_time")}</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 1em; color: {c.text_secondary};">{t("instant_capture")}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_feat2:
        st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: {c.surface_variant}; border-radius: 15px; min-height: 180px; display: flex; flex-direction: column; justify-content: center; border: 1px solid {c.border};">
            <h1 style="margin: 0; font-size: 3em;">🤖</h1>
            <p style="margin: 15px 0 5px 0; font-size: 1.3em;"><strong>{t("advanced_ai")}</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 1em; color: {c.text_secondary};">{t("ml_models")}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_feat3:
        st.markdown(f"""
        <div style="text-align: center; padding: 30px; background: {c.surface_variant}; border-radius: 15px; min-height: 180px; display: flex; flex-direction: column; justify-content: center; border: 1px solid {c.border};">
            <h1 style="margin: 0; font-size: 3em;">📊</h1>
            <p style="margin: 15px 0 5px 0; font-size: 1.3em;"><strong>{t("visualization")}</strong></p>
            <p style="margin: 5px 0 0 0; font-size: 1em; color: {c.text_secondary};">{t("interactive_reports")}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Descripción principal
    st.markdown(f"""
    <div style="background: {c.surface_overlay}; padding: 2rem; border-radius: 15px; 
                border-left: 4px solid {c.primary}; margin: 2rem 0;">
        <p style="font-size: 1.2rem; line-height: 1.8; text-align: justify;">
            {t("welcome_text")}
        </p>
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 1rem;">
            {t("models_description")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Características Principales
    st.markdown("---")
    st.markdown(f"""
    <h2 style="text-align: center; color: {c.heading_primary}; margin: 3rem 0 2rem 0;">
        {t("main_features")}
    </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: {c.success_light}; padding: 1.5rem; 
                    border-radius: 15px; text-align: center; min-height: 200px; 
                    border: 1px solid rgba(16, 185, 129, 0.25);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: {c.success}; margin-bottom: 1rem;">{t("real_time_detection")}</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">{t("continuous_monitoring")}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: {c.surface_variant}; padding: 1.5rem; 
                    border-radius: 15px; text-align: center; min-height: 200px; 
                    border: 1px solid {c.border_active};">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🧠</div>
            <h3 style="color: {c.heading_secondary}; margin-bottom: 1rem;">{t("advanced_ai")}</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">{t("latest_ml")}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: {c.warning_light}; padding: 1.5rem; 
                    border-radius: 15px; text-align: center; min-height: 200px; 
                    border: 1px solid rgba(245, 158, 11, 0.25);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: {c.warning}; margin-bottom: 1rem;">{t("predictive_analysis")}</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">{t("threat_prediction")}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: {c.error_light}; padding: 1.5rem; 
                    border-radius: 15px; text-align: center; min-height: 200px; 
                    border: 1px solid rgba(239, 68, 68, 0.25);">
            <div style="font-size: 3.5rem; margin-bottom: 1rem;">🚫</div>
            <h3 style="color: {c.error}; margin-bottom: 1rem;">{t("active_protection")}</h3>
            <p style="font-size: 0.95rem; line-height: 1.6;">{t("threat_mitigation")}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: {c.surface_overlay}; padding: 1.2rem 1.5rem; border-radius: 15px; border: 1px solid {c.border};">
        <h3 style="margin-top: 0; color: {c.heading_primary};">{t("supervised_models")}</h3>
        <p style="margin-bottom: 0.75rem; color: {c.text_secondary};">{t("supervised_models_description")}</p>
        <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.75rem;">
            <div style="padding: 0.8rem 1rem; background: rgba(56, 189, 248, 0.08); border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.2);">
                <strong>DecisionTree</strong><br><span style="color: {c.text_secondary};">{t("decision_tree_description")}</span>
            </div>
            <div style="padding: 0.8rem 1rem; background: rgba(16, 185, 129, 0.08); border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.2);">
                <strong>ExtraTrees</strong><br><span style="color: {c.text_secondary};">{t("extra_trees_description")}</span>
            </div>
            <div style="padding: 0.8rem 1rem; background: rgba(239, 68, 68, 0.08); border-radius: 10px; border: 1px solid rgba(239, 68, 68, 0.2);">
                <strong>RandomForest</strong><br><span style="color: {c.text_secondary};">{t("random_forest_description")}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Interpretación de Resultados
    st.markdown("---")
    st.markdown(f"""
    <h2 style="text-align: center; color: {c.heading_primary}; margin: 3rem 0 2rem 0;">
        {t("results_interpretation")}
    </h2>
    """, unsafe_allow_html=True)

    # Tres columnas para métricas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background: {c.success_light}; padding: 1.5rem; border-radius: 12px; 
                    border-left: 4px solid {c.success};">
            <h3 style="color: {c.success}; margin-bottom: 1rem;">{t("validation_metrics")}</h3>
            <ul style="line-height: 2;">
                <li><strong>Silhouette Score:</strong> {t("cluster_quality")}</li>
                <li><strong>Calinski Score:</strong> {t("cluster_separation")}</li>
                <li><strong>Davies Score:</strong> {t("cluster_similarity")}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background: {c.surface_variant}; padding: 1.5rem; border-radius: 12px; 
                    border-left: 4px solid {c.primary};">
            <h3 style="color: {c.heading_secondary}; margin-bottom: 1rem;">{t("anomaly_classification")}</h3>
            <ul style="line-height: 2;">
                <li><strong>Normal:</strong> {t("expected_network_traffic")}</li>
                <li><strong>{t("anomalous_label")}:</strong> {t("suspicious_patterns")}</li>
                <li><strong>Multiclase:</strong>
                    <ul>
                        <li>DDoS_TCP</li>
                        <li>DDoS_UDP</li>
                        <li>Reconnaissance</li>
                    </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background: {c.warning_light}; padding: 1.5rem; border-radius: 12px; 
                    border-left: 4px solid {c.warning};">
            <h3 style="color: {c.warning}; margin-bottom: 1rem;">{t("performance_metrics")}</h3>
            <ul style="line-height: 2;">
                <li><strong>CPU:</strong> {t("cpu_usage")}</li>
                <li><strong>Memoria:</strong> {t("ram_usage")}</li>
                <li><strong>Disco:</strong> {t("storage_usage")}</li>
                <li><strong>Tiempo:</strong> {t("duration_seconds")}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Modelos de Detección
    st.markdown("---")
    st.markdown(f"""
    <h2 style="text-align: center; color: {c.heading_primary}; margin: 3rem 0 2rem 0;">
        {t("anomaly_models")}
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="background: {c.surface_variant}; padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid {c.primary};">
            <h3 style="color: {c.heading_secondary};">🔵 OCSVM (One Class Support Vector Machine)</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                {t("ocsvm_description")}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: {c.success_light}; padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid {c.success};">
            <h3 style="color: {c.success};">🟢 IForest (Isolation Forest)</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                {t("iforest_description")}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background: {c.warning_light}; padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid {c.warning};">
            <h3 style="color: {c.warning};">🟠 K-means</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                {t("kmeans_description")}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: {c.error_light}; padding: 1.5rem; border-radius: 12px; 
                    margin-bottom: 1rem; border: 2px solid {c.error};">
            <h3 style="color: {c.error};">🔴 Autoencoder multiclase</h3>
            <p style="line-height: 1.8; margin-top: 1rem;">
                {t("autoencoder_description")}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Guía de Uso
    st.markdown("---")
    st.markdown(f"""
    <h2 style="text-align: center; color: {c.heading_primary}; margin: 3rem 0 2rem 0;">
        {t("usage_guide")}
    </h2>
    """, unsafe_allow_html=True)

    steps = [
        ("🔌", t("step_select_model"), t("step_select_model_desc")),
        ("📡", t("step_capture"), t("step_capture_desc")),
        ("🖱️", t("step_predict"), t("step_predict_desc")),
        ("📊", t("step_results"), t("step_results_desc")),
        ("💾", t("step_save"), t("step_save_desc"))
    ]

    cols = st.columns(5)
    for idx, (icon, title, desc) in enumerate(steps):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: {c.surface_variant}; padding: 1rem; 
                        border-radius: 12px; text-align: center; min-height: 150px;
                        border: 1px solid {c.border_active};">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
                <h3 style="font-size: 0.95rem; margin: 0.5rem 0;">{title}</h3>
                <p style="font-size: 0.8rem; margin: 0; color: {c.text_secondary};">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sección CTA con fondo de otra imagen
    st.markdown("---")
    st.markdown(f"""
    <style>
        .cta-banner {{
            position: relative;
            padding: 60px 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 20px 0;
            overflow: hidden;
            background: url('{cta_b64}') center center / cover no-repeat;
        }}
        .cta-banner::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: {c.surface_overlay};
            z-index: 1;
        }}
        .cta-content {{
            position: relative;
            z-index: 2;
        }}
    </style>
    <div class="cta-banner">
        <div class="cta-content">
            <h2 style="color: {c.hero_title}; margin-bottom: 1rem; font-size: 2rem;">
                {t("ready_to_start")}
            </h2>
            <p style="color: {c.hero_subtitle}; font-size: 1.2rem; margin-bottom: 1.5rem;">
                {t("access_dashboard")}
            </p>
            <div style="font-size: 3rem;">🚀</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; color: {c.text_secondary};">
        <p style="margin: 0.5rem 0;">
            <strong>{t("ids_footer")}</strong> v1.0
        </p>
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">
            {t("developed_by")}
        </p>
        <p style="margin: 0.5rem 0; font-size: 0.85rem; color: {c.text_disabled};">
            {t("all_rights_reserved")}
        </p>
    </div>
    """, unsafe_allow_html=True)