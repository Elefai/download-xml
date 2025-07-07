from pydantic import BaseModel, HttpUrl
from typing import Optional

class DownloadRequest(BaseModel):
    url: HttpUrl
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://www.exemplo.com.br/arquivo.xml"
            }
        }

class SuccessResponse(BaseModel):
    status: str = "sucesso"
    xml_content: str
    
    class Config:
        schema_extra = {
            "example": {
                "status": "sucesso",
                "xml_content": "<?xml version='1.0' encoding='UTF-8'?><nota>...</nota>"
            }
        }

class ErrorResponse(BaseModel):
    status: str = "erro"
    mensagem: str
    
    class Config:
        schema_extra = {
            "example": {
                "status": "erro",
                "mensagem": "Falha ao baixar ou processar o arquivo XML."
            }
        }