from pydantic import BaseModel

class GeneroBase(BaseModel):
    nombre:str

class GeneroCreate(GeneroBase):
    pass

class GeneroUpdate(GeneroBase):
    pass

class GeneroResponse(GeneroBase):
    id: int
    
    class Config:
        from_attributes = True