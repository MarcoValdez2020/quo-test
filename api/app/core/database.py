from sqlmodel import create_engine, Session
from core.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # Verifica las conexiones antes de usarlas
    pool_size=10,         # Número de conexiones en el pool
    max_overflow=20       # Conexiones temporales adicionales que se pueden crear por encima de pool_size
)


def get_session():
    """Get database session - Dependency provider for FastAPI"""
    with Session(engine) as session:
        yield session
