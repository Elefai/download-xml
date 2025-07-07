#!/bin/bash

# =============================================================================
# XML Download API - Quick Install (One-liner)
# =============================================================================
# Este script baixa o código e executa a instalação automaticamente
# Uso: curl -sSL https://raw.githubusercontent.com/seu-usuario/xml-download-api/main/quick-install.sh | bash
# =============================================================================

set -e

echo "🚀 XML Download API - Instalação Automática"
echo "============================================="
echo ""

# Configurações
REPO_URL="https://github.com/seu-usuario/xml-download-api"
INSTALL_DIR="$HOME/xml-download-api"
TEMP_DIR="/tmp/xml-download-api-install"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se git está disponível
if ! command -v git &> /dev/null; then
    log_error "Git não está instalado. Por favor, instale git primeiro."
    echo "Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y git"
    echo "CentOS/RHEL: sudo yum install -y git"
    echo "Alpine: sudo apk add git"
    exit 1
fi

# Limpar instalação anterior se existir
if [ -d "$INSTALL_DIR" ]; then
    log_info "Removendo instalação anterior..."
    rm -rf "$INSTALL_DIR"
fi

# Criar diretório temporário
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

log_info "Baixando código da aplicação..."

# Tentar clonar o repositório
if git clone "$REPO_URL" "$TEMP_DIR" 2>/dev/null; then
    log_success "Código baixado com sucesso!"
else
    log_error "Falha ao baixar código do repositório: $REPO_URL"
    log_error "Certifique-se de que:"
    log_error "1. O repositório existe e está público"
    log_error "2. Você tem conexão com a internet"
    log_error "3. A URL do repositório está correta"
    exit 1
fi

# Mover para diretório final
log_info "Instalando em: $INSTALL_DIR"
mv "$TEMP_DIR" "$INSTALL_DIR"

# Executar instalação
log_info "Executando instalação automática..."
cd "$INSTALL_DIR"

if [ -x "./install.sh" ]; then
    ./install.sh
else
    log_error "Script de instalação não encontrado ou não é executável"
    exit 1
fi

echo ""
log_success "Instalação automática concluída!"
echo ""
echo -e "${YELLOW}💡 Próximos passos:${NC}"
echo -e "   1. ${GREEN}cd $INSTALL_DIR${NC}"
echo -e "   2. ${GREEN}./start.sh${NC}"
echo ""