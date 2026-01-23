from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.directores_schemas import DirectorCreate, DirectorResponse, DirectorUpdate
from src.controllers import directores_controller

router = APIRouter(prefix="/directores", tags=["Directores"])

# 1. Crear Director
@router.post("/", response_model=DirectorResponse, status_code=status.HTTP_201_CREATED)
def create_director(director: DirectorCreate, db: Session = Depends(get_db)):
    return directores_controller.create_director(db, director)

# 2. Obtener todos (Lista)
@router.get("/", response_model=List[DirectorResponse])
def read_directores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return directores_controller.get_all_directores(db, skip=skip, limit=limit)

# 3. Obtener uno por ID
@router.get("/{director_id}", response_model=DirectorResponse)
def read_director(director_id: int, db: Session = Depends(get_db)):
    return directores_controller.get_director(db, director_id)

# 4. Actualizar Director (PATCH)
@router.patch("/{director_id}", response_model=DirectorResponse)
def update_director(director_id: int, director_update: DirectorUpdate, db: Session = Depends(get_db)):
    return directores_controller.update_director(db, director_id, director_update)

# 5. Eliminar Director
@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_director(director_id: int, db: Session = Depends(get_db)):
    directores_controller.delete_director(db, director_id)
    return 
