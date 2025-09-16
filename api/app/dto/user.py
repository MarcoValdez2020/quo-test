from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class UserCreateDTO(BaseModel):
    """DTO para crear un usuario"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Juan Pérez",
                "email": "juan.perez@example.com",
                "fecha_registro": "2024-01-15T10:30:00"
            }
        }
    )
    
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email válido del usuario")  
    fecha_registro: Optional[datetime] = None


class UserResponseDTO(BaseModel):
    """DTO para respuesta de un usuario"""
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "nombre": "Juan Pérez", 
                "email": "juan.perez@example.com",
                "fecha_registro": "2024-01-15T10:30:00"
            }
        }
    )
    
    id: UUID
    nombre: str
    email: EmailStr  # Validación automática de formato email
    fecha_registro: datetime


class UserPaginationResponseDTO(BaseModel):
    """DTO para respuesta paginada de usuarios"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "nombre": "Juan Pérez",
                        "email": "juan.perez@example.com", 
                        "fecha_registro": "2024-01-15T10:30:00"
                    }
                ],
                "current_page": 1,
                "total_pages": 3,
                "total_items": 25,
                "items_in_this_page": 10
            }
        }
    )
    
    items: List[UserResponseDTO]
    current_page: int
    total_pages: int
    total_items: int
    items_in_this_page: int
