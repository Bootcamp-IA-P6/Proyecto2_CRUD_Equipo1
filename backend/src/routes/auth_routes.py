from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.users_model import User
from src.utils.security import verify_password, create_access_token
from datetime import timedelta

router = APIRouter(tags=["Authentication"])

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Buscar usuario por username
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # 2. Verificar si usuario existe y password coincide
    if not user or not verify_password(form_data.password, user.password): #type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generar Token
    access_token_expires = timedelta(minutes=60) # 1 hora
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value}, # Guardamos username y rol en el token
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}