#!/bin/bash

echo "=========================================="
echo "🧪 VitalTriage Update Patient Flow Test"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_BASE="http://localhost:8002/api/v1"
TEST_PATIENT_ID="P_UPDATE_TEST_$(date +%s)"

echo -e "${BLUE}Step 1: Check health endpoint${NC}"
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE/health")
if [ "$HEALTH" = "200" ]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed (HTTP $HEALTH)${NC}"
    exit 1
fi
echo ""

echo -e "${BLUE}Step 2: Create test patient${NC}"
CREATE_RESPONSE=$(curl -s -X POST "$API_BASE/patient" \
  -H "Content-Type: application/json" \
  -d "{
    \"patient_id\": \"$TEST_PATIENT_ID\",
    \"age\": 45,
    \"gender\": \"M\",
    \"ward\": \"ICU\",
    \"room\": \"101\",
    \"vitals\": {
      \"heart_rate\": 72,
      \"spo2\": 98,
      \"systolic_bp\": 120,
      \"diastolic_bp\": 80,
      \"temperature\": 98.6,
      \"respiratory_rate\": 16
    },
    \"symptoms\": [\"none\"],
    \"notes\": \"Initial assessment\"
  }")

echo "Create Response:"
echo "$CREATE_RESPONSE" | jq .

INITIAL_SCORE=$(echo "$CREATE_RESPONSE" | jq '.score')
INITIAL_SEVERITY=$(echo "$CREATE_RESPONSE" | jq -r '.severity')

if [ "$INITIAL_SCORE" != "null" ]; then
    echo -e "${GREEN}✓ Patient created${NC}"
    echo "  - Patient ID: $TEST_PATIENT_ID"
    echo "  - Initial Score: $INITIAL_SCORE"
    echo "  - Initial Severity: $INITIAL_SEVERITY"
else
    echo -e "${RED}✗ Failed to create patient${NC}"
    exit 1
fi
echo ""

echo -e "${BLUE}Step 3: Update patient with critical vitals${NC}"
echo "  - Changing HR from 72 → 115 (HIGH-RISK)"
echo "  - Changing SpO2 from 98 → 85 (CRITICAL)"
echo "  - Changing Temp from 98.6 → 102.5 (HIGH-RISK)"
echo "  - Changing RR from 16 → 28 (HIGH-RISK)"

UPDATE_RESPONSE=$(curl -s -X PUT "$API_BASE/patient/$TEST_PATIENT_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"vitals\": {
      \"heart_rate\": 115,
      \"spo2\": 85,
      \"systolic_bp\": 165,
      \"diastolic_bp\": 105,
      \"temperature\": 102.5,
      \"respiratory_rate\": 28
    },
    \"symptoms\": [\"chest pain\", \"shortness of breath\"],
    \"notes\": \"Patient deteriorated\"
  }")

echo "Update Response:"
echo "$UPDATE_RESPONSE" | jq .

UPDATED_SCORE=$(echo "$UPDATE_RESPONSE" | jq '.score')
UPDATED_SEVERITY=$(echo "$UPDATE_RESPONSE" | jq -r '.severity')

if [ "$UPDATED_SCORE" != "null" ]; then
    echo -e "${GREEN}✓ Patient updated${NC}"
    echo "  - Updated Score: $UPDATED_SCORE"
    echo "  - Updated Severity: $UPDATED_SEVERITY"
else
    echo -e "${RED}✗ Failed to update patient${NC}"
    echo "Response: $UPDATE_RESPONSE"
    exit 1
fi
echo ""

echo -e "${BLUE}Step 4: Verify changes${NC}"
GET_RESPONSE=$(curl -s "$API_BASE/patient/$TEST_PATIENT_ID")
FINAL_HR=$(echo "$GET_RESPONSE" | jq '.vitals.heart_rate')
FINAL_SPO2=$(echo "$GET_RESPONSE" | jq '.vitals.spo2')
FINAL_SEVERITY=$(echo "$GET_RESPONSE" | jq -r '.severity')

echo "Verification Results:"
echo "  - Heart Rate: 72 → 115 → $FINAL_HR ✓"
echo "  - SpO2: 98 → 85 → $FINAL_SPO2 ✓"
echo "  - Severity: $INITIAL_SEVERITY → $UPDATED_SEVERITY → $FINAL_SEVERITY"

if [ "$FINAL_HR" = "115" ] && [ "$FINAL_SPO2" = "85" ]; then
    echo -e "${GREEN}✓ Update verified in database${NC}"
else
    echo -e "${RED}✗ Update verification failed${NC}"
fi
echo ""

echo -e "${BLUE}Step 5: Check dashboard${NC}"
DASHBOARD=$(curl -s "$API_BASE/dashboard")
echo "Dashboard Response:"
echo "$DASHBOARD" | jq '.[] | length'

echo ""
echo -e "${GREEN}=========================================="
echo "✅ Test Complete!"
echo "==========================================${NC}"
echo ""
echo "Summary:"
echo "  - Patient ID: $TEST_PATIENT_ID"
echo "  - Initial Severity: $INITIAL_SEVERITY"
echo "  - Final Severity: $FINAL_SEVERITY"
echo "  - Score Changed: $INITIAL_SCORE → $UPDATED_SCORE"
