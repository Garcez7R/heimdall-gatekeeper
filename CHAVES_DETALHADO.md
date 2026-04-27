# 📚 GUIA COMPLETO - COMO CRIAR TODAS AS CHAVES DE API

## 🎯 ÍNDICE
1. [JWT Secret (OBRIGATÓRIO)](#jwt-secret)
2. [Cloudflare (OBRIGATÓRIO PARA PRODUÇÃO)](#cloudflare)
3. [Threat Intelligence - OTX](#otx)
4. [Threat Intelligence - VirusTotal](#virustotal)
5. [Threat Intelligence - AbuseIPDB](#abuseipdb)
6. [Threat Intelligence - Shodan](#shodan)
7. [SIEM - Splunk](#splunk)
8. [SIEM - Elasticsearch](#elasticsearch)
9. [Redis (Opcional)](#redis)
10. [Template .env Pronto](#template-env-pronto)

---

## 1️⃣ JWT SECRET (OBRIGATÓRIO)

### O que é?
Uma chave criptográfica que protege os tokens de autenticação do seu sistema.

### 🔥 Como criar (SUPER FÁCIL):

**No seu terminal, execute:**
```bash
openssl rand -hex 32
```

**Você vai ver algo assim:**
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
```

**Copie exato esse resultado!**

### ✅ Como usar no .env:

Abra o arquivo `.env` que está em:
```
/home/rgarcez/Documentos/heimdall-gatekeeper/.env
```

Procure por esta linha:
```
HEIMDALL_JWT_SECRET=change-me-in-production-please-use-strong-random-key
```

E substitua por:
```
HEIMDALL_JWT_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
```

✅ **PRONTO! JWT configurado!**

---

## 2️⃣ CLOUDFLARE (OBRIGATÓRIO PARA PRODUÇÃO)

### O que é?
Cloudflare hospeda seu site, banco de dados (D1), funções serverless (Workers) e gerencia DNS.

### 📋 Passo 1: Criar Conta Cloudflare

1. Acesse: https://dash.cloudflare.com/sign-up
2. Preencha com seu email e senha
3. Confirme no email
4. Você vai para o dashboard

### 📋 Passo 2: Obter Account ID

1. No dashboard Cloudflare, click em **"Account"** (canto inferior esquerdo)
2. Você vai ver uma página com vários información
3. Procure por: **"Account ID"** 
4. Clique no ícone de copiar ao lado
5. Cole aqui: (você vai precisar depois)

**Exemplo do que você vai encontrar:**
```
Account ID: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

### 📋 Passo 3: Criar API Token

1. No dashboard Cloudflare, clique em **"Account"** (canto inferior esquerdo)
2. Vá em: **API Tokens** (na barra esquerda)
3. Clique em **"Create Token"**
4. Selecione template: **"Edit Cloudflare Workers"** (já vem com as permissões certas)
5. Scroll para baixo e clique em "Continue to summary"
6. Clique em "Create Token"
7. **COPIE O TOKEN** (você só vê uma vez!)

**Exemplo do que você vai copiar:**
```
Vy6l4zM4vP2eF4wZ5xJ6kQ8nH9bR3sT1yU2aW4dF5gH6jK7lM0nP1qR2sT3uV4wX5
```

### ✅ Como usar no .env:

Abra o `.env` e procure:
```
CF_ACCOUNT_ID=
CF_API_TOKEN=
```

Substitua por:
```
CF_ACCOUNT_ID=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
CF_API_TOKEN=Vy6l4zM4vP2eF4wZ5xJ6kQ8nH9bR3sT1yU2aW4dF5gH6jK7lM0nP1qR2sT3uV4wX5
```

✅ **PRONTO! Cloudflare configurado!**

---

## 3️⃣ THREAT INTELLIGENCE - OTX (AlienVault)

### O que é?
Banco de dados de ameaças (IPs maliciosos, domínios suspeitos, malware, etc.)

### 📋 Passo 1: Criar Conta OTX

1. Acesse: https://otx.alienvault.com/
2. Clique em **"Sign Up"** (canto superior direito)
3. Preencha:
   - Email
   - Senha
   - Username (seu nome de usuário)
4. Confirme no email
5. Faça login

### 📋 Passo 2: Obter API Key

1. **Menu > Settings** (canto superior direito, ao lado do seu username)
2. Clique em **"API Keys"** (barra esquerda)
3. Você vai ver uma seção: **"API Key"**
4. Clique no ícone de "Show" ou copie direto

**Exemplo do que você vai ver:**
```
API Key: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

### ✅ Como usar no .env:

Procure:
```
OTX_API_KEY=
```

Substitua por:
```
OTX_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

✅ **PRONTO! OTX configurado!**

---

## 4️⃣ THREAT INTELLIGENCE - VirusTotal

### O que é?
Verifica se um arquivo, URL ou IP é malicioso (integração com 70+ antivírus).

### 📋 Passo 1: Criar Conta

1. Acesse: https://www.virustotal.com/
2. Clique em **"Sign in"** (canto superior direito)
3. Clique em **"Create an account"**
4. Preencha email e senha
5. Confirme no email

### 📋 Passo 2: Obter API Key

1. **Menu > Settings** (canto superior direito)
2. Clique em **"API Key"** (barra esquerda)
3. Você vai ver: **"Public API Key"**
4. Copie o valor

**Exemplo:**
```
API Key: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f
```

### ⚠️ Limitações (Free Tier):
- 500 requisições/dia
- Ideal para testes

### ✅ Como usar no .env:

Procure:
```
VIRUSTOTAL_API_KEY=
```

Substitua por:
```
VIRUSTOTAL_API_KEY=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f
```

✅ **PRONTO! VirusTotal configurado!**

---

## 5️⃣ THREAT INTELLIGENCE - AbuseIPDB

### O que é?
Banco de dados de IPs que abusam da rede (spam, hackers, etc.)

### 📋 Passo 1: Criar Conta

1. Acesse: https://www.abuseipdb.com/
2. Clique em **"Sign Up"** (canto superior direito)
3. Preencha informações
4. Confirme no email

### 📋 Passo 2: Obter API Key

1. **Menu > Account** (canto superior direito)
2. Clique em **"API"** (barra esquerda)
3. Role para baixo até "API Key"
4. Copie a chave

**Exemplo:**
```
API Key: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

### ✅ Como usar no .env:

Procure:
```
ABUSEIPDB_API_KEY=
```

Substitua por:
```
ABUSEIPDB_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

✅ **PRONTO! AbuseIPDB configurado!**

---

## 6️⃣ THREAT INTELLIGENCE - Shodan

### O que é?
Motor de busca para dispositivos conectados à internet (IoT, servidores, câmeras, etc.)

### 📋 Passo 1: Criar Conta

1. Acesse: https://www.shodan.io/
2. Clique em **"Register"** (canto superior direito)
3. Preencha email e senha
4. Confirme no email

### 📋 Passo 2: Obter API Key

1. **Menu > Account** (canto superior direito)
2. Você vai ver: **"API Key"** na página
3. Copie a chave

**Exemplo:**
```
API Key: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

### ⚠️ Limitações (Free Tier):
- 100 requisições/dia
- Bom para começar

### ✅ Como usar no .env:

Procure:
```
SHODAN_API_KEY=
```

Substitua por:
```
SHODAN_API_KEY=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

✅ **PRONTO! Shodan configurado!**

---

## 7️⃣ SIEM - SPLUNK

### O que é?
Plataforma de log centralizado que recebe eventos do seu sistema.

### 📋 Passo 1: Instalar Splunk (LOCAL OU CLOUD)

**Opção A: Splunk Cloud (mais fácil)**
1. Acesse: https://www.splunk.com/
2. Clique em **"Free Trial"**
3. Crie conta
4. Você recebe acesso ao Splunk Cloud

**Opção B: Splunk Local (Docker)**
```bash
docker run -d -p 8000:8000 -e SPLUNK_PASSWORD=yourpassword splunk/splunk:latest start-service
```

### 📋 Passo 2: Criar HTTP Event Collector (HEC)

1. No Splunk, vá em: **Settings > Data Inputs**
2. Clique em **"HTTP Event Collector"**
3. Clique em **"New Token"**
4. Dê um nome: "Heimdall"
5. Clique em "Next"
6. Selecione um índice (ou crie "heimdall")
7. Clique em "Review"
8. Clique em "Submit"
9. **COPIE O TOKEN** que aparece

**Exemplo do que você vai copiar:**
```
Token: a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6
```

### 📋 Passo 3: Pegar URL do HEC

1. No Splunk, vá em: **Settings > Data Inputs > HTTP Event Collector**
2. Procure por: **"HEC Token Endpoint"** ou **"Check HEC connectivity"**
3. A URL vai ser algo como:
   ```
   https://seu-splunk-instance.splunkcloud.com:8088
   ```

### ✅ Como usar no .env:

Procure:
```
SPLUNK_HEC_URL=
SPLUNK_HEC_TOKEN=
SPLUNK_INDEX=heimdall
```

Substitua por:
```
SPLUNK_HEC_URL=https://seu-splunk-instance.splunkcloud.com:8088
SPLUNK_HEC_TOKEN=a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6
SPLUNK_INDEX=heimdall
```

✅ **PRONTO! Splunk configurado!**

---

## 8️⃣ SIEM - ELASTICSEARCH

### O que é?
Engine de busca e análise de logs (como Splunk, mas open-source).

### 📋 Passo 1: Elasticsearch Cloud (mais fácil)

1. Acesse: https://www.elastic.co/cloud
2. Clique em **"Start free"**
3. Crie conta
4. Você vai receber:
   ```
   URL: https://abc123.es.us-central1.gcp.cloud.es.io:9200
   Username: elastic
   Password: sua-senha-gerada
   ```
5. **ANOTE TUDO ISSO!**

### 📋 Passo 2: Criar API Key (recomendado)

1. No Elasticsearch, vá em: **Management > API Keys**
2. Clique em **"Create API key"**
3. Nome: "Heimdall"
4. Permissões: marque **"All"**
5. Clique em "Create API key"
6. **COPIE O API KEY** (vem em formato base64)

### ✅ Como usar no .env (Opção A - API Key):

Procure:
```
ELASTICSEARCH_URL=
ELASTICSEARCH_API_KEY=
ELASTICSEARCH_INDEX_PREFIX=heimdall
```

Substitua por:
```
ELASTICSEARCH_URL=https://abc123.es.us-central1.gcp.cloud.es.io:9200
ELASTICSEARCH_API_KEY=VTIxMjM0NTY3ODkwYWJjZGVmX2tleQ==
ELASTICSEARCH_INDEX_PREFIX=heimdall
```

### ✅ Como usar no .env (Opção B - Username/Password):

```
ELASTICSEARCH_URL=https://abc123.es.us-central1.gcp.cloud.es.io:9200
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=sua-senha-gerada
ELASTICSEARCH_INDEX_PREFIX=heimdall
```

✅ **PRONTO! Elasticsearch configurado!**

---

## 9️⃣ REDIS (OPCIONAL)

### O que é?
Cache rápido em memória (melhora muito a performance).

### 📋 Opção A: Redis Local (Docker - Mais Fácil)

```bash
docker run -d -p 6379:6379 redis:latest
```

### 📋 Opção B: Redis Cloud (Azure, AWS, DigitalOcean)

1. Acesse: https://redis.com/try-free/
2. Crie conta
3. Crie um banco de dados
4. Você vai receber:
   ```
   Host: seu-redis.redis.cache.windows.net
   Port: 6380
   Password: sua-senha
   SSL: true
   ```

### ✅ Como usar no .env (Opção A - Local):

```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

### ✅ Como usar no .env (Opção B - Cloud):

```
REDIS_HOST=seu-redis.redis.cache.windows.net
REDIS_PORT=6380
REDIS_DB=0
REDIS_PASSWORD=sua-senha
```

✅ **PRONTO! Redis configurado!**

---

## 🎯 TEMPLATE .ENV PRONTO PARA COPIAR E COLAR

Depois de conseguir todas as chaves, copie e cole tudo isso no seu arquivo `.env`:

```bash
# ==========================================
# SECURITY & AUTHENTICATION
# ==========================================
HEIMDALL_JWT_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2

# ==========================================
# REDIS CACHE
# ==========================================
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# ==========================================
# THREAT INTELLIGENCE FEEDS
# ==========================================
OTX_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
ABUSEIPDB_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
VIRUSTOTAL_API_KEY=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f
SHODAN_API_KEY=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p

# ==========================================
# SIEM INTEGRATIONS
# ==========================================
# Splunk
SPLUNK_HEC_URL=https://seu-splunk-instance.splunkcloud.com:8088
SPLUNK_HEC_TOKEN=a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6
SPLUNK_INDEX=heimdall

# Elasticsearch
ELASTICSEARCH_URL=https://abc123.es.us-central1.gcp.cloud.es.io:9200
ELASTICSEARCH_API_KEY=VTIxMjM0NTY3ODkwYWJjZGVmX2tleQ==
ELASTICSEARCH_INDEX_PREFIX=heimdall

# ==========================================
# CLOUDFLARE DEPLOYMENT
# ==========================================
CF_ACCOUNT_ID=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
CF_API_TOKEN=Vy6l4zM4vP2eF4wZ5xJ6kQ8nH9bR3sT1yU2aW4dF5gH6jK7lM0nP1qR2sT3uV4wX5
```

---

## ✅ CHECKLIST FINAL

Antes de fazer commit e deploy:

- [ ] JWT Secret gerado e configurado
- [ ] Cloudflare Account ID obtido
- [ ] Cloudflare API Token criado
- [ ] OTX API Key obtido
- [ ] VirusTotal API Key obtido
- [ ] AbuseIPDB API Key obtido
- [ ] Shodan API Key obtido
- [ ] Splunk HEC Token criado
- [ ] Elasticsearch URL e credenciais obtidos
- [ ] Redis configurado
- [ ] Arquivo `.env` salvo com todas as chaves
- [ ] Testes rodando localmente: `python -m pytest tests/ -v`
- [ ] Commit criado: `git add . && git commit -m "Production API Configuration"`
- [ ] Push feito: `git push origin main`

---

## 🚀 PRÓXIMOS PASSOS

1. **Seguir este guia** e obter todas as chaves
2. **Atualizar o arquivo `.env`** com as chaves
3. **Rodar os testes**: `python -m pytest tests/ -v`
4. **Fazer commit e push**:
   ```bash
   git add .
   git commit -m "Production API Configuration: All APIs configured"
   git push origin main
   ```
5. **Deploy para Cloudflare**:
   ```bash
   bash cloudflare/deploy.sh
   ```

---

## 💡 DICAS

- **Não compartilhe suas chaves com ninguém!**
- **Nunca commite o `.env` com senhas reais** (adicione ao `.gitignore`)
- **Rotacione as chaves periodicamente** para segurança
- **Use variáveis de ambiente** em produção, não arquivos `.env`

Boa sorte! 🎯
