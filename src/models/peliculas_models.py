from sqlalchemy import Column, Integer, String, ForeignKey
from database.database import Base


class Director(Base):
    __tablename__ = "directores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    anio_nacimiento = Column(Integer)


class Genero(Base):
    __tablename__= "generos"
    id= Column(Integer)
    nombre= Column(String)
    

class Pelicula(Base):
    __tablename__= "peliculas"
    id = Column(Integer, primary_key=True, index=True)
    id_director = Column(Integer, ForeignKey("directores.id"), index=True )
    titulo = Column(String, index=True)
    anio = Column(Integer, index=True)
    descripcion = Column(String)
    

class Peliculas_genero(Base):
    __tablemame__= "peliculas_genero"
    id_pelicula= Column(Integer, ForeignKey("peliculas.id"), index=True)
    id_genero= Column(Integer, ForeignKey("genero.id"), index=True)
    



    