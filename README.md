# 🛡️ Sistema de Detección de Intrusiones para Redes IoT

## 📋 Descripción
Sistema avanzado de detección de intrusiones (IDS) diseñado específicamente para redes IoT, utilizando técnicas de aprendizaje automático para identificar y alertar sobre posibles amenazas de seguridad en tiempo real.

## ✨ Características Principales

### 🤖 Modelos de Detección
- **IForest (Isolation Forest)** - Para detección de anomalías basada en aislamiento
- **OCSVM (One Class Support Vector Machine)** - Efectivo en datos de alta dimensionalidad
- **K-MEANS** - Agrupamiento para identificación de patrones
- **Autoencoder Multiclase** - Detección y clasificación combinada de amenazas

### 🎯 Tipos de Amenazas Detectadas
- DDoS TCP
- DDoS UDP
- Reconocimiento
- Tráfico Normal (baseline)

### 📊 Análisis y Métricas
- Métricas internas y externas de evaluación
- Visualización en tiempo real
- Monitoreo continuo del tráfico de red

## 🚀 Requisitos del Sistema

### 📌 Software
- Python 3.11+
- Streamlit
- TensorFlow/Keras
- Scikit-learn
- Pandas
- NumPy

### 📌 Hardware Recomendado
- Raspberry Pi (compatible)
- Memoria RAM: 2GB mínimo
- Almacenamiento: 16GB mínimo

## 🛠️ Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/innovasicgit/IDS-para-Raspberry.git
```

2. Crear y activar el entorno virtual:
```bash
python -m venv nuevoEntorno
source nuevoEntorno/bin/activate  # Linux/Mac
.\nuevoEntorno\Scripts\activate   # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 🎮 Uso

1. Activar el entorno virtual
2. Ejecutar la aplicación:
```bash
streamlit run app2IPV2.py
```

3. Acceder a través del navegador:
```
http://localhost:8501
```

## 🔍 Guía de Uso

1. **Selección de Modelo**: Elegir el algoritmo de detección más adecuado
2. **Configuración**: Ajustar parámetros según necesidades
3. **Monitoreo**: Visualizar detecciones en tiempo real
4. **Análisis**: Revisar métricas y resultados

## 📊 Panel de Control

- Visualización en tiempo real del tráfico
- Estadísticas de detección
- Gráficos de rendimiento
- Alertas configurables

## 🔒 Seguridad

- Monitoreo continuo del tráfico de red
- Detección temprana de amenazas
- Alertas en tiempo real
- Análisis de patrones de tráfico

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, lee las guías de contribución antes de enviar un pull request.

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## ✉️ Contacto

Para preguntas y soporte, por favor abrir un issue en el repositorio.

---
⌨️ con ❤️ por [innovasicgit](https://github.com/innovasicgit)
