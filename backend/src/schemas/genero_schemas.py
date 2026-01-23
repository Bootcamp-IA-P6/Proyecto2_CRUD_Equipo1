from pydantic import BaseModel
from typing import Optional

class GeneroBase(BaseModel):
    nombre:str

class GeneroCreate(GeneroBase):
    pass

class GeneroUpdate(GeneroBase):
    nombre: Optional[str] = None

class GeneroResponse(GeneroBase):
    id: int
    
    class Config:
        from_attributes = True