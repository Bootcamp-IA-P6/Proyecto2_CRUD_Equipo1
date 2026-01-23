from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.peliculas_models import Pelicula, Director, Genero
from src.schemas.peliculas_schemas import PeliculaCreate, PeliculaUpdate
from typing import List

# --- CREATE ---
def create_pelicula(db: Session, pelicula: PeliculaCreate):
    db_director = db.query(Director).filter(Director.id == pelicula.id_director).first()
    if not db_director:
        raise HTTPException(status_code=404, detail="Director no encontrado")

    new_pelicula = Pelicula(
        titulo=pelicula.titulo,
        anio=pelicula.anio,
        descripcion=pelicula.descripcion,
        id_director=pelicula.id_director
    )

    if pelicula.generos:
        db_generos = db.query(Genero).filter(Genero.id.in_(pelicula.generos)).all()
        
        if len(db_generos) != len(pelicula.generos):
            raise HTTPException(status_code=404, detail="Uno o más géneros no existen")
            
        new_pelicula.generos.extend(db_generos)

    db.add(new_pelicula)
    db.commit()
    db.refresh(new_pelicula)
    return new_pelicula

def create_pelicula_bulk(db: Session, peliculas: List[create_pelicula]):
    nuevas_peliculas = []

    for pelicula in peliculas:
        new_pelicula = Pelicula(
            titulo=pelicula.titulo,
            anio=pelicula.anio,
            descripcion=pelicula.descripcion,
            id_director=pelicula.id_director
    )

        db.add(new_pelicula)
        nuevas_peliculas.append(new_pelicula)

    db.commit()

    for pelicula in nuevas_peliculas:
        db.refresh(pelicula)

    return nuevas_peliculas


# --- READ ONE ---
def get_pelicula(db: Session, pelicula_id: int):
    pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula

# --- READ ALL ---
def get_all_peliculas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pelicula).offset(skip).limit(limit).all()

# --- UPDATE (PATCH) ---
def update_pelicula(db: Session, pelicula_id: int, pelicula_update: PeliculaUpdate):
    db_pelicula = get_pelicula(db, pelicula_id)

    update_data = pelicula_update.model_dump(exclude_unset=True)

    if "id_director" in update_data:
        director_exists = db.query(Director).filter(Director.id == update_data["id_director"]).first()
        if not director_exists:
            raise HTTPException(status_code=404, detail="El nuevo Director no existe")
    if "generos" in update_data:
        generos_ids = update_data.pop("generos") # Sacamos genéros del dict para tratarlos manual
        if generos_ids is not None:
             db_generos = db.query(Genero).filter(Genero.id.in_(generos_ids)).all()
             if len(db_generos) != len(generos_ids):
                 raise HTTPException(status_code=404, detail="Uno o más géneros no existen")
             
             db_pelicula.generos = db_generos 

    for key, value in update_data.items():
        setattr(db_pelicula, key, value)

    db.add(db_pelicula)
    db.commit()
    db.refresh(db_pelicula)
    return db_pelicula

# --- DELETE ---
def delete_pelicula(db: Session, pelicula_id: int):
    db_pelicula = get_pelicula(db, pelicula_id)
    
    db.delete(db_pelicula)
    db.commit()
    return db_pelicula
