from sqlalchemy.orm import Session
from src.models.pelicula_model import Pelicula
from src.models.genero_model import Genero
from src.schemas.pelicula_schema import PeliculaCreate

def crear_pelicula(db: Session, data: PeliculaCreate):
    pelicula = Pelicula(
        titulo=data.titulo,
        anio=data.anio,
        descripcion=data.descripcion,
        id_director=data.id_director
    )

    # Relación many-to-many con géneros
    if data.generos:
        generos = db.query(Genero).filter(Genero.id_genero.in_(data.generos)).all()
        pelicula.generos.extend(generos)

    db.add(pelicula)
    db.commit()
    db.refresh(pelicula)
    return pelicula

def obtener_peliculas(db: Session):
    return db.query(Pelicula).all()

def obtener_pelicula(db: Session, id_pelicula: int):
    return db.query(Pelicula).filter(Pelicula.id_pelicula == id_pelicula).first()

def eliminar_pelicula(db: Session, id_pelicula: int):
    pelicula = obtener_pelicula(db, id_pelicula)
    if pelicula:
        db.delete(pelicula)
        db.commit()
    return pelicula
