#!/bin/bash

# =============================================================================
# XML Download API - Script de Release
# =============================================================================
# Este script automatiza o processo de release do projeto
# Uso: ./release.sh [nova-versao]
# Exemplo: ./release.sh 0.0.2
# =============================================================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

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
    echo -e "${CYAN}➡️  $1${NC}"
}

# Cabeçalho
print_header() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                                                                  ║"
    echo "║              🚀 XML Download API - Release Script                ║"
    echo "║                                                                  ║"
    echo "║            Automatiza o processo de criação de releases         ║"
    echo "║                                                                  ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
}

# Verificar se foi fornecida uma versão
check_version_argument() {
    if [ $# -eq 0 ]; then
        log_error "Versão não especificada!"
        echo "Uso: $0 <nova-versao>"
        echo "Exemplo: $0 0.0.2"
        echo ""
        echo "Formato de versionamento semântico: MAJOR.MINOR.PATCH"
        echo "  MAJOR: mudanças incompatíveis na API"
        echo "  MINOR: funcionalidades adicionadas de forma compatível"
        echo "  PATCH: correções de bugs compatíveis"
        exit 1
    fi
    
    NEW_VERSION=$1
    
    # Validar formato de versão (x.y.z)
    if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        log_error "Formato de versão inválido: $NEW_VERSION"
        log_error "Use o formato: x.y.z (exemplo: 0.0.2)"
        exit 1
    fi
}

# Obter versão atual
get_current_version() {
    if [ -f "VERSION" ]; then
        CURRENT_VERSION=$(cat VERSION)
        log_info "Versão atual: $CURRENT_VERSION"
    else
        log_warning "Arquivo VERSION não encontrado. Assumindo primeira versão."
        CURRENT_VERSION="0.0.0"
    fi
}

# Verificar se o git está limpo
check_git_status() {
    log_step "Verificando status do Git..."
    
    if ! git diff-index --quiet HEAD --; then
        log_error "Existem mudanças não commitadas no repositório"
        log_error "Commit ou stash suas mudanças antes de fazer o release"
        git status --short
        exit 1
    fi
    
    log_success "Repositório Git está limpo"
}

# Verificar se a versão já existe
check_version_exists() {
    log_step "Verificando se a versão já existe..."
    
    if git rev-parse "v$NEW_VERSION" >/dev/null 2>&1; then
        log_error "Tag v$NEW_VERSION já existe!"
        log_error "Use uma versão diferente ou delete a tag existente"
        exit 1
    fi
    
    if [[ "$NEW_VERSION" == "$CURRENT_VERSION" ]]; then
        log_error "Nova versão ($NEW_VERSION) é igual à versão atual ($CURRENT_VERSION)"
        exit 1
    fi
    
    log_success "Versão $NEW_VERSION é válida"
}

# Atualizar arquivos com nova versão
update_version_files() {
    log_step "Atualizando arquivos de versão..."
    
    # Atualizar VERSION
    echo "$NEW_VERSION" > VERSION
    log_info "VERSION atualizado"
    
    # Atualizar app/main.py
    sed -i.bak "s/version=\"[^\"]*\"/version=\"$NEW_VERSION\"/g" app/main.py
    sed -i.bak "s/\"version\": \"[^\"]*\"/\"version\": \"$NEW_VERSION\"/g" app/main.py
    rm -f app/main.py.bak
    log_info "app/main.py atualizado"
    
    # Atualizar docker-stack.yml
    sed -i.bak "s/xml-downloader-api:[^[:space:]]*/xml-downloader-api:$NEW_VERSION/g" docker-stack.yml
    rm -f docker-stack.yml.bak
    log_info "docker-stack.yml atualizado"
    
    # Atualizar exemplo-uso-interno.yml
    sed -i.bak "s/xml-downloader-api:[^[:space:]]*/xml-downloader-api:$NEW_VERSION/g" exemplo-uso-interno.yml
    rm -f exemplo-uso-interno.yml.bak
    log_info "exemplo-uso-interno.yml atualizado"
    
    log_success "Todos os arquivos de versão atualizados"
}

# Executar testes
run_tests() {
    log_step "Executando testes..."
    
    # Verificar sintaxe Python
    for file in $(find app -name "*.py"); do
        python3 -m py_compile "$file"
    done
    log_info "Sintaxe Python verificada"
    
    # Verificar sintaxe YAML
    for file in *.yml; do
        python3 -c "import yaml; yaml.safe_load(open('$file'))"
    done
    log_info "Sintaxe YAML verificada"
    
    # Verificar sintaxe bash
    for file in *.sh; do
        bash -n "$file"
    done
    log_info "Sintaxe Bash verificada"
    
    log_success "Todos os testes passaram"
}

# Atualizar CHANGELOG
update_changelog() {
    log_step "Preparando atualização do CHANGELOG..."
    
    # Criar backup do CHANGELOG
    cp CHANGELOG.md CHANGELOG.md.bak
    
    # Criar entrada temporária para nova versão
    cat > temp_changelog.md << EOF
# Changelog

Todas as mudanças importantes deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [$NEW_VERSION] - $(date +%Y-%m-%d)

### ✨ Adicionado
- (Adicione novas funcionalidades aqui)

### 🔄 Alterado
- (Adicione mudanças em funcionalidades existentes aqui)

### 🐛 Corrigido
- (Adicione correções de bugs aqui)

### 🗑️ Removido
- (Adicione funcionalidades removidas aqui)

EOF
    
    # Anexar o restante do changelog (pular o cabeçalho)
    tail -n +8 CHANGELOG.md >> temp_changelog.md
    mv temp_changelog.md CHANGELOG.md
    
    log_warning "CHANGELOG.md foi preparado com entrada para v$NEW_VERSION"
    log_warning "Edite o CHANGELOG.md para adicionar as mudanças específicas desta versão"
    
    # Perguntar se quer editar o changelog
    read -p "Deseja editar o CHANGELOG.md agora? (y/N): " edit_changelog
    if [[ $edit_changelog =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} CHANGELOG.md
    fi
}

# Criar commit e tag
create_git_tag() {
    log_step "Criando commit e tag Git..."
    
    # Adicionar arquivos modificados
    git add VERSION app/main.py docker-stack.yml exemplo-uso-interno.yml CHANGELOG.md
    
    # Criar commit
    git commit -m "release: bump version to $NEW_VERSION

- Update version in all relevant files
- Update CHANGELOG.md with release notes
- Prepare for v$NEW_VERSION release"
    
    log_info "Commit criado"
    
    # Criar tag anotada
    git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION

XML Download API v$NEW_VERSION

$(date '+%Y-%m-%d %H:%M:%S')

Features and changes documented in CHANGELOG.md"
    
    log_success "Tag v$NEW_VERSION criada"
}

# Build da imagem Docker
build_docker_image() {
    log_step "Fazendo build da imagem Docker..."
    
    # Nome da imagem base
    IMAGE_NAME="xml-downloader-api"
    
    # Build com múltiplas tags
    docker build -t "$IMAGE_NAME:$NEW_VERSION" .
    docker tag "$IMAGE_NAME:$NEW_VERSION" "$IMAGE_NAME:latest"
    
    log_success "Imagem Docker construída:"
    log_info "  - $IMAGE_NAME:$NEW_VERSION"
    log_info "  - $IMAGE_NAME:latest"
}

# Instruções finais
show_final_instructions() {
    log_success "Release v$NEW_VERSION preparado com sucesso!"
    echo ""
    echo -e "${WHITE}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${WHITE}║                    🎉 RELEASE PREPARADO!                        ║${NC}"
    echo -e "${WHITE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}📍 Versão:${NC} $CURRENT_VERSION → $NEW_VERSION"
    echo -e "${CYAN}🏷️  Tag Git:${NC} v$NEW_VERSION"
    echo -e "${CYAN}🐳 Imagem Docker:${NC} xml-downloader-api:$NEW_VERSION"
    echo ""
    echo -e "${WHITE}🚀 Próximos passos:${NC}"
    echo ""
    echo -e "${YELLOW}1. Revisar mudanças:${NC}"
    echo -e "   ${GREEN}git show HEAD${NC}"
    echo -e "   ${GREEN}git log --oneline -n 5${NC}"
    echo ""
    echo -e "${YELLOW}2. Push para repositório:${NC}"
    echo -e "   ${GREEN}git push origin main${NC}"
    echo -e "   ${GREEN}git push origin v$NEW_VERSION${NC}"
    echo ""
    echo -e "${YELLOW}3. Push da imagem Docker (opcional):${NC}"
    echo -e "   ${GREEN}docker tag xml-downloader-api:$NEW_VERSION seu-registro/xml-downloader-api:$NEW_VERSION${NC}"
    echo -e "   ${GREEN}docker push seu-registro/xml-downloader-api:$NEW_VERSION${NC}"
    echo -e "   ${GREEN}docker push seu-registro/xml-downloader-api:latest${NC}"
    echo ""
    echo -e "${YELLOW}4. Criar release no GitHub:${NC}"
    echo -e "   • Acesse: https://github.com/seu-usuario/xml-download-api/releases"
    echo -e "   • Clique em 'Create a new release'"
    echo -e "   • Use a tag: v$NEW_VERSION"
    echo -e "   • Copie as mudanças do CHANGELOG.md"
    echo ""
    echo -e "${YELLOW}💡 Para desfazer (se necessário):${NC}"
    echo -e "   ${RED}git tag -d v$NEW_VERSION${NC}"
    echo -e "   ${RED}git reset --hard HEAD~1${NC}"
    echo ""
}

# Função principal
main() {
    print_header
    
    # Verificações iniciais
    check_version_argument "$@"
    get_current_version
    check_git_status
    check_version_exists
    
    # Mostrar resumo
    echo -e "${WHITE}📋 Resumo do Release:${NC}"
    echo -e "   Versão atual: ${RED}$CURRENT_VERSION${NC}"
    echo -e "   Nova versão:  ${GREEN}$NEW_VERSION${NC}"
    echo ""
    
    # Confirmar com usuário
    read -p "Continuar com o release? (y/N): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        log_info "Release cancelado pelo usuário"
        exit 0
    fi
    
    # Executar processo de release
    update_version_files
    run_tests
    update_changelog
    create_git_tag
    build_docker_image
    
    # Instruções finais
    show_final_instructions
}

# Verificar se o script está sendo executado (não sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi