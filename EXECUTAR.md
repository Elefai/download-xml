# Como Executar a XML Download API

Este documento fornece instruções detalhadas para executar e testar a API de download de XML.

## 🚀 Métodos de Execução

### 1. Usando Docker (Recomendado)

#### Pré-requisitos
- Docker instalado
- Docker Compose instalado

#### Execução
```bash
# Para produção
docker-compose up -d xml-download-api

# Para desenvolvimento (com hot-reload)
docker-compose --profile dev up -d xml-download-api-dev
```

#### URLs de Acesso
- **Produção**: http://localhost:8000
- **Desenvolvimento**: http://localhost:8001
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 2. Execução Local com Python

#### Pré-requisitos
- Python 3.10+ instalado
- pip ou pipenv

#### Instalação e Execução

##### Opção A: Com venv (Recomendado)
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

##### Opção B: Com pipx (Se disponível)
```bash
# Instalar pipx se não estiver instalado
python3 -m pip install --user pipx

# Instalar dependências
pipx install fastapi uvicorn requests pydantic

# Executar aplicação
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

##### Opção C: Instalação global (Apenas para teste)
```bash
# ATENÇÃO: Só usar se não conseguir criar ambiente virtual
pip install --break-system-packages -r requirements.txt

# Executar aplicação
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🧪 Testando a API

### 1. Usando o Script de Teste Automático

```bash
# Certifique-se de que a API esteja rodando primeiro
# Em seguida, execute:
python3 test_api.py
```

### 2. Teste Manual com cURL

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Download de XML
```bash
curl -X POST "http://localhost:8000/api/v1/download_xml" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.w3schools.com/xml/note.xml"}'
```

#### Teste com URL inválida
```bash
curl -X POST "http://localhost:8000/api/v1/download_xml" \
     -H "Content-Type: application/json" \
     -d '{"url": "not-a-valid-url"}'
```

### 3. Usando a Documentação Interativa

1. Acesse http://localhost:8000/docs
2. Clique em "Try it out" no endpoint `/download_xml`
3. Insira uma URL válida de XML
4. Clique em "Execute"

### 4. Exemplos de URLs de XML para Teste

- `https://www.w3schools.com/xml/note.xml`
- `https://www.w3schools.com/xml/simple.xml`
- `https://httpbin.org/xml` (XML simples)

## 📊 Monitoramento e Logs

### Visualizar Logs em Tempo Real

#### Docker
```bash
# Logs da aplicação
docker-compose logs -f xml-download-api

# Logs específicos
docker logs -f <container-id>
```

#### Execução Local
Os logs aparecerão diretamente no terminal onde a aplicação está rodando.

### Health Check
```bash
# Verificar se a aplicação está saudável
curl http://localhost:8000/health
```

## 🔧 Configurações Avançadas

### Variáveis de Ambiente Opcionais

Você pode configurar as seguintes variáveis:

```bash
# Para produção
export PYTHONPATH=/workspace
export UVICORN_HOST=0.0.0.0
export UVICORN_PORT=8000
export UVICORN_WORKERS=4

# Para desenvolvimento
export UVICORN_RELOAD=true
```

### Configuração de Logs
```bash
# Nível de log (DEBUG, INFO, WARNING, ERROR)
export LOG_LEVEL=INFO
```

## 🐛 Resolução de Problemas

### Problemas Comuns

1. **Erro "Port already in use"**
   ```bash
   # Verificar processos usando a porta
   lsof -i :8000
   
   # Matar processo se necessário
   kill -9 <PID>
   ```

2. **Erro de dependências**
   ```bash
   # Reinstalar dependências
   pip install --upgrade -r requirements.txt
   ```

3. **Erro de permissão Docker**
   ```bash
   # Adicionar usuário ao grupo docker
   sudo usermod -aG docker $USER
   # Fazer logout e login novamente
   ```

### Verificação da Instalação

```bash
# Verificar se todos os módulos são importáveis
python3 -c "
import sys
sys.path.append('.')
from app.main import app
from app.services.xml_service import XMLDownloadService
from app.models.schemas import DownloadRequest
print('✅ Todos os módulos importados com sucesso!')
"
```

## 📈 Performance

### Configurações de Produção

Para ambiente de produção, considere:

1. **Usar múltiplos workers**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Usar proxy reverso** (nginx, Apache)

3. **Configurar SSL/TLS**

4. **Implementar rate limiting**

5. **Adicionar cache para URLs frequentes**

## 🔐 Segurança

### Considerações de Segurança

1. **Validação de URL**: A API já valida URLs usando Pydantic
2. **Timeout**: Requisições têm timeout de 30 segundos
3. **Headers**: User-Agent configurado para simular navegador
4. **Container**: Executa com usuário não-root
5. **CORS**: Configurado para desenvolvimento (ajustar para produção)

### Para Produção
- Configurar CORS adequadamente
- Implementar autenticação se necessário
- Adicionar rate limiting
- Configurar HTTPS
- Monitorar logs de segurança

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs da aplicação
2. Teste o health check
3. Confirme que todas as dependências estão instaladas
4. Verifique a conectividade de rede para URLs externas