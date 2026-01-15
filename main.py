from fastapi import FastAPI
from src.database.database import engine
from src.database.base import Base

# Importar modelos para que SQLAlchemy los reconozca al crear tablas (Insertar todas las necesarias)
from src.models import peliculas_models

# Importar tus routers cuando estén listos
from src.routes import directores_routes 

app = FastAPI(title="Catálogo de Películas AI")

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "API de Películas funcionando correctamente"}

app.include_router(directores_routes.router)
