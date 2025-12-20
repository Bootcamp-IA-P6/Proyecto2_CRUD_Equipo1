from pydantic import BaseModel
from typing import List, Optional

class PeliculaBase(BaseModel):
    titulo: str
    anio: Optional[int] = None
    descripcion: Optional[str] = None
    id_director: int

class PeliculaCreate(PeliculaBase):
    generos: List[int] = []  # lista de IDs de géneros

class Pelicula(PeliculaBase):
    id_pelicula: int
    generos: List[str] = []

    class Config:
        orm_mode = True
