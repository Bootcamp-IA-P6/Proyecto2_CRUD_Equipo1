
#### `./Proyecto2_CRUD_Equipo1/requirements.txt `

```Text
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.12.0
certifi==2026.1.4
click==8.3.1
colorama==0.4.6
dnspython==2.8.0
dotenv==0.9.9
email-validator==2.3.0
fastapi==0.125.0
fastapi-cli==0.0.20
fastapi-cloud-cli==0.11.0
fastar==0.8.0
greenlet==3.3.0
h11==0.16.0
httpcore==1.0.9
httptools==0.7.1
httpx==0.28.1
idna==3.11
iniconfig==2.3.0
itsdangerous==2.2.0
Jinja2==3.1.6
markdown-it-py==4.0.0
MarkupSafe==3.0.3
mdurl==0.1.2
orjson==3.11.5
packaging==25.0
passlib==1.7.4
pluggy==1.6.0
pydantic==2.12.5
pydantic-extra-types==2.11.0
pydantic-settings==2.12.0
pydantic_core==2.41.5
Pygments==2.19.2
PyMySQL==1.1.2
pytest==9.0.2
python-dotenv==1.2.1
python-multipart==0.0.21
PyYAML==6.0.3
rich==14.2.0
rich-toolkit==0.17.1
rignore==0.7.6
sentry-sdk==2.50.0
shellingham==1.5.4
SQLAlchemy==2.0.45
starlette==0.50.0
typer==0.21.1
typing-inspection==0.4.2
typing_extensions==4.15.0
ujson==5.11.0
urllib3==2.6.3
uvicorn==0.40.0
watchfiles==1.1.1
websockets==16.0

```

#### `./Proyecto2_CRUD_Equipo1/main.py `

```Python
from fastapi import FastAPI
from src.database.database import engine
from src.database.base import Base

# 1. IMPORTAR TODOS LOS MODELOS
from src.models import users_model 
from src.models import peliculas_models

# 2. IMPORTAR ROUTERS
from src.routes import user_routes  
from src.routes import directores_routes
from src.routes import genero_routes
from src.routes import peliculas_routes

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
app.include_router(genero_routes.router, prefix="/api/v1")
app.include_router(directores_routes.router, prefix="/api/v1")
app.include_router(peliculas_routes.router, prefix="/api/v1")

```

#### `./Proyecto2_CRUD_Equipo1/.env.example `

```Text
DB_USER=root
DB_PASSWORD=PASSWORD
DB_HOST=HOST
DB_NAME=DB_NAME
SECRET_KEY=supersecretkey
ALGORITHM=HS256

```

#### `./Proyecto2_CRUD_Equipo1/.gitignore `

```Text
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[codz]
*$py.class
.DS_Store
# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock
#poetry.toml

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#   pdm recommends including project-wide configuration in pdm.toml, but excluding .pdm-python.
#   https://pdm-project.org/en/latest/usage/project/#working-with-version-control
#pdm.lock
#pdm.toml
.pdm-python
.pdm-build/

# pixi
#   Similar to Pipfile.lock, it is generally recommended to include pixi.lock in version control.
#pixi.lock
#   Pixi creates a virtual environment in the .pixi directory, just like venv module creates one
#   in the .venv directory. It is recommended not to include this directory in version control.
.pixi

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# Abstra
# Abstra is an AI-powered process automation framework.
# Ignore directories containing user credentials, local state, and settings.
# Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#  Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#  that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#  and can be added to the global gitignore or merged into this file. However, if you prefer, 
#  you could uncomment the following to ignore the entire vscode folder
# .vscode/

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Cursor
#  Cursor is an AI-powered code editor. `.cursorignore` specifies files/directories to
#  exclude from AI features like autocomplete and code analysis. Recommended for sensitive data
#  refer to https://docs.cursor.com/context/ignore-files
.cursorignore
.cursorindexingignore

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/

```

#### `./Proyecto2_CRUD_Equipo1/src/__init__.py `

```Python

```

#### `./Proyecto2_CRUD_Equipo1/src/config/config_variables.py `

```Python
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
# Cargar variables de entorno desde el archivo .env
load_dotenv() 

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str
    
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings() #type: ignore
```

