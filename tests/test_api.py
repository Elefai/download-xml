"""
Testes de integração para a API XML Download
"""
import pytest
from fastapi.testclient import TestClient
from tests.test_app import test_app

client = TestClient(test_app)

class TestXMLDownloadAPI:
    
    def test_root_endpoint(self):
        """Testa o endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "features" in data
    
    def test_health_endpoint(self):
        """Testa o endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_cache_stats_endpoint(self):
        """Testa o endpoint de estatísticas do cache"""
        response = client.get("/api/v1/cache/stats")
        assert response.status_code == 200
        data = response.json()
        assert "cache_size" in data
        assert "max_cache_size" in data
        assert "ttl_seconds" in data
    
    def test_download_xml_invalid_url(self):
        """Testa download com URL inválida"""
        response = client.post(
            "/api/v1/download_xml",
            json={"url": "not-a-valid-url"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_download_xml_localhost_blocked(self):
        """Testa bloqueio de URLs localhost"""
        response = client.post(
            "/api/v1/download_xml",
            json={"url": "http://localhost/test.xml"}
        )
        assert response.status_code == 500
        data = response.json()
        assert data["detail"]["status"] == "erro"
        assert "privados/localhost" in data["detail"]["mensagem"]
    
    def test_download_xml_private_ip_blocked(self):
        """Testa bloqueio de IPs privados"""
        response = client.post(
            "/api/v1/download_xml",
            json={"url": "http://192.168.1.1/test.xml"}
        )
        assert response.status_code == 500
        data = response.json()
        assert data["detail"]["status"] == "erro"
        assert "privados/localhost" in data["detail"]["mensagem"]
    
    def test_download_xml_invalid_scheme(self):
        """Testa bloqueio de esquemas inválidos"""
        response = client.post(
            "/api/v1/download_xml",
            json={"url": "ftp://example.com/test.xml"}
        )
        assert response.status_code == 422  # Pydantic validation error
    
    def test_openapi_docs(self):
        """Testa se a documentação OpenAPI está disponível"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_docs(self):
        """Testa se a documentação ReDoc está disponível"""
        response = client.get("/redoc")
        assert response.status_code == 200