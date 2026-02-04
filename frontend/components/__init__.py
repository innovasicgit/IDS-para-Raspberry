"""
Componentes reutilizables del frontend.
"""

from .charts import (
    create_pie_chart,
    create_bar_chart,
    create_histogram,
    create_traffic_pattern_chart,
    create_comparison_bar_chart
)

from .metrics_display import (
    show_resource_metrics,
    show_prediction_summary,
    show_welcome_message,
    show_capture_status,
    show_dataset_info,
    create_metrics_card
)

from .data_uploader import (
    upload_csv_file,
    check_session_data,
    data_source_selector,
    validate_dataframe,
    show_dataframe_stats
)

from .sidebar import (
    render_model_selector,
    render_metric_selector,
    render_manual_capture_controls,
    render_auto_capture_controls,
    render_auto_capture_buttons,
    initialize_auto_capture_state
)

__all__ = [
    # Charts
    'create_pie_chart',
    'create_bar_chart',
    'create_histogram',
    'create_traffic_pattern_chart',
    'create_comparison_bar_chart',
    # Metrics
    'show_resource_metrics',
    'show_prediction_summary',
    'show_welcome_message',
    'show_capture_status',
    'show_dataset_info',
    'create_metrics_card',
    # Data
    'upload_csv_file',
    'check_session_data',
    'data_source_selector',
    'validate_dataframe',
    'show_dataframe_stats',
    # Sidebar
    'render_model_selector',
    'render_metric_selector',
    'render_manual_capture_controls',
    'render_auto_capture_controls',
    'render_auto_capture_buttons',
    'initialize_auto_capture_state',
]

