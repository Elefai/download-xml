#!/bin/bash

# =============================================================================
# XML Download API - Script de Commit para Release v0.0.1
# =============================================================================
# Este script faz todos os commits necessários para o release v0.0.1
# =============================================================================

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Preparando commits para Release v0.0.1${NC}"
echo ""

# Verificar se estamos em um repositório Git
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Erro: Não está em um repositório Git${NC}"
    echo "Execute este script no diretório raiz do projeto"
    exit 1
fi

# Verificar status atual
echo -e "${YELLOW}📋 Status atual do Git:${NC}"
git status --short
echo ""

# Confirmar com usuário
read -p "Continuar com os commits? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "❌ Cancelado pelo usuário"
    exit 0
fi

echo ""
echo -e "${BLUE}📝 Fazendo commits organizados...${NC}"
echo ""

# Commit 1: Sistema de versionamento
echo -e "${YELLOW}1/4 - Commit: Sistema de versionamento${NC}"
git add VERSION CHANGELOG.md release.sh
git commit -m "feat: add version control system

- Add VERSION file with semantic versioning (0.0.1)
- Add comprehensive CHANGELOG.md with release notes
- Add automated release.sh script for future releases
- Implement semantic versioning workflow"

echo -e "${GREEN}✅ Commit 1 concluído${NC}"
echo ""

# Commit 2: Atualização da API para v0.0.1
echo -e "${YELLOW}2/4 - Commit: Atualização da API${NC}"
git add app/main.py
git commit -m "feat: update API to version 0.0.1

- Update FastAPI app version to 0.0.1
- Add /version endpoint with detailed version info
- Include version in health check response
- Standardize version across all API responses"

echo -e "${GREEN}✅ Commit 2 concluído${NC}"
echo ""

# Commit 3: Atualização de configurações Docker
echo -e "${YELLOW}3/4 - Commit: Configurações Docker${NC}"
git add docker-stack.yml exemplo-uso-interno.yml README.md README_SHOWCASE.md
git commit -m "feat: update Docker configurations for v0.0.1

- Update docker-stack.yml with versioned image tags
- Update exemplo-uso-interno.yml with v0.0.1 image
- Update README.md with version references and release docs
- Update README_SHOWCASE.md with version badge
- Add release and versioning documentation"

echo -e "${GREEN}✅ Commit 3 concluído${NC}"
echo ""

# Commit 4: Documentação do release
echo -e "${YELLOW}4/4 - Commit: Documentação do release${NC}"
git add RELEASE_v0.0.1.md commit-release.sh
git commit -m "docs: add release documentation

- Add RELEASE_v0.0.1.md with complete release notes
- Add commit-release.sh script for automated commits
- Prepare comprehensive release documentation for GitHub
- Include all technical specifications and usage examples"

echo -e "${GREEN}✅ Commit 4 concluído${NC}"
echo ""

# Criar tag do release
echo -e "${YELLOW}🏷️  Criando tag v0.0.1...${NC}"
git tag -a v0.0.1 -m "Release v0.0.1 - First Stable Release

XML Download API v0.0.1

This is the first stable release of the XML Download API, featuring:
- Complete FastAPI implementation
- Docker containerization with Swarm support
- Automated installation scripts for multiple Linux distributions
- Comprehensive documentation and examples
- Internal Docker network optimization
- Production-ready configuration

Release date: $(date '+%Y-%m-%d %H:%M:%S')
"

echo -e "${GREEN}✅ Tag v0.0.1 criada${NC}"
echo ""

# Mostrar resumo
echo -e "${BLUE}📊 Resumo dos commits:${NC}"
git log --oneline -n 5
echo ""

# Mostrar próximos passos
echo -e "${GREEN}🎉 Todos os commits concluídos com sucesso!${NC}"
echo ""
echo -e "${BLUE}📋 Próximos passos:${NC}"
echo ""
echo -e "${YELLOW}1. Push para o repositório:${NC}"
echo -e "   ${GREEN}git push origin main${NC}"
echo -e "   ${GREEN}git push origin v0.0.1${NC}"
echo ""
echo -e "${YELLOW}2. Criar release no GitHub:${NC}"
echo -e "   • Acesse: https://github.com/SEU-USUARIO/xml-download-api/releases"
echo -e "   • Clique em 'Create a new release'"
echo -e "   • Tag version: v0.0.1"
echo -e "   • Release title: v0.0.1 - First Stable Release"
echo -e "   • Description: Copie o conteúdo de RELEASE_v0.0.1.md"
echo ""
echo -e "${YELLOW}3. Build e push da imagem Docker (opcional):${NC}"
echo -e "   ${GREEN}docker build -t xml-downloader-api:0.0.1 .${NC}"
echo -e "   ${GREEN}docker tag xml-downloader-api:0.0.1 SEU-USUARIO/xml-downloader-api:0.0.1${NC}"
echo -e "   ${GREEN}docker push SEU-USUARIO/xml-downloader-api:0.0.1${NC}"
echo ""

echo -e "${BLUE}🎯 Release v0.0.1 está pronto para ser publicado!${NC}"