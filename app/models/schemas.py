from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import Optional
from datetime import datetime

class DownloadRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://www.exemplo.com.br/arquivo.xml"
            }
        }
    )
    
    url: HttpUrl

class SuccessResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "sucesso",
                "xml_content": "<?xml version='1.0' encoding='UTF-8'?><nota>...</nota>",
                "cached": False,
                "content_size": 1024,
                "timestamp": "2024-01-15T10:30:00"
            }
        }
    )
    
    status: str = "sucesso"
    xml_content: str
    cached: bool = Field(default=False, description="Indica se o resultado veio do cache")
    content_size: int = Field(description="Tamanho do conteúdo XML em bytes")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")

class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "erro",
                "mensagem": "Falha ao baixar ou processar o arquivo XML."
            }
        }
    )
    
    status: str = "erro"
    mensagem: str