#### `./Proyecto2_CRUD_Equipo1/src/controllers/directores_controller.py `

```Python
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.peliculas_models import Director
from src.schemas.directores_schemas import DirectorCreate, DirectorUpdate
from typing import List
# --- CREATE ---
def create_director(db: Session, director: DirectorCreate):
    
    new_director = Director(
        nombre=director.nombre,
        anio_nacimiento=director.anio_nacimiento
    )
    db.add(new_director)
    db.commit()
    db.refresh(new_director)
    return new_director

def create_directores_bulk(db: Session, directores: List[DirectorCreate]):
    nuevos_directores = []

    for director in directores:
        nuevo = Director(
            nombre=director.nombre,
            anio_nacimiento=director.anio_nacimiento
        )
        db.add(nuevo)
        nuevos_directores.append(nuevo)

    db.commit()

    for director in nuevos_directores:
        db.refresh(director)

    return nuevos_directores

# --- GET ONE ---
def get_director(db: Session, director_id: int):
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director no encontrado")
    return director

# --- GET ALL ---
def get_all_directores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Director).offset(skip).limit(limit).all()

# --- UPDATE  ---
def update_director(db: Session, director_id: int, director_update: DirectorUpdate):
    db_director = get_director(db, director_id)

    update_data = director_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_director, key, value)

    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director

# --- DELETE ---
def delete_director(db: Session, director_id: int):
    db_director = get_director(db, director_id)
    
    db.delete(db_director)
    db.commit()
    return db_director

```

#### `./Proyecto2_CRUD_Equipo1/src/controllers/genero_controller.py `

```Python
from sqlalchemy.orm import Session
from src.schemas.genero_schemas import GeneroCreate, GeneroUpdate
from src.models.peliculas_models import Genero

def get_generos(db: Session):
    return db.query(Genero).all()

def get_genero_by_id(db: Session, genero_id:int):
    return db.query(Genero).filter(Genero.id == genero_id).first()

def create_genero(db: Session, genero: GeneroCreate):
    db_genero = Genero(**genero.model_dump())
    db.add(db_genero)
    db.commit()
    db.refresh(db_genero)
    return db_genero

def update_genero(db: Session, genero_id: int, genero: GeneroUpdate):
    db_genero = db.query(Genero).filter(Genero.id == genero_id).first()

    if not db_genero:
        return None

    if genero.nombre is not None:
        db_genero.nombre = genero.nombre

    db.commit()
    db.refresh(db_genero)
    return db_genero

    
def delete_genero(db: Session, genero_id: int):
    db_genero = db.query(Genero).filter(Genero.id == genero_id).first()

    if not db_genero:
        return None

    db.delete(db_genero)
    db.commit()
    return db_genero

        
```

#### `./Proyecto2_CRUD_Equipo1/src/controllers/peliculas_controller.py `

```Python
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

```

#### `./Proyecto2_CRUD_Equipo1/src/controllers/users_controller.py `

```Python
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.users_model import User
from src.schemas.users_schemas import UserCreate, UserUpdate
from src.utils.security import get_password_hash

# --- CREATE ---
def create_user(db: Session, user: UserCreate):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="El email ya existe")
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="El username ya existe")

    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- READ ONE ---
def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# --- READ ALL (Con paginación básica) ---
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# --- UPDATE (PATCH) ---
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    # 1. Buscar usuario
    db_user = get_user(db, user_id) 

    update_data = user_update.model_dump(exclude_unset=True)

    # 2. Validaciones extra si se cambia el email o username
    if "email" in update_data:
        check_email = db.query(User).filter(User.email == update_data["email"]).first()
        if check_email and check_email.id != user_id: #type: ignore
            raise HTTPException(status_code=400, detail="Ese email ya está siendo usado por otro usuario")

    if "username" in update_data:
        check_username = db.query(User).filter(User.username == update_data["username"]).first()
        if check_username and check_username.id != user_id: #type: ignore
            raise HTTPException(status_code=400, detail="Ese username ya está ocupado")

    # 3. Si se actualiza el password, hay que hashearlo de nuevo
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])

    # 4. Actualizar campos
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- DELETE (SOFT DELETE) ---
def soft_delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    
    # Simplemente cambiamos el estado
    db_user.is_active = False #type: ignore
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

#### `./Proyecto2_CRUD_Equipo1/src/database/base.py `

```Python
from sqlalchemy.orm import declarative_base
# Base para evitar importaciones circulares
Base = declarative_base()
```

#### `./Proyecto2_CRUD_Equipo1/src/database/database.py `

```Python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.config_variables import settings
from src.database.base import Base 

