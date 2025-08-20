from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import download
from app.config import settings

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Adicionar middleware de rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configurar CORS para permitir requisições de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir as rotas
app.include_router(download.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "XML Download API está funcionando!",
        "docs": "/docs",
        "version": settings.API_VERSION,
        "features": [
            "Rate limiting",
            "Cache inteligente",
            "Validação de segurança",
            "Proteção contra XXE",
            "Validação de tamanho de arquivo"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}