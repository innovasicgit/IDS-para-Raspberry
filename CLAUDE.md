# IDS para Raspberry Pi

IDS (detección de intrusiones/anomalías) para redes IoT. App **Streamlit** de un solo proceso: el
"backend" es una librería Python que importa el frontend (no hay servidor aparte). Captura tráfico con
`tshark`, lo convierte en DataFrame y lo clasifica con modelos ya entrenados (`model/*.pkl`).
Proyecto de tesis (Innovasic | UCC). Repo: github.com/innovasicgit/IDS-para-Raspberry.

## Comandos

El entorno virtual es `.nuevoentorno/` (el `python3` del sistema no tiene numpy/pandas):

```bash
.nuevoentorno/bin/streamlit run app.py          # app en http://localhost:8501 (captura requiere permisos para tshark)
.nuevoentorno/bin/python -m pytest -q tests     # tests
docker compose up -d                            # imagen publicada juancaing/ids-iot-appv2 (network_mode: host, NET_ADMIN/NET_RAW)
./build_and_push_arm.sh                         # buildx linux/arm64 → Docker Hub
```

En la Raspberry, `start_ids.sh` / `stop_ids.sh` levantan Streamlit + Cloudflare Tunnel (rutas absolutas de la Pi).

## Arquitectura

- `app.py`: punto de entrada. Estado de sesión, sidebar (idioma, navegación, umbrales, email, filtro ARP, tema) y router a las páginas.
- `frontend/pages/dashboard.py`: el núcleo. Captura automática (ciclos con `st.rerun()`), manual y carga de CSV; `run_prediction_on_data()` → predicción, gráficas, alertas por email, PDF.
- `frontend/pages/compare.py`: varios modelos sobre el mismo dataset. `guia.py`, `home_page.py`, `pdf_report.py`, `style.py`: guía, inicio, reporte PDF y CSS.
- `backend/capture_utils.py`: comando `tshark`, parseo con `type_packet()`; columnas en `CAPTURE_FIELDNAMES`.
- `backend/model_utils.py`: `load_model()` (joblib + `@st.cache_resource`). `backend/constants.py`: rutas de modelos y `MODEL_PATHS` / `MODEL_TYPE_BY_ID`.
- `backend/predict.py`: `predecir(model, df, model_option)` → `(pp3, y_pred, scores)`, con lógica por modelo.
- `backend/notifications*.py`: alertas Gmail SMTP; configuración en SQLite (`notifications_config.db`).
- `metricas.py`: métricas internas (silhouette/calinski/davies) y externas (accuracy/precision/recall/F1/ROC-AUC).
- `config/i18n.py`: catálogo es/en; `config/theme.py`: tema claro/oscuro.

Modelos: no supervisados (IForest, OCSVM, KMEANS, AUTOENCODER) → métricas **internas**;
supervisados (DecisionTree, ExtraTrees, RandomForest) → métricas **externas**.

## Convenciones y trampas

- **Pickles**: `autoencoder_classifier.py` y `del_columns.py` en la raíz son módulos puente que `joblib.load` necesita; no moverlos ni renombrarlos. `del_columns` está duplicado en `backend/`: mantener ambos iguales.
- **Etiquetas**: 0 = Normal, 1 = Ataque (`metricas.to_binary_attack_labels`). `scores` debe ser la probabilidad/puntuación de **ataque** (lo espera `roc_curve`/`roc_auc_score`).
- **Métricas externas** solo con etiquetas reales (CSV etiquetado). Las columnas de captura nunca son candidatas a etiqueta; en capturas en vivo se omiten. Métrica no definida → `None` → "N/A".
- **Umbrales** en `st.session_state`, definidos en la sidebar de `app.py` y leídos en `predict.py` (`ae_normal_threshold`, `ae_reconstruction_threshold`, `ocsvm_use_sign`, `ocsvm_percentile`, `supervised_attack_threshold`).
- **Textos de UI** siempre con `t("clave", **valores)` / `t_list()`, añadiendo la clave en `es` **y** en `en` (lo verifica `tests/test_i18n.py`). Los marcadores admiten formato: `{minutes:02d}`, `{percent:.0f}`.
- Código y comentarios en español.

## Problemas conocidos

- `tests/test_kmeans_feature_reconciliation.py` importa `align_features_to_model`, que no existe en `backend/predict.py` (falla al recolectarse).
- La autenticación está deshabilitada en `app.py` (`ensure_auth()` comentado).
- `config/settings.py` lista modelos supervisados sin `.pkl` (GradientBoosting, LogisticRegression); la fuente real es `backend/constants.py`.
