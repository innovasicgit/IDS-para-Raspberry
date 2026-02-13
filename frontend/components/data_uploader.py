"""
Componentes para carga y validación de datos.
"""

import streamlit as st
import pandas as pd
from typing import Optional, Tuple


def upload_csv_file(
    label: str = "📂 Cargar archivo CSV",
    key: str = "csv_uploader",
    show_preview: bool = True,
    preview_rows: int = 5
) -> Optional[pd.DataFrame]:
    """
    Componente para cargar archivo CSV con validación y preview.
    
    Args:
        label: Etiqueta del uploader
        key: Key único para el widget
        show_preview: Mostrar preview de datos
        preview_rows: Número de filas a mostrar en preview
        
    Returns:
        DataFrame o None si no se cargó nada
    """
    uploaded_file = st.file_uploader(
        label,
        type="csv",
        help="Cargue sus datos de red en formato CSV",
        key=key
    )
    
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            
            # Validación básica
            if data.empty or data.shape[1] == 0:
                st.error("❌ El archivo CSV está vacío o no contiene columnas válidas.")
                return None
            
            # Mensaje de éxito
            st.success("✅ Datos cargados exitosamente")
            
            # Preview de datos
            if show_preview:
                with st.expander("📊 Vista previa de datos"):
                    st.dataframe(data.head(preview_rows))
                    st.info(f"Dimensiones del dataset: {data.shape[0]} filas, {data.shape[1]} columnas")
            
            return data
            
        except pd.errors.EmptyDataError:
            st.error("❌ El archivo CSV está vacío o no tiene columnas válidas.")
            return None
        except Exception as e:
            st.error(f"❌ Error al cargar el archivo: {str(e)}")
            return None
    
    return None


def check_session_data() -> Tuple[bool, Optional[pd.DataFrame]]:
    """
    Verificar si hay datos en session_state.
    
    Returns:
        Tuple (tiene_datos, dataframe)
    """
    if 'data' in st.session_state and st.session_state.data is not None:
        return True, st.session_state.data
    return False, None


def data_source_selector() -> Optional[pd.DataFrame]:
    """
    Selector de fuente de datos (captura o CSV).
    
    Returns:
        DataFrame seleccionado o None
    """
    has_session_data, session_data = check_session_data()
    
    if has_session_data:
        st.info("✅ Usando datos de la captura de paquetes")
        st.markdown(
            '<div class="notification" style="background-color: #10B981; color: white;">'
            '✅ Datos capturados listos para predicción</div>',
            unsafe_allow_html=True
        )
        return session_data
    else:
        return upload_csv_file(key="csv_uploader_main")


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: list = None,
    min_rows: int = 1
) -> Tuple[bool, str]:
    """
    Validar DataFrame con reglas específicas.
    
    Args:
        df: DataFrame a validar
        required_columns: Lista de columnas requeridas
        min_rows: Número mínimo de filas
        
    Returns:
        Tuple (es_valido, mensaje_error)
    """
    if df is None:
        return False, "DataFrame es None"
    
    if df.empty:
        return False, "DataFrame está vacío"
    
    if len(df) < min_rows:
        return False, f"Se requieren al menos {min_rows} filas, se encontraron {len(df)}"
    
    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            return False, f"Columnas faltantes: {', '.join(missing)}"
    
    return True, ""


def show_dataframe_stats(df: pd.DataFrame) -> None:
    """
    Mostrar estadísticas básicas del DataFrame.
    
    Args:
        df: DataFrame a analizar
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Filas", f"{len(df):,}")
    with col2:
        st.metric("Columnas", f"{len(df.columns):,}")
    with col3:
        # Calcular valores faltantes
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("% Valores Faltantes", f"{missing_pct:.2f}%")
