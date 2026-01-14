from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class Director(Base):
    __tablename__ = "directores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    anio_nacimiento = Column(Integer)
    
    peliculas = relationship("Pelicula", back_populates="director")
    
class Genero(Base):
    __tablename__ = "generos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

class Pelicula(Base):
    __tablename__ = "peliculas"

    id = Column(Integer, primary_key=True, index=True)
    id_director = Column(Integer, ForeignKey("directores.id"))
    titulo = Column(String, index=True, nullable=False)
    anio = Column(Integer)
    descripcion = Column(String)

    director = relationship("Director", back_populates="peliculas")
    generos = relationship(
        "Genero",
        secondary="peliculas_genero",
        backref="peliculas"
    )

class PeliculasGenero(Base):
    __tablename__ = "peliculas_genero"
    
    id = Column(Integer, primary_key=True, index=True)
    id_pelicula = Column(Integer, ForeignKey("peliculas.id"))
    id_genero = Column(Integer, ForeignKey("generos.id"))