#!/bin/bash
# Heimdall Gatekeeper - API Configuration Guide Generator
# This script generates a detailed guide for configuring all APIs

cat << 'EOF'
# 🚀 HEIMDALL GATEKEEPER - CONFIGURAÇÃO COMPLETA DE APIs

## 📋 LISTA COMPLETA DE APIs NECESSÁRIAS

### 1. 🔐 SEGURANÇA & AUTENTICAÇÃO
#### JWT Secret (OBRIGATÓRIO)
- **Onde configurar**: .env → `HEIMDALL_JWT_SECRET`
- **Como gerar**: `openssl rand -hex 32`
- **Exemplo**: `HEIMDALL_JWT_SECRET=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z`

---

### 2. ☁️ CLOUDFLARE (OBRIGATÓRIO PARA PRODUÇÃO)
#### Account ID & API Token
- **Como obter**:
  1. Acesse: https://dash.cloudflare.com/profile/api-tokens
  2. Crie token com permissões: Account, Zone, Pages, D1, Functions
  3. Account ID: https://dash.cloudflare.com/ (no URL)

- **Onde configurar**:
  ```bash
  CF_ACCOUNT_ID=1234567890abcdef1234567890abcdef
  CF_API_TOKEN=your-cloudflare-api-token-here
  ```

---

### 3. 🧠 THREAT INTELLIGENCE FEEDS (OPCIONAIS)

#### 🔸 AlienVault OTX (GRÁTIS - RECOMENDADO)
- **Site**: https://otx.alienvault.com/
- **Como obter**:
  1. Crie conta gratuita
  2. Vá em: Settings → API Key
  3. Copie a API Key

- **Onde configurar**: .env → `OTX_API_KEY=your-key-here`
- **Rate Limit**: 1000 requests/dia

#### 🔸 MISP (OPEN SOURCE)
- **Site**: https://www.misp-project.org/
- **Como obter**:
  1. Instale MISP ou use instância pública
  2. Vá em: Administration → List Auth Keys
  3. Gere nova API Key

- **Onde configurar**:
  ```bash
  MISP_URL=https://your-misp-instance.com
  MISP_API_KEY=your-misp-api-key
  ```

#### 🔸 AbuseIPDB (GRÁTIS)
- **Site**: https://www.abuseipdb.com/
- **Como obter**:
  1. Crie conta gratuita
  2. Vá em: Settings → API
  3. Copie API Key

- **Onde configurar**: .env → `ABUSEIPDB_API_KEY=your-key-here`
- **Rate Limit**: 1000 requests/dia

#### 🔸 VirusTotal (FREEMIUM)
- **Site**: https://www.virustotal.com/
- **Como obter**:
  1. Crie conta gratuita
  2. Vá em: Profile → API Key
  3. Use a Public API Key

- **Onde configurar**: .env → `VIRUSTOTAL_API_KEY=your-key-here`
- **Rate Limit**: 500 requests/dia (free tier)

#### 🔸 Shodan (FREEMIUM)
- **Site**: https://www.shodan.io/
- **Como obter**:
  1. Crie conta gratuita
  2. Vá em: Account → API Key
  3. Copie API Key

- **Onde configurar**: .env → `SHODAN_API_KEY=your-key-here`
- **Rate Limit**: 100 requests/dia (free tier)

---

### 4. 📊 SIEM INTEGRATIONS (OPCIONAIS)

#### 🔸 Splunk HTTP Event Collector (HEC)
- **Como configurar no Splunk**:
  1. Vá em: Settings → Data Inputs → HTTP Event Collector
  2. Crie novo HEC input
  3. Copie Token Value

- **Onde configurar**:
  ```bash
  SPLUNK_HEC_URL=https://your-splunk-server:8088/services/collector
  SPLUNK_HEC_TOKEN=your-hec-token-here
  SPLUNK_INDEX=heimdall
  ```

#### 🔸 Elasticsearch
- **Opção 1 - API Key**:
  ```bash
  ELASTICSEARCH_URL=https://your-elasticsearch:9200
  ELASTICSEARCH_API_KEY=your-base64-encoded-api-key
  ELASTICSEARCH_INDEX_PREFIX=heimdall
  ```

