# 🛡️ IDS para Raspberry (Streamlit)

Sistema de detección de intrusiones/anomalías para redes IoT con interfaz **Streamlit**. Permite:

- Capturar tráfico (TCP/UDP/ARP/ICMP) con `tshark`.
- Ejecutar modelos de detección (no supervisados y uno multiclase).
- Visualizar resultados, métricas y estado del sistema (CPU/RAM/Disco).
- (Opcional) enviar notificaciones por email en capturas automáticas.

## 📁 Estructura del proyecto (qué es cada módulo)

Entry point:

- `app.py`: inicializa Streamlit, sidebar (tema/config), navegación y enruta a las páginas.

UI (Streamlit):

- `frontend/style.py`: estilos y configuración general de la página.
- `frontend/home_page.py`: página de inicio.
- `frontend/auth_ui.py`: autenticación (actualmente deshabilitada en `app.py`).
- `frontend/pages/dashboard.py`: panel de control (captura, predicción, gráficos, alertas).
- `frontend/pages/compare.py`: comparación de múltiples modelos sobre el mismo dataset.
- `frontend/pages/guia.py`: guía/explicaciones del sistema.

Backend (lógica):

- `backend/capture_utils.py`: construcción del comando `tshark`, captura y parseo a DataFrame.
- `backend/model_utils.py`: `load_model()` (joblib + cache), `dict_predict()` (mapeos) y umbral binario.
- `backend/predict.py`: `predecir()` (ejecución de cada modelo) + `mostrar_metricas()` (UI de métricas internas).
- `backend/constants.py`: rutas de artefactos (`model/*.pkl`, `model/list_kmeans_over.txt`).
- `backend/notifications.py` y `backend/notifications_db.py`: notificaciones y persistencia de configuración.

Métricas:

- `metricas.py`: métricas internas (Silhouette/Calinski/Davies) y otras utilidades.

Artefactos:

- `model/`: modelos serializados (`.pkl`) y archivos auxiliares (p.ej. mapping de KMeans).

Compatibilidad con modelos serializados:

- `del_columns.py`: transformer usado por pipelines antiguos (necesario para `joblib.load`).
- `autoencoder_classifier.py`: “módulo puente” para que `joblib.load()` pueda resolver `AutoencoderClassifier`.

## 🧠 Cómo funciona (flujo de alto nivel)

1. **Captura** (Panel de Control): `backend/capture_utils.build_tshark_command()` + `capturing_packets()`.
2. **Normalización rápida** de campos (en `frontend/pages/dashboard.py` y `frontend/pages/compare.py`).
3. **Carga del modelo**: `backend/model_utils.load_model()` (usa `joblib` y cachea el resultado).
4. **Predicción**: `backend/predict.predecir(model, data_df, model_option)`.
	 - Devuelve `pp3` (features para métricas/gráficos), `y_pred` (labels) y `scores` (si aplica).
5. **Post-proceso**:
	 - Conteos por clase (binario o multiclase) y cálculo de % anomalías.
	 - (Opcional) notificaciones por email en captura automática.
6. **Visualización**: gráficos Plotly, panel de métricas internas y rendimiento del sistema.

## 🤖 Modelos incluidos (y formato de salida)

Actualmente la UI expone estas opciones (ver `frontend/pages/dashboard.py` y `frontend/pages/compare.py`):

- `IForest`: salida binaria (0=Normal, 1=Anómalo).
- `OCSVM`: salida binaria (0=Normal, 1=Anómalo) con dos modos (signo o percentil).
- `KMEANS`: salida por cluster entero y **mapeo a etiquetas** vía `model/list_kmeans_over.txt`.
- `AUTOENCODER`: salida multiclase (convención usada en el código: 0=Normal, 1=DDoS_TCP, 2=Reconnaissance, 3=DDoS_UDP).

## 📊 Métricas (internas/externas)

Métricas internas (clustering):

- Se calculan en `metricas.py` usando **scikit-learn** (`sklearn.metrics`):
	- `silhouette_score(X, labels, metric='sqeuclidean')`
	- `calinski_harabasz_score(X, labels)`
	- `davies_bouldin_score(X, labels)`

Notas:

- Requieren al menos 2 clases/labels distintos en `y_pred`.
- “Mejor” típicamente: Silhouette ↑, Calinski ↑, Davies ↓.

Métricas externas (con etiquetas reales):

- Están implementadas principalmente en `frontend/pages/compare.py` (matriz de confusión y ROC AUC con `sklearn.metrics`).

## ✅ Requisitos

- Python 3.11+
- Dependencias Python: ver `requirements.txt`
- **`tshark` instalado** (Wireshark CLI), ya que la captura de tráfico depende de él.

