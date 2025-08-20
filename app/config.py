"""
Configurações da aplicação XML Download API
"""
import os
from typing import List

class Settings:
    """Configurações da aplicação"""
    
    # Configurações da API
    API_TITLE: str = "XML Download API"
    API_DESCRIPTION: str = "API para download e validação de arquivos XML a partir de URLs"
    API_VERSION: str = "1.1.0"
    
    # Configurações de segurança
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    MAX_FILE_SIZE: int = MAX_FILE_SIZE_MB * 1024 * 1024
    
    # Rate limiting
    RATE_LIMIT_DOWNLOADS: str = os.getenv("RATE_LIMIT_DOWNLOADS", "10/minute")
    RATE_LIMIT_STATS: str = os.getenv("RATE_LIMIT_STATS", "30/minute")
    
    # Cache
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "900"))  # 15 minutos
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "100"))
    
    # Timeout para requisições HTTP
    HTTP_TIMEOUT_SECONDS: int = int(os.getenv("HTTP_TIMEOUT_SECONDS", "30"))
    
    # Domínios bloqueados
    BLOCKED_DOMAINS: List[str] = [
        'localhost', '127.0.0.1', '0.0.0.0',
        '10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.',
        '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.',
        '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.'
    ]
    
    # Configurações de CORS
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    # Configurações de logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# Instância global das configurações
settings = Settings()