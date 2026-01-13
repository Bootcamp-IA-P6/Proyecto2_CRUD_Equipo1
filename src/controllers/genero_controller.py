from sqlalchemy.orm import Session
from schemas import genero_schema
from models.peliculas_models import Genero

def get_generos(db: Session):
    return db.query(Genero).all()


def get_genero_by_id(db: Session, genero_id:int):
    return db.query(Genero).filter(Genero.id == genero_id).first()

def create_genero(db: Session, genero: genero_schema.GeneroCreate):
    db_genero = Genero(**genero.dict())
    db.add(db_genero)
    db.commit()
    db.refresh(db_genero)
    return db_genero 

def update_genero(db: Session, genero_id:int, genero: genero_schema.GeneroUpdate):
    db_genero = db.query(Genero).filter(Genero.id == genero_id).first()
    
    if not db_genero:
        return None 
    
    db_genero.nombre = genero.nombre
    db.commit()
    db.refresh(db_genero)
    return db_genero
    

def delete_genero(db: Session, genero_id: int):
    db_genero = db.query(Genero).filter(Genero.id == genero_id).first()

    if not db_genero:
        return None

    db.delete(db_genero)
    db.commit()
    return db_genero

        