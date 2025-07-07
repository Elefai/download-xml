# 🚀 Instalação Automática - XML Download API

Este documento explica como usar os scripts de instalação automática da XML Download API.

## 📋 Scripts Disponíveis

### 1. `quick-install.sh` - Instalação Via Internet

**Uso mais simples:** Um comando instala tudo automaticamente

```bash
curl -sSL https://raw.githubusercontent.com/seu-usuario/xml-download-api/main/quick-install.sh | bash
```

**O que faz:**
- ✅ Baixa o código do GitHub automaticamente
- ✅ Detecta o sistema operacional (Ubuntu, Debian, CentOS, Alpine, etc.)
- ✅ Instala todas as dependências do sistema
- ✅ Configura ambiente Python virtual
- ✅ Instala dependências Python
- ✅ Cria scripts de controle (start.sh, stop.sh, test.sh)
- ✅ Testa a instalação

### 2. `install.sh` - Instalação Local

**Para quando você já tem o código localmente:**

```bash
git clone https://github.com/seu-usuario/xml-download-api.git
cd xml-download-api
./install.sh
```

**O que faz:**
- ✅ Mesmas funcionalidades do quick-install.sh
- ✅ Usa código local em vez de baixar
- ✅ Ideal para desenvolvimento ou quando você já clonou o repo

### 3. `demo-install.sh` - Demonstração

**Para testar no ambiente atual:**

```bash
./demo-install.sh
```

**O que faz:**
- ✅ Demonstra o processo de instalação
- ✅ Usa código local
- ✅ Perfeito para testes e desenvolvimento

## 🖥 Sistemas Suportados

Os scripts funcionam automaticamente nos seguintes sistemas:

| Sistema | Testado | Gerenciador de Pacotes |
|---------|---------|------------------------|
| **Ubuntu** | ✅ | apt-get |
| **Debian** | ✅ | apt-get |
| **CentOS** | ✅ | yum/dnf |
| **RHEL** | ✅ | yum/dnf |
| **Amazon Linux** | ✅ | yum/dnf |
| **Rocky Linux** | ✅ | dnf |
| **AlmaLinux** | ✅ | dnf |
| **Alpine** | ✅ | apk |

## 📦 O que é Instalado Automaticamente

### Dependências do Sistema:
- **Python 3.8+** (se não estiver instalado)
- **pip3** (gerenciador de pacotes Python)
- **python3-venv** (ambiente virtual)
- **curl, wget, git** (ferramentas de rede)
- **build-essential/gcc** (compilação de pacotes)
- **ca-certificates** (certificados SSL)

### Dependências Python:
- **FastAPI** (framework web)
- **Uvicorn** (servidor ASGI)
- **Requests** (requisições HTTP)
- **Pydantic** (validação de dados)

### Scripts Criados:
- **start.sh** - Iniciar a API
- **stop.sh** - Parar a API
- **test.sh** - Testar todos os endpoints

## 🎯 Fluxo de Uso Completo

### Instalação e Teste Rápido:

```bash
# 1. Instalar (escolha uma opção)
curl -sSL https://raw.githubusercontent.com/seu-usuario/xml-download-api/main/quick-install.sh | bash

# 2. Navegar para o diretório
cd xml-download-api

# 3. Iniciar a API
./start.sh
```

Em outro terminal:

```bash
# 4. Testar a API
cd xml-download-api
./test.sh

# 5. Parar quando terminar
./stop.sh
```

## ⚙️ Configurações Avançadas

### Variáveis de Ambiente

Você pode personalizar a instalação com variáveis de ambiente:

```bash
# Mudar porta da API (padrão: 8000)
export API_PORT=9000

# Configurar host (padrão: 0.0.0.0)
export API_HOST=localhost

# Executar instalação
./install.sh
```

### Customização de Scripts

Os scripts criados (`start.sh`, `stop.sh`, `test.sh`) respeitam as seguintes variáveis:

