#!/bin/bash

# =============================================================================
# XML Download API - Instalador Automático
# =============================================================================
# Este script instala e configura automaticamente a XML Download API
# Compatível com: Ubuntu, Debian, CentOS, RHEL, Amazon Linux, Alpine
# =============================================================================

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Símbolos
CHECK_MARK="✅"
CROSS_MARK="❌"
ARROW="➡️"
ROCKET="🚀"
GEAR="⚙️"
PACKAGE="📦"

# Configurações
API_PORT=${API_PORT:-8000}
API_HOST=${API_HOST:-"0.0.0.0"}
INSTALL_DIR="$HOME/xml-download-api"
VENV_DIR="$INSTALL_DIR/venv"
SERVICE_NAME="xml-download-api"

# Função para imprimir cabeçalho
print_header() {
    clear
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                                                                  ║"
    echo "║               🚀 XML Download API - Instalador                   ║"
    echo "║                                                                  ║"
    echo "║          Instalação automática para containers Linux            ║"
    echo "║                                                                  ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
}

# Função para logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${CYAN}${ARROW} $1${NC}"
}

# Função para detectar o sistema operacional
detect_os() {
    log_step "Detectando sistema operacional..."
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        log_info "Sistema detectado: $OS $VER"
    elif type lsb_release >/dev/null 2>&1; then
        OS=$(lsb_release -si)
        VER=$(lsb_release -sr)
        log_info "Sistema detectado: $OS $VER"
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        OS=$DISTRIB_ID
        VER=$DISTRIB_RELEASE
        log_info "Sistema detectado: $OS $VER"
    else
        log_error "Não foi possível detectar o sistema operacional"
        exit 1
    fi
}

# Função para instalar dependências baseado no OS
install_dependencies() {
    log_step "Instalando dependências do sistema..."
    
    case "$OS" in
        *"Ubuntu"*|*"Debian"*)
            log_info "Usando apt para instalar dependências..."
            export DEBIAN_FRONTEND=noninteractive
            apt-get update -qq
            apt-get install -y -qq \
                python3 \
                python3-pip \
                python3-venv \
                python3-dev \
                curl \
                wget \
                git \
                build-essential \
                ca-certificates \
                gnupg \
                lsb-release > /dev/null 2>&1
            ;;
        *"CentOS"*|*"Red Hat"*|*"Amazon Linux"*|*"Rocky"*|*"AlmaLinux"*)
            log_info "Usando yum/dnf para instalar dependências..."
            if command -v dnf &> /dev/null; then
                PKG_MANAGER="dnf"
            else
                PKG_MANAGER="yum"
            fi
            $PKG_MANAGER update -y -q
            $PKG_MANAGER install -y -q \
                python3 \
                python3-pip \
                python3-devel \
                curl \
                wget \
                git \
                gcc \
                gcc-c++ \
                make \
                ca-certificates > /dev/null 2>&1
            ;;
        *"Alpine"*)
            log_info "Usando apk para instalar dependências..."
            apk update > /dev/null 2>&1
            apk add --no-cache \
                python3 \
                python3-dev \
                py3-pip \
                curl \
                wget \
                git \
                build-base \
                ca-certificates > /dev/null 2>&1
            ;;
        *)
            log_warning "Sistema operacional não reconhecido. Tentando instalação genérica..."
            if command -v python3 &> /dev/null && command -v pip3 &> /dev/null; then
                log_info "Python3 e pip3 já estão disponíveis"
            else
                log_error "Python3 ou pip3 não encontrados. Instale manualmente."
                exit 1
            fi
            ;;
    esac
    
    log_success "Dependências instaladas com sucesso!"
}

# Função para verificar e instalar Python
check_python() {
    log_step "Verificando instalação do Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        log_success "Python $PYTHON_VERSION encontrado"
        
        # Verificar se a versão é 3.8+
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
            log_success "Versão do Python é compatível (>= 3.8)"
        else
            log_error "Python 3.8+ é necessário. Versão atual: $PYTHON_VERSION"
            exit 1
        fi
    else
        log_error "Python3 não encontrado"
        exit 1
    fi
    
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
        log_success "pip $PIP_VERSION encontrado"
    else
        log_error "pip3 não encontrado"
        exit 1
    fi
}

# Função para clonar o repositório ou usar código local
setup_application() {
    log_step "Configurando aplicação..."
    
    # Se já estivermos no diretório da aplicação, usar código local
    if [ -f "app/main.py" ] && [ -f "requirements.txt" ]; then
        log_info "Usando código local da aplicação"
        INSTALL_DIR=$(pwd)
        VENV_DIR="$INSTALL_DIR/venv"
    else
        log_info "Código local não encontrado. Por favor, execute este script no diretório da aplicação."
        log_info "Ou certifique-se de que os arquivos app/main.py e requirements.txt existem."
        exit 1
    fi
    
    log_success "Aplicação localizada em: $INSTALL_DIR"
}

