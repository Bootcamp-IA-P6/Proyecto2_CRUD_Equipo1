from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.controllers import genero_controller
from src.schemas.genero_schemas import GeneroCreate, GeneroUpdate, GeneroResponse 

router = APIRouter(prefix="/generos", tags=["Generos"])

@router.get("/", response_model=list[GeneroResponse])
def get_generos(db: Session = Depends(get_db)):
    return genero_controller.get_generos(db)

@router.get("/{genero_id}", response_model=GeneroResponse, responses={
    404: {"description": "Género no encontrado"}
})
def get_genero(genero_id: int, db: Session = Depends(get_db)):
    return genero_controller.get_genero_by_id(db, genero_id)

@router.post("/", response_model=GeneroResponse, status_code=status.HTTP_201_CREATED, responses={
    409: {"description": "Ya existe un género con ese nombre"},
    422: {"description": "Datos inválidos"}
})
def create_genero(genero: GeneroCreate, db: Session = Depends(get_db)):
    return genero_controller.create_genero(db, genero)

@router.put("/{genero_id}", response_model=GeneroResponse, responses={
    404: {"description": "Género no encontrado"},
    409: {"description": "Nombre de género duplicado"},
    422: {"description": "Datos inválidos"}
})
def update_genero(genero_id: int, genero: GeneroUpdate, db: Session = Depends(get_db)):
    return genero_controller.update_genero(db, genero_id, genero)
    

@router.delete("/{genero_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    404: {"description": "Género no encontrado"}
} )
def delete_genero(genero_id: int, db: Session = Depends(get_db)):
    genero_controller.delete_genero(db, genero_id)
    
