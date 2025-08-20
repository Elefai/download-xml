"""
Aplicação de teste sem rate limiting para facilitar os testes
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import download
from app.config import settings

# Criar uma versão da app sem rate limiting para testes
test_app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
test_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router simples sem rate limiting para testes
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import DownloadRequest, SuccessResponse, ErrorResponse
from app.services.xml_service import XMLDownloadService
import logging

logger = logging.getLogger(__name__)
test_router = APIRouter()

@test_router.post("/download_xml", response_model=SuccessResponse)
async def test_download_xml(request: DownloadRequest):
    """Endpoint de teste sem rate limiting"""
    try:
        url_str = str(request.url)
        success, xml_content, error_message, from_cache = XMLDownloadService.download_and_validate_xml(url_str)
        
        if success:
            return SuccessResponse(
                status="sucesso",
                xml_content=xml_content,
                cached=from_cache,
                content_size=len(xml_content.encode('utf-8'))
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "erro",
                    "mensagem": f"Falha ao baixar ou processar o arquivo XML. {error_message}"
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "erro",
                "mensagem": "Erro interno do servidor."
            }
        )

@test_router.get("/cache/stats")
async def test_cache_stats():
    """Endpoint de estatísticas sem rate limiting"""
    from app.services.xml_service import XMLDownloadService
    
    cache = XMLDownloadService._cache
    return {
        "cache_size": len(cache),
        "max_cache_size": cache.maxsize,
        "ttl_seconds": cache.ttl,
        "cache_info": {
            "hits": getattr(cache, 'hits', 0),
            "misses": getattr(cache, 'misses', 0)
        }
    }

# Incluir as rotas de teste
test_app.include_router(test_router, prefix="/api/v1")

@test_app.get("/")
async def test_root():
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

@test_app.get("/health")
async def test_health_check():
    return {"status": "healthy"}