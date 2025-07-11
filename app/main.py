import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request, status
from app.routers import download

# Configurar logging mais detalhado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="XML Download API",
    description="API para download e validação de arquivos XML a partir de URLs com suporte a streaming",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requisições de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global para exceções não tratadas"""
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "erro",
            "mensagem": "Erro interno do servidor"
        }
    )

# Incluir as rotas
app.include_router(download.router, prefix="/api/v1")

@app.get("/")
async def root():
    logger.info("Endpoint raiz acessado")
    return {
        "message": "XML Download API está funcionando!",
        "docs": "/docs",
        "version": "1.1.0",
        "features": [
            "Download assíncrono de XML",
            "Streaming para arquivos grandes",
            "Análise iterativa de XML",
            "Validação completa"
        ]
    }

@app.get("/health")
async def health_check():
    logger.debug("Health check realizado")
    return {"status": "healthy", "version": "1.1.0"}

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 XML Download API iniciada com sucesso!")
    logger.info("📚 Documentação disponível em: /docs")
    logger.info("🔍 Redoc disponível em: /redoc")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("⛔ XML Download API finalizada")