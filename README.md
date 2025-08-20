# XML Download API

Uma API RESTful desenvolvida em Python usando FastAPI para download e validação de arquivos XML a partir de URLs fornecidas.

## 📋 Recursos

- **Endpoint único**: `/api/v1/download_xml` para download de XML
- **Validação robusta**: Verifica se o conteúdo baixado é um XML válido
- **Rate Limiting**: Proteção contra abuso com limite de requisições por IP
- **Cache inteligente**: Sistema de cache TTL para melhor performance
- **Validações de segurança**: Proteção contra URLs maliciosas e XXE attacks
- **Controle de tamanho**: Limite de tamanho de arquivo configurável
- **Documentação automática**: Swagger UI e ReDoc gerados automaticamente
- **Containerização**: Totalmente dockerizado para fácil implantação
- **Logging**: Sistema de logs para monitoramento e debugging
- **Tratamento de erros**: Respostas consistentes para diferentes tipos de erro
- **Testes automatizados**: Suíte completa de testes unitários e de integração
- **Configuração centralizada**: Configurações via variáveis de ambiente

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI**: Framework web moderno e rápido
- **Uvicorn**: Servidor ASGI de alta performance
- **Requests**: Biblioteca para requisições HTTP
- **Pydantic**: Validação de dados e serialização
- **SlowAPI**: Rate limiting para proteção contra abuso
- **CacheTools**: Sistema de cache em memória
- **Docker**: Containerização da aplicação
- **Pytest**: Framework de testes automatizados

## 📁 Estrutura do Projeto

```
xml-download-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── config.py            # Configurações centralizadas 🆕
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Modelos Pydantic (v2)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── download.py      # Router com rate limiting
│   └── services/
│       ├── __init__.py
│       └── xml_service.py   # Lógica de negócio com cache e segurança
├── tests/                   # Testes automatizados 🆕
│   ├── __init__.py
│   ├── test_api.py         # Testes de integração
│   ├── test_xml_service.py # Testes unitários
│   └── test_app.py         # App de teste
├── Dockerfile               # Container para a aplicação
├── docker-compose.yml       # Execução local/desenvolvimento
├── docker-stack.yml         # Deploy em produção (Docker Swarm)
├── requirements.txt         # Dependências Python (atualizadas)
├── pytest.ini              # Configuração de testes 🆕
├── install.sh              # Instalador automático
├── quick-install.sh         # Instalação via internet
├── demo-install.sh          # Demo de instalação
├── test_api.py             # Script de testes
├── exemplo-uso-interno.yml  # Exemplo de uso em rede Docker
├── consumer-example.py      # Exemplo de serviço consumidor
├── EXECUTAR.md             # Instruções detalhadas
├── INSTALACAO-AUTOMATICA.md # Guia dos scripts de instalação
├── README_SHOWCASE.md       # Página de vitrine do projeto
└── README.md               # Documentação principal
```

## 🔧 Instalação e Execução

### 🚀 **Opção 1: Instalação Automática (Um Comando)**

**Para containers Linux (Ubuntu, Debian, CentOS, Alpine, etc.):**

```bash
# Instalação automática via internet (recomendado)
curl -sSL https://raw.githubusercontent.com/seu-usuario/xml-download-api/main/quick-install.sh | bash

# OU clone o repositório e execute localmente
git clone https://github.com/seu-usuario/xml-download-api.git
cd xml-download-api
chmod +x install.sh && ./install.sh
```

> 🎉 **Pronto!** O script instala tudo automaticamente: Python, dependências, ambiente virtual e scripts de controle.  
> Depois da instalação: `cd xml-download-api && ./start.sh`

