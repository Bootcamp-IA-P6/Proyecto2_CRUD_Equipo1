from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.schemas.genero_schemas import GeneroCreate, GeneroUpdate
from src.models.peliculas_models import Genero

def get_generos(db: Session):
    return db.query(Genero).all()

def get_genero_by_id(db: Session, genero_id:int):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()
    if not genero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Género no encontrado")
    return genero
 

def create_genero(db: Session, genero: GeneroCreate):
    genero_existente = db.query(Genero).filter(
            Genero.nombre == genero.nombre).first()
            
    if genero_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un género con ese nombre"
        )
        
    new_genero = Genero(**genero.model_dump())
    db.add(new_genero)
    db.commit()
    db.refresh(new_genero)
    return new_genero

def update_genero(db: Session, genero_id: int, genero: GeneroUpdate):
    db_genero = get_genero_by_id(db, genero_id)
    
    update_data = genero.model_dump(exclude_unset=True)
    
    if "nombre" in update_data:
        genero_existente = db.query(Genero).filter(
            Genero.nombre == update_data["nombre"],
            Genero.id != genero_id
            ).first()
        if genero_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Ya existe otro género con ese nombre"
            )
    for key, value in update_data.items():
        setattr(db_genero, key, value)
        
    db.commit()
    db.refresh(db_genero)
    return db_genero

    
def delete_genero(db: Session, genero_id: int):
    db_genero = get_genero_by_id(db, genero_id)
    db.delete(db_genero)
    db.commit()
    
        