# Fíjate que añadimos :{settings.DB_PORT}
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### `./Proyecto2_CRUD_Equipo1/src/models/peliculas_models.py `

```Python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class Director(Base):
    __tablename__ = "directores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    anio_nacimiento = Column(Integer)
    
    peliculas = relationship("Pelicula", back_populates="director")
    
class Genero(Base):
    __tablename__ = "generos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

class Pelicula(Base):
    __tablename__ = "peliculas"

    id = Column(Integer, primary_key=True, index=True)
    id_director = Column(Integer, ForeignKey("directores.id"))
    titulo = Column(String(100), index=True, nullable=False)
    anio = Column(Integer)
    descripcion = Column(String(200))

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
```

#### `./Proyecto2_CRUD_Equipo1/src/models/users_model.py `

```Python
import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum as SqlEnum
from src.database.base import Base

# Definimos los roles disponibles.
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CLIENTE = "cliente"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False) # Guardará el Hash
    role = Column(SqlEnum(UserRole), default=UserRole.CLIENTE, nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User {self.username} - {self.role}>"
```

#### `./Proyecto2_CRUD_Equipo1/src/routes/directores_routes.py `

```Python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.directores_schemas import DirectorCreate, DirectorResponse, DirectorUpdate
from src.controllers import directores_controller

router = APIRouter(prefix="/directores", tags=["Directores"])

# 1. Crear Director
@router.post("/", response_model=DirectorResponse, status_code=status.HTTP_201_CREATED)
def create_director(director: DirectorCreate, db: Session = Depends(get_db)):
    return directores_controller.create_director(db, director)

@router.post("/bulk",response_model=List[DirectorResponse],status_code=status.HTTP_201_CREATED)
def create_directores_bulk(
    directores: List[DirectorCreate],
    db: Session = Depends(get_db)
):
    return directores_controller.create_directores_bulk(db, directores)

# 2. Obtener todos (Lista)
@router.get("/", response_model=List[DirectorResponse])
def read_directores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return directores_controller.get_all_directores(db, skip=skip, limit=limit)

# 3. Obtener uno por ID
@router.get("/{director_id}", response_model=DirectorResponse)
def read_director(director_id: int, db: Session = Depends(get_db)):
    return directores_controller.get_director(db, director_id)

# 4. Actualizar Director (PATCH)
@router.patch("/{director_id}", response_model=DirectorResponse)
def update_director(director_id: int, director_update: DirectorUpdate, db: Session = Depends(get_db)):
    return directores_controller.update_director(db, director_id, director_update)

# 5. Eliminar Director
@router.delete("/{director_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_director(director_id: int, db: Session = Depends(get_db)):
    directores_controller.delete_director(db, director_id)
    return 

```

#### `./Proyecto2_CRUD_Equipo1/src/routes/genero_routes.py `

```Python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.controllers import genero_controller
from src.schemas.genero_schemas import GeneroCreate, GeneroUpdate, GeneroResponse 

router = APIRouter(prefix="/generos", tags=["Generos"])

@router.get("/", response_model=list[GeneroResponse])
def get_generos(db: Session = Depends(get_db)):
    return genero_controller.get_generos(db)

@router.get("/{genero_id}", response_model=GeneroResponse)
def get_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = genero_controller.get_genero_by_id(db, genero_id)
    if not genero:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return genero

@router.post("/", response_model=GeneroResponse)
def create_genero(genero: GeneroCreate, db: Session = Depends(get_db)):
    return genero_controller.create_genero(db, genero)

@router.put("/{genero_id}", response_model=GeneroResponse)
def update_genero(genero_id: int, genero: GeneroUpdate, db: Session = Depends(get_db)):
    genero_actualizado = genero_controller.update_genero(db, genero_id, genero)
    if not genero_actualizado:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return genero_actualizado

@router.delete("/{genero_id}")
def delete_genero(genero_id: int, db: Session = Depends(get_db)):
    genero_eliminado = genero_controller.delete_genero(db, genero_id)
    if not genero_eliminado:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return {"message": "Género eliminado correctamente"}

```

