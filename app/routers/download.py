from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from app.models.schemas import DownloadRequest, SuccessResponse, ErrorResponse, XMLInfoResponse
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
        
        # Tentar baixar e validar o XML usando método assíncrono
        success, xml_content, error_message = await XMLDownloadService.download_and_validate_xml(url_str)
        
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

@router.post(
    "/download_xml_stream",
    responses={
        200: {"description": "XML em streaming", "content": {"application/xml": {}}},
        400: {"model": ErrorResponse, "description": "URL não fornecida ou inválida"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"}
    },
    summary="Download de arquivo XML em streaming",
    description="Baixa um arquivo XML grande em streaming, ideal para arquivos > 10MB"
)
async def download_xml_stream(request: DownloadRequest):
    """
    Endpoint para download de arquivos XML grandes em streaming.
    
    - **url**: URL do arquivo XML a ser baixado
    
    Retorna o XML em streaming, processando chunks de forma eficiente.
    """
    try:
        if not request.url:
            logger.warning("URL não fornecida na requisição de streaming")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "erro",
                    "mensagem": "URL não fornecida ou inválida."
                }
            )
        
        url_str = str(request.url)
        logger.info(f"Iniciando streaming de XML da URL: {url_str}")
        
        # Retornar streaming response
        return StreamingResponse(
            XMLDownloadService.stream_and_validate_xml(url_str),
            media_type="application/xml",
            headers={
                "Content-Disposition": "attachment; filename=downloaded.xml",
                "Cache-Control": "no-cache"
            }
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Erro inesperado no endpoint download_xml_stream: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "erro",
                "mensagem": "Erro interno do servidor durante streaming."
            }
        )

@router.post(
    "/xml_info",
    response_model=XMLInfoResponse,
    responses={
        200: {"model": XMLInfoResponse, "description": "Informações do XML extraídas com sucesso"},
        400: {"model": ErrorResponse, "description": "URL não fornecida ou inválida"},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor"}
    },
    summary="Análise de arquivo XML grande",
    description="Analisa um arquivo XML grande de forma iterativa, extraindo informações sem carregar todo o conteúdo na memória"
)
async def analyze_large_xml(request: DownloadRequest):
    """
    Endpoint para análise de arquivos XML muito grandes.
    
    - **url**: URL do arquivo XML a ser analisado
    
    Retorna informações sobre a estrutura do XML sem carregar todo o conteúdo na memória.
    """
    try:
        if not request.url:
            logger.warning("URL não fornecida na requisição de análise")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "erro",
                    "mensagem": "URL não fornecida ou inválida."
                }
            )
        
        url_str = str(request.url)
        logger.info(f"Iniciando análise iterativa de XML da URL: {url_str}")
        
        # Processar XML iterativamente
        success, xml_info, error_message = await XMLDownloadService.process_large_xml_iteratively(url_str)
        
        if success:
            logger.info(f"Análise bem-sucedida da URL: {url_str}")
            return XMLInfoResponse(
                status="sucesso",
                xml_info=xml_info
            )
        else:
            logger.error(f"Falha na análise da URL: {url_str}. Erro: {error_message}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status": "erro",
                    "mensagem": f"Falha ao analisar o arquivo XML. {error_message}"
                }
            )
            
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Erro inesperado no endpoint analyze_large_xml: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "erro",
                "mensagem": "Erro interno do servidor durante análise."
            }
        )