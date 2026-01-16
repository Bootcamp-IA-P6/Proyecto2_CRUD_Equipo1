from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class DirectorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    anio_nacimiento: Optional[int] = None

class DirectorCreate(DirectorBase):
    pass

class DirectorUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    anio_nacimiento: Optional[int] = None

class DirectorResponse(DirectorBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
