# Configuração do Traefik para Docker Swarm

Este documento fornece instruções para configurar o Traefik v2+ em um cluster Docker Swarm, necessário para o deploy da XML Download API.

## 📋 Pré-requisitos

- Cluster Docker Swarm ativo
- Domínios DNS configurados apontando para o IP do cluster
- Portas 80 e 443 abertas no firewall

## 🚀 Setup Inicial do Traefik

### 1. Criar Rede Overlay

```bash
# Criar rede overlay externa para o Traefik
docker network create --driver=overlay --attachable traefik-public
```

### 2. Criar Arquivo de Configuração do Traefik

Crie o arquivo `traefik-stack.yml`:

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    command:
      # Enable Docker Swarm mode
      - --providers.docker.swarmmode=true
      - --providers.docker.exposedbydefault=false
      - --providers.docker.network=traefik-public
      
      # Configure entrypoints
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      
      # Global redirect to HTTPS
      - --entrypoints.web.http.redirections.entryPoint.to=websecure
      - --entrypoints.web.http.redirections.entryPoint.scheme=https
      
      # Let's Encrypt configuration
      - --certificatesresolvers.letsencryptresolver.acme.httpchallenge=true
      - --certificatesresolvers.letsencryptresolver.acme.httpchallenge.entrypoint=web
      - --certificatesresolvers.letsencryptresolver.acme.email=seu-email@dominio.com
      - --certificatesresolvers.letsencryptresolver.acme.storage=/letsencrypt/acme.json
      
      # Enable API and dashboard
      - --api.dashboard=true
      - --api.insecure=false
      
      # Logging
      - --log.level=INFO
      - --accesslog=true
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - letsencrypt:/letsencrypt
    networks:
      - traefik-public
    deploy:
      placement:
        constraints:
          - node.role == manager
      labels:
        # Dashboard
        - traefik.enable=true
        - traefik.http.routers.api.rule=Host(`traefik.seu-dominio.com`)
        - traefik.http.routers.api.tls=true
        - traefik.http.routers.api.tls.certresolver=letsencryptresolver
        - traefik.http.routers.api.service=api@internal
        - traefik.http.routers.api.middlewares=auth
        
        # Basic Auth (gerar com: echo $(htpasswd -nb admin senha) | sed -e s/\\$/\\$\\$/g)
        - traefik.http.middlewares.auth.basicauth.users=admin:$$2y$$10$$exemplo
        
      restart_policy:
        condition: on-failure

volumes:
  letsencrypt:

networks:
  traefik-public:
    external: true
```

### 3. Gerar Hash de Senha para Dashboard

```bash
# Instalar htpasswd se necessário
sudo apt-get install apache2-utils

# Gerar hash da senha (substitua 'admin' e 'senha123')
echo $(htpasswd -nb admin senha123) | sed -e s/\\$/\\$\\$/g
```

Copie o resultado e substitua na label `traefik.http.middlewares.auth.basicauth.users`.

### 4. Deploy do Traefik

```bash
# Deploy da stack do Traefik
docker stack deploy -c traefik-stack.yml traefik

# Verificar se está rodando
docker stack ps traefik
```

## 🔧 Configuração DNS

Configure seus domínios DNS para apontar para o IP público do cluster:

```
# Exemplos de registros DNS tipo A
traefik.seu-dominio.com    IN A    xxx.xxx.xxx.xxx
api-xml.seu-dominio.com    IN A    xxx.xxx.xxx.xxx
```

## ✅ Verificação

### Testar o Dashboard do Traefik

```bash
# Acessar dashboard (use suas credenciais)
curl -u admin:senha123 https://traefik.seu-dominio.com
```

### Verificar Certificados SSL

```bash
# Verificar se o certificado foi gerado
curl -I https://traefik.seu-dominio.com
```

## 🔧 Troubleshooting

### Verificar Logs do Traefik

```bash
# Ver logs do Traefik
docker service logs traefik_traefik
```

### Verificar Certificados Let's Encrypt

```bash
# Verificar volume de certificados
docker volume inspect traefik_letsencrypt
```

### Problemas Comuns

1. **Erro de DNS**: Certificar que DNS está propagado
2. **Portas bloqueadas**: Verificar firewall (portas 80/443)
3. **Rate limit Let's Encrypt**: Aguardar ou usar staging environment

## 📚 Próximos Passos

Após configurar o Traefik, você pode proceder com o deploy da XML Download API usando o arquivo `docker-stack.yml` fornecido no projeto.

## 🔐 Considerações de Segurança

- Alterar credenciais padrão do dashboard
- Configurar firewall adequadamente
- Monitorar logs de acesso
- Implementar rate limiting se necessário