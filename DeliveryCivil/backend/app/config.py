"""
Configurações da aplicação
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]
    
    # Data Paths (relativos ao diretório raiz do projeto)
    DATA_RAW_DIR: str = "data/raw"
    DATA_PROCESSED_DIR: str = "data/processed"
    DATA_OUTPUT_DIR: str = "data/output/powerbi"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()

# Resolver caminhos relativos à raiz do projeto (não à pasta backend)
# O backend está em backend/, então precisamos subir dois níveis para a raiz
# __file__ = backend/app/config.py
# .parent = backend/app/
# .parent.parent = backend/
# .parent.parent.parent = raiz do projeto (DeliveryCivil)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Converter caminhos relativos para absolutos baseados na raiz do projeto
DATA_RAW_DIR = PROJECT_ROOT / settings.DATA_RAW_DIR
DATA_PROCESSED_DIR = PROJECT_ROOT / settings.DATA_PROCESSED_DIR
DATA_OUTPUT_DIR = PROJECT_ROOT / settings.DATA_OUTPUT_DIR

# Atualizar settings com caminhos absolutos
settings.DATA_RAW_DIR = str(DATA_RAW_DIR)
settings.DATA_PROCESSED_DIR = str(DATA_PROCESSED_DIR)
settings.DATA_OUTPUT_DIR = str(DATA_OUTPUT_DIR)

# Garantir que os diretórios existam
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

