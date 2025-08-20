import requests
import xml.etree.ElementTree as ET
from typing import Tuple, Optional
import logging
import re
import hashlib
from urllib.parse import urlparse
from cachetools import TTLCache
from app.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XMLDownloadService:
    
    # Cache TTL (Time To Live) para XMLs baixados
    _cache = TTLCache(maxsize=settings.CACHE_MAX_SIZE, ttl=settings.CACHE_TTL_SECONDS)
    
    @staticmethod
    def _is_safe_url(url: str) -> Tuple[bool, Optional[str]]:
        """
        Valida se a URL é segura para download.
        
        Args:
            url (str): URL a ser validada
            
        Returns:
            Tuple[bool, Optional[str]]: (é_segura, mensagem_erro)
        """
        try:
            parsed = urlparse(url)
            
            # Verificar se o esquema é HTTP ou HTTPS
            if parsed.scheme not in ['http', 'https']:
                return False, "Apenas URLs HTTP e HTTPS são permitidas"
            
            # Verificar domínios bloqueados
            hostname = parsed.hostname
            if hostname:
                hostname_lower = hostname.lower()
                for blocked in settings.BLOCKED_DOMAINS:
                    if hostname_lower.startswith(blocked):
                        return False, "URLs para endereços privados/localhost não são permitidas"
            
            return True, None
            
        except Exception as e:
            return False, f"URL inválida: {str(e)}"
    
    @staticmethod
    def _get_url_hash(url: str) -> str:
        """Gera um hash SHA256 da URL para usar como chave do cache."""
        return hashlib.sha256(url.encode('utf-8')).hexdigest()
    
    @staticmethod
    def download_and_validate_xml(url: str) -> Tuple[bool, Optional[str], Optional[str], bool]:
        """
        Baixa e valida um arquivo XML de uma URL.
        
        Args:
            url (str): URL do arquivo XML
            
        Returns:
            Tuple[bool, Optional[str], Optional[str], bool]: 
            (sucesso, conteudo_xml, mensagem_erro, veio_do_cache)
        """
        try:
            # Verificar cache primeiro
            url_hash = XMLDownloadService._get_url_hash(url)
            if url_hash in XMLDownloadService._cache:
                logger.info(f"XML encontrado no cache para URL: {url}")
                cached_content = XMLDownloadService._cache[url_hash]
                return True, cached_content, None, True
            
            # Validar se a URL é segura
            is_safe, safety_error = XMLDownloadService._is_safe_url(url)
            if not is_safe:
                logger.warning(f"URL não segura rejeitada: {url} - {safety_error}")
                return False, None, safety_error, False
            
            # Configurar headers para simular um navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/xml, text/xml, */*',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache'
            }
            
            logger.info(f"Iniciando download da URL: {url}")
            
            # Fazer a requisição com timeout e verificação de tamanho
            response = requests.get(url, headers=headers, timeout=settings.HTTP_TIMEOUT_SECONDS, stream=True)
            response.raise_for_status()
            
            # Verificar o tamanho do arquivo
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > settings.MAX_FILE_SIZE:
                return False, None, f"Arquivo muito grande. Tamanho máximo permitido: {settings.MAX_FILE_SIZE_MB}MB", False
            
            # Verificar Content-Type
            content_type = response.headers.get('content-type', '').lower()
            logger.info(f"Content-Type recebido: {content_type}")
            
            # Baixar o conteúdo de forma segura (verificando tamanho durante o download)
            content_chunks = []
            total_size = 0
            
            for chunk in response.iter_content(chunk_size=8192, decode_unicode=True):
                if chunk:
                    total_size += len(chunk.encode('utf-8'))
                    if total_size > settings.MAX_FILE_SIZE:
                        return False, None, f"Arquivo muito grande. Tamanho máximo permitido: {settings.MAX_FILE_SIZE_MB}MB", False
                    content_chunks.append(chunk)
            
            content = ''.join(content_chunks)
            
            # Verificar se o conteúdo parece ser XML
            if not content.strip().startswith('<?xml') and not content.strip().startswith('<'):
                return False, None, "O conteúdo baixado não parece ser um arquivo XML", False
            
            # Verificar por padrões suspeitos em XML (proteção básica contra XXE)
            suspicious_patterns = [
                r'<!ENTITY.*SYSTEM',
                r'<!ENTITY.*PUBLIC',
                r'<!ELEMENT.*ANY'
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    logger.warning(f"Padrão suspeito detectado no XML: {pattern}")
                    return False, None, "XML contém elementos potencialmente perigosos", False
            
            # Tentar fazer parse do XML para validar
            try:
                # Usar parser XML padrão (mais seguro em versões recentes)
                root = ET.fromstring(content)
                logger.info("XML validado com sucesso")
                
                # Verificar se o XML não é muito complexo (proteção contra XML bombs)
                xml_str = ET.tostring(root, encoding='unicode')
                if len(xml_str) > settings.MAX_FILE_SIZE:
                    return False, None, "XML expandido é muito grande", False
                
                # Salvar no cache apenas se o XML for válido e não muito grande
                XMLDownloadService._cache[url_hash] = content
                logger.info(f"XML salvo no cache para URL: {url}")
                
                return True, content, None, False
                
            except ET.ParseError as e:
                logger.error(f"Erro ao fazer parse do XML: {e}")
                return False, None, f"O arquivo baixado não é um XML válido: {str(e)}", False
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout ao tentar baixar o arquivo da URL fornecida"
            logger.error(error_msg)
            return False, None, error_msg, False
            
        except requests.exceptions.ConnectionError:
            error_msg = "Erro de conexão ao tentar acessar a URL"
            logger.error(error_msg)
            return False, None, error_msg, False
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"Erro HTTP ao acessar a URL: {e.response.status_code}"
            logger.error(error_msg)
            return False, None, error_msg, False
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro ao fazer requisição: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg, False
            
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg, False