### 🐳 **Opção 2: Usando Docker (Recomendado para desenvolvimento)**

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd xml-download-api
   ```

2. **Execute com Docker Compose:**
   ```bash
   # Para produção
   docker-compose up -d xml-download-api
   
   # Para desenvolvimento (com hot-reload)
   docker-compose --profile dev up -d xml-download-api-dev
   ```

3. **A API estará disponível em:**
   - Produção: http://localhost:8000
   - Desenvolvimento: http://localhost:8001

### 🐍 **Opção 3: Execução Manual (Python)**

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute a aplicação:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

 > 💡 **Instruções detalhadas:** [`EXECUTAR.md`](EXECUTAR.md) | **Instalação automática:** [`INSTALACAO-AUTOMATICA.md`](INSTALACAO-AUTOMATICA.md)

## 📖 Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🛠 Uso da API

### Endpoints Disponíveis

#### **POST** `/api/v1/download_xml`

**Request Body:**
```json
{
  "url": "https://www.exemplo.com.br/arquivo.xml"
}
```

**Respostas:**

**✅ Sucesso (200 OK):**
```json
{
  "status": "sucesso",
  "xml_content": "<?xml version='1.0' encoding='UTF-8'?><nota>...</nota>",
  "cached": false,
  "content_size": 1024,
  "timestamp": "2024-01-15T10:30:00"
}
```

**❌ Erro de Cliente (400 Bad Request):**
```json
{
  "status": "erro",
  "mensagem": "URL não fornecida ou inválida."
}
```

**❌ Erro do Servidor (500 Internal Server Error):**
```json
{
  "status": "erro",
  "mensagem": "Falha ao baixar ou processar o arquivo XML."
}
```

**⚠️ Rate Limit (429 Too Many Requests):**
```json
{
  "detail": "Rate limit exceeded: 10 per 1 minute"
}
```

#### **GET** `/api/v1/cache/stats`

Endpoint para obter estatísticas do cache da aplicação.

**✅ Sucesso (200 OK):**
```json
{
  "cache_size": 5,
  "max_cache_size": 100,
  "ttl_seconds": 900,
  "cache_info": {
    "hits": 0,
    "misses": 0
  }
}
```

### Exemplo de Uso com cURL

```bash
# Download de XML
curl -X POST "http://localhost:8000/api/v1/download_xml" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.exemplo.com.br/arquivo.xml"}'

# Verificar estatísticas do cache
curl -X GET "http://localhost:8000/api/v1/cache/stats"
```

### Exemplo de Uso com Python

```python
import requests

url = "http://localhost:8000/api/v1/download_xml"
payload = {
    "url": "https://www.exemplo.com.br/arquivo.xml"
}

response = requests.post(url, json=payload)
result = response.json()

if response.status_code == 200:
    print("XML baixado com sucesso!")
    print(result["xml_content"])
else:
    print(f"Erro: {result['mensagem']}")
```

## 🔍 Validações e Recursos de Segurança

A API implementa múltiplas camadas de validação e segurança:

### 🛡️ Validações de Segurança
1. **Validação de URL**: Verifica se a URL é válida usando Pydantic
2. **Bloqueio de URLs privadas**: Impede acesso a localhost e IPs privados
3. **Validação de esquema**: Apenas HTTP/HTTPS são permitidos
4. **Proteção XXE**: Detecta e bloqueia padrões suspeitos em XML
5. **Controle de tamanho**: Limite de 10MB por arquivo (configurável)
6. **Rate Limiting**: Máximo de 10 requisições por minuto por IP

### ⚡ Performance e Cache
1. **Cache TTL**: Cache inteligente de 15 minutos para XMLs válidos
2. **Download streaming**: Download otimizado com verificação de tamanho
3. **Headers otimizados**: Headers HTTP otimizados para melhor compatibilidade

### 🔧 Validações Técnicas
1. **Validação de Conteúdo**: Verifica se o conteúdo baixado é um XML válido
2. **Timeout configurável**: Requisições têm timeout de 30 segundos (configurável)
3. **Tratamento de Erros**: Captura e trata diversos tipos de exceções
4. **Logging estruturado**: Sistema de logs para monitoramento e debugging

## 🚀 Deploy em Produção

### Docker

```bash
# Build da imagem
docker build -t xml-download-api .

