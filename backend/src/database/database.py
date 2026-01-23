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