```bash
# Exemplo: usar porta 9000
export API_PORT=9000
./start.sh

# A API será iniciada em http://localhost:9000
```

## 🔧 Scripts Gerados

### `start.sh` - Inicialização

```bash
#!/bin/bash
# Ativa ambiente virtual
# Configura PYTHONPATH
# Verifica porta disponível
# Inicia uvicorn com hot-reload
```

**Uso:**
```bash
./start.sh
```

**Saída:**
```
🚀 Iniciando XML Download API...
📡 Iniciando servidor em http://0.0.0.0:8000
📖 Documentação disponível em: http://0.0.0.0:8000/docs
🔧 Para parar o servidor, pressione Ctrl+C
```

### `stop.sh` - Parada

```bash
#!/bin/bash
# Encontra processos uvicorn
# Para graciosamente (SIGTERM)
# Força parada se necessário (SIGKILL)
```

**Uso:**
```bash
./stop.sh
```

### `test.sh` - Testes

```bash
#!/bin/bash
# Aguarda API estar disponível
# Testa health check
# Testa endpoints com dados válidos/inválidos
# Mostra resultados coloridos
```

**Uso:**
```bash
./test.sh
```

**Saída:**
```
🧪 Testando XML Download API em http://localhost:8000

⏳ Aguardando API estar disponível...
✅ API está respondendo!

🔍 Testando: Health Check
✅ Sucesso (200)

🔍 Testando: Download de XML válido
✅ Sucesso (200)
📄 Resposta: {"status":"sucesso","xml_content":"<?xml version='1.0' encoding='UTF-8'?>...

🏁 Testes concluídos!
📖 Acesse a documentação em: http://localhost:8000/docs
```

## 🐛 Resolução de Problemas

### Problema: "Permissão negada"

```bash
# Dar permissão de execução
chmod +x install.sh
./install.sh
```

### Problema: "Python não encontrado"

O script detecta e instala Python automaticamente. Se falhar:

```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install -y python3 python3-pip

# Alpine
sudo apk add python3 py3-pip
```

### Problema: "Porta em uso"

```bash
# Verificar processos na porta 8000
lsof -i :8000

# Usar porta alternativa
export API_PORT=9000
./start.sh
```

### Problema: "Dependências não instaladas"

```bash
# Reinstalar dependências
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 🔐 Considerações de Segurança

### Execução de Scripts Remotos

Quando usar `curl | bash`, sempre verifique o script primeiro:

```bash
# Ver o script antes de executar
curl -sSL https://raw.githubusercontent.com/seu-usuario/xml-download-api/main/quick-install.sh

# Baixar e revisar antes de executar
curl -sSL https://raw.githubusercontent.com/seu-usuario/xml-download-api/main/quick-install.sh -o install-temp.sh
less install-temp.sh
bash install-temp.sh
```

### Permissões Root

Os scripts podem precisar de sudo para instalar dependências do sistema:

```bash
# Se solicitado, forneça senha do sudo
sudo apt-get install python3

# Ou execute como root em containers
docker run -it --rm ubuntu bash
curl -sSL ... | bash
```

## 📈 Performance e Otimização

### Instalação Rápida

Para instalação mais rápida, use cache do pip:

```bash
# Usar cache global do pip (se disponível)
export PIP_CACHE_DIR=/tmp/pip-cache
./install.sh
```

### Produção

Para ambiente de produção, considere:

```bash
# Usar múltiplos workers
export UVICORN_WORKERS=4
./start.sh

# Ou editar start.sh para usar:
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🚀 Próximos Passos

Após instalação bem-sucedida:

1. **Explore a API**: http://localhost:8000/docs
2. **Leia a documentação**: [README.md](README.md)
3. **Teste em produção**: [Deploy com Docker Swarm](README.md#deploy-em-produção-com-docker-swarm-e-traefik)
4. **Contribua**: [Como contribuir](README.md#contribuição)