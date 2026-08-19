# Despliegue

## Desarrollo

El entorno local usa Docker Compose con PostgreSQL, FastAPI y Next.js. La API ejecuta `alembic upgrade head` y el seed mock al arrancar el contenedor. El seed es idempotente y sólo agrega datos identificados como `mock`.

## Producción propuesta

```text
GitHub -> Vercel (apps/web) -> Render Web Service (Docker) -> Supabase PostgreSQL
```

Supabase no requiere un SDK especial: se utiliza su cadena PostgreSQL estándar en `DATABASE_URL`, manteniendo SQLAlchemy y Alembic portables. En Supabase crea un proyecto, copia la connection string de PostgreSQL/pooled connection y configúrala como `DATABASE_URL` en el servicio FastAPI. Ejecuta `alembic upgrade head` como paso de release; no uses el seed mock en producción.

En Vercel configura `NEXT_PUBLIC_API_URL` con la URL pública del backend FastAPI. En el backend configura `CORS_ORIGINS` con el dominio de Vercel y, sólo cuando exista un proveedor real, sus claves `SPORTS_PROVIDER_API_KEY` y `ODDS_PROVIDER_API_KEY`.

### Backend en Render

El repositorio incluye `render.yaml` como configuración opcional. Crea un Web Service desde GitHub usando Docker, conserva el contexto `apps/api`, configura `DATABASE_URL` y `CORS_ORIGINS` como variables del servicio, y usa `/health/db` como health check. El contenedor ejecuta `alembic upgrade head` y luego Uvicorn sin `--reload`, sin seed mock y escuchando el `PORT` que Render inyecta.

Render es la opción más sencilla para esta etapa porque despliega directamente el Dockerfile desde GitHub, ofrece una URL pública `onrender.com`, variables secretas y health checks HTTP. El plan gratuito puede dormir tras inactividad; para una API productiva con latencia estable conviene un servicio de pago básico.

No hay URLs, contraseñas ni tokens reales en este repositorio. La creación de cuentas, proyectos cloud y configuración de secretos requiere una acción del propietario.
