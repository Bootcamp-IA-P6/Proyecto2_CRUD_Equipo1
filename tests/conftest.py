import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import database
from src.database.base import Base

# Importar modelos para que se registren en Base.metadata
from src.models import users_model, peliculas_models

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# PATCH ENGINE GLOBALLY BEFORE IMPORTING MAIN
database.engine = engine
database.SessionLocal = TestingSessionLocal

from main import app
from src.database.database import get_db
# (Asegúrate de importar los demás modelos si existen: directores, generos, etc.)
# Si no están importados en main.py o aquí, create_all no creará sus tablas.

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Crea una nueva base de datos en memoria para cada test,
    crea las tablas y luego las elimina al finalizar.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Sobrescribe la dependencia get_db para usar la sesión de test
    y devuelve un TestClient de FastAPI.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass # db_session se cierra en el fixture db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
