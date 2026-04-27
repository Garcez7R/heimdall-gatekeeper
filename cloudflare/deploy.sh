#!/bin/bash
# Heimdall Gatekeeper - Automated Cloudflare Deployment Script
# This script handles complete deployment to Cloudflare Pages + Functions + D1

set -e  # Exit on any error

echo "🚀 Starting Heimdall Gatekeeper Cloudflare Deployment"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="heimdall-gatekeeper"
D1_DATABASE_NAME="heimdall-db"
CF_ACCOUNT_ID=${CF_ACCOUNT_ID:-""}
CF_API_TOKEN=${CF_API_TOKEN:-""}

# Validate environment
if [ -z "$CF_ACCOUNT_ID" ]; then
    echo -e "${RED}Error: CF_ACCOUNT_ID not set${NC}"
    exit 1
fi

if [ -z "$CF_API_TOKEN" ]; then
    echo -e "${RED}Error: CF_API_TOKEN not set${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Installing dependencies...${NC}"
npm install -g wrangler@latest
pip install -r requirements.txt

echo -e "${YELLOW}Step 2: Creating D1 Database...${NC}"
wrangler d1 create $D1_DATABASE_NAME --yes || echo "Database may already exist"

echo -e "${YELLOW}Step 3: Running database migrations...${NC}"
wrangler d1 execute $D1_DATABASE_NAME --remote --file=cloudflare/d1/0001_init.sql

echo -e "${YELLOW}Step 4: Deploying Cloudflare Functions...${NC}"
wrangler deploy

echo -e "${YELLOW}Step 5: Deploying Cloudflare Pages...${NC}"
cd frontend
wrangler pages deploy . --project-name=$PROJECT_NAME-frontend --yes
cd ..

echo -e "${YELLOW}Step 6: Running production tests...${NC}"
bash cloudflare/test-production.sh

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo ""
echo "🌐 Frontend URL: https://$PROJECT_NAME-frontend.pages.dev"
echo "🔧 API URL: https://$PROJECT_NAME.workers.dev"
echo ""
echo "📊 To monitor:"
echo "  - wrangler tail"
echo "  - Check Cloudflare Dashboard"
echo "  - Prometheus metrics at /metrics"