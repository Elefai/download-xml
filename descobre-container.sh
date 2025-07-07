#!/bin/bash

# ============================================================================
# Script para descobrir informações do container para chamadas internas
# ============================================================================

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}🔍 Descobrindo informações do container para chamadas internas${NC}"
echo ""

# Nome do container
echo -e "${YELLOW}📛 Nome do container:${NC}"
CONTAINER_NAME=$(hostname)
echo -e "   ${GREEN}$CONTAINER_NAME${NC}"
echo ""

# IP do container
echo -e "${YELLOW}🌐 IP interno do container:${NC}"
CONTAINER_IP=$(hostname -I | awk '{print $1}')
echo -e "   ${GREEN}$CONTAINER_IP${NC}"
echo ""

# Verificar se a API está rodando
echo -e "${YELLOW}🔍 Verificando se a API está rodando:${NC}"
if ps aux | grep -q "[u]vicorn.*app\.main:app"; then
    echo -e "   ${GREEN}✅ API está rodando (uvicorn)${NC}"
    
    # Testar endpoint local
    echo ""
    echo -e "${YELLOW}🧪 Testando endpoint local:${NC}"
    if command -v curl >/dev/null 2>&1; then
        if curl -s http://localhost:8000/health >/dev/null 2>&1; then
            echo -e "   ${GREEN}✅ API respondendo em localhost:8000${NC}"
            
            # Mostrar resposta do health
            HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
            echo -e "   ${CYAN}Resposta:${NC} $HEALTH_RESPONSE"
        else
            echo -e "   ❌ API não está respondendo em localhost:8000"
        fi
    else
        echo -e "   ⚠️  curl não encontrado - instale para testar"
    fi
else
    echo -e "   ❌ API não está rodando"
    echo -e "   💡 Execute ./start.sh para iniciar"
fi

echo ""
echo -e "${BLUE}📋 Como outros containers podem chamar sua API:${NC}"
echo ""

echo -e "${YELLOW}🔗 Por nome do container:${NC}"
echo -e "   ${GREEN}curl http://$CONTAINER_NAME:8000/health${NC}"
echo -e "   ${GREEN}curl http://$CONTAINER_NAME:8000/download-xml/${NC}"
echo ""

echo -e "${YELLOW}🔗 Por IP do container:${NC}"
echo -e "   ${GREEN}curl http://$CONTAINER_IP:8000/health${NC}"
echo -e "   ${GREEN}curl http://$CONTAINER_IP:8000/download-xml/${NC}"
echo ""

echo -e "${YELLOW}📝 Exemplo de POST para download de XML:${NC}"
echo -e "${GREEN}curl -X POST \"http://$CONTAINER_NAME:8000/download-xml/\" \\${NC}"
echo -e "${GREEN}     -H \"Content-Type: application/json\" \\${NC}"
echo -e "${GREEN}     -d '{\"url\": \"https://www.w3schools.com/xml/note.xml\"}'${NC}"
echo ""

echo -e "${YELLOW}🔧 Para testar de outro container:${NC}"
echo ""
echo -e "${CYAN}# 1. Criar container de teste:${NC}"
echo -e "${GREEN}docker run --rm -it alpine sh${NC}"
echo ""
echo -e "${CYAN}# 2. Dentro do container de teste:${NC}"
echo -e "${GREEN}apk add curl${NC}"
echo -e "${GREEN}curl http://$CONTAINER_NAME:8000/health${NC}"
echo ""

echo -e "${BLUE}🎯 Informações salvas em: container-info.txt${NC}"

# Salvar informações em arquivo
cat > container-info.txt << EOF
# Informações do Container - XML Download API
# ============================================

Nome do container: $CONTAINER_NAME
IP interno: $CONTAINER_IP
Data/Hora: $(date)

# Como outros containers podem chamar:
# ------------------------------------

# Por nome:
curl http://$CONTAINER_NAME:8000/health
curl http://$CONTAINER_NAME:8000/download-xml/

# Por IP:
curl http://$CONTAINER_IP:8000/health  
curl http://$CONTAINER_IP:8000/download-xml/

# Exemplo de POST:
curl -X POST "http://$CONTAINER_NAME:8000/download-xml/" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.w3schools.com/xml/note.xml"}'

# Teste de outro container:
docker run --rm -it alpine sh
# Dentro do Alpine:
apk add curl
curl http://$CONTAINER_NAME:8000/health
EOF

echo -e "${GREEN}✅ Informações salvas em container-info.txt${NC}"