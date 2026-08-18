# ParacoBet

Plataforma privada de análisis deportivo cuantitativo. Convierte datos normalizados en estadísticas explicables, probabilidades, cuota implícita, edge, EV y análisis de parlays. No es una casa de apuestas.

## Arquitectura

- `apps/web`: Next.js, TypeScript y Tailwind; interfaz de terminal analítica.
- `apps/api`: FastAPI, SQLAlchemy, Alembic y servicios cuantitativos.
- `data/fixtures`: datos sintéticos de desarrollo.
- `docs`: decisiones de arquitectura, modelo y prevención de leakage.
- `docs/deployment.md`: despliegue propuesto GitHub → Vercel → FastAPI → Supabase.

Los proveedores se integran mediante adaptadores. El MVP usa `MockDataProvider`, por lo que no requiere claves externas.

La Fase 2 añade contratos `SportsProvider`/`OddsProvider`, pipeline fetch → validation → normalization → persistence, identidades externas `(provider, external_id)`, seed idempotente y repositorio de lectura PostgreSQL con fallback de desarrollo cuando la base no está disponible.

## Inicio rápido

```bash
cp .env.example .env
docker compose up --build
```

Dashboard: `http://localhost:3000/dashboard` · documentación API: `http://localhost:8000/docs`.

## Tests y calidad

```bash
make test-api
make test-web
make lint-api
make lint-web
```

Seed local (con PostgreSQL disponible): `python apps/api/scripts/seed_mock.py` o `./scripts/seed-mock.ps1`.

También pueden ejecutarse directamente desde cada aplicación. `.env` está ignorado y `.env.example` no contiene secretos.

## Producción y Supabase

Supabase se consume como PostgreSQL estándar: configura su connection string como `DATABASE_URL` y conserva SQLAlchemy/Alembic. `NEXT_PUBLIC_API_URL` apunta al backend cloud y `CORS_ORIGINS` al dominio web. Consulta [docs/deployment.md](docs/deployment.md) para los pasos que requieren cuentas externas.

## Alcance MVP

Incluye partidos, estadísticas, mercados y cuotas mock, analytics básicos y análisis de parlays bajo una aproximación explícita de independencia. Quedan para fases posteriores: ingesta de proveedores reales, modelos calibrados, correcciones de dependencia, constructor combinatorio y motor de backtesting completo.
