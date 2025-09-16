from sqlmodel import Session
from fastapi import HTTPException, status
from repositories.user import UserRepository
from dto.user import UserCreateDTO, UserResponseDTO, UserPaginationResponseDTO


class UserService:
    """Servicio para la gestión de usuarios.
    
    Esta clase maneja la lógica de negocio para las operaciones relacionadas
    con usuarios, incluyendo validaciones y transformaciones de datos.
    """
    
    def __init__(self, session: Session):
        """Inicializa el servicio de usuarios.
        
        Args:
            session (Session): Sesión de base de datos de SQLModel.
        """
        self.repository = UserRepository(session)
    
    def create_user(self, user_data: UserCreateDTO) -> UserResponseDTO:
        """Crea un nuevo usuario con validaciones de negocio.
        
        Valida que el email no esté registrado previamente antes de crear
        el usuario en la base de datos.
        
        Args:
            user_data (UserCreateDTO): Datos del usuario a crear.
            
        Returns:
            UserResponseDTO: Usuario creado con todos sus datos.
            
        Raises:
            HTTPException: Error 400 si el email ya está registrado.
        """
        # Validar que el email no exista
        existing_user = self.repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Crear usuario
        user = self.repository.create_user(user_data)
        
        # Convertir a DTO
        return UserResponseDTO.model_validate(user)
    
    def get_users_paginated(self, page: int = 1, per_page: int = 10) -> UserPaginationResponseDTO:
        """Obtiene usuarios con paginación aplicada.
        
        Recupera una lista paginada de usuarios con validaciones de parámetros
        y metadatos de paginación incluidos en la respuesta.
        
        Args:
            page (int, optional): Número de página a obtener. Por defecto 1.
            per_page (int, optional): Cantidad de elementos por página. Por defecto 10.
            
        Returns:
            UserPaginationResponseDTO: Respuesta con usuarios paginados y metadatos.
            
        Raises:
            HTTPException: Error 400 si los parámetros de paginación son inválidos.
        """
        # Validar parámetros
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page must be greater than 0"
            )
        
        if per_page < 1 or per_page > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Per page must be between 1 and 100"
            )
        
        # Obtener usuarios paginados del repository
        return self.repository.get_users_paginated(page, per_page)
