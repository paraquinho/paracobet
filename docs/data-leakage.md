# Prevención de data leakage

Toda observación predictiva debe conservar:

- `event_time`: cuándo ocurrió el evento deportivo.
- `available_at`: cuándo el sistema pudo conocer el dato.
- `source`: origen del dato.
- `methodology_version`: versión de proveedor, transformación o modelo.

Un backtest sólo puede usar registros cuyo `available_at` sea anterior o igual al instante de predicción. Los resultados, estadísticas finales y cuotas posteriores no pueden filtrarse hacia atrás. Esta condición debe ser aplicada en los repositorios de entrenamiento y evaluada en cada motor de backtesting futuro.
