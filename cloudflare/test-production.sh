#!/bin/bash
# Production Testing Script for Heimdall Gatekeeper
# Validates all critical functionality before production deployment

set -e

echo "🧪 Running Production Readiness Tests"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL=${BASE_URL:-"http://localhost:8000"}
JWT_TOKEN=${JWT_TOKEN:-""}

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

test_result() {
    local test_name=$1
    local result=$2

    if [ $result -eq 0 ]; then
        echo -e "${GREEN}✅ $test_name: PASSED${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ $test_name: FAILED${NC}"
        ((TESTS_FAILED++))
    fi
}

# Test 1: Health Check
echo -e "${YELLOW}Testing system health...${NC}"
if curl -s -f $BASE_URL/api/system/health > /dev/null 2>&1; then
    test_result "Health Check" 0
else
    test_result "Health Check" 1
fi

# Test 2: Authentication
echo -e "${YELLOW}Testing authentication...${NC}"
AUTH_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "admin123"}')

if echo "$AUTH_RESPONSE" | grep -q "access_token"; then
    JWT_TOKEN=$(echo "$AUTH_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    test_result "Authentication" 0
else
    test_result "Authentication" 1
fi

# Test 3: Event Ingestion
echo -e "${YELLOW}Testing event ingestion...${NC}"
EVENT_RESPONSE=$(curl -s -X POST $BASE_URL/api/events/ingest \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -d '{
        "source": "test",
        "event_type": "security_alert",
        "severity": "high",
        "title": "Test Security Event",
        "message": "This is a test security event",
        "ip_address": "192.168.1.100"
    }')

if echo "$EVENT_RESPONSE" | grep -q "id"; then
    test_result "Event Ingestion" 0
else
    test_result "Event Ingestion" 1
fi

# Test 4: Alert Generation
echo -e "${YELLOW}Testing alert generation...${NC}"
sleep 2  # Wait for processing
ALERTS_RESPONSE=$(curl -s $BASE_URL/api/alerts \
    -H "Authorization: Bearer $JWT_TOKEN")

if echo "$ALERTS_RESPONSE" | grep -q "test"; then
    test_result "Alert Generation" 0
else
    test_result "Alert Generation" 1
fi

# Test 5: Webhook Delivery
echo -e "${YELLOW}Testing webhook delivery...${NC}"
WEBHOOKS_RESPONSE=$(curl -s $BASE_URL/api/webhooks \
    -H "Authorization: Bearer $JWT_TOKEN")

if echo "$WEBHOOKS_RESPONSE" | grep -q "webhook_id"; then
    test_result "Webhook Configuration" 0
else
    test_result "Webhook Configuration" 1
fi

# Test 6: Threat Intelligence
echo -e "${YELLOW}Testing threat intelligence...${NC}"
THREAT_RESPONSE=$(curl -s "$BASE_URL/api/threat-intel/enrich/ip/8.8.8.8" \
    -H "Authorization: Bearer $JWT_TOKEN")

if echo "$THREAT_RESPONSE" | grep -q "ip"; then
    test_result "Threat Intelligence" 0
else
    test_result "Threat Intelligence" 1
fi

# Test 7: Audit Trail
echo -e "${YELLOW}Testing audit trail...${NC}"
AUDIT_RESPONSE=$(curl -s "$BASE_URL/api/audit/events?limit=10" \
    -H "Authorization: Bearer $JWT_TOKEN")

if echo "$AUDIT_RESPONSE" | grep -q "event_type"; then
    test_result "Audit Trail" 0
else
    test_result "Audit Trail" 1
fi

# Test 8: Custom Dashboards
echo -e "${YELLOW}Testing custom dashboards...${NC}"
DASHBOARD_RESPONSE=$(curl -s "$BASE_URL/api/dashboards" \
    -H "Authorization: Bearer $JWT_TOKEN")

if echo "$DASHBOARD_RESPONSE" | grep -q "dashboard_id"; then
    test_result "Custom Dashboards" 0
else
    test_result "Custom Dashboards" 1
fi

# Test 9: Prometheus Metrics
echo -e "${YELLOW}Testing Prometheus metrics...${NC}"
METRICS_RESPONSE=$(curl -s $BASE_URL/metrics)

if echo "$METRICS_RESPONSE" | grep -q "heimdall_"; then
    test_result "Prometheus Metrics" 0
else
    test_result "Prometheus Metrics" 1
fi

# Test 10: Rate Limiting
echo -e "${YELLOW}Testing rate limiting...${NC}"
RATE_LIMIT_TEST=0
for i in {1..650}; do
    RESPONSE=$(curl -s -w "%{http_code}" $BASE_URL/api/system/health)
    if [ "$RESPONSE" = "429" ]; then
        RATE_LIMIT_TEST=1
        break
    fi
done

test_result "Rate Limiting" $RATE_LIMIT_TEST

# Test 11: Performance Benchmark
echo -e "${YELLOW}Running performance benchmark...${NC}"
PERF_RESULT=$(ab -n 100 -c 10 -H "Authorization: Bearer $JWT_TOKEN" \
    $BASE_URL/api/system/health 2>/dev/null | grep "Requests per second" | awk '{print $4}')

if (( $(echo "$PERF_RESULT > 50" | bc -l) )); then
    test_result "Performance Benchmark" 0
else
    test_result "Performance Benchmark" 1
fi

# Test 12: Memory Usage
echo -e "${YELLOW}Checking memory usage...${NC}"
MEMORY_USAGE=$(ps aux --no-headers -o pmem -C python | awk '{sum+=$1} END {print sum}')

if (( $(echo "$MEMORY_USAGE < 500" | bc -l) )); then
    test_result "Memory Usage" 0
else
    test_result "Memory Usage" 1
fi

# Summary
echo ""
echo "📊 Test Results Summary:"
echo "✅ Tests Passed: $TESTS_PASSED"
echo "❌ Tests Failed: $TESTS_FAILED"
echo "📈 Success Rate: $((TESTS_PASSED * 100 / (TESTS_PASSED + TESTS_FAILED)))%"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! System is production-ready.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please review before deploying to production.${NC}"
    exit 1
fi