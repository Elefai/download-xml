# XML Download API

Uma API RESTful desenvolvida em Python usando FastAPI para download e validação de arquivos XML a partir de URLs fornecidas.

## 📋 Recursos

- **Endpoint único**: `/api/v1/download_xml` para download de XML
- **Validação robusta**: Verifica se o conteúdo baixado é um XML válido
- **Documentação automática**: Swagger UI e ReDoc gerados automaticamente
- **Containerização**: Totalmente dockerizado para fácil implantação
- **Logging**: Sistema de logs para monitoramento e debugging
- **Tratamento de erros**: Respostas consistentes para diferentes tipos de erro

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI**: Framework web moderno e rápido
- **Uvicorn**: Servidor ASGI de alta performance
- **Requests**: Biblioteca para requisições HTTP
- **Pydantic**: Validação de dados e serialização
- **Docker**: Containerização da aplicação

## 📁 Estrutura do Projeto

```
xml-download-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Modelos Pydantic
│   ├── routers/
│   │   ├── __init__.py
│   │   └── download.py      # Router do endpoint
│   └── services/
│       ├── __init__.py
│       └── xml_service.py   # Lógica de negócio
├── Dockerfile               # Container para a aplicação
├── docker-compose.yml       # Execução local/desenvolvimento
├── docker-stack.yml         # Deploy em produção (Docker Swarm)
├── requirements.txt         # Dependências Python
├── install.sh              # Instalador automático 🆕
├── quick-install.sh         # Instalação via internet 🆕
├── demo-install.sh          # Demo de instalação 🆕
├── release.sh               # Script de release automático 🆕
├── test_api.py             # Script de testes
├── exemplo-uso-interno.yml  # Exemplo de uso em rede Docker 🆕
├── consumer-example.py      # Exemplo de serviço consumidor 🆕
├── VERSION                  # Controle de versão 🆕
├── CHANGELOG.md            # Histórico de mudanças 🆕
├── EXECUTAR.md             # Instruções detalhadas
├── INSTALACAO-AUTOMATICA.md # Guia dos scripts de instalação 🆕
├── README_SHOWCASE.md       # Página de vitrine do projeto 🆕
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

### Endpoint Principal

**POST** `/api/v1/download_xml`

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
  "xml_content": "<?xml version='1.0' encoding='UTF-8'?><nota>...</nota>"
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

### Exemplo de Uso com cURL

```bash
curl -X POST "http://localhost:8000/api/v1/download_xml" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.exemplo.com.br/arquivo.xml"}'
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

## 🔍 Validações Implementadas

A API realiza as seguintes validações:

1. **Validação de URL**: Verifica se a URL é válida usando Pydantic
2. **Validação de Conteúdo**: Verifica se o conteúdo baixado é um XML válido
3. **Timeout**: Requisições têm timeout de 30 segundos
4. **Headers HTTP**: Simula um navegador para evitar bloqueios
5. **Tratamento de Erros**: Captura e trata diversos tipos de exceções

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
docker build -t seu-registro/xml-downloader-api:0.0.1 .

# Fazer login no registro (se necessário)
docker login seu-registro

# Push da imagem para o registro
docker push seu-registro/xml-downloader-api:0.0.1

# Opcional: criar tag 'latest' para facilitar futuras atualizações
docker tag seu-registro/xml-downloader-api:0.0.1 seu-registro/xml-downloader-api:latest
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
docker build -t seu-registro/xml-downloader-api:0.0.2 .
docker push seu-registro/xml-downloader-api:0.0.2

# Atualizar o serviço (rolling update automático)
docker service update --image seu-registro/xml-downloader-api:0.0.2 xml-downloader_xml-api
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
    image: seu-registro/xml-downloader-api:0.0.1
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

### 🏷️ Releases e Versionamento

O projeto segue [Versionamento Semântico](https://semver.org/) e inclui script automatizado para releases:

#### Fazer um Release:

```bash
# Para próxima versão patch (0.0.1 → 0.0.2)
./release.sh 0.0.2

# Para próxima versão minor (0.0.x → 0.1.0)
./release.sh 0.1.0

# Para próxima versão major (0.x.x → 1.0.0)
./release.sh 1.0.0
```

#### O script automaticamente:
- ✅ Atualiza versão em todos os arquivos
- ✅ Executa testes de sintaxe
- ✅ Atualiza CHANGELOG.md
- ✅ Cria commit e tag Git
- ✅ Faz build da imagem Docker
- ✅ Fornece instruções para push

#### Verificar Versão Atual:
```bash
cat VERSION                    # Arquivo de versão
curl http://localhost:8000/version  # Via API
```

### 🔧 Configurações Avançadas

Para ambientes de produção, considere também:

- **Monitoramento**: Integrar com Prometheus + Grafana
- **Logs centralizados**: Configurar ELK Stack ou similar
- **Redes internas**: Configurar redes overlay para isolamento
- **Service discovery**: Usar nomes de serviço para comunicação entre containers
- **CI/CD**: Automatizar o processo de build, test e deploy

## 📊 Monitoramento

A aplicação inclui:

- **Health Check**: Endpoint `/health` para verificação de saúde
- **Logs estruturados**: Sistema de logging para monitoramento
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