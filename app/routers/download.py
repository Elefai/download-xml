from fastapi import APIRouter, HTTPException, status
from app.models.schemas import DownloadRequest, SuccessResponse, ErrorResponse
from app.services.xml_service import XMLDownloadService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/download_xml",
    response_model=SuccessResponse,
    responses={
        200: {"model": SuccessResponse, "description": "XML baixado e validado com sucesso"},
        400: {"model": ErrorResponse, "description": "URL não fornecida ou inválida"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"}
    },
    summary="Download de arquivo XML",
    description="Baixa um arquivo XML de uma URL fornecida e retorna seu conteúdo validado"
)
async def download_xml(request: DownloadRequest):
    """
    Endpoint para download de arquivos XML.
    
    - **url**: URL do arquivo XML a ser baixado
    
    Retorna o conteúdo do XML se o download e validação forem bem-sucedidos.
    """
    try:
        # Validar se a URL foi fornecida (já feito pelo Pydantic, mas deixamos explícito)
        if not request.url:
            logger.warning("URL não fornecida na requisição")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "erro",
                    "mensagem": "URL não fornecida ou inválida."
                }
            )
        
        # Converter para string para uso no serviço
        url_str = str(request.url)
        
        # Tentar baixar e validar o XML
        success, xml_content, error_message = XMLDownloadService.download_and_validate_xml(url_str)
        
        if success:
            logger.info(f"Download bem-sucedido da URL: {url_str}")
            return SuccessResponse(
                status="sucesso",
                xml_content=xml_content
            )
        else:
            logger.error(f"Falha no download da URL: {url_str}. Erro: {error_message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "erro",
                    "mensagem": f"Falha ao baixar ou processar o arquivo XML. {error_message}"
                }
            )
            
    except HTTPException:
        # Re-raise HTTPExceptions para manter os códigos de status corretos
        raise
        
    except Exception as e:
        logger.error(f"Erro inesperado no endpoint download_xml: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "erro",
                "mensagem": "Erro interno do servidor."
            }
        )