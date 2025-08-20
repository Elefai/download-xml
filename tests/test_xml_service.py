"""
Testes unitários para o XMLDownloadService
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.xml_service import XMLDownloadService

class TestXMLDownloadService:
    
    def test_is_safe_url_valid_https(self):
        """Testa validação de URL HTTPS válida"""
        is_safe, error = XMLDownloadService._is_safe_url("https://example.com/file.xml")
        assert is_safe is True
        assert error is None
    
    def test_is_safe_url_valid_http(self):
        """Testa validação de URL HTTP válida"""
        is_safe, error = XMLDownloadService._is_safe_url("http://example.com/file.xml")
        assert is_safe is True
        assert error is None
    
    def test_is_safe_url_blocked_localhost(self):
        """Testa bloqueio de URLs localhost"""
        is_safe, error = XMLDownloadService._is_safe_url("http://localhost/file.xml")
        assert is_safe is False
        assert "privados/localhost" in error
    
    def test_is_safe_url_blocked_private_ip(self):
        """Testa bloqueio de IPs privados"""
        is_safe, error = XMLDownloadService._is_safe_url("http://192.168.1.1/file.xml")
        assert is_safe is False
        assert "privados/localhost" in error
    
    def test_is_safe_url_invalid_scheme(self):
        """Testa bloqueio de esquemas inválidos"""
        is_safe, error = XMLDownloadService._is_safe_url("ftp://example.com/file.xml")
        assert is_safe is False
        assert "HTTP e HTTPS" in error
    
    def test_get_url_hash(self):
        """Testa geração de hash da URL"""
        url = "https://example.com/test.xml"
        hash1 = XMLDownloadService._get_url_hash(url)
        hash2 = XMLDownloadService._get_url_hash(url)
        
        assert hash1 == hash2  # Mesmo URL deve gerar mesmo hash
        assert len(hash1) == 64  # SHA256 tem 64 caracteres hexadecimais
    
    @patch('app.services.xml_service.requests.get')
    def test_download_and_validate_xml_success(self, mock_get):
        """Testa download e validação bem-sucedidos"""
        # Mock da resposta HTTP
        mock_response = MagicMock()
        mock_response.headers = {'content-type': 'application/xml'}
        mock_response.iter_content.return_value = ['<?xml version="1.0"?><root></root>']
        mock_get.return_value = mock_response
        
        url = "https://example.com/test.xml"
        success, content, error, from_cache = XMLDownloadService.download_and_validate_xml(url)
        
        assert success is True
        assert content == '<?xml version="1.0"?><root></root>'
        assert error is None
        assert from_cache is False
    
    def test_download_and_validate_xml_cache(self):
        """Testa funcionamento do cache"""
        # Limpar cache
        XMLDownloadService._cache.clear()
        
        # Simular item no cache
        url = "https://example.com/cached.xml"
        xml_content = '<?xml version="1.0"?><cached></cached>'
        url_hash = XMLDownloadService._get_url_hash(url)
        XMLDownloadService._cache[url_hash] = xml_content
        
        success, content, error, from_cache = XMLDownloadService.download_and_validate_xml(url)
        
        assert success is True
        assert content == xml_content
        assert error is None
        assert from_cache is True
    
    def test_download_and_validate_xml_unsafe_url(self):
        """Testa rejeição de URL não segura"""
        url = "http://localhost/test.xml"
        success, content, error, from_cache = XMLDownloadService.download_and_validate_xml(url)
        
        assert success is False
        assert content is None
        assert "privados/localhost" in error
        assert from_cache is False