Si no hay permisos para capturar:

- En Linux/Raspberry, `tshark`/`dumpcap` puede requerir permisos elevados o configuración de capabilities.
- La opción más simple para pruebas es ejecutar con permisos adecuados (o usar Docker con capacidades de red).

## ▶️ Ejecutar (local)

```bash
python -m venv nuevoEntorno
source nuevoEntorno/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Abrir:

- `http://localhost:8501`

## 🐳 Ejecutar con Docker

El `Dockerfile` instala `tshark` y dependencias y ejecuta `app.py`.

Build local:

```bash
docker build -t ids-iot-app .
```

Run (recomendado con host network y capacidades de captura):

```bash
sudo docker run --rm -it \
	--net=host \
	--cap-add=NET_ADMIN --cap-add=NET_RAW \
	ids-iot-app
```

ARM/Raspberry: el repo incluye `build_and_push_arm.sh` (usa `docker buildx`).

## 🧰 Scripts de arranque/parada (opcional)

- `start_ids.sh`: inicia Streamlit y opcionalmente un túnel Cloudflare.
- `stop_ids.sh`: detiene Streamlit y el túnel.

Importante: en `start_ids.sh` revisa y ajusta `PROJECT_DIR` a tu ruta real (el script puede estar apuntando a un directorio antiguo).

## ➕ Cómo agregar o reemplazar modelos

La app tiene 3 puntos principales donde “se enchufa” un modelo:

1) **Artefacto del modelo** (archivo en `model/`)

- Guarda tu modelo/pipeline (típicamente con `joblib.dump(...)`) en `model/`.
- Añade/actualiza su ruta en `backend/constants.py`.

2) **Carga**

- La carga se hace con `backend/model_utils.load_model()` (usa `joblib.load`).
- Si tu pipeline usa clases/transformers propios, deben ser importables al cargar.
	- Ejemplo real del repo: `autoencoder_classifier.py` existe como módulo puente para deserialización.

3) **Predicción**

- Implementa la lógica en `backend/predict.predecir()` agregando un nuevo caso `if model_option == 'TU_MODELO': ...`.
- Debes retornar:
	- `predicciones` como `np.ndarray`/serie de ints
	- `scores` (opcional) si tu modelo expone un score (útil para histogramas/umbrales)
	- `pp3` (features) para métricas internas: el código intenta sacar el transformer del pipeline; si no, usa columnas numéricas.

### Checklist: modelo no supervisado binario (Normal/Anómalo)

1. Añade el `.pkl` en `model/`.
2. Declara una constante en `backend/constants.py`.
3. En `frontend/pages/dashboard.py`:
	 - Agrega la opción en el `selectbox` de modelos.
	 - Añade la carga (`load_model(...)`) para esa opción.
	 - Asegura que tu `y_pred` sea 0/1 para que conteos/alertas funcionen.
4. En `backend/predict.py`:
	 - Agrega el branch en `predecir()`.
5. En `frontend/pages/compare.py`:
	 - Agrega el modelo en la lista de `multiselect`.
	 - Completa `_load_model_path()` y `_predict()`/`_counts()`.

### Checklist: modelo de clustering/multiclase

Si tu modelo devuelve clusters (0..k-1) y necesitas nombres:

- Crea un archivo de mapping similar a `model/list_kmeans_over.txt` y léelo con `backend/model_utils.dict_predict()`.
- Actualiza conteos en `dashboard.py`/`compare.py` para reflejar tus etiquetas.

### Checklist: modelo supervisado

La página `Comparar Modelos` ya soporta **métricas externas** si el dataset tiene una columna de etiquetas reales:

- En `frontend/pages/compare.py` se calcula `confusion_matrix` y `roc_auc_score` (binario).

Si tu modelo es multiclase y quieres métricas más ricas:

- Decide si evaluar en binario (Normal vs Ataque) o implementar métricas multiclase.
- En ambos casos, define una convención de labels estable (p.ej. 0=Normal, resto=ataque/tipo).

## 🧩 Tips de compatibilidad al serializar modelos

- Si guardas un `Pipeline` con transformers custom, asegúrate de que el módulo/clase exista con el mismo import path al cargar.
- Mantén estable el esquema de columnas esperado por el pipeline.
	- `backend/predict.predecir()` intenta alinear columnas usando `feature_names_in_` cuando está disponible.

## Soporte

Si algo falla al capturar/predict:

- Verifica que `tshark` esté instalado y tenga permisos.
- Revisa la consola/log de Streamlit para ver el traceback que muestra `load_model()` o `predecir()`.
