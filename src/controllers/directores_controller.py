from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.peliculas_models import Director
from src.schemas.directores_schemas import DirectorCreate, DirectorUpdate

# --- CREATE ---
def create_director(db: Session, director: DirectorCreate):
    
    new_director = Director(
        nombre=director.nombre,
        anio_nacimiento=director.anio_nacimiento
    )
    db.add(new_director)
    db.commit()
    db.refresh(new_director)
    return new_director

# --- GET ONE ---
def get_director(db: Session, director_id: int):
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director no encontrado")
    return director

# --- GET ALL ---
def get_all_directores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Director).offset(skip).limit(limit).all()

# --- UPDATE  ---
def update_director(db: Session, director_id: int, director_update: DirectorUpdate):
    db_director = get_director(db, director_id)

    update_data = director_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_director, key, value)

    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director

# --- DELETE ---
def delete_director(db: Session, director_id: int):
    db_director = get_director(db, director_id)
    
    db.delete(db_director)
    db.commit()
    return db_director