# Função para criar ambiente virtual
create_virtualenv() {
    log_step "Criando ambiente virtual Python..."
    
    if [ -d "$VENV_DIR" ]; then
        log_warning "Ambiente virtual já existe. Removendo..."
        rm -rf "$VENV_DIR"
    fi
    
    python3 -m venv "$VENV_DIR"
    log_success "Ambiente virtual criado em: $VENV_DIR"
    
    # Ativar ambiente virtual
    source "$VENV_DIR/bin/activate"
    log_success "Ambiente virtual ativado"
    
    # Atualizar pip
    log_info "Atualizando pip..."
    pip install --upgrade pip > /dev/null 2>&1
}

# Função para instalar dependências Python
install_python_deps() {
    log_step "Instalando dependências Python..."
    
    if [ ! -f "$INSTALL_DIR/requirements.txt" ]; then
        log_error "Arquivo requirements.txt não encontrado em $INSTALL_DIR"
        exit 1
    fi
    
    source "$VENV_DIR/bin/activate"
    pip install -r "$INSTALL_DIR/requirements.txt" > /dev/null 2>&1
    log_success "Dependências Python instaladas!"
}

# Função para testar a aplicação
test_application() {
    log_step "Testando aplicação..."
    
    source "$VENV_DIR/bin/activate"
    cd "$INSTALL_DIR"
    
    # Testar importação dos módulos
    python3 -c "
import sys
sys.path.append('.')
try:
    from app.main import app
    from app.services.xml_service import XMLDownloadService
    from app.models.schemas import DownloadRequest
    print('✅ Todos os módulos importados com sucesso!')
except ImportError as e:
    print(f'❌ Erro na importação: {e}')
    sys.exit(1)
" || {
        log_error "Falha no teste de importação dos módulos"
        exit 1
    }
    
    log_success "Teste da aplicação concluído com sucesso!"
}

# Função para criar script de inicialização
create_start_script() {
    log_step "Criando script de inicialização..."
    
    cat > "$INSTALL_DIR/start.sh" << 'EOF'
#!/bin/bash

# Script para iniciar a XML Download API
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "🚀 Iniciando XML Download API..."

# Verificar se o ambiente virtual existe
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Ambiente virtual não encontrado. Execute install.sh primeiro."
    exit 1
fi

# Ativar ambiente virtual
source "$VENV_DIR/bin/activate"

# Navegar para o diretório da aplicação
cd "$SCRIPT_DIR"

# Configurar variáveis de ambiente
export PYTHONPATH="$SCRIPT_DIR"

# Verificar porta disponível
PORT=${API_PORT:-8000}
HOST=${API_HOST:-"0.0.0.0"}

if command -v lsof &> /dev/null; then
    if lsof -i :$PORT &> /dev/null; then
        echo "⚠️  Porta $PORT está em uso. Tentando porta alternativa..."
        PORT=$((PORT + 1))
    fi
fi

echo "📡 Iniciando servidor em http://$HOST:$PORT"
echo "📖 Documentação disponível em: http://$HOST:$PORT/docs"
echo "🔧 Para parar o servidor, pressione Ctrl+C"
echo ""

# Iniciar aplicação
uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
EOF
    
    chmod +x "$INSTALL_DIR/start.sh"
    log_success "Script de inicialização criado: $INSTALL_DIR/start.sh"
}

# Função para criar script de parada
create_stop_script() {
    log_step "Criando script de parada..."
    
    cat > "$INSTALL_DIR/stop.sh" << 'EOF'
#!/bin/bash

echo "🛑 Parando XML Download API..."

# Encontrar e parar processos uvicorn relacionados
PIDS=$(pgrep -f "uvicorn.*app\.main:app" 2>/dev/null || true)

if [ -n "$PIDS" ]; then
    echo "📋 Encontrados processos: $PIDS"
    echo "$PIDS" | xargs kill -TERM 2>/dev/null || true
    sleep 2
    
    # Verificar se ainda existem processos
    REMAINING_PIDS=$(pgrep -f "uvicorn.*app\.main:app" 2>/dev/null || true)
    if [ -n "$REMAINING_PIDS" ]; then
        echo "⚡ Forçando parada de processos restantes..."
        echo "$REMAINING_PIDS" | xargs kill -KILL 2>/dev/null || true
    fi
    
    echo "✅ XML Download API parada com sucesso!"
else
    echo "ℹ️  Nenhum processo da XML Download API encontrado"
fi
EOF
    
    chmod +x "$INSTALL_DIR/stop.sh"
    log_success "Script de parada criado: $INSTALL_DIR/stop.sh"
}

