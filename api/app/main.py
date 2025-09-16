from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import router as user_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Quo Test API",
    version="1.0.0",
    description="API para gestión de usuarios - Prueba técnica"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(user_router, prefix="/api/v1")

# Endpoint de salud
@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy", "version": "1.0.0"}

# Endpoint raíz
@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Bienvenido a Quo Test API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

