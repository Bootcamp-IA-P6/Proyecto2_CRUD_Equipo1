from sqlalchemy.orm import Session
from src.schemas.genero_schemas import GeneroCreate, GeneroUpdate
from src.models.peliculas_models import Genero

def get_generos(db: Session):
    return db.query(Genero).all()


def get_genero_by_id(db: Session, genero_id:int):
    return db.query(Genero).filter(Genero.id == genero_id).first()

def create_genero(db: Session, genero: GeneroCreate):
    db_genero = Genero(**genero.model_dump())
    db.add(db_genero)
    db.commit()
    db.refresh(db_genero)
    return db_genero

def update_genero(db: Session, genero_id: int, genero: GeneroUpdate):
    db_genero = db.query(Genero).filter(Genero.id == genero_id).first()

    if not db_genero:
        return None

    if genero.nombre is not None:
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

        