"""
Pruebas unitarias esenciales para los endpoints de usuarios.

Estas pruebas verifican que:
1. POST /users - Se pueden crear usuarios correctamente
2. GET /users - Se pueden listar usuarios correctamente
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from uuid import uuid4
from datetime import datetime

# Importar la aplicación y dependencias
from main import app
from core.database import get_session
from models.user import User


# Configuración de base de datos de prueba en memoria
@pytest.fixture(name="session")
def session_fixture():
    """Crear una base de datos de prueba en memoria para cada test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Cliente de prueba que usa la base de datos de prueba."""
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestCreateUser:
    """Pruebas para el endpoint POST /api/v1/users/"""
    
    def test_create_user_success(self, client: TestClient):
        """
        PRUEBA PRINCIPAL: Verificar que POST /users funciona correctamente
        """
        # Datos de prueba
        user_data = {
            "nombre": "Juan Pérez",
            "email": "juan.perez@example.com"
        }
        
        # Hacer request POST
        response = client.post("/api/v1/users/", json=user_data)
        
        # Verificar que la respuesta sea exitosa
        assert response.status_code == 201
        
        # Verificar el contenido de la respuesta
        data = response.json()
        assert data["nombre"] == user_data["nombre"]
        assert data["email"] == user_data["email"]
        assert "id" in data  # Debe tener un ID
        assert "fecha_registro" in data  # Debe tener fecha de registro
        
        print(f"Usuario creado exitosamente: {data['nombre']} ({data['email']})")


class TestGetUsers:
    """Pruebas para el endpoint GET /api/v1/users/"""
    
    def test_get_users_empty(self, client: TestClient):
        """
        PRUEBA: Verificar que GET /users funciona cuando no hay usuarios
        """
        response = client.get("/api/v1/users/")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total_items" in data
        assert data["items"] == []
        assert data["total_items"] == 0
        
        print("GET /users funciona correctamente cuando está vacío")

    def test_get_users_with_data(self, client: TestClient, session: Session):
        """
        PRUEBA PRINCIPAL: Verificar que GET /users devuelve usuarios correctamente
        """
        # Crear algunos usuarios de prueba
        users = [
            User(
                id=uuid4(),
                nombre=f"Usuario {i}",
                email=f"user{i}@example.com",
                fecha_registro=datetime.now()
            )
            for i in range(1, 4)  # Crear 3 usuarios
        ]
        
        # Guardar en la base de datos
        for user in users:
            session.add(user)
        session.commit()
        
        # Hacer request GET
        response = client.get("/api/v1/users/")
        
        # Verificar que la respuesta sea exitosa
        assert response.status_code == 200
        
        # Verificar el contenido
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total_items"] == 3
        
        # Verificar que cada usuario tenga los campos correctos
        for user_data in data["items"]:
            assert "id" in user_data
            assert "nombre" in user_data
            assert "email" in user_data
            assert "fecha_registro" in user_data
        
        print(f"GET /users devuelve {len(data['items'])} usuarios correctamente")