# Função para criar script de teste
create_test_script() {
    log_step "Criando script de teste..."
    
    cat > "$INSTALL_DIR/test.sh" << 'EOF'
#!/bin/bash

# Script para testar a XML Download API

HOST=${API_HOST:-"localhost"}
PORT=${API_PORT:-8000}
BASE_URL="http://$HOST:$PORT"

echo "🧪 Testando XML Download API em $BASE_URL"
echo ""

# Função para testar endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo "🔍 Testando: $description"
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" \
                   -H "Content-Type: application/json" \
                   -d "$data" 2>/dev/null)
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" 2>/dev/null)
    fi
    
    # Separar resposta e código HTTP
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        echo "✅ Sucesso ($http_code)"
        echo "📄 Resposta: $(echo "$body" | head -c 100)..."
    else
        echo "❌ Falha ($http_code)"
        echo "📄 Resposta: $body"
    fi
    echo ""
}

# Aguardar API estar disponível
echo "⏳ Aguardando API estar disponível..."
for i in {1..30}; do
    if curl -s "$BASE_URL/health" > /dev/null 2>&1; then
        echo "✅ API está respondendo!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Timeout: API não está respondendo após 30 tentativas"
        echo "💡 Certifique-se de que a API está rodando com: ./start.sh"
        exit 1
    fi
    sleep 1
done

echo ""

# Executar testes
test_endpoint "GET" "/health" "" "Health Check"
test_endpoint "GET" "/" "" "Endpoint raiz"
test_endpoint "POST" "/api/v1/download_xml" '{"url":"https://www.w3schools.com/xml/note.xml"}' "Download de XML válido"
test_endpoint "POST" "/api/v1/download_xml" '{"url":"invalid-url"}' "URL inválida (deve retornar erro)"
test_endpoint "POST" "/api/v1/download_xml" '{}' "Sem URL (deve retornar erro)"

echo "🏁 Testes concluídos!"
echo "📖 Acesse a documentação em: $BASE_URL/docs"
EOF
    
    chmod +x "$INSTALL_DIR/test.sh"
    log_success "Script de teste criado: $INSTALL_DIR/test.sh"
}

# Função para exibir informações finais
show_final_info() {
    log_success "Instalação concluída com sucesso!"
    echo ""
    echo -e "${WHITE}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${WHITE}║                     🎉 INSTALAÇÃO CONCLUÍDA!                    ║${NC}"
    echo -e "${WHITE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}📍 Localização da aplicação:${NC} $INSTALL_DIR"
    echo -e "${CYAN}🐍 Ambiente virtual:${NC} $VENV_DIR"
    echo ""
    echo -e "${WHITE}🚀 Para iniciar a aplicação:${NC}"
    echo -e "   ${GREEN}cd $INSTALL_DIR && ./start.sh${NC}"
    echo ""
    echo -e "${WHITE}🧪 Para testar a aplicação:${NC}"
    echo -e "   ${GREEN}cd $INSTALL_DIR && ./test.sh${NC}"
    echo ""
    echo -e "${WHITE}🛑 Para parar a aplicação:${NC}"
    echo -e "   ${GREEN}cd $INSTALL_DIR && ./stop.sh${NC}"
    echo ""
    echo -e "${WHITE}📖 URLs importantes:${NC}"
    echo -e "   ${BLUE}Documentação:${NC} http://localhost:$API_PORT/docs"
    echo -e "   ${BLUE}Health Check:${NC} http://localhost:$API_PORT/health"
    echo -e "   ${BLUE}API Endpoint:${NC} http://localhost:$API_PORT/api/v1/download_xml"
    echo ""
    echo -e "${YELLOW}💡 Dicas:${NC}"
    echo -e "   • Use ${GREEN}export API_PORT=9000${NC} para mudar a porta"
    echo -e "   • Use ${GREEN}export API_HOST=0.0.0.0${NC} para aceitar conexões externas"
    echo -e "   • Logs aparecem no terminal onde você executou ./start.sh"
    echo ""
    echo -e "${PURPLE}🎯 Exemplo de uso:${NC}"
    echo -e '   curl -X POST "http://localhost:'$API_PORT'/api/v1/download_xml" \'
    echo -e '        -H "Content-Type: application/json" \'
    echo -e '        -d '"'"'{"url": "https://www.w3schools.com/xml/note.xml"}'"'"
    echo ""
}

# Função principal
main() {
    print_header
    
    log_info "Iniciando instalação automática da XML Download API..."
    echo ""
    
    # Verificar se está rodando como root em container
    if [ "$EUID" -ne 0 ] && [ ! -w /usr/local/bin ] 2>/dev/null; then
        log_warning "Recomenda-se executar como root em containers para instalar dependências do sistema"
        log_info "Continuando com instalação no diretório do usuário..."
    fi
    
    # Executar etapas de instalação
    detect_os
    install_dependencies
    check_python
    setup_application
    create_virtualenv
    install_python_deps
    test_application
    create_start_script
    create_stop_script
    create_test_script
    
    # Informações finais
    show_final_info
}

# Verificar se o script está sendo executado (não sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi