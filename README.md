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
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🔧 Instalação e Execução

### Opção 1: Usando Docker (Recomendado)

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

### Opção 2: Execução Local

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute a aplicação:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

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