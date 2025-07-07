from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import download

app = FastAPI(
    title="XML Download API",
    description="API para download e validação de arquivos XML a partir de URLs",
    version="1.0.0",
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

# Incluir as rotas
app.include_router(download.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "XML Download API está funcionando!",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}