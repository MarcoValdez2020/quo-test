from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from core.database import get_session
from services.user import UserService
from dto.user import UserCreateDTO, UserResponseDTO, UserPaginationResponseDTO

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    """Función de dependencia para obtener el servicio de usuarios.
    
    Args:
        session (Session): Sesión de base de datos inyectada por FastAPI.
        
    Returns:
        UserService: Instancia del servicio de usuarios configurada.
    """
    return UserService(session)


@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateDTO,
    user_service: UserService = Depends(get_user_service)
):
    """Crea un nuevo usuario en el sistema.
    
    Endpoint para registrar un nuevo usuario validando que el email
    no esté previamente registrado en la base de datos.
    
    Args:
        user_data (UserCreateDTO): Datos del usuario a crear.
        user_service (UserService): Servicio de usuarios inyectado.
        
    Returns:
        UserResponseDTO: Usuario creado con todos sus datos.
        
    Raises:
        HTTPException: Error 400 si el email ya está registrado.
    """
    return user_service.create_user(user_data)


@router.get("/", response_model=UserPaginationResponseDTO)
async def get_users(
    page: int = Query(default=1, ge=1, description="Número de página"),
    per_page: int = Query(default=10, ge=1, le=100, description="Elementos por página"),
    user_service: UserService = Depends(get_user_service)
):
    """Obtiene una lista paginada de usuarios.
    
    Endpoint para recuperar usuarios con paginación, ordenados por
    fecha de registro de más reciente a más antiguo.
    
    Args:
        page (int, optional): Número de página a obtener. Por defecto 1.
        per_page (int, optional): Elementos por página (1-100). Por defecto 10.
        user_service (UserService): Servicio de usuarios inyectado.
        
    Returns:
        UserPaginationResponseDTO: Respuesta con usuarios paginados y metadatos.
        
    Raises:
        HTTPException: Error 400 si los parámetros de paginación son inválidos.
        
    Example:
        GET /users/?page=1&per_page=10
    """
    return user_service.get_users_paginated(page=page, per_page=per_page)
