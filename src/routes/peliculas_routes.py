from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.peliculas_schemas import PeliculaCreate, PeliculaResponse, PeliculaUpdate
from src.controllers import peliculas_controller

router = APIRouter(prefix="/peliculas", tags=["Peliculas"])

# 1. Crear Pelicula
@router.post("/", response_model=PeliculaResponse, status_code=status.HTTP_201_CREATED)
def create_pelicula(pelicula: PeliculaCreate, db: Session = Depends(get_db)):
    return peliculas_controller.create_pelicula(db, pelicula)

@router.post("/bulk", response_model=List[PeliculaResponse], status_code=status.HTTP_201_CREATED)
def create_pelicula_bulk(peliculas: List[PeliculaCreate], db: Session = Depends(get_db)):
    return peliculas_controller.create_pelicula_bulk(db, peliculas)

# 2. Obtener todas (Lista)
@router.get("/", response_model=List[PeliculaResponse])
def read_peliculas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return peliculas_controller.get_all_peliculas(db, skip=skip, limit=limit)

# 3. Obtener una por ID
@router.get("/{pelicula_id}", response_model=PeliculaResponse)
def read_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    return peliculas_controller.get_pelicula(db, pelicula_id)

# 4. Actualizar Pelicula (PATCH)
@router.patch("/{pelicula_id}", response_model=PeliculaResponse)
def update_pelicula(pelicula_id: int, pelicula_update: PeliculaUpdate, db: Session = Depends(get_db)):
    return peliculas_controller.update_pelicula(db, pelicula_id, pelicula_update)

# 5. Eliminar Pelicula
@router.delete("/{pelicula_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    peliculas_controller.delete_pelicula(db, pelicula_id)
    return
