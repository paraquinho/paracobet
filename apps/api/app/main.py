from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import catalog, health, matches, parlay
from app.core.config import cors_origin_list

app = FastAPI(title="ParacoBet API", version="0.1.0", description="Synthetic data analytics MVP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origin_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router)
app.include_router(matches.router, prefix="/api/v1")
app.include_router(matches.teams_router, prefix="/api/v1")
app.include_router(catalog.router, prefix="/api/v1")
app.include_router(parlay.router, prefix="/api/v1")
