# Desarrollo

1. Copia `.env.example` como `.env` y ajusta sólo valores locales.
2. Ejecuta `docker compose up --build`.
3. API: `http://localhost:8000/docs`; web: `http://localhost:3000/dashboard`.

Para trabajo sin Docker instala dependencias de `apps/api` y `apps/web`, inicia PostgreSQL y ejecuta `alembic upgrade head` desde `apps/api` antes de arrancar la API. En Docker, la API aplica esa migración automáticamente antes de iniciar Uvicorn.

Los datos de demostración son sintéticos. No añadas datos de producción a `data/raw` ni secretos al repositorio.
