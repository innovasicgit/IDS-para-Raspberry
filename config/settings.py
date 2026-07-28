"""
Configuración general de la aplicación IDS.
"""

# Información de la aplicación
APP_NAME = "Sistema de Detección de Anomalías IoT"
APP_VERSION = "2.0.0"
ORGANIZATION = "Innovasic | UCC"

# Configuración de captura
DEFAULT_MANUAL_PACKETS = 100
DEFAULT_AUTO_DURATION_MIN = 1
DEFAULT_AUTO_INTERVAL_MIN = 5
MAX_PACKETS = 50000
MAX_DURATION_MIN = 1440

# Configuración de modelos
AVAILABLE_UNSUPERVISED_MODELS = ['IForest', 'OCSVM', 'KMEANS', 'AUTOENCODER']
AVAILABLE_SUPERVISED_MODELS = [
	'DecisionTree',
	'ExtraTrees',
	'GradientBoosting',
	'LogisticRegression',
	'RandomForest',
]
AVAILABLE_MODELS = AVAILABLE_UNSUPERVISED_MODELS + AVAILABLE_SUPERVISED_MODELS
METRIC_TYPES = ['Externas', 'Internas']

# Configuración de UI
TRAFFIC_WINDOW_SIZE = 20  # Ventana para rolling calculations en gráficos
