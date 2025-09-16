from sqlmodel import Session, select, func
from typing import Optional
from models.user import User
from dto.user import UserCreateDTO, UserPaginationResponseDTO, UserResponseDTO
import math


class UserRepository:
    """Repositorio para el acceso a datos de usuarios.
    
    Maneja todas las operaciones de base de datos relacionadas con la entidad User,
    incluyendo consultas, creación y paginación.
    """
    
    def __init__(self, session: Session):
        """Inicializa el repositorio de usuarios.
        
        Args:
            session (Session): Sesión de base de datos de SQLModel.
        """
        self.session = session
    
    def create_user(self, user_data: UserCreateDTO) -> User:
        """Crea un nuevo usuario en la base de datos.
        
        Args:
            user_data (UserCreateDTO): Datos del usuario a crear.
            
        Returns:
            User: Usuario creado con ID asignado por la base de datos.
        """
        user = User(
            nombre=user_data.nombre,
            email=user_data.email,
            fecha_registro=user_data.fecha_registro
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su dirección de email.
        
        Args:
            email (str): Dirección de email del usuario a buscar.
            
        Returns:
            Optional[User]: Usuario encontrado o None si no existe.
        """
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()
    
    def get_users_paginated(self, page: int = 1, per_page: int = 10) -> UserPaginationResponseDTO:
        """Obtiene usuarios con paginación aplicada.
        
        Recupera una lista paginada de usuarios ordenados por fecha de registro
        descendente, junto con metadatos de paginación encapsulados en el DTO.
        
        Args:
            page (int, optional): Número de página a obtener. Por defecto 1.
            per_page (int, optional): Cantidad de elementos por página. Por defecto 10.
            
        Returns:
            UserPaginationResponseDTO: DTO con usuarios y metadatos de paginación.
        """
        # Calcular offset
        offset = (page - 1) * per_page
        
        # Obtener total de usuarios
        total_statement = select(func.count(User.id))
        total_items = self.session.exec(total_statement).one()
        
        # Calcular total de páginas
        total_pages = math.ceil(total_items / per_page) if total_items > 0 else 1
        
        # Obtener usuarios de la página actual
        users_statement = select(User).offset(offset).limit(per_page).order_by(User.fecha_registro.desc())
        users = self.session.exec(users_statement).all()
        
        # Elementos en esta página
        items_in_this_page = len(users)
        
        # Convertir usuarios a DTOs
        user_dtos = [UserResponseDTO.model_validate(user) for user in users]
        
        return UserPaginationResponseDTO(
            items=user_dtos,
            current_page=page,
            total_pages=total_pages,
            total_items=total_items,
            items_in_this_page=items_in_this_page
        )
