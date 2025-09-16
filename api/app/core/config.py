import os
from dotenv import load_dotenv
from urllib.parse import quote

# Carga variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    # Configuración de la base de datos
        db_user = os.getenv("POSTGRES_USER")
        db_password = quote(os.getenv("POSTGRES_PASSWORD", ""), safe="")
        db_host = os.getenv("POSTGRES_HOST")
        db_port = os.getenv("POSTGRES_PORT")
        db_name = os.getenv("POSTGRES_DB")

        # Configurar la URL de la base de datos
        DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Crear una instancia de configuración
settings = Settings()