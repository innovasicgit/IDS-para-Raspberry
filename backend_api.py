"""
Backend API FastAPI para IDS IoT
Ejecutar en la Raspberry Pi para captura de red y predicciones ML
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
import psutil
import time
import threading
import select
from datetime import datetime
import uvicorn

# Imports del proyecto
from backend.capture_utils import (
    build_tshark_command,
    capturing_packets,
    type_packet,
    packet_df,
)
from backend.model_utils import load_model, dict_predict
from backend.predict import predecir
from backend.constants import (
    IFOREST_MODEL_PATHS,
    OCSVM_MODEL_PATH,
    KMEANS_MODEL_PATHS,
    AUTOENCODER_MODEL_PATH,
    KMEANS_TXT_PATH,
)
from backend.arp_filter import apply_realtime_arp_filter
from del_columns import del_columns
import metricas

# ==================== CONFIGURACIÓN ====================

app = FastAPI(
    title="IDS IoT Backend API",
    description="API para captura de paquetes de red y detección de anomalías en Raspberry Pi",
    version="1.0.0"
)

# CORS para permitir acceso desde Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica el dominio de tu Streamlit Cloud
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELOS EN MEMORIA ====================

MODELS_CACHE = {}

def load_all_models():
    """Carga todos los modelos ML al iniciar el servidor"""
    global MODELS_CACHE
    print("🔄 Cargando modelos ML...")
    try:
        MODELS_CACHE['IFOREST'] = load_model(IFOREST_MODEL_PATHS)
        MODELS_CACHE['OCSVM'] = load_model(OCSVM_MODEL_PATH)
        MODELS_CACHE['KMEANS'] = load_model(KMEANS_MODEL_PATHS)
        MODELS_CACHE['AUTOENCODER'] = load_model(AUTOENCODER_MODEL_PATH)
        MODELS_CACHE['KMEANS_DICT'] = dict_predict(KMEANS_TXT_PATH)
        print("✅ Modelos cargados correctamente")
    except Exception as e:
        print(f"❌ Error cargando modelos: {e}")

# ==================== PYDANTIC MODELS ====================

class CaptureRequest(BaseModel):
    duration: int = 60  # segundos
    interface: Optional[str] = None  # eth0, wlan0, o ambas
    arp_filter_mode: str = 'low'  # low, medium, high, none

class PredictRequest(BaseModel):
    data: List[Dict[str, Any]]  # DataFrame como lista de diccionarios
    model_name: str  # IForest, OCSVM, KMEANS, AUTOENCODER
    metric_type: Optional[str] = 'Internas'  # Internas, Externas
    config: Optional[Dict[str, Any]] = {}  # Configuración adicional (thresholds, etc.)

class SystemMetrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    memory_available_mb: float
    disk_usage_percent: float
    network_interfaces: List[str]
    timestamp: str

class CaptureResponse(BaseModel):
    status: str
    packets_captured: int
    data: List[Dict[str, Any]]
    duration_seconds: float
    timestamp: str

class PredictionResponse(BaseModel):
    status: str
    predictions: List[int]
    n_normal: int
    n_anomalous: int
    metrics: Optional[Dict[str, float]] = None
    timestamp: str

# ==================== STATE MANAGEMENT ====================

# Estado global para captura en background
capture_state = {
    'active': False,
    'process': None,
    'df': None,
    'lock': threading.Lock()
}

# ==================== UTILIDADES ====================

def clean_data(df):
    """Limpia y prepara el DataFrame para predicción"""
    df = df.copy()
    
    # Reemplazar valores vacíos
    df = df.replace('', np.nan).infer_objects(copy=False)
    
    # Eliminar columnas problemáticas
    df = del_columns(df)
    
    # Convertir tipos
    numeric_cols = [
        'delta_time', 'frame_len', 'udp_len', 'ip_ttl', 'icmp_type',
        'tos', 'ip_flags_rb', 'ip_flags_df', 'ip_flags_mf',
        'tcp_flags_res', 'tcp_flags_ns', 'tcp_flags_cwr', 'tcp_flags_ecn',
        'tcp_flags_urg', 'tcp_flags_ack', 'tcp_flags_push', 'tcp_flags_reset',
        'tcp_flags_syn', 'tcp_flags_fin'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Rellenar NaN
    df = df.fillna(0)
    
    return df

def prepare_session_state_for_prediction(config: dict):
    """Simula session_state de Streamlit para compatibilidad"""
    class SessionState:
        def __init__(self, config):
            self.config = config
        
        def get(self, key, default=None):
            return self.config.get(key, default)
    
    return SessionState(config)

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "IDS IoT Backend API",
        "version": "1.0.0",
        "models_loaded": len(MODELS_CACHE) > 0
    }

@app.get("/health")
async def health_check():
    """Endpoint detallado de salud del sistema"""
    return {
        "status": "healthy",
        "models_available": list(MODELS_CACHE.keys()),
        "capture_active": capture_state['active'],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics", response_model=SystemMetrics)
async def get_system_metrics():
    """Obtiene métricas del sistema (CPU, memoria, disco)"""
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Interfaces de red disponibles
        net_interfaces = list(psutil.net_if_addrs().keys())
        
        return SystemMetrics(
            cpu_percent=cpu,
            memory_percent=mem.percent,
            memory_available_mb=mem.available / (1024 * 1024),
            disk_usage_percent=disk.percent,
            network_interfaces=net_interfaces,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas: {str(e)}")

@app.post("/capture", response_model=CaptureResponse)
async def capture_packets(request: CaptureRequest):
    """
    Captura paquetes de red por un tiempo determinado
    """
    if capture_state['active']:
        raise HTTPException(status_code=409, detail="Ya hay una captura en proceso")
    
    start_time = time.time()
    
    try:
        with capture_state['lock']:
            capture_state['active'] = True
            capture_state['df'] = None
        
        # Construir comando tshark
        comm_arg = build_tshark_command()
        process = capturing_packets(comm_arg)
        
        df = None
        end_time = start_time + request.duration
        
        print(f"📡 Captura iniciada por {request.duration}s...")
        
        while time.time() < end_time:
            if process.poll() is not None:
                break
            
            # Leer salida de tshark con timeout
            ready, _, _ = select.select([process.stdout], [], [], 0.1)
            if ready:
                line = process.stdout.readline()
                if line:
                    packet = line.strip().split('\t')
                    packet_dict = type_packet(packet)
                    df = packet_df(packet_dict, df)
            
            time.sleep(0.05)
        
        # Detener proceso
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
        
        duration = time.time() - start_time
        
        # Aplicar filtro ARP si se especifica
        if df is not None and request.arp_filter_mode != 'none':
            df = apply_realtime_arp_filter(df, mode=request.arp_filter_mode)
        
        packets_captured = len(df) if df is not None else 0
        
        # Convertir a lista de diccionarios
        data_list = df.to_dict('records') if df is not None else []
        
        with capture_state['lock']:
            capture_state['active'] = False
            capture_state['df'] = df
        
        print(f"✅ Captura completada: {packets_captured} paquetes")
        
        return CaptureResponse(
            status="success",
            packets_captured=packets_captured,
            data=data_list,
            duration_seconds=duration,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        with capture_state['lock']:
            capture_state['active'] = False
        
        raise HTTPException(status_code=500, detail=f"Error en captura: {str(e)}")

@app.post("/predict", response_model=PredictionResponse)
async def predict_anomalies(request: PredictRequest):
    """
    Realiza predicciones de anomalías sobre datos capturados
    """
    try:
        # Validar que el modelo existe
        if request.model_name not in MODELS_CACHE:
            raise HTTPException(
                status_code=400, 
                detail=f"Modelo '{request.model_name}' no disponible. Opciones: {list(MODELS_CACHE.keys())}"
            )
        
        # Convertir datos a DataFrame
        df = pd.DataFrame(request.data)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="No hay datos para procesar")
        
        # Limpiar datos
        df_clean = clean_data(df)
        
        # La función predecir no debería necesitar st.session_state
        # Si lo necesita, pasamos un diccionario simple en su lugar
        
        # Obtener modelo
        model = MODELS_CACHE[request.model_name]
        
        # Realizar predicción
        predictions = predecir(model, df_clean, request.model_name)
        
        if isinstance(predictions, pd.DataFrame):
            predictions = predictions['Pred'].values
        elif isinstance(predictions, pd.Series):
            predictions = predictions.values
        
        predictions = predictions.astype(int).tolist()
        
        # Calcular métricas
        n_normal = int(np.sum(np.array(predictions) == 0))
        n_anomalous = int(np.sum(np.array(predictions) != 0))
        
        metrics_dict = None
        
        if request.metric_type == 'Internas' and len(np.unique(predictions)) >= 2:
            y_pred = np.array(predictions)
            unique_labels = np.unique(y_pred)
            n_samples = len(y_pred)
            
            if len(unique_labels) >= 2 and n_samples > len(unique_labels):
                try:
                    silhouette, calinski, davies = metricas.metrica_internas(df_clean, y_pred)
                    metrics_dict = {
                        'silhouette': float(silhouette),
                        'calinski_harabasz': float(calinski),
                        'davies_bouldin': float(davies)
                    }
                except Exception as e:
                    print(f"⚠️ Error calculando métricas internas: {e}")
        
        return PredictionResponse(
            status="success",
            predictions=predictions,
            n_normal=n_normal,
            n_anomalous=n_anomalous,
            metrics=metrics_dict,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")

@app.get("/models")
async def list_models():
    """Lista modelos disponibles en el servidor"""
    return {
        "available_models": list(MODELS_CACHE.keys()),
        "loaded": len(MODELS_CACHE) > 0,
        "model_paths": {
            "IFOREST": IFOREST_MODEL_PATHS,
            "OCSVM": OCSVM_MODEL_PATH,
            "KMEANS": KMEANS_MODEL_PATHS,
            "AUTOENCODER": AUTOENCODER_MODEL_PATH
        }
    }

@app.post("/reload-models")
async def reload_models():
    """Recarga todos los modelos (útil después de actualizaciones)"""
    try:
        load_all_models()
        return {
            "status": "success",
            "models_reloaded": list(MODELS_CACHE.keys()),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recargando modelos: {str(e)}")

# ==================== STARTUP ====================

@app.on_event("startup")
async def startup_event():
    """Carga modelos al iniciar el servidor"""
    print("🚀 Iniciando Backend API para IDS IoT...")
    load_all_models()
    print("✅ Servidor listo para recibir peticiones")

# ==================== MAIN ====================

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
