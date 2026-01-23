from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.users_model import User
from src.schemas.users_schemas import UserCreate, UserUpdate
from src.utils.security import get_password_hash

# --- CREATE ---
def create_user(db: Session, user: UserCreate):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya existe")
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El username ya existe")

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
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
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ese email ya está siendo usado por otro usuario")

    if "username" in update_data:
        check_username = db.query(User).filter(User.username == update_data["username"]).first()
        if check_username and check_username.id != user_id: #type: ignore
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ese username ya está ocupado")

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