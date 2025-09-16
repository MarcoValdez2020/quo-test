# Quo Test API - Sistema de Gestión de Usuarios

API REST desarrollada en **FastAPI con PostgreSQL** para la gestión básica de usuarios. Incluye endpoints para crear usuarios y listarlos con paginación básica.

## 📋 Requerimientos Implementados

### ✅ 1. Endpoints REST
- **POST /api/v1/users/** - Crear usuario con validación de email único
- **GET /api/v1/users/** - Listar usuarios con paginación (page/per_page)

### ✅ 2. Base de datos PostgreSQL
- ✅ Script SQL con tabla `users` (id, nombre, email, fecha_registro)
- ✅ Restricción UNIQUE en email + índices optimizados
- ✅ Queries especiales incluidas como vistas:
  - Usuarios de últimos 7 días
  - Conteo por dominio de email

### ✅ 3. Pruebas unitarias
- ✅ Prueba que verifica POST /users funciona correctamente
- ✅ Prueba que verifica GET /users funciona correctamente

### ✅ 4. README completo
- ✅ Instrucciones de instalación
- ✅ Cómo correr las pruebas
- ✅ Ejemplos de API calls

### 🚀 Extras Implementados
- ✅ **Dockerfile funcional** para contenerizar la aplicación
- ✅ **Docker Compose** para levantar todo con un comando
- ✅ **Manejo robusto de errores** con códigos HTTP correctos
- ✅ **Validaciones completas** (email inválido, campos faltantes, etc.)
- ✅ **Documentación automática** con Swagger/OpenAPI

## 🏗️ Arquitectura del Proyecto

```
quo-test/
├── api/                     # Aplicación FastAPI
│   ├── app/
│   │   ├── main.py          # Punto de entrada FastAPI
│   │   ├── core/            # Configuración y base de datos
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/          # Modelos SQLModel para DB
│   │   │   └── user.py
│   │   ├── dto/             # DTOs request/response
│   │   │   └── user.py
│   │   ├── repositories/    # Acceso a datos
│   │   │   └── user.py
│   │   ├── services/        # Lógica de negocio
│   │   │   └── user.py
│   │   ├── routes/          # Endpoints REST
│   │   │   └── user.py
│   │   └── test/            # Pruebas unitarias
│   │       └── test_users.py
│   ├── Dockerfile           # Imagen Docker para API
│   └── requirements.txt     # Dependencias Python
├── database/
│   └── init.sql            # Script inicialización PostgreSQL
├── docker-compose.dev.yml  # Docker Compose desarrollo
├── docker-compose.prod.yml # Docker Compose producción
└── README.md               # Este archivo
```

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Docker y Docker Compose
- Git

### 1. Clonar el repositorio
```bash
git clone https://github.com/MarcoValdez2020/quo-test.git
cd quo-test
```

### 2. Configurar variables de entorno
```bash
cp .env.prod.example .env.prod
# Editar .env.prod para ajustar configuración si es necesario
```

### 3. Levantar la aplicación completa
```bash
# Levantar PostgreSQL + API con un solo comando
docker-compose --env-file .env.prod -f docker-compose.prod.yml up --build

# Servicios disponibles:
# - API: http://localhost:8000
# - PostgreSQL: localhost:5432
# - Swagger Docs: http://localhost:8000/docs
```

### 4. Verificar instalación
```bash
# Health check
curl http://localhost:8000/health

# Documentación automática
open http://localhost:8000/docs
```

## 🧪 Ejecutar Pruebas

### Pruebas unitarias con Docker
```bash
# Ejecutar todas las pruebas
docker exec -it quo-test-fastapi-container python -m pytest test/ -v

# Ejecutar solo pruebas principales
docker exec -it quo-test-fastapi-container python -m pytest test/test_users.py::TestCreateUser::test_create_user_success test/test_users.py::TestGetUsers::test_get_users_with_data -v

```

### Pruebas implementadas
- ✅ **test_create_user_success** - Verifica POST /users funciona
- ✅ **test_get_users_with_data** - Verifica GET /users funciona


## 📡 Ejemplos de Uso del API

### Crear Usuario (POST /users)
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan.perez@example.com"
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "nombre": "Juan Pérez",
  "email": "juan.perez@example.com",
  "fecha_registro": "2024-01-15T10:30:00+00:00"
}
```

**Error email duplicado (400):**
```json
{
  "detail": "El email juan.perez@example.com ya está registrado"
}
```

### Listar Usuarios con Paginación (GET /users)
```bash
# Primera página, 10 usuarios por página
curl "http://localhost:8000/api/v1/users/?page=1&per_page=10"

# Segunda página, 5 usuarios por página  
curl "http://localhost:8000/api/v1/users/?page=2&per_page=5"
```

**Respuesta:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "nombre": "Juan Pérez",
      "email": "juan.perez@example.com",
      "fecha_registro": "2024-01-15T10:30:00+00:00"
    }
  ],
  "current_page": 1,
  "total_pages": 3,
  "total_items": 25,
  "items_in_this_page": 10
}
```

## 🗄️ Base de Datos PostgreSQL

### Esquema de tabla users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    fecha_registro TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Índices para optimización
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_fecha_registro ON users(fecha_registro);
```

### Queries especiales implementadas

#### 1. Usuarios registrados en últimos 7 días
```sql
-- Como vista de BD:
SELECT * FROM usuarios_ultimos_7_dias;

-- Query directo:
SELECT * FROM users 
WHERE fecha_registro >= CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER BY fecha_registro DESC;
```

#### 2. Conteo de usuarios por dominio de email
```sql
-- Como vista de BD:
SELECT * FROM usuarios_por_dominio;

-- Query directo:
SELECT 
    SPLIT_PART(email, '@', 2) as dominio,
    COUNT(*) as total_usuarios
FROM users 
GROUP BY dominio
ORDER BY total_usuarios DESC;
```

### Conectar a PostgreSQL directamente
```bash
# Conectar al contenedor de PostgreSQL
docker exec -it quo-test-postgres-container psql -U postgres -d quo_test

# Ejecutar queries especiales
\d users                           -- Ver estructura tabla
SELECT * FROM usuarios_ultimos_7_dias;  -- Últimos 7 días
SELECT * FROM usuarios_por_dominio;     -- Por dominio
```

## 🐳 Docker y Containerización

### Servicios incluidos
- **PostgreSQL 17**: Base de datos con datos de prueba
- **FastAPI**: API REST con auto-reload en desarrollo

### Comandos Docker útiles
```bash
# Levantar en modo desarrollo (con auto-reload)
docker-compose --env-file .env.prod -f docker-compose.dev.yml up --build

# Levantar en modo producción
docker-compose --env-file .env.prod -f docker-compose.prod.yml up -d


```

## 🔧 Tecnologías y Decisiones de Diseño

### Stack Tecnológico
- **FastAPI**: Framework web moderno, alto rendimiento
- **SQLModel**: ORM que combina SQLAlchemy + Pydantic
- **PostgreSQL 17**: Base de datos relacional robusta
- **Pydantic V2**: Validación de datos con ConfigDict
- **Docker**: Containerización y portabilidad
- **Pytest**: Framework de testing con fixtures

### Decisiones de Diseño

1. **Repository Pattern**: Separación clara entre lógica de negocio y acceso a datos
2. **DTOs explícitos**: Control total sobre request/response, mejor documentación
3. **UUID para IDs**: Mejor para sistemas distribuidos, más seguro
4. **Paginación offset-based**: Simple y eficiente para este caso de uso
5. **SQLite en memoria para tests**: Pruebas rápidas y aisladas
6. **Validaciones en múltiples capas**: Pydantic + base de datos + lógica de negocio

### Manejo de Errores Implementado
- ✅ **422** - Datos inválidos (email malformado, campos faltantes)
- ✅ **400** - Email duplicado, errores de lógica de negocio  
- ✅ **404** - Recursos no encontrados
- ✅ **500** - Errores internos del servidor



## 📊 Validaciones y Seguridad

### Validaciones implementadas
- ✅ Formato de email con `EmailStr` de Pydantic
- ✅ Campos requeridos y longitudes máximas
- ✅ Email único a nivel de base de datos
- ✅ Parámetros de paginación válidos (page ≥ 1, per_page ≤ 100)
- ✅ UUIDs válidos para IDs


### Seguridad básica
- ✅ Validación de entrada en todas las capas
- ✅ Escapado automático de SQL (SQLModel/SQLAlchemy)
- ✅ CORS configurado apropiadamente
- ✅ Headers de seguridad básicos

## 📈 Rendimiento

### Optimizaciones incluidas
- ✅ Índices en email y fecha_registro
- ✅ Paginación para evitar cargar todos los registros
- ✅ Pool de conexiones de base de datos
- ✅ Respuestas JSON eficientes

## 🔍 Monitoreo y Logging

- ✅ Health check endpoint: `/health`
- ✅ Documentación automática: `/docs`
- ✅ Logging automático de FastAPI
- ✅ Validación de datos con mensajes de error claros

## 📝 Declaración de Autenticidad

Por medio de la presente declaro que:

- ✅ **Todo el código, pruebas, scripts y documentación** son de mi autoría personal
- ✅ **No he presentado trabajo generado completamente por IA** como si fuera mío
- ✅ **Utilicé IA como asistencia** específicamente para:
  - **Consultas de sintaxis** de FastAPI, SQLModel y Pytest 
  - **Desarrollo de pruebas unitarias** ya que nunca había implementado tests antes
  - **Autocompletado y snippets** durante el desarrollo
- ✅ **Revisé, modifiqué y entendí** todo el código asistido por IA
- ✅ **Estoy preparado para explicar** decisiones de diseño, lógica del código, estructura y deployment durante entrevista técnica

### Mi participación personal:
- **Arquitectura completa del proyecto** (Repository pattern, separación de capas)
- **Configuración de Docker y Docker Compose**
- **Implementación de endpoints y lógica de negocio**
- **Diseño de base de datos y queries especiales**
- **Configuración de FastAPI y middlewares**
- **Estructura del proyecto y organización de archivos**

## 👨‍💻 Autor

**Marco Valdez**
- GitHub: [@MarcoValdez2020](https://github.com/MarcoValdez2020)

---

*Este proyecto fue desarrollado como parte de una prueba técnica, cumpliendo con todos los requerimientos solicitados.*