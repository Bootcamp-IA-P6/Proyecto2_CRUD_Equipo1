from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from src.database.database import get_db
from src.controllers import peliculas_controller
from src.schemas.peliculas_schemas import PeliculaCreate, PeliculaUpdate, PeliculaResponse
from src.utils.security import get_current_user
from typing import List
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/peliculas", tags=["Películas"])

# ← CORRECCIÓN: Ruta absoluta a uploads (raíz del backend)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Sube hasta backend/
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# ============ UPLOAD DE IMÁGENES ============

# ← PROTEGIDO: Solo admin puede subir imágenes
@router.post("/upload")
async def upload_poster(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Subir imagen de póster - Solo admin"""
    
    try:
        # Validar que sea admin
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores pueden subir imágenes"
            )
        
        # Validar que hay archivo
        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionó archivo"
            )
        
        # Validar extensión
        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Extensión no permitida. Usa: {', '.join(allowed_extensions)}"
            )
        
        # Generar nombre único con UUID
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Guardar archivo
        contents = await file.read()
        
        if not contents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo está vacío"
            )
        
        # Escribir archivo
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Verificar que se guardó
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo guardar el archivo en el servidor"
            )
        
        # Retornar ruta de API
        return {
            "poster_url": f"/api/v1/peliculas/imagen/{unique_filename}",
            "filename": unique_filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en upload: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar archivo: {str(e)}"
        )

# ← PÚBLICO: Obtener imagen
@router.get("/imagen/{filename}")
async def get_image(filename: str):
    """
    Obtener imagen de película por nombre de archivo
    PÚBLICO - No requiere autenticación
    """
    try:
        file_path = UPLOAD_DIR / filename
        
        # Validar que el archivo existe
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Imagen no encontrada"
            )
        
        # Validar que el archivo está dentro de UPLOAD_DIR (seguridad)
        if not str(file_path.resolve()).startswith(str(UPLOAD_DIR.resolve())):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado"
            )
        
        # Detectar tipo de media según extensión
        media_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        
        file_ext = file_path.suffix.lower()
        media_type = media_types.get(file_ext, 'image/jpeg')
        
        return FileResponse(
            path=file_path,
            media_type=media_type,
            headers={"Cache-Control": "public, max-age=86400"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener imagen: {str(e)}"
        )

# ============ CRUD DE PELÍCULAS ============

# ← PÚBLICO: Listar todas las películas
@router.get("/", response_model=List[PeliculaResponse], responses={200: {"description": "Lista de películas"}})
async def get_all_peliculas_public(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Obtener todas las películas - PÚBLICO"""
    return peliculas_controller.get_all_peliculas(db, skip, limit)

# ← PROTEGIDO: Solo admin puede crear
@router.post("/", response_model=PeliculaResponse, status_code=status.HTTP_201_CREATED, responses={
    404: {"description": "Director o género no encontrado"},
    409: {"description": "Película duplicada"},
    422: {"description": "Datos inválidos"},
    403: {"description": "Solo administradores"}
})
async def create_pelicula(
    pelicula: PeliculaCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear película - Solo admin"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden crear películas"
        )
    return peliculas_controller.create_pelicula(db, pelicula)

# ← PROTEGIDO: Solo admin puede crear en bulk
@router.post("/bulk", response_model=List[PeliculaResponse], status_code=status.HTTP_201_CREATED, responses={
    403: {"description": "Solo administradores"}
})
async def create_pelicula_bulk(
    peliculas: List[PeliculaCreate],
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear múltiples películas - Solo admin"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden crear películas"
        )
    return peliculas_controller.create_pelicula_bulk(db, peliculas)

# ← PÚBLICO: Obtener una película por ID
@router.get("/{pelicula_id}", response_model=PeliculaResponse, responses={404: {"description": "Película no encontrada"}})
async def read_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    """Obtener una película por ID - PÚBLICO"""
    return peliculas_controller.get_pelicula(db, pelicula_id)

# ← PROTEGIDO: Solo admin puede editar
@router.patch("/{pelicula_id}", response_model=PeliculaResponse, responses={
    404: {"description": "Película, director o género no encontrado"},
    409: {"description": "Título duplicado"},
    422: {"description": "Datos inválidos"},
    403: {"description": "Solo administradores"}
})
async def update_pelicula(
    pelicula_id: int,
    pelicula_update: PeliculaUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar película - Solo admin"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden editar películas"
        )
    return peliculas_controller.update_pelicula(db, pelicula_id, pelicula_update)

# ← PROTEGIDO: Solo admin puede eliminar
@router.delete("/{pelicula_id}", responses={
    404: {"description": "Película no encontrada"},
    403: {"description": "Solo administradores"}
})
async def delete_pelicula(
    pelicula_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar película - Solo admin"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo administradores pueden eliminar películas"
        )
    peliculas_controller.delete_pelicula(db, pelicula_id)
    return {"message": "Película eliminada correctamente"}
