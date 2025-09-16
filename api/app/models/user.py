from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    """Modelo de usuario para la base de datos.
    
    Representa la entidad User en la base de datos con todos sus campos
    y restricciones correspondientes.
    
    Attributes:
        id (UUID): Identificador único del usuario (clave primaria).
        nombre (str): Nombre completo del usuario (máximo 100 caracteres).
        email (str): Dirección de email única del usuario (máximo 255 caracteres).
        fecha_registro (datetime): Fecha y hora de registro del usuario.
    """
    __tablename__ = "users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Identificador único del usuario")
    nombre: str = Field(max_length=100, nullable=False, description="Nombre completo del usuario")
    email: str = Field(max_length=255, nullable=False, unique=True, description="Email único del usuario")
    fecha_registro: datetime = Field(default_factory=datetime.utcnow, description="Fecha de registro")