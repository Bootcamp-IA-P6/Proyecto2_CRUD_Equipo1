from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Base de datos
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 3306 # Puerto por defecto de MySQL
    DB_NAME: str

    # Seguridad (Auth)
    SECRET_KEY: str
    ALGORITHM: str

settings = Settings()