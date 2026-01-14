from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker   
from src.config import config_variables

settings = config_variables.Settings()
# Variables de entorno para no exponer información sensible
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_HOST = settings.DB_HOST
DB_NAME = settings.DB_NAME

# Conexión con la base de datos
DATABASE_URL = "mysql+pymysql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_HOST+"/"+DB_NAME+""  # MySQL

# Crea un engine
engine = create_engine(DATABASE_URL)

# Crea una clase para configurar la sesión
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea una clase base para los modelos
Base = declarative_base()

# función para obtener la sesión de la base de datos
def get_db():
    db = Session()  # Crea una nueva sesión
    try:
        yield db  # Usa la sesión
        print("DB session used")
    finally:
        db.close()  # Cierra la sesión al terminar
        print("DB session closed")