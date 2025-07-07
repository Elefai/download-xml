#!/bin/bash

# =============================================================================
# XML Download API - Demo de Instalação (Para Testes)
# =============================================================================
# Este script demonstra como a instalação automática funciona
# Usa o código local em vez de baixar do Git (para testes)
# =============================================================================

set -e

echo "🎬 XML Download API - Demo de Instalação Automática"
echo "===================================================="
echo ""
echo "📝 Este é um demo que simula a instalação automática completa."
echo "   Em produção, você usaria o quick-install.sh ou install.sh diretamente."
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "app/main.py" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ Este script deve ser executado no diretório raiz da aplicação"
    echo "   Certifique-se de que os arquivos app/main.py e requirements.txt existem"
    exit 1
fi

echo "✅ Código da aplicação encontrado no diretório atual"
echo ""

# Verificar se o script de instalação existe
if [ ! -f "install.sh" ]; then
    echo "❌ Script install.sh não encontrado"
    exit 1
fi

echo "🚀 Executando instalação automática..."
echo ""

# Executar o script de instalação
./install.sh

echo ""
echo "🎉 Demo de instalação concluído!"
echo ""
echo "🔧 Scripts disponíveis agora:"
echo "   • ./start.sh  - Iniciar a API"
echo "   • ./stop.sh   - Parar a API"
echo "   • ./test.sh   - Testar a API"
echo ""
echo "💡 Exemplo de uso completo:"
echo "   1. ./start.sh     # Iniciar em um terminal"
echo "   2. ./test.sh      # Testar em outro terminal"
echo "   3. ./stop.sh      # Parar quando terminar"
echo ""