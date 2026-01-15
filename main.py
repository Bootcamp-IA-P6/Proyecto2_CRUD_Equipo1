from fastapi import FastAPI
from src.database.database import engine
from src.database.base import Base

# 1. IMPORTAR TODOS LOS MODELOS
from src.models import users_model 

# 2. IMPORTAR ROUTERS
from src.routes import user_routes  
app = FastAPI(title="Catálogo de Películas AI")

# 3. CREAR TABLAS
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "API de Películas funcionando correctamente"}

# 4. INCLUIR ROUTERS
# Agregamos tus rutas. 
# Usamos prefix="/api/v1" por convención. La ruta final quedará: /api/v1/{Nombre de tu CRUD}/
app.include_router(user_routes.router, prefix="/api/v1")