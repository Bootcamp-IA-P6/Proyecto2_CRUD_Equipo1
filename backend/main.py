from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from src.database.database import engine
from src.database.base import Base

from src.routes import user_routes, directores_routes, genero_routes, peliculas_routes, auth_routes

app = FastAPI(title="Catálogo de Películas")

# --- CONFIGURACIÓN CORS (ANTES de cualquier ruta) ---
origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex="http://127\\.0\\.0\\.1.*",
)

Base.metadata.create_all(bind=engine)

# ← Crear carpeta si no existe
BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# ← Servir archivos estáticos ANTES de incluir routers
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

@app.get("/")
async def root():
    return {"message": "API de Películas funcionando correctamente"}

# Incluir Routers (DESPUÉS de CORS y static files)
app.include_router(auth_routes.router)
app.include_router(user_routes.router, prefix="/api/v1")
app.include_router(genero_routes.router, prefix="/api/v1")
app.include_router(directores_routes.router, prefix="/api/v1")
app.include_router(peliculas_routes.router, prefix="/api/v1")