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