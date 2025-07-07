#!/usr/bin/env python3
"""
Exemplo de como consumir a XML Download API de outro serviço Docker
"""

import os
import time
import requests
import json
from datetime import datetime

# Configuração da API
XML_API_URL = os.getenv('XML_API_URL', 'http://xml-api:8000')
XML_API_ENDPOINT = f"{XML_API_URL}/api/v1/download_xml"

def wait_for_api():
    """Aguarda a API estar disponível"""
    print("🕐 Aguardando XML Download API estar disponível...")
    
    for attempt in range(30):
        try:
            response = requests.get(f"{XML_API_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✅ XML Download API está disponível!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"⏳ Tentativa {attempt + 1}/30 - Aguardando...")
        time.sleep(2)
    
    print("❌ Timeout: XML Download API não está disponível")
    return False

def download_xml(url):
    """Baixa XML usando a API"""
    try:
        print(f"📥 Baixando XML de: {url}")
        
        payload = {"url": url}
        response = requests.post(
            XML_API_ENDPOINT,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Download bem-sucedido! Tamanho: {len(result['xml_content'])} caracteres")
            return result['xml_content']
        else:
            error = response.json()
            print(f"❌ Erro no download: {error.get('mensagem', 'Erro desconhecido')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None

def process_xml(xml_content):
    """Processa o conteúdo XML (exemplo)"""
    if not xml_content:
        return
    
    print("🔄 Processando XML...")
    
    # Exemplo simples: contar elementos
    import xml.etree.ElementTree as ET
    
    try:
        root = ET.fromstring(xml_content)
        element_count = len(list(root.iter()))
        print(f"📊 XML processado: {element_count} elementos encontrados")
        print(f"📋 Elemento raiz: {root.tag}")
        
        # Salvar para análise posterior (opcional)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/tmp/xml_processed_{timestamp}.xml"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"💾 XML salvo em: {filename}")
        
    except ET.ParseError as e:
        print(f"❌ Erro ao processar XML: {e}")

def main():
    """Função principal"""
    print("🚀 Iniciando Consumer da XML Download API")
    print(f"🌐 URL da API: {XML_API_URL}")
    
    # Aguardar API estar disponível
    if not wait_for_api():
        return
    
    # URLs de exemplo para testar
    test_urls = [
        "https://www.w3schools.com/xml/note.xml",
        "https://www.w3schools.com/xml/simple.xml",
        "https://httpbin.org/xml"
    ]
    
    print(f"\n📋 Testando {len(test_urls)} URLs...")
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n--- Teste {i}/{len(test_urls)} ---")
        
        # Baixar XML
        xml_content = download_xml(url)
        
        # Processar se baixou com sucesso
        if xml_content:
            process_xml(xml_content)
        
        # Aguardar entre requisições
        if i < len(test_urls):
            print("⏳ Aguardando 3 segundos...")
            time.sleep(3)
    
    print("\n🏁 Testes concluídos!")
    
    # Manter o container rodando para demonstração
    print("\n🔄 Entrando em loop de monitoramento...")
    while True:
        try:
            # Verificar saúde da API a cada 30 segundos
            response = requests.get(f"{XML_API_URL}/health", timeout=5)
            status = "🟢 OK" if response.status_code == 200 else f"🔴 ERROR {response.status_code}"
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] API Status: {status}")
            
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] API Status: 🔴 OFFLINE ({e})")
        
        time.sleep(30)

if __name__ == "__main__":
    main()