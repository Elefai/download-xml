# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.1.0] - 2024-01-15

### ✨ Adicionado
- **Rate Limiting**: Proteção contra abuso com limite de 10 requisições por minuto por IP
- **Sistema de Cache**: Cache TTL inteligente de 15 minutos para XMLs válidos
- **Validações de Segurança**: 
  - Bloqueio de URLs para localhost e IPs privados
  - Proteção básica contra ataques XXE
  - Validação de esquemas de URL (apenas HTTP/HTTPS)
- **Controle de Tamanho**: Limite configurável de tamanho de arquivo (padrão: 10MB)
- **Endpoint de Estatísticas**: `/api/v1/cache/stats` para monitoramento do cache
- **Configuração Centralizada**: Sistema de configuração via variáveis de ambiente
- **Testes Automatizados**: Suíte completa de testes unitários e de integração
- **Melhor Logging**: Logs mais detalhados para debugging e monitoramento

### 🔄 Alterado
- **Dependências Atualizadas**:
  - FastAPI: 0.104.1 → 0.115.6
  - Uvicorn: 0.24.0 → 0.32.1
  - Requests: 2.31.0 → 2.32.3
  - Pydantic: 2.5.0 → 2.10.4
  - Python-multipart: 0.0.6 → 0.0.20
- **Modelos Pydantic**: Migrados para sintaxe v2 (ConfigDict)
- **Resposta de Sucesso**: Agora inclui informações sobre cache, tamanho e timestamp
- **Headers HTTP**: Headers otimizados para melhor compatibilidade
- **Download Streaming**: Implementado download com verificação de tamanho em tempo real

### 🛡️ Segurança
- **Proteção XXE**: Detecção de padrões suspeitos em XML
- **Validação de URL**: Bloqueio de URLs maliciosas
- **Rate Limiting**: Proteção contra ataques de negação de serviço
- **Controle de Tamanho**: Prevenção contra download de arquivos muito grandes

### 🚀 Performance
- **Cache Inteligente**: Reduz latência para XMLs frequentemente acessados
- **Download Otimizado**: Streaming com verificação de tamanho
- **Headers Otimizados**: Melhor compatibilidade com servidores

### 🧪 Qualidade
- **Testes Unitários**: Cobertura completa das funções principais
- **Testes de Integração**: Validação dos endpoints da API
- **Configuração de Testes**: Setup do pytest com configurações adequadas

## [1.0.0] - 2024-01-01

### ✨ Adicionado
- Implementação inicial da API de download de XML
- Endpoint `/api/v1/download_xml` para download e validação
- Validação básica de XML
- Documentação automática com Swagger UI e ReDoc
- Containerização com Docker
- Sistema básico de logging
- Tratamento de erros HTTP