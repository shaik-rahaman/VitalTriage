#!/bin/bash

# ============================================================================
# VitalTriage - Complete Test Execution Guide
# ============================================================================
# Run this script to execute all tests for the VitalTriage application
# ============================================================================

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║      🏥 VitalTriage - QA Test Suite Execution                           ║
║                                                                          ║
║      Comprehensive Testing of Backend + Frontend + E2E                  ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Default values
RUN_BACKEND=true
RUN_FRONTEND=true
RUN_MANUAL=false
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-only)
            RUN_FRONTEND=false
            shift
            ;;
        --frontend-only)
            RUN_BACKEND=false
            shift
            ;;
        --manual)
            RUN_MANUAL=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# ============================================================================
# BACKEND TESTS
# ============================================================================

if [ "$RUN_BACKEND" = true ]; then
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🧪 Backend Tests${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
    
    cd "$PROJECT_ROOT/backend"
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
    else
        source .venv/bin/activate
    fi
    
    # Check if pytest is installed
    if ! command -v pytest &> /dev/null; then
        echo -e "${YELLOW}Installing pytest...${NC}"
        pip install pytest pytest-asyncio httpx
    fi
    
    echo -e "${YELLOW}Running Backend Test Suite...${NC}\n"
    
    # Run comprehensive API tests
    echo -e "${BLUE}1. Comprehensive API Tests${NC}"
    if [ "$VERBOSE" = true ]; then
        pytest tests/test_api_comprehensive.py -v --tb=short || true
    else
        pytest tests/test_api_comprehensive.py -v --tb=line || true
    fi
    
    # Run integration tests
    echo -e "\n${BLUE}2. Integration Tests${NC}"
    if [ "$VERBOSE" = true ]; then
        pytest tests/test_integration.py -v --tb=short || true
    else
        pytest tests/test_integration.py -v --tb=line || true
    fi
    
    # Run all tests with coverage
    echo -e "\n${BLUE}3. Test Coverage Report${NC}"
    pytest tests/ --cov=app --cov-report=term-missing --cov-report=html || true
    
    echo -e "\n${GREEN}✅ Backend tests complete!${NC}"
    
    # Deactivate virtual environment
    deactivate
fi

# ============================================================================
# FRONTEND TESTS
# ============================================================================

if [ "$RUN_FRONTEND" = true ]; then
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🧪 Frontend Tests${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
    
    cd "$PROJECT_ROOT/frontend"
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}⚠️  Dependencies not installed. Running npm install...${NC}"
        npm install
    fi
    
    echo -e "${YELLOW}Running Frontend Test Suite...${NC}\n"
    
    # Run tests
    echo -e "${BLUE}1. Component Tests${NC}"
    if [ "$VERBOSE" = true ]; then
        npm test -- --run --reporter=verbose || true
    else
        npm test -- --run || true
    fi
    
    # Run with coverage
    echo -e "\n${BLUE}2. Coverage Report${NC}"
    npm test -- --run --coverage || true
    
    echo -e "\n${GREEN}✅ Frontend tests complete!${NC}"
fi

# ============================================================================
# MANUAL API TESTING (Optional)
# ============================================================================

if [ "$RUN_MANUAL" = true ]; then
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🧪 Manual API Testing${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
    
    cd "$PROJECT_ROOT/backend"
    
    if [ -f "test_api_manual.sh" ]; then
        chmod +x test_api_manual.sh
        ./test_api_manual.sh
    else
        echo -e "${RED}Manual test script not found!${NC}"
    fi
fi

# ============================================================================
# SUMMARY
# ============================================================================

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Test Execution Complete!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${BLUE}📊 Test Reports:${NC}"
echo -e "  Backend Coverage: ${PROJECT_ROOT}/backend/htmlcov/index.html"
echo -e "  Frontend Coverage: ${PROJECT_ROOT}/frontend/coverage/index.html"
echo -e "\n${BLUE}📝 Full QA Report: QA_TEST_REPORT.md${NC}\n"

echo -e "${GREEN}Next Steps:${NC}"
echo -e "  1. Review test results above"
echo -e "  2. Check coverage reports in htmlcov/ and coverage/"
echo -e "  3. Fix any failing tests"
echo -e "  4. Address bugs in QA_TEST_REPORT.md\n"
