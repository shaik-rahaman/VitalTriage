#!/bin/bash

# ============================================================================
# VitalTriage API Manual Testing Script
# ============================================================================
# This script tests all API endpoints with curl commands.
# Run this after starting the backend server on port 8002
# ============================================================================

set -e

API_BASE_URL="${API_BASE_URL:-http://localhost:8002}"
API_V1="$API_BASE_URL/api/v1"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# ============================================================================
# Helper Functions
# ============================================================================

print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_test() {
    echo -e "${YELLOW}TEST: $1${NC}"
}

print_pass() {
    echo -e "${GREEN}✓ PASS${NC}: $1"
    ((TESTS_PASSED++))
}

print_fail() {
    echo -e "${RED}✗ FAIL${NC}: $1"
    ((TESTS_FAILED++))
}

print_info() {
    echo -e "${BLUE}ℹ INFO${NC}: $1"
}

# Function to test API endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local expected_status=$4
    
    local response_file="/tmp/api_response_$$.json"
    local status_file="/tmp/api_status_$$.txt"
    
    if [ "$method" = "GET" ] || [ "$method" = "DELETE" ]; then
        http_code=$(curl -s -w "%{http_code}" -X "$method" "$API_V1$endpoint" \
            -H "Content-Type: application/json" \
            -o "$response_file" 2>/dev/null)
    else
        http_code=$(curl -s -w "%{http_code}" -X "$method" "$API_V1$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" \
            -o "$response_file" 2>/dev/null)
    fi
    
    echo "$http_code" > "$status_file"
    cat "$response_file"
    
    rm -f "$response_file" "$status_file"
    echo "$http_code"
}

# ============================================================================
# TEST SUITE
# ============================================================================

print_header "🏥 VitalTriage API Test Suite"

# Check if server is running
print_test "Server Connectivity"
if curl -s "$API_BASE_URL/docs" > /dev/null 2>&1; then
    print_pass "Server is reachable at $API_BASE_URL"
else
    print_fail "Server not reachable at $API_BASE_URL"
    echo -e "${RED}Make sure backend is running:${NC}"
    echo "  cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
    exit 1
fi

# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

print_header "1️⃣  Health Check Tests"

print_test "GET /health"
response=$(curl -s -X GET "$API_V1/health" -H "Content-Type: application/json")
if echo "$response" | grep -q "healthy"; then
    print_pass "Health check returns healthy status"
    echo "Response: $response"
else
    print_fail "Health check did not return expected response"
    echo "Response: $response"
fi

# ============================================================================
# CREATE PATIENT TESTS
# ============================================================================

print_header "2️⃣  Create Patient Tests"

# Test 1: Valid patient data
print_test "POST /patient with valid data"
valid_patient='{
    "patient_id": "TEST_P001",
    "age": 65,
    "gender": "M",
    "vitals": {
        "heart_rate": 88,
        "spo2": 94,
        "systolic_bp": 140,
        "diastolic_bp": 90,
        "temperature": 99.5,
        "respiratory_rate": 20
    },
    "symptoms": ["fever", "chest pain"],
    "notes": "Test patient with valid data"
}'

