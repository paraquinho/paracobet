# Modelo de datos

Entidades centrales: `Sport`, `Country`, `Competition`, `Season`, `Team`, `Player`, `Venue`, `Match`, `MatchTeam`, `MatchStatistic`, `PlayerStatistic`, `Bookmaker`, `Market`, `MarketSelection`, `OddsSnapshot` y `DataProvider`.

`OddsSnapshot` es inmutable: cada actualización de una cuota inserta un registro con bookmaker, selección, línea, cuota, `observed_at`, `available_at` y fuente. Nunca se actualiza un snapshot histórico.

Los identificadores internos son UUIDs. Las claves externas viven en los adaptadores o en una tabla de mapeo que se añadirá al conectar un proveedor real.

En Fase 2, `Competition`, `Team` y `Match` conservan además `provider` y `external_id` con constraints únicos compuestos. Esto permite re-ejecutar ingestion sin duplicar entidades. `event_time` y `available_at` se mantienen separados en matches y estadísticas.
