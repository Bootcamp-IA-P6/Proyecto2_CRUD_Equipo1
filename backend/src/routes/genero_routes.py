from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.controllers import genero_controller
from src.schemas.genero_schemas import GeneroCreate, GeneroUpdate, GeneroResponse 

router = APIRouter(prefix="/generos", tags=["Generos"])

@router.get("/", response_model=list[GeneroResponse])
def get_generos(db: Session = Depends(get_db)):
    return genero_controller.get_generos(db)

@router.get("/{genero_id}", response_model=GeneroResponse)
def get_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = genero_controller.get_genero_by_id(db, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return genero

@router.post("/", response_model=GeneroResponse)
def create_genero(genero: GeneroCreate, db: Session = Depends(get_db)):
    return genero_controller.create_genero(db, genero)

@router.put("/{genero_id}", response_model=GeneroResponse)
def update_genero(genero_id: int, genero: GeneroUpdate, db: Session = Depends(get_db)):
    genero_actualizado = genero_controller.update_genero(db, genero_id, genero)
    if not genero_actualizado:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return genero_actualizado

@router.delete("/{genero_id}")
def delete_genero(genero_id: int, db: Session = Depends(get_db)):
    genero_eliminado = genero_controller.delete_genero(db, genero_id)
    if not genero_eliminado:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return {"message": "Género eliminado correctamente"}
