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

# Set production settings
export DJANGO_SETTINGS_MODULE=production_settings

echo -e "${BLUE}📋 Step 1: Checking Python environment...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    exit 1
fi
echo -e "${GREEN}✅ Python found: $(python3 --version)${NC}"

echo -e "\n${BLUE}📋 Step 2: Installing/Updating dependencies...${NC}"
pip install -q gunicorn whitenoise 2>/dev/null || echo "Dependencies already installed"
echo -e "${GREEN}✅ Dependencies ready${NC}"

echo -e "\n${BLUE}📋 Step 3: Collecting static files...${NC}"
python3 manage.py collectstatic --noinput --settings=production_settings
echo -e "${GREEN}✅ Static files collected${NC}"

echo -e "\n${BLUE}📋 Step 4: Running database migrations...${NC}"
python3 manage.py migrate --noinput --settings=production_settings
echo -e "${GREEN}✅ Database migrated${NC}"

echo -e "\n${BLUE}📋 Step 5: Creating media directories...${NC}"
mkdir -p media/qr_codes media/vehicles media/parts media/inventory_items
echo -e "${GREEN}✅ Media directories created${NC}"

echo -e "\n${BLUE}📋 Step 6: Checking for superuser...${NC}"
python3 manage.py shell --settings=production_settings << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("Creating default admin user...")
    User.objects.create_superuser('admin@shparts.com', 'admin@shparts.com', 'admin123')
    print("✅ Admin user created: admin@shparts.com / admin123")
else:
    print("✅ Admin user already exists")
EOF

echo -e "\n${GREEN}=========================================="
echo "✅ Server is ready to start!"
echo "✅ السيرفر جاهز للتشغيل!"
echo "==========================================${NC}"

echo -e "\n${YELLOW}📝 Server Information:${NC}"
echo "   - Host: 0.0.0.0"
echo "   - Port: 8000"
echo "   - Workers: 4"
echo "   - Settings: production_settings"

echo -e "\n${BLUE}🚀 Starting Gunicorn server...${NC}"
echo ""

# Start Gunicorn with production settings
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --env DJANGO_SETTINGS_MODULE=production_settings \
    sh_parts.wsgi:application

