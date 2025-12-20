from fastapi import FastAPI
from src.routes.pelicula_routes import router as pelicula_router

app = FastAPI()

app.include_router(pelicula_router)