# Run do container
docker run -d -p 8000:8000 --name xml-api xml-download-api
```

### Docker Compose

```bash
docker-compose up -d xml-download-api
```

## Deploy em Produção com Docker Swarm

Esta seção descreve como implantar a XML Download API em um ambiente de produção usando Docker Swarm para orquestração de contêineres. Essa configuração oferece escalabilidade horizontal automática, alta disponibilidade com recuperação automática de falhas, balanceamento de carga entre réplicas e facilita o uso interno em redes Docker.

### 📋 Pré-requisitos

Antes de prosseguir com o deploy, certifique-se de que você possui:

- **Cluster Docker Swarm ativo**: Um cluster Docker Swarm funcional com pelo menos um nó manager
- **Rede overlay**: Uma rede overlay para comunicação interna entre serviços (ex: `api-network`)
- **Registro de contêineres**: Acesso a um registro Docker (Docker Hub, ECR, etc.) para armazenar a imagem

### 📝 Arquivo de Stack (docker-stack.yml)

Crie um arquivo `docker-stack.yml` com o seguinte conteúdo:

```yaml
version: '3.8'

services:
  xml-api:
    image: seu-registro/xml-downloader-api:1.0  # Substitua pela sua imagem
    ports:
      - "8000:8000"  # Expor porta para acesso interno
    networks:
      - api-network
    environment:
      - PYTHONPATH=/app
    deploy:
      replicas: 2  # Pode ser facilmente escalado: docker service scale stack_xml-api=5
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
        order: start-first
      # Uncomment to constrain deployment to specific node types
      # placement:
      #   constraints:
      #     - node.role == worker
      #     - node.labels.environment == production

networks:
  api-network:
    driver: overlay
    attachable: true
```

### 🚀 Passos para Deploy

#### 1. Build e Push da Imagem

Primeiro, construa e envie a imagem Docker para seu registro:

```bash
# Navegar para o diretório do projeto
cd xml-downloader-api

# Build da imagem com tag versionada
docker build -t seu-registro/xml-downloader-api:1.0 .

# Fazer login no registro (se necessário)
docker login seu-registro

# Push da imagem para o registro
docker push seu-registro/xml-downloader-api:1.0

# Opcional: criar tag 'latest' para facilitar futuras atualizações
docker tag seu-registro/xml-downloader-api:1.0 seu-registro/xml-downloader-api:latest
docker push seu-registro/xml-downloader-api:latest
```

#### 2. Criação do Arquivo de Stack

No nó manager do seu cluster Docker Swarm, crie o arquivo de configuração:

```bash
# Conectar ao nó manager do Swarm
ssh usuario@seu-servidor-manager

# Criar diretório para stacks (se não existir)
mkdir -p ~/docker-stacks/xml-api

# Criar o arquivo docker-stack.yml
nano ~/docker-stacks/xml-api/docker-stack.yml
```

Cole o conteúdo do arquivo `docker-stack.yml` mostrado acima e **substitua**:
- `seu-registro/xml-downloader-api:1.0` pelo caminho real da sua imagem
- `api-xml.seu-dominio.com` pelo seu domínio real

#### 3. Deploy da Stack

Execute o deploy da stack no cluster:

```bash
# Deploy da stack (substitua 'xml-downloader' pelo nome desejado)
docker stack deploy -c ~/docker-stacks/xml-api/docker-stack.yml xml-downloader

# Verificar se a stack foi criada
docker stack ls
```

#### 4. Verificação do Deploy

Monitore o status do deployment:

```bash
# Verificar status dos serviços na stack
docker stack ps xml-downloader

# Verificar logs do serviço (se necessário)
docker service logs xml-downloader_xml-api

# Verificar se o serviço está rodando
docker service ls | grep xml-api
```

#### 5. Teste da API

Teste se a API está funcionando corretamente:

```bash
# Obter IP do nó manager ou usar localhost se estiver local
NODE_IP=$(docker node inspect self --format '{{.Status.Addr}}')

# Teste do health check
curl http://$NODE_IP:8000/health

# Teste da documentação
curl http://$NODE_IP:8000/docs

# Teste do endpoint principal
curl -X POST "http://$NODE_IP:8000/api/v1/download_xml" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.w3schools.com/xml/note.xml"}'

# Para acesso de outros containers na mesma rede
curl http://xml-downloader_xml-api:8000/health
```

### 📈 Escalabilidade e Manutenção

#### Escalar o serviço:
```bash
# Escalar para 3 réplicas
docker service scale xml-downloader_xml-api=3