- **Opção 2 - Username/Password**:
  ```bash
  ELASTICSEARCH_URL=https://your-elasticsearch:9200
  ELASTICSEARCH_USERNAME=elastic
  ELASTICSEARCH_PASSWORD=your-password
  ELASTICSEARCH_INDEX_PREFIX=heimdall
  ```

---

### 5. ⚡ REDIS CACHE (OPCIONAL - MELHORA PERFORMANCE)
#### Redis Configuration
- **Para Redis local**:
  ```bash
  REDIS_HOST=localhost
  REDIS_PORT=6379
  REDIS_DB=0
  REDIS_PASSWORD=
  ```

- **Para Redis na nuvem (Redis Labs, etc.)**:
  ```bash
  REDIS_HOST=your-redis-host.redis.cache.windows.net
  REDIS_PORT=6380
  REDIS_PASSWORD=your-redis-password
  ```

---

## 🔧 CONFIGURAÇÃO PASSO A PASSO

### PASSO 1: Preparar arquivo .env
```bash
cd /home/rgarcez/Documentos/heimdall-gatekeeper
cp .env.example .env
# Edite o arquivo .env com suas chaves
```

### PASSO 2: Configurar JWT Secret (OBRIGATÓRIO)
```bash
# Gere uma chave segura
openssl rand -hex 32

# Cole no .env:
HEIMDALL_JWT_SECRET=sua-chave-gerada-aqui
```

### PASSO 3: Configurar Cloudflare (OBRIGATÓRIO PARA PRODUÇÃO)
```bash
# Obtenha Account ID e API Token no dashboard Cloudflare
# Cole no .env:
CF_ACCOUNT_ID=seu-account-id
CF_API_TOKEN=seu-api-token
```

### PASSO 4: Configurar Threat Intelligence (OPCIONAL)
```bash
# Recomendado: OTX (gratuito e confiável)
# Vá em https://otx.alienvault.com/ e crie conta
# Cole no .env:
OTX_API_KEY=sua-chave-otx
```

### PASSO 5: Testar configuração
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar testes
python -m pytest tests/ -v

# Testar produção
bash cloudflare/test-production.sh
```

### PASSO 6: Deploy
```bash
# Deploy completo
bash cloudflare/deploy.sh

# Ou testar localmente primeiro
uvicorn backend.api.main:app --reload
```

---

## 📊 STATUS DE CONFIGURAÇÃO

Após configurar, execute:
```bash
python3 -c "
from backend.core.threat_intel_config import get_enabled_feeds, validate_feed_configs
feeds = get_enabled_feeds()
issues = validate_feed_configs()
print(f'Feeds habilitados: {len(feeds)}')
print(f'Problemas encontrados: {len(issues)}')
for issue in issues:
    print(f'  - {issue}')
if not issues:
    print('✅ Todas as configurações válidas!')
"
```

---

## 🎯 APIs RECOMENDADAS PARA COMEÇAR

### MÍNIMO (Obrigatório):
- JWT Secret ✅
- Cloudflare Account ✅

### RECOMENDADO (Básico):
- AlienVault OTX ✅ (Threat Intel gratuito)

### AVANÇADO (Enterprise):
- Splunk HEC ✅ (SIEM integration)
- Elasticsearch ✅ (SIEM integration)
- MISP ✅ (Advanced threat sharing)

---

## ❓ DÚVIDAS FREQUENTES

**Q: Posso usar sem APIs externas?**
A: Sim! O sistema funciona perfeitamente sem elas, apenas com menos enrichment.

**Q: Qual a diferença entre OTX e MISP?**
A: OTX é mais fácil de usar (gratuito), MISP é mais avançado para sharing de ameaças.

**Q: Como testar se as APIs estão funcionando?**
A: Execute `bash cloudflare/test-production.sh` - ele testa todas as integrações.

**Q: Posso mudar as APIs depois?**
A: Sim! Apenas edite o .env e reinicie o serviço.

---

## 📞 SUPORTE

Se tiver dúvidas sobre alguma API específica, consulte:
- OTX: https://otx.alienvault.com/docs
- MISP: https://www.misp-project.org/documentation/
- Splunk: https://docs.splunk.com/Documentation/Splunk/latest/Data/HECExamples
- Elasticsearch: https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html

EOF