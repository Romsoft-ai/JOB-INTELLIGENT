import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()


class Settings:
    """Configuration générale de l'application."""

    # Application
    APP_NAME: str = "Job Intelligent App"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # Base de données (SQLite en local)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./job_intelligent.db")

    # API France Travail (à configurer plus tard)
    FRANCE_TRAVAIL_API_KEY: str = os.getenv("FRANCE_TRAVAIL_API_KEY", "")
    FRANCE_TRAVAIL_API_SECRET: str = os.getenv("FRANCE_TRAVAIL_API_SECRET", "")


settings = Settings()
