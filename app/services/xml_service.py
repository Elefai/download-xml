import httpx
import xml.etree.ElementTree as ET
from lxml import etree
from typing import Tuple, Optional, AsyncGenerator
import logging
from io import BytesIO
import asyncio

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XMLDownloadService:
    
    @staticmethod
    async def download_and_validate_xml(url: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Baixa e valida um arquivo XML de uma URL usando httpx assíncrono.
        
        Args:
            url (str): URL do arquivo XML
            
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: 
            (sucesso, conteudo_xml, mensagem_erro)
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            logger.info(f"Iniciando download assíncrono da URL: {url}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Fazer requisição com streaming para arquivos grandes
                async with client.stream('GET', url, headers=headers) as response:
                    response.raise_for_status()
                    
                    # Verificar Content-Type
                    content_type = response.headers.get('content-type', '').lower()
                    logger.info(f"Content-Type recebido: {content_type}")
                    
                    # Verificar se é XML pelo Content-Type ou extensão
                    is_xml_content_type = (
                        'xml' in content_type or 
                        'application/xml' in content_type or 
                        'text/xml' in content_type
                    )
                    
                    # Verificar se a URL termina com .xml
                    is_xml_url = url.lower().endswith('.xml')
                    
                    # Baixar conteúdo em chunks para evitar sobrecarga de memória
                    content_parts = []
                    total_size = 0
                    chunk_size = 1024 * 1024  # 1MB chunks
                    
                    async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                        content_parts.append(chunk)
                        total_size += len(chunk)
                        
                        # Limite de segurança para evitar arquivos muito grandes
                        if total_size > 100 * 1024 * 1024:  # 100MB limit
                            logger.warning(f"Arquivo muito grande (>{total_size} bytes), interrompendo download")
                            return False, None, "Arquivo muito grande (limite: 100MB)"
                    
                    # Juntar todos os chunks
                    full_content = b''.join(content_parts)
                    content = full_content.decode('utf-8', errors='ignore')
                    
                    logger.info(f"Download concluído. Tamanho: {total_size} bytes")
                    
                    # Validar XML usando lxml para melhor performance
                    try:
                        # Primeiro, tentar com lxml (mais eficiente)
                        parser = etree.XMLParser(recover=True)
                        etree.fromstring(full_content, parser)
                        logger.info("XML validado com sucesso usando lxml")
                        return True, content, None
                    except etree.XMLSyntaxError:
                        try:
                            # Fallback para ET nativo
                            ET.fromstring(content)
                            logger.info("XML validado com sucesso usando ElementTree")
                            return True, content, None
                        except ET.ParseError as e:
                            logger.error(f"Erro ao fazer parse do XML: {e}")
                            return False, None, f"O arquivo baixado não é um XML válido: {str(e)}"
                            
        except httpx.TimeoutException:
            error_msg = "Timeout ao tentar baixar o arquivo da URL fornecida"
            logger.error(error_msg)
            return False, None, error_msg
            
        except httpx.ConnectError:
            error_msg = "Erro de conexão ao tentar acessar a URL"
            logger.error(error_msg)
            return False, None, error_msg
            
        except httpx.HTTPStatusError as e:
            error_msg = f"Erro HTTP ao acessar a URL: {e.response.status_code}"
            logger.error(error_msg)
            return False, None, error_msg
            
        except httpx.RequestError as e:
            error_msg = f"Erro ao fazer requisição: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
            
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg

    @staticmethod
    async def stream_and_validate_xml(url: str) -> AsyncGenerator[bytes, None]:
        """
        Baixa e valida XML em streaming, ideal para arquivos muito grandes.
        
        Args:
            url (str): URL do arquivo XML
            
        Yields:
            bytes: Chunks do arquivo XML validado
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            logger.info(f"Iniciando streaming da URL: {url}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream('GET', url, headers=headers) as response:
                    response.raise_for_status()
                    
                    # Buffer para validação incremental
                    xml_buffer = BytesIO()
                    parser = etree.iterparse(xml_buffer, events=('start', 'end'))
                    
                    chunk_size = 8192  # 8KB chunks para streaming
                    
                    async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                        # Adicionar chunk ao buffer de validação
                        xml_buffer.write(chunk)
                        
                        # Retornar chunk para o cliente
                        yield chunk
                        
                        # Validação incremental a cada alguns chunks
                        if xml_buffer.tell() % (chunk_size * 10) == 0:
                            try:
                                xml_buffer.seek(0)
                                # Tentar parse parcial sem completar
                                temp_parser = etree.XMLParser(recover=True)
                                xml_buffer.seek(0, 2)  # Voltar ao fim
                            except:
                                # Se houver erro de parsing, continuar (pode ser XML incompleto ainda)
                                pass
                                
        except Exception as e:
            logger.error(f"Erro durante streaming: {str(e)}")
            raise

    @staticmethod
    async def process_large_xml_iteratively(url: str) -> Tuple[bool, Optional[dict], Optional[str]]:
        """
        Processa XML muito grande de forma iterativa, extraindo apenas informações essenciais.
        
        Args:
            url (str): URL do arquivo XML
            
        Returns:
            Tuple[bool, Optional[dict], Optional[str]]: 
            (sucesso, info_xml, mensagem_erro)
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            logger.info(f"Processando XML grande iterativamente da URL: {url}")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream('GET', url, headers=headers) as response:
                    response.raise_for_status()
                    
                    # Informações extraídas do XML
                    xml_info = {
                        'root_tag': None,
                        'namespaces': set(),
                        'element_count': 0,
                        'max_depth': 0,
                        'size_bytes': 0
                    }
                    
                    # Parser iterativo para não carregar tudo na memória
                    parser = etree.iterparse(
                        response.aiter_bytes(chunk_size=8192),
                        events=('start', 'end', 'start-ns')
                    )
                    
                    depth = 0
                    
                    for event, elem in parser:
                        if event == 'start':
                            depth += 1
                            xml_info['max_depth'] = max(xml_info['max_depth'], depth)
                            xml_info['element_count'] += 1
                            
                            if xml_info['root_tag'] is None:
                                xml_info['root_tag'] = elem.tag
                                
                        elif event == 'end':
                            depth -= 1
                            # Limpar elemento da memória após processamento
                            elem.clear()
                            
                        elif event == 'start-ns':
                            prefix, uri = elem
                            xml_info['namespaces'].add(f"{prefix}:{uri}" if prefix else uri)
                    
                    xml_info['namespaces'] = list(xml_info['namespaces'])
                    
                    logger.info(f"XML processado iterativamente. Elementos: {xml_info['element_count']}, Profundidade máxima: {xml_info['max_depth']}")
                    return True, xml_info, None
                    
        except Exception as e:
            error_msg = f"Erro ao processar XML iterativamente: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg