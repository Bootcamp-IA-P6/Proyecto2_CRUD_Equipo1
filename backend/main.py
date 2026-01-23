from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.database import engine
from src.database.base import Base

from src.routes import user_routes, directores_routes, genero_routes, peliculas_routes, auth_routes # Importar auth

app = FastAPI(title="Catálogo de Películas AI")

# --- CONFIGURACIÓN CORS ---
origins = [
    "http://localhost",
    "http://localhost:5500", # Puerto común de Live Server
    "http://127.0.0.1:5500",
    "null" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "API de Películas funcionando correctamente"}

# Incluir Routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router, prefix="/api/v1")
app.include_router(genero_routes.router, prefix="/api/v1")
app.include_router(directores_routes.router, prefix="/api/v1")
app.include_router(peliculas_routes.router, prefix="/api/v1")