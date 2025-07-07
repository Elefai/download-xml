#!/usr/bin/env python3
"""
Script de teste para a XML Download API
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testando XML Download API\n")
    
    # Teste 1: Health Check
    print("1. Testando Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health Check OK")
        else:
            print(f"❌ Health Check falhou: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Certifique-se de que a API está rodando.")
        return
    
    # Teste 2: Endpoint principal com URL inválida
    print("\n2. Testando com URL inválida...")
    invalid_payload = {"url": "not-a-valid-url"}
    try:
        response = requests.post(f"{base_url}/api/v1/download_xml", json=invalid_payload)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 3: Endpoint principal sem URL
    print("\n3. Testando sem fornecer URL...")
    try:
        response = requests.post(f"{base_url}/api/v1/download_xml", json={})
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 4: Teste com URL válida (exemplo de XML público)
    print("\n4. Testando com URL de XML válida...")
    # Usando um XML de exemplo que geralmente está disponível
    valid_payload = {
        "url": "https://www.w3schools.com/xml/note.xml"
    }
    try:
        response = requests.post(f"{base_url}/api/v1/download_xml", json=valid_payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        if response.status_code == 200:
            print("✅ Download bem-sucedido!")
            print(f"XML Content (primeiros 200 caracteres): {result['xml_content'][:200]}...")
        else:
            print(f"❌ Falha no download: {result}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n🏁 Testes concluídos!")

if __name__ == "__main__":
    test_api()