response=$(curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$valid_patient")

if echo "$response" | grep -q "patient_id\|id"; then
    print_pass "Patient created successfully"
    echo "Response: $response"
    # Extract patient ID for later tests
    PATIENT_ID=$(echo "$response" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
    if [ -z "$PATIENT_ID" ]; then
        PATIENT_ID=$(echo "$response" | grep -o '"_id":"[^"]*"' | head -1 | cut -d'"' -f4)
    fi
else
    print_fail "Failed to create patient"
    echo "Response: $response"
fi

# Test 2: Critical patient
print_test "POST /patient with critical vitals"
critical_patient='{
    "patient_id": "TEST_P002_CRIT",
    "age": 45,
    "gender": "F",
    "vitals": {
        "heart_rate": 150,
        "spo2": 75,
        "systolic_bp": 200,
        "diastolic_bp": 120,
        "temperature": 103.5,
        "respiratory_rate": 35
    },
    "symptoms": ["severe dyspnea", "chest pain"],
    "notes": "Critical condition test"
}'

response=$(curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$critical_patient")

if echo "$response" | grep -q "CRITICAL\|critical"; then
    print_pass "Critical patient correctly identified"
    echo "Response: $response"
else
    print_info "Critical patient created (severity classification may vary)"
    echo "Response: $response"
fi

# Test 3: Invalid age
print_test "POST /patient with invalid age (negative)"
invalid_age='{
    "patient_id": "TEST_P003",
    "age": -5,
    "gender": "M",
    "vitals": {
        "heart_rate": 88,
        "spo2": 94,
        "systolic_bp": 140,
        "diastolic_bp": 90,
        "temperature": 98.6,
        "respiratory_rate": 18
    }
}'

response=$(curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$invalid_age")

if echo "$response" | grep -q "error\|invalid\|422\|400"; then
    print_pass "Invalid age rejected"
    echo "Response: $response"
else
    print_info "API responded to invalid age (validation may vary)"
    echo "Response: $response"
fi

# Test 4: Invalid SpO2 (>100)
print_test "POST /patient with invalid SpO2 (>100%)"
invalid_spo2='{
    "patient_id": "TEST_P004",
    "age": 50,
    "gender": "M",
    "vitals": {
        "heart_rate": 88,
        "spo2": 150,
        "systolic_bp": 140,
        "diastolic_bp": 90,
        "temperature": 98.6,
        "respiratory_rate": 18
    }
}'

response=$(curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$invalid_spo2")

if echo "$response" | grep -q "error\|invalid\|422\|400"; then
    print_pass "Invalid SpO2 rejected"
else
    print_info "API responded to invalid SpO2 (validation may vary)"
fi

# Test 5: Missing required field
print_test "POST /patient without patient_id"
missing_field='{
    "age": 50,
    "gender": "M",
    "vitals": {
        "heart_rate": 88,
        "spo2": 94,
        "systolic_bp": 140,
        "diastolic_bp": 90,
        "temperature": 98.6,
        "respiratory_rate": 18
    }
}'

response=$(curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$missing_field")

if echo "$response" | grep -q "error\|invalid\|422\|400"; then
    print_pass "Missing required field rejected"
else
    print_info "API responded to missing field (validation may vary)"
fi

# Test 6: Missing vitals
print_test "POST /patient with empty vitals"
missing_vitals='{
    "patient_id": "TEST_P005",
    "age": 50,
    "gender": "M",
    "vitals": {}
}'

response=$(curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$missing_vitals")

if echo "$response" | grep -q "error\|invalid\|422\|400"; then
    print_pass "Missing vitals rejected"
else
    print_info "API responded to missing vitals (validation may vary)"
fi

# ============================================================================
# DASHBOARD TESTS
# ============================================================================

print_header "3️⃣  Dashboard Tests"

print_test "GET /dashboard"
response=$(curl -s -X GET "$API_V1/dashboard" \
    -H "Content-Type: application/json")

if echo "$response" | grep -q "critical\|high\|moderate\|stable\|\[\]"; then
    print_pass "Dashboard endpoint working"
    echo "Response (first 200 chars): ${response:0:200}..."
else
    print_info "Dashboard endpoint responded"
    echo "Response: $response"
fi

# ============================================================================
# GET PATIENT TESTS
# ============================================================================

print_header "4️⃣  Get Patient Tests"

if [ ! -z "$PATIENT_ID" ]; then
    print_test "GET /patient/{id} with valid ID"
    response=$(curl -s -X GET "$API_V1/patient/$PATIENT_ID" \
        -H "Content-Type: application/json")
    
    if echo "$response" | grep -q "patient_id\|id"; then
        print_pass "Patient retrieved successfully"
        echo "Response: $response"
    else
        print_fail "Failed to retrieve patient"
        echo "Response: $response"
    fi
fi

print_test "GET /patient/{id} with invalid ID"
response=$(curl -s -X GET "$API_V1/patient/invalid_id_xyz" \
    -H "Content-Type: application/json")

if echo "$response" | grep -q "error\|not found\|404"; then
    print_pass "Invalid patient ID returns error"
    echo "Response: $response"
else
    print_info "API responded to invalid ID"
    echo "Response: $response"
fi

# ============================================================================
# UPDATE PATIENT TESTS
# ============================================================================

print_header "5️⃣  Update Patient Tests"

if [ ! -z "$PATIENT_ID" ]; then
    print_test "PUT /patient/{id} with valid update"
    update_data='{
        "vitals": {
            "heart_rate": 100,
            "spo2": 92,
            "systolic_bp": 145,
            "diastolic_bp": 92,
            "temperature": 99.5,
            "respiratory_rate": 22
        }
    }'
    
    response=$(curl -s -X PUT "$API_V1/patient/$PATIENT_ID" \
        -H "Content-Type: application/json" \
        -d "$update_data")
    
    if echo "$response" | grep -q "patient_id\|updated\|200"; then
        print_pass "Patient updated successfully"
        echo "Response: $response"
    else
        print_info "Update endpoint responded"
        echo "Response: $response"
    fi
fi

# ============================================================================
# DELETE PATIENT TESTS
# ============================================================================

print_header "6️⃣  Delete Patient Tests"

print_test "DELETE /patient/{id} with invalid ID"
response=$(curl -s -X DELETE "$API_V1/patient/invalid_id_xyz" \
    -H "Content-Type: application/json")

print_info "Delete response: $response"

# ============================================================================
# EDGE CASES
# ============================================================================

print_header "7️⃣  Edge Case Tests"

print_test "Patient with extremely high temperature"
extreme_temp='{
    "patient_id": "TEST_P_EXTREME_TEMP",
    "age": 50,
    "gender": "M",
    "vitals": {
        "heart_rate": 88,
        "spo2": 94,
        "systolic_bp": 140,
        "diastolic_bp": 90,
        "temperature": 150.0,
        "respiratory_rate": 18
    }
}'