# Verificar status das réplicas
docker service ps xml-downloader_xml-api
```

#### Atualizar a aplicação:
```bash
# Fazer build e push da nova versão
docker build -t seu-registro/xml-downloader-api:1.1 .
docker push seu-registro/xml-downloader-api:1.1

# Atualizar o serviço (rolling update automático)
docker service update --image seu-registro/xml-downloader-api:1.1 xml-downloader_xml-api
```

#### Remover a stack:
```bash
docker stack rm xml-downloader
```

### 🌐 Uso em Redes Docker Internas

A API é projetada para uso interno em redes Docker, oferecendo:

- **Service Discovery**: Acesse via nome do serviço `xml-downloader_xml-api:8000`
- **Rede Overlay**: Comunicação segura entre containers
- **Load Balancing**: Distribuição automática entre réplicas
- **Health Checks**: Monitoramento automático de saúde dos containers

#### Exemplo de Uso por Outros Serviços:

```bash
# De dentro de outro container na mesma rede
curl http://xml-downloader_xml-api:8000/api/v1/download_xml \
     -H "Content-Type: application/json" \
     -d '{"url": "https://exemplo.com/file.xml"}'
```

#### Docker Compose para Desenvolvimento:

```yaml
version: '3.8'
services:
  xml-api:
    image: seu-registro/xml-downloader-api:1.0
    networks:
      - internal-network
  
  seu-app:
    image: sua-aplicacao:latest
    environment:
      - XML_API_URL=http://xml-api:8000
    networks:
      - internal-network
    depends_on:
      - xml-api

networks:
  internal-network:
    driver: bridge
```

> 💡 **Exemplo completo disponível:** Consulte [`exemplo-uso-interno.yml`](exemplo-uso-interno.yml) e [`consumer-example.py`](consumer-example.py) para ver implementação prática.

### 🔧 Configurações Avançadas

Para ambientes de produção, considere também:

- **Monitoramento**: Integrar com Prometheus + Grafana
- **Logs centralizados**: Configurar ELK Stack ou similar
- **Redes internas**: Configurar redes overlay para isolamento
- **Service discovery**: Usar nomes de serviço para comunicação entre containers
- **CI/CD**: Automatizar o processo de build, test e deploy

## ⚙️ Configuração

A aplicação pode ser configurada através de variáveis de ambiente:

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `MAX_FILE_SIZE_MB` | `10` | Tamanho máximo do arquivo em MB |
| `CACHE_TTL_SECONDS` | `900` | Tempo de vida do cache em segundos |
| `CACHE_MAX_SIZE` | `100` | Número máximo de itens no cache |
| `HTTP_TIMEOUT_SECONDS` | `30` | Timeout para requisições HTTP |
| `RATE_LIMIT_DOWNLOADS` | `10/minute` | Limite de rate para downloads |
| `RATE_LIMIT_STATS` | `30/minute` | Limite de rate para estatísticas |
| `CORS_ORIGINS` | `*` | Origens permitidas para CORS |
| `LOG_LEVEL` | `INFO` | Nível de logging |

### Exemplo de uso com variáveis de ambiente:

```bash
export MAX_FILE_SIZE_MB=20
export CACHE_TTL_SECONDS=1800
export RATE_LIMIT_DOWNLOADS="20/minute"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🧪 Testes

Execute a suíte de testes com:

```bash
# Instalar dependências de teste
pip install -r requirements.txt

# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=app tests/

# Executar apenas testes unitários
pytest tests/test_xml_service.py

# Executar apenas testes de integração
pytest tests/test_api.py
```

## 📊 Monitoramento

A aplicação inclui:

- **Health Check**: Endpoint `/health` para verificação de saúde
- **Cache Stats**: Endpoint `/api/v1/cache/stats` para estatísticas do cache
- **Logs estruturados**: Sistema de logging para monitoramento
- **Rate Limiting**: Proteção automática contra abuso
- **CORS configurado**: Permite requisições de diferentes origens

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📧 Contato

Desenvolvido com ❤️ usando FastAPI e Docker.