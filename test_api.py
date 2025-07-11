#!/usr/bin/env python3
"""
Script de teste para a XML Download API
"""

import pytest
import httpx
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Testa o endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "XML Download API está funcionando!"
    assert "docs" in data
    assert "version" in data

def test_download_xml_success():
    """Testa download de XML válido"""
    test_url = "https://www.w3schools.com/xml/note.xml"
    
    response = client.post(
        "/api/v1/download_xml",
        json={"url": test_url}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "sucesso"
    assert "xml_content" in data
    assert "<?xml" in data["xml_content"]

def test_download_xml_invalid_url():
    """Testa download com URL inválida"""
    response = client.post(
        "/api/v1/download_xml",
        json={"url": "invalid-url"}
    )
    
    assert response.status_code == 422  # Pydantic validation error

def test_download_xml_missing_url():
    """Testa download sem URL"""
    response = client.post(
        "/api/v1/download_xml",
        json={}
    )
    
    assert response.status_code == 422  # Pydantic validation error

def test_download_xml_nonexistent_url():
    """Testa download de URL que não existe"""
    response = client.post(
        "/api/v1/download_xml",
        json={"url": "https://exemplo-nao-existe-12345.com/arquivo.xml"}
    )
    
    assert response.status_code == 500
    data = response.json()
    assert data["detail"]["status"] == "erro"

def test_download_xml_stream_success():
    """Testa download de XML em streaming"""
    test_url = "https://www.w3schools.com/xml/note.xml"
    
    response = client.post(
        "/api/v1/download_xml_stream",
        json={"url": test_url}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml; charset=utf-8"
    assert "Content-Disposition" in response.headers
    
    # Verificar se o conteúdo é XML válido
    content = response.content.decode('utf-8')
    assert "<?xml" in content

def test_download_xml_stream_invalid_url():
    """Testa streaming com URL inválida"""
    response = client.post(
        "/api/v1/download_xml_stream",
        json={"url": "invalid-url"}
    )
    
    assert response.status_code == 422  # Pydantic validation error

def test_analyze_large_xml_success():
    """Testa análise de XML grande"""
    test_url = "https://www.w3schools.com/xml/note.xml"
    
    response = client.post(
        "/api/v1/xml_info",
        json={"url": test_url}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "sucesso"
    assert "xml_info" in data
    
    xml_info = data["xml_info"]
    assert "root_tag" in xml_info
    assert "element_count" in xml_info
    assert "max_depth" in xml_info
    assert "namespaces" in xml_info
    assert isinstance(xml_info["element_count"], int)
    assert xml_info["element_count"] > 0

def test_analyze_large_xml_invalid_url():
    """Testa análise com URL inválida"""
    response = client.post(
        "/api/v1/xml_info",
        json={"url": "invalid-url"}
    )
    
    assert response.status_code == 422  # Pydantic validation error

@pytest.mark.asyncio
async def test_xml_service_directly():
    """Testa o XMLDownloadService diretamente"""
    from app.services.xml_service import XMLDownloadService
    
    test_url = "https://www.w3schools.com/xml/note.xml"
    
    # Testar download assíncrono
    success, content, error = await XMLDownloadService.download_and_validate_xml(test_url)
    
    assert success is True
    assert content is not None
    assert error is None
    assert "<?xml" in content

@pytest.mark.asyncio 
async def test_xml_service_large_analysis():
    """Testa análise iterativa diretamente"""
    from app.services.xml_service import XMLDownloadService
    
    test_url = "https://www.w3schools.com/xml/note.xml"
    
    # Testar análise iterativa
    success, xml_info, error = await XMLDownloadService.process_large_xml_iteratively(test_url)
    
    assert success is True
    assert xml_info is not None
    assert error is None
    assert "root_tag" in xml_info
    assert "element_count" in xml_info
    assert xml_info["element_count"] > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])