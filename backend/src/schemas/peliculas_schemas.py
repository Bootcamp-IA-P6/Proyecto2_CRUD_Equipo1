from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

# --- Bases y Creación ---
class PeliculaBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=100)
    anio: Optional[int] = None
    descripcion: Optional[str] = Field(None, max_length=200)

class PeliculaCreate(PeliculaBase):
    id_director: int
    generos: Optional[List[int]] = [] 

# --- Schema para Actualización (PATCH) ---
class PeliculaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=100)
    anio: Optional[int] = None
    descripcion: Optional[str] = Field(None, max_length=200)
    id_director: Optional[int] = None
    generos: Optional[List[int]] = None 

# --- Respuesta ---
class PeliculaResponse(PeliculaBase):
    id: int
    id_director: int
    
    model_config = ConfigDict(from_attributes=True)
