# Arquitectura

ParacoBet usa un monorepo con una aplicación Next.js, una API FastAPI y PostgreSQL. El dominio no conoce proveedores externos: un adaptador implementa el contrato `SportsDataProvider`, normaliza respuestas y los servicios consumen esos modelos internos.

```text
Proveedor -> Adapter -> modelos normalizados -> repositorio/BD -> servicios -> API -> web
```

En esta fase `MockDataProvider` es la implementación activa. Produce datos sintéticos identificados por `source=mock`; sustituirlo por Betano u otro proveedor requiere un nuevo adaptador, no cambios en analytics ni en el frontend.

La Fase 2 separa contratos de deportes y cuotas (`app/providers/contracts.py`) del pipeline de ingestion (`fetch`, validación Pydantic, normalización y persistencia). Los registros externos se identifican con `provider + external_id`, y el repositorio PostgreSQL se usa cuando está disponible; la API cae al proveedor mock sólo para que el desarrollo siga funcionando sin base local.

La capa `analytics` contiene cálculos puros y testeables. Las rutas sólo validan transporte HTTP y delegan en servicios.
