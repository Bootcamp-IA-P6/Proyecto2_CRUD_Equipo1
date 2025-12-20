from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.pelicula_schema import Pelicula, PeliculaCreate
from src.controllers.pelicula_controller import (
    crear_pelicula,
    obtener_peliculas,
    obtener_pelicula,
    eliminar_pelicula,
)

router = APIRouter(prefix="/peliculas", tags=["Películas"])

@router.post("/", response_model=Pelicula)
def create_pelicula(data: PeliculaCreate, db: Session = Depends(get_db)):
    return crear_pelicula(db, data)

@router.get("/", response_model=list[Pelicula])
def list_peliculas(db: Session = Depends(get_db)):
    return obtener_peliculas(db)

@router.get("/{id_pelicula}", response_model=Pelicula)
def get_pelicula(id_pelicula: int, db: Session = Depends(get_db)):
    pelicula = obtener_pelicula(db, id_pelicula)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula

@router.delete("/{id_pelicula}", response_model=Pelicula)
def delete_pelicula(id_pelicula: int, db: Session = Depends(get_db)):
    pelicula = eliminar_pelicula(db, id_pelicula)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula
