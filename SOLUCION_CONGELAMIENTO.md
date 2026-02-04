# Solución de Congelamiento en Captura Automática

## Problemas Identificados y Solucionados

### 1. **`st.rerun()` dentro del loop (CRÍTICO)**
**Problema:** Causaba que la página se reiniciara constantemente, perdiendo contexto y congelando la interfaz.
**Solución:** 
- Eliminado `st.rerun()` del ciclo principal de captura
- Solo se ejecuta `st.rerun()` en el countdown cuando es necesario
- Conservación de estado en `session_state` entre recargas

### 2. **`process.stdout.readline()` Bloqueante**
**Problema:** Si no había datos, se bloqueaba indefinidamente sin timeout.
**Solución:**
- Implementada función `safe_readline_with_timeout()`
- Usa `select` en Linux/Mac y `threading` en Windows
- Timeout de 2 segundos en captura manual, 1 segundo en automática
- Retorna `None` si no hay datos, permitiendo continuar

### 3. **Falta de Manejo de Procesos Colgados**
**Problema:** Los procesos de tshark podían quedar colgados sin ser killados adecuadamente.
**Solución:**
- Función `safe_terminate_process()` con timeout
- Primero intenta `terminate()`, luego `kill()` si es necesario
- Espera configurable antes de forzar kill
- Nuevo módulo `backend/process_monitor.py` para monitoreo avanzado

### 4. **Falta de Recuperación de Errores**
**Problema:** Un error no capturado congelaba toda la captura automática.
**Solución:**
- Try-catch exhaustivo en captura automática
- Contador de errores (`error_count`) con máximo (`max_errors`)
- Registra errores sin detener completamente
- Nuevo módulo `backend/auto_capture_handler.py` con gestor robusto

### 5. **Ausencia de Heartbeat/Detección de Congelamiento**
**Problema:** No había forma de detectar si el proceso se había congelado.
**Solución:**
- Clase `AutoCaptureHandler` con detección de congelamiento
- Método `is_frozen()` que verifica inactividad
- Heartbeat configurable (default 30 segundos)
- Método `check_health()` para diagnosticar problemas

## Cambios Realizados en Código

### En `app2IPV2.py`:

#### 1. Importes Agregados
```python
import subprocess
from backend.auto_capture_handler import AutoCaptureHandler
from backend.process_monitor import (
    ProcessMonitor, 
    cleanup_orphan_processes,
    is_tshark_running
)
```

#### 2. Nueva Función: `safe_readline_with_timeout()`
```python
def safe_readline_with_timeout(process, timeout=2.0):
    """Lee línea del proceso con timeout para evitar bloqueos."""
    # Usa select en Linux/Mac, threading en Windows
    # Retorna None si timeout o error
```

#### 3. Nueva Función: `safe_terminate_process()`
```python
def safe_terminate_process(process, timeout=2):
    """Termina proceso de forma segura con timeout."""
    # Primero terminate(), luego kill() si es necesario
```

#### 4. Captura Manual Mejorada
- Ahora usa `safe_readline_with_timeout()`
- Mejor manejo de excepciones
- Contador de errores con máximo
- Try-catch envolvente todo el proceso
- Decodificación segura de strings (UTF-8)

#### 5. Captura Automática Mejorada
- **Sin `st.rerun()` en ciclo**: Evita congelamiento
- **Métricas en tiempo real**: Muestra estado en columnas
- **Try-catch envolvente**: Maneja todos los errores
- **Timeout en readline**: No se bloquea indefinidamente
- **Manejo seguro de procesos**: Termina correctamente
- **Contadores de ciclos**: Rastrea intentos exitosos/fallidos
- **Rerun solo en countdown**: Actualiza UI cada segundo si espera

## Configuración Recomendada

### Para Captura Automática Estable:

```python
# En Pestaña: Captura Automática
Duración de captura: 30-60 segundos (por defecto 60)
Intervalo entre capturas: 5-15 minutos (por defecto 5)
```

### Variables de Timeout (en segundos):
- `safe_readline_with_timeout` manual: 2.0 segundos
- `safe_readline_with_timeout` automática: 1.0 segundos
- `safe_terminate_process`: 2.0 segundos
- Heartbeat máximo sin actividad: 30 segundos

## Monitoreo Avanzado Disponible

### Módulo `backend/auto_capture_handler.py`:
- `AutoCaptureHandler`: Maneja thread-safe de capturas
- `CaptureStateManager`: Gestiona estado con locks
- `create_robust_capture_session()`: Crea sesión robusta
- `is_capture_session_healthy()`: Verifica salud de sesión

### Módulo `backend/process_monitor.py`:
- `ProcessMonitor`: Monitorea procesos individuales
- `check_process_health()`: Diagnóstico de procesos
- `force_kill_process_tree()`: Mata proceso y descendientes
- `restart_failed_process()`: Reinicia con reintentos
- `cleanup_orphan_processes()`: Limpia procesos huérfanos
- `get_network_interface_status()`: Estado de interfaces

## Cómo Usar el Nuevo Sistema

### Inicializar Captura Robusta (Opcional):
```python
from backend.auto_capture_handler import create_robust_capture_session

if 'capture_session' not in st.session_state:
    st.session_state.capture_session = create_robust_capture_session()
```

### Verificar Salud de Captura:
```python
from backend.auto_capture_handler import is_capture_session_healthy

if not is_capture_session_healthy(st.session_state.get('capture_session')):
    st.error("⚠️ Sesión de captura se ha congelado, reiniciando...")
    st.session_state.capture_session.reset()
```

### Limpiar Procesos Huérfanos:
```python
from backend.process_monitor import cleanup_orphan_processes

cleanup_orphan_processes()  # Ejecutar al inicio o después de errores
```

## Indicadores de Mejora

✅ **Antes:**
- Se congelaba después de ~5-20 minutos
- Requería refresco de página y relogueo
- Sin detección de congelamiento
- Sin recuperación de errores

✅ **Después:**
- Debería funcionar indefinidamente sin congelarse
- Detección automática de congelamiento
- Recuperación de errores sin parar ciclos
- Timeouts configurables
- Logs detallados de problemas

## Limitantes de Streamlit

**Sí, Streamlit tiene limitaciones:**
1. No soporta threads de larga duración bien
2. Cada `st.rerun()` reinicia el script completamente
3. Session state es volátil entre recargas
4. No hay soporte nativo para tareas de background

**Cómo se mitigan estas limitaciones:**
- Minimizando uso de `st.rerun()`
- Guardando estado en `session_state` de forma robusta
- Usando timeouts en I/O para no bloquear
- Try-catch exhaustivo en lógica crítica

## Próximos Pasos Recomendados

1. **Testing extendido**: Dejar captura automática corriendo 1+ hora
2. **Monitoreo**: Usar logs para identificar patrones de congelamiento
3. **Alternativa (Opcional)**: Usar Streamlit Cloud con workers backend
4. **Scheduler (Opcional)**: Considerar APScheduler para tareas programadas
