#!/bin/bash

# Test Setup Script - اختبار الإعداد
# This script checks if everything is ready for deployment

echo "=========================================="
echo "🔍 Testing SH Parts Setup"
echo "🔍 اختبار إعداد نظام SH Parts"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

# Test 1: Python
echo -e "\n📋 Test 1: Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python3 not found!${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Test 2: Required Python packages
echo -e "\n📋 Test 2: Checking Python packages..."
if pip list | grep -q "Django"; then
    echo -e "${GREEN}✅ Django installed${NC}"
else
    echo -e "${RED}❌ Django not installed${NC}"
    ERRORS=$((ERRORS + 1))
fi

if pip list | grep -q "gunicorn"; then
    echo -e "${GREEN}✅ gunicorn installed${NC}"
else
    echo -e "${RED}❌ gunicorn not installed${NC}"
    ERRORS=$((ERRORS + 1))
fi

if pip list | grep -q "whitenoise"; then
    echo -e "${GREEN}✅ whitenoise installed${NC}"
else
    echo -e "${RED}❌ whitenoise not installed${NC}"
    ERRORS=$((ERRORS + 1))
fi

if pip list | grep -q "djangorestframework"; then
    echo -e "${GREEN}✅ djangorestframework installed${NC}"
else
    echo -e "${RED}❌ djangorestframework not installed${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Test 3: Script files
echo -e "\n📋 Test 3: Checking script files..."
SCRIPTS=("start_production.sh" "start_with_cloudflare.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo -e "${GREEN}✅ $script exists and is executable${NC}"
        else
            echo -e "${YELLOW}⚠️  $script exists but not executable (will be fixed)${NC}"
            chmod +x "$script"
        fi
    else
        echo -e "${RED}❌ $script not found${NC}"
        ERRORS=$((ERRORS + 1))
    fi
done

# Test 4: Settings file
echo -e "\n📋 Test 4: Checking production settings..."
if [ -f "production_settings.py" ]; then
    echo -e "${GREEN}✅ production_settings.py exists${NC}"
else
    echo -e "${RED}❌ production_settings.py not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Test 5: Django project structure
echo -e "\n📋 Test 5: Checking Django project..."
if [ -f "manage.py" ]; then
    echo -e "${GREEN}✅ manage.py found${NC}"
else
    echo -e "${RED}❌ manage.py not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

if [ -d "sh_parts" ]; then
    echo -e "${GREEN}✅ sh_parts directory found${NC}"
else
    echo -e "${RED}❌ sh_parts directory not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Test 6: Internet connection
echo -e "\n📋 Test 6: Checking internet connection..."
if ping -c 1 cloudflare.com &> /dev/null; then
    echo -e "${GREEN}✅ Internet connection OK${NC}"
else
    echo -e "${YELLOW}⚠️  Cannot reach cloudflare.com (check internet)${NC}"
fi

# Test 7: Port 8000 availability
echo -e "\n📋 Test 7: Checking port 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use${NC}"
    echo -e "   Run: ${YELLOW}lsof -ti:8000 | xargs kill -9${NC} to free it"
else
    echo -e "${GREEN}✅ Port 8000 is available${NC}"
fi

# Summary
echo -e "\n=========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo -e "${GREEN}✅ جميع الاختبارات نجحت!${NC}"
    echo -e "\n${GREEN}You can now run:${NC}"
    echo -e "${YELLOW}./start_with_cloudflare.sh${NC}"
else
    echo -e "${RED}❌ $ERRORS test(s) failed${NC}"
    echo -e "${RED}❌ فشل $ERRORS اختبار${NC}"
    echo -e "\n${YELLOW}Please fix the errors above before deploying${NC}"
fi
echo "=========================================="