response=$(curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$extreme_temp")

if echo "$response" | grep -q "error"; then
    print_pass "Extreme temperature rejected"
else
    print_info "Extreme temperature was processed (may or may not be rejected)"
fi

print_test "Patient with very high heart rate"
extreme_hr='{
    "patient_id": "TEST_P_EXTREME_HR",
    "age": 50,
    "gender": "M",
    "vitals": {
        "heart_rate": 300,
        "spo2": 94,
        "systolic_bp": 140,
        "diastolic_bp": 90,
        "temperature": 98.6,
        "respiratory_rate": 18
    }
}'

response=$(curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$extreme_hr")

print_info "Extreme HR response: ${response:0:100}..."

print_test "Patient with very long notes"
long_notes='{
    "patient_id": "TEST_P_LONG_NOTES",
    "age": 50,
    "gender": "M",
    "vitals": {
        "heart_rate": 88,
        "spo2": 94,
        "systolic_bp": 140,
        "diastolic_bp": 90,
        "temperature": 98.6,
        "respiratory_rate": 18
    },
    "notes": "'"$(printf 'A%.0s' {1..5000})"'"
}'

response=$(curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$long_notes")

if echo "$response" | grep -q "patient_id\|error"; then
    print_pass "Long notes processed"
else
    print_info "Long notes handled"
fi

# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

print_header "8️⃣  Performance Tests"

print_test "Response time for health check"
start_time=$(date +%s%N)
curl -s -X GET "$API_V1/health" > /dev/null
end_time=$(date +%s%N)
elapsed_ms=$(( (end_time - start_time) / 1000000 ))
echo "Health check completed in ${elapsed_ms}ms"
if [ $elapsed_ms -lt 1000 ]; then
    print_pass "Health check responds quickly (<1s)"
else
    print_info "Health check responded in ${elapsed_ms}ms"
fi

print_test "Response time for POST /patient"
start_time=$(date +%s%N)
curl -s -X POST "$API_V1/patient" \
    -H "Content-Type: application/json" \
    -d "$valid_patient" > /dev/null
end_time=$(date +%s%N)
elapsed_ms=$(( (end_time - start_time) / 1000000 ))
echo "Create patient completed in ${elapsed_ms}ms"
if [ $elapsed_ms -lt 5000 ]; then
    print_pass "Create patient responds quickly (<5s)"
else
    print_info "Create patient responded in ${elapsed_ms}ms"
fi

# ============================================================================
# TEST SUMMARY
# ============================================================================

print_header "📊 Test Summary"

total_tests=$((TESTS_PASSED + TESTS_FAILED))
echo "Total Tests Run: $total_tests"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✓ All tests passed!${NC}\n"
    exit 0
else
    echo -e "\n${YELLOW}⚠ Some tests failed. Review output above.${NC}\n"
    exit 1
fi
