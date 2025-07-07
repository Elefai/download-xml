import requests
import xml.etree.ElementTree as ET
from typing import Tuple, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class XMLDownloadService:
    
    @staticmethod
    def download_and_validate_xml(url: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Baixa e valida um arquivo XML de uma URL.
        
        Args:
            url (str): URL do arquivo XML
            
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: 
            (sucesso, conteudo_xml, mensagem_erro)
        """
        try:
            # Configurar headers para simular um navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            logger.info(f"Iniciando download da URL: {url}")
            
            # Fazer a requisição com timeout
            response = requests.get(url, headers=headers, timeout=30)
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
            
            # Obter o conteúdo
            content = response.text
            
            # Tentar fazer parse do XML para validar
            try:
                ET.fromstring(content)
                logger.info("XML validado com sucesso")
                return True, content, None
            except ET.ParseError as e:
                logger.error(f"Erro ao fazer parse do XML: {e}")
                return False, None, f"O arquivo baixado não é um XML válido: {str(e)}"
                
        except requests.exceptions.Timeout:
            error_msg = "Timeout ao tentar baixar o arquivo da URL fornecida"
            logger.error(error_msg)
            return False, None, error_msg
            
        except requests.exceptions.ConnectionError:
            error_msg = "Erro de conexão ao tentar acessar a URL"
            logger.error(error_msg)
            return False, None, error_msg
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"Erro HTTP ao acessar a URL: {e.response.status_code}"
            logger.error(error_msg)
            return False, None, error_msg
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro ao fazer requisição: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
            
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg