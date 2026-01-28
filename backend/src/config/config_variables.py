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