#### `./Proyecto2_CRUD_Equipo1/src/routes/peliculas_routes.py `

```Python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.peliculas_schemas import PeliculaCreate, PeliculaResponse, PeliculaUpdate
from src.controllers import peliculas_controller

router = APIRouter(prefix="/peliculas", tags=["Peliculas"])

# 1. Crear Pelicula
@router.post("/", response_model=PeliculaResponse, status_code=status.HTTP_201_CREATED)
def create_pelicula(pelicula: PeliculaCreate, db: Session = Depends(get_db)):
    return peliculas_controller.create_pelicula(db, pelicula)

@router.post("/bulk", response_model=List[PeliculaResponse], status_code=status.HTTP_201_CREATED)
def create_pelicula_bulk(peliculas: List[PeliculaCreate], db: Session = Depends(get_db)):
    return peliculas_controller.create_pelicula_bulk(db, peliculas)

# 2. Obtener todas (Lista)
@router.get("/", response_model=List[PeliculaResponse])
def read_peliculas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return peliculas_controller.get_all_peliculas(db, skip=skip, limit=limit)

# 3. Obtener una por ID
@router.get("/{pelicula_id}", response_model=PeliculaResponse)
def read_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    return peliculas_controller.get_pelicula(db, pelicula_id)

# 4. Actualizar Pelicula (PATCH)
@router.patch("/{pelicula_id}", response_model=PeliculaResponse)
def update_pelicula(pelicula_id: int, pelicula_update: PeliculaUpdate, db: Session = Depends(get_db)):
    return peliculas_controller.update_pelicula(db, pelicula_id, pelicula_update)

# 5. Eliminar Pelicula
@router.delete("/{pelicula_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    peliculas_controller.delete_pelicula(db, pelicula_id)
    return

```

#### `./Proyecto2_CRUD_Equipo1/src/routes/user_routes.py `

```Python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.users_schemas import UserCreate, UserResponse, UserUpdate
from src.controllers import users_controller

router = APIRouter(prefix="/users", tags=["Users"])

# 1. Crear Usuario
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return users_controller.create_user(db, user)

# 2. Obtener todos (Lista)
@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return users_controller.get_all_users(db, skip=skip, limit=limit)

# 3. Obtener uno por ID
@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return users_controller.get_user(db, user_id)

# 4. Actualizar Usuario (PATCH)
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Actualiza parcialmente al usuario (envía solo los campos que quieras cambiar)"""
    return users_controller.update_user(db, user_id, user_update)

# 5. Eliminar Usuario (Soft Delete)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Desactiva al usuario (is_active = False)"""
    users_controller.soft_delete_user(db, user_id)
    return # 204 No Content no devuelve body
```

#### `./Proyecto2_CRUD_Equipo1/src/schemas/directores_schemas.py `

```Python
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

```

#### `./Proyecto2_CRUD_Equipo1/src/schemas/genero_schemas.py `

```Python
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
```

#### `./Proyecto2_CRUD_Equipo1/src/schemas/peliculas_schemas.py `

```Python
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

```

#### `./Proyecto2_CRUD_Equipo1/src/schemas/users_schemas.py `

```Python
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from src.models.users_model import UserRole

# --- Bases y Creación ---
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: Optional[UserRole] = UserRole.CLIENTE

# --- Schema para Actualización (PATCH) ---
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# --- Respuesta ---
class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
```

#### `./Proyecto2_CRUD_Equipo1/src/utils/security.py `

```Python
from passlib.context import CryptContext

# Configuramos passlib para usar bcrypt, que es robusto y lento (bueno contra fuerza bruta)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña plana con su hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña."""
    return pwd_context.hash(password)
```

