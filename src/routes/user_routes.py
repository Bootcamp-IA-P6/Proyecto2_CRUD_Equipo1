from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.users_schemas import UserCreate, UserResponse, UserUpdate
from src.controllers import users_controller

router = APIRouter(prefix="/users", tags=["Users"])

# 1. Crear Usuario
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, responses={
    409: {"description": "Email o username ya existe"},
    422: {"description": "Datos inválidos"}
})
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario"""
    return users_controller.create_user(db, user)

# 2. Obtener todos (Lista)
@router.get("/", response_model=List[UserResponse],status_code=status.HTTP_200_OK)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return users_controller.get_all_users(db, skip=skip, limit=limit)

# 3. Obtener uno por ID
@router.get("/{user_id}", response_model=UserResponse,status_code=status.HTTP_200_OK, responses={
    404:{"description": "Usuario no encontrado"}
})
def read_user(user_id: int, db: Session = Depends(get_db)):
    return users_controller.get_user(db, user_id)

# 4. Actualizar Usuario (PATCH)
@router.patch("/{user_id}", response_model=UserResponse, responses={
    404: {"description": "Usuario no encontrado"},
    409: {"description": "Email o username duplicado"},
    422: {"description": "Datos inválidos"}
}
)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Actualiza parcialmente al usuario (envía solo los campos que quieras cambiar)"""
    return users_controller.update_user(db, user_id, user_update)

# 5. Eliminar Usuario (Soft Delete)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,responses={
    404: {"description": "Usuario no encontrado"}
})
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Desactiva al usuario (is_active = False)"""
    users_controller.soft_delete_user(db, user_id)
    return # 204 No Content no devuelve body