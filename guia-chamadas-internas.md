# 🔗 Guia: Chamadas Internas para XML Download API

## 📋 Situação Atual
Você instalou a API usando `install.sh` - a aplicação roda **diretamente** com uvicorn (não como Docker service).

## 🌐 Como Outros Containers Chamam Sua API

### **Cenário 1: Container com nome específico**
```bash
# Se você criou assim:
docker run -d --name minha-api -p 8000:8000 ubuntu

# Outros containers podem chamar por:
curl http://minha-api:8000/health
```

### **Cenário 2: Container sem nome personalizado**
```bash
# Se criou assim:
docker run -d -p 8000:8000 ubuntu

# Descubra o nome:
docker ps
# NAMES: boring_tesla (exemplo)

# Outros containers chamam:
curl http://boring_tesla:8000/health
```

### **Cenário 3: IP do container**
```bash
# Descubra o IP:
docker inspect NOME_CONTAINER | grep IPAddress

# Outros containers podem chamar:
curl http://172.17.0.2:8000/health  # (exemplo de IP)
```

## 🔧 Exemplos Práticos

### **Teste 1: Descobrir nome do seu container**
```bash
# Execute DENTRO do seu container:
hostname
# OU
cat /etc/hostname

# Resultado: nome do container (ex: abc123def456)
```

### **Teste 2: Descobrir IP interno**
```bash
# Execute DENTRO do seu container:
hostname -I
# OU
ip addr show eth0 | grep inet

# Resultado: IP interno (ex: 172.17.0.2)
```

### **Teste 3: De outro container**
```bash
# Criar container de teste:
docker run --rm -it alpine sh

# Dentro do container de teste:
apk add curl
curl http://NOME_DO_SEU_CONTAINER:8000/health
# OU
curl http://IP_DO_SEU_CONTAINER:8000/health
```

## 🏗️ Cenários Comuns

### **A. Container standalone (atual)**
```bash
# Seu container API
Container: minha-api (172.17.0.2:8000)

# Outro container cliente  
docker run --rm alpine sh
curl http://minha-api:8000/health      # ✅ Por nome
curl http://172.17.0.2:8000/health     # ✅ Por IP
```

### **B. Com rede personalizada**
```bash
# Criar rede
docker network create minha-rede

# Executar containers na mesma rede
docker run -d --name api --network minha-rede your-image
docker run --rm --network minha-rede alpine sh

# Dentro do Alpine:
curl http://api:8000/health  # ✅ Nome do container
```

### **C. Com docker-compose**
```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    image: your-image
    ports: 
      - "8000:8000"
    
  client:
    image: alpine
    command: sh -c "apk add curl && curl http://api:8000/health"
    depends_on:
      - api
```

## 🚨 **Questão da Porta 8000**

### ✅ **SEM conflito entre containers!**
```bash
# Container 1: API na porta 8000 interna
Container A: 172.17.0.2:8000 ✅

# Container 2: Outra API na porta 8000 interna  
Container B: 172.17.0.3:8000 ✅

# Cada container tem seu namespace isolado!
```

### ❌ **Conflito apenas no HOST**
```bash
# Isto SIM dá conflito:
docker run -p 8000:8000 container-a  # ✅ OK
docker run -p 8000:8000 container-b  # ❌ ERRO!

# Solução: Portas externas diferentes
docker run -p 8000:8000 container-a  # ✅ 
docker run -p 8001:8000 container-b  # ✅
```

## 🎯 **Para Descobrir SEU Caso**

Execute estes comandos **dentro do seu container**:
```bash
# 1. Nome do container
hostname

# 2. IP do container  
hostname -I

# 3. Processo da API
ps aux | grep uvicorn

# 4. Porta em uso
netstat -tlnp | grep 8000
```

## 📞 **Resumo para Chamadas:**

### **Do mesmo container:**
```bash
curl http://localhost:8000/health
```

### **De outros containers:**
```bash
curl http://$(hostname):8000/health        # Usando nome
curl http://$(hostname -I | awk '{print $1}'):8000/health  # Usando IP
```

### **Template de teste:**
```bash
# Salve este script no seu container como test-calls.sh:
#!/bin/bash
echo "Nome do container: $(hostname)"
echo "IP do container: $(hostname -I)"
echo "Teste local: $(curl -s http://localhost:8000/health)"
echo ""
echo "Para outros containers usarem:"
echo "curl http://$(hostname):8000/health"
echo "curl http://$(hostname -I | awk '{print $1}'):8000/health"
```