#!/bin/bash

# SH Parts Production Server Startup Script
# سكريبت تشغيل سيرفر الإنتاج لنظام SH Parts

echo "=========================================="
echo "🚀 Starting SH Parts Production Server"
echo "🚀 بدء تشغيل سيرفر الإنتاج لنظام SH Parts"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo -e "${BLUE}📋 Activating virtual environment...${NC}"
    source .venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
elif [ -d "venv" ]; then
    echo -e "${BLUE}📋 Activating virtual environment...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
else
    echo -e "${YELLOW}⚠️  No virtual environment found, using system Python${NC}"
fi

# Use existing Django settings (not production_settings to preserve database)
export DJANGO_SETTINGS_MODULE=sh_parts.settings
export DEBUG=False
export ALLOWED_HOSTS=*

echo -e "\n${BLUE}📋 Step 1: Checking Python environment...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    exit 1
fi
echo -e "${GREEN}✅ Python found: $(python3 --version)${NC}"

echo -e "\n${BLUE}📋 Step 2: Installing/Updating dependencies...${NC}"
pip install -q gunicorn whitenoise 2>/dev/null || echo "Dependencies already installed"
echo -e "${GREEN}✅ Dependencies ready${NC}"

echo -e "\n${BLUE}📋 Step 3: Collecting static files...${NC}"
python3 manage.py collectstatic --noinput
echo -e "${GREEN}✅ Static files collected${NC}"

echo -e "\n${BLUE}📋 Step 4: Checking database...${NC}"
if [ -f "db.sqlite3" ]; then
    echo -e "${GREEN}✅ Database exists ($(du -h db.sqlite3 | cut -f1)), skipping migrations${NC}"
else
    echo -e "${YELLOW}⚠️  Database not found, running migrations...${NC}"
    python3 manage.py migrate --noinput
    echo -e "${GREEN}✅ Database created${NC}"
fi

echo -e "\n${BLUE}📋 Step 5: Creating media directories...${NC}"
mkdir -p media/qr_codes media/vehicles media/parts media/inventory_items
echo -e "${GREEN}✅ Media directories created${NC}"

echo -e "\n${BLUE}📋 Step 6: Database ready${NC}"
echo -e "${GREEN}✅ Using existing database${NC}"

echo -e "\n${GREEN}=========================================="
echo "✅ Server is ready to start!"
echo "✅ السيرفر جاهز للتشغيل!"
echo "==========================================${NC}"

echo -e "\n${YELLOW}📝 Server Information:${NC}"
echo "   - Host: 0.0.0.0"
echo "   - Port: 8000"
echo "   - Workers: 4"
echo "   - Settings: sh_parts.settings"
echo "   - Database: db.sqlite3 (preserved)"

echo -e "\n${BLUE}🚀 Starting Gunicorn server...${NC}"
echo ""

# Start Gunicorn with existing settings
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --env DJANGO_SETTINGS_MODULE=sh_parts.settings \
    sh_parts.wsgi:application

