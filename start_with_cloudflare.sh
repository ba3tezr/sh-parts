#!/bin/bash

# SH Parts - Cloudflare Tunnel Deployment Script
# سكريبت نشر نظام SH Parts مع Cloudflare Tunnel

echo "=========================================="
echo "☁️  SH Parts + Cloudflare Tunnel"
echo "☁️  نظام SH Parts مع Cloudflare Tunnel"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

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
    echo -e "${YELLOW}⚠️  No virtual environment found${NC}"
fi

# Check if cloudflared is installed
echo -e "${BLUE}📋 Checking for cloudflared...${NC}"
if ! command -v cloudflared &> /dev/null; then
    echo -e "${YELLOW}⚠️  cloudflared not found. Installing...${NC}"
    
    # Detect OS and install
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Installing for Linux..."
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i cloudflared-linux-amd64.deb
        rm cloudflared-linux-amd64.deb
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing for macOS..."
        brew install cloudflared
    else
        echo -e "${RED}❌ Unsupported OS. Please install cloudflared manually from:${NC}"
        echo "   https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
        exit 1
    fi
fi

echo -e "${GREEN}✅ cloudflared is installed: $(cloudflared --version)${NC}"

# Create a temporary directory for logs
mkdir -p logs

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down...${NC}"
    kill $DJANGO_PID 2>/dev/null
    kill $TUNNEL_PID 2>/dev/null
    echo -e "${GREEN}✅ Cleanup complete${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

echo -e "\n${BLUE}=========================================="
echo "🚀 Starting Django Production Server"
echo "🚀 بدء تشغيل سيرفر Django"
echo "==========================================${NC}"

# Make start script executable
chmod +x start_production.sh

# Start Django server in background
./start_production.sh > logs/django.log 2>&1 &
DJANGO_PID=$!

echo -e "${GREEN}✅ Django server started (PID: $DJANGO_PID)${NC}"
echo -e "${BLUE}⏳ Waiting for Django to be ready...${NC}"

# Wait for Django to start
sleep 5

# Check if Django is running
if ! kill -0 $DJANGO_PID 2>/dev/null; then
    echo -e "${RED}❌ Django server failed to start. Check logs/django.log${NC}"
    cat logs/django.log
    exit 1
fi

# Test if Django is responding
for i in {1..10}; do
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Django server is responding!${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ Django server not responding after 10 attempts${NC}"
        kill $DJANGO_PID
        exit 1
    fi
    echo -e "${YELLOW}⏳ Attempt $i/10...${NC}"
    sleep 2
done

echo -e "\n${BLUE}=========================================="
echo "☁️  Starting Cloudflare Tunnel"
echo "☁️  بدء تشغيل Cloudflare Tunnel"
echo "==========================================${NC}"

echo -e "${YELLOW}"
echo "📝 Note: This will create a temporary tunnel."
echo "📝 ملاحظة: سيتم إنشاء نفق مؤقت."
echo "📝 The URL will change each time you restart."
echo "📝 الرابط سيتغير في كل مرة تعيد التشغيل."
echo -e "${NC}"

# Start Cloudflare tunnel
cloudflared tunnel --url http://localhost:8000 > logs/cloudflare.log 2>&1 &
TUNNEL_PID=$!

echo -e "${GREEN}✅ Cloudflare tunnel started (PID: $TUNNEL_PID)${NC}"
echo -e "${BLUE}⏳ Waiting for tunnel URL...${NC}"

# Wait for tunnel URL to appear in logs
sleep 3

# Extract and display the URL
for i in {1..15}; do
    if [ -f logs/cloudflare.log ]; then
        TUNNEL_URL=$(grep -oP 'https://[a-zA-Z0-9-]+\.trycloudflare\.com' logs/cloudflare.log | head -1)
        if [ ! -z "$TUNNEL_URL" ]; then
            echo -e "\n${GREEN}=========================================="
            echo "✅ SUCCESS! Your app is now live!"
            echo "✅ نجح! تطبيقك الآن على الإنترنت!"
            echo "==========================================${NC}"
            echo -e "\n${BLUE}🌐 Public URL / الرابط العام:${NC}"
            echo -e "${GREEN}   $TUNNEL_URL${NC}"
            echo -e "\n${BLUE}👤 Admin Login / تسجيل دخول المدير:${NC}"
            echo -e "   URL: ${GREEN}$TUNNEL_URL/admin/${NC}"
            echo -e "   Email: ${YELLOW}admin@shparts.com${NC}"
            echo -e "   Password: ${YELLOW}admin123${NC}"
            echo -e "\n${BLUE}📊 Dashboard / لوحة التحكم:${NC}"
            echo -e "   ${GREEN}$TUNNEL_URL/dashboard/${NC}"
            echo -e "\n${BLUE}🔧 API Endpoints:${NC}"
            echo -e "   ${GREEN}$TUNNEL_URL/api/${NC}"
            echo -e "\n${YELLOW}=========================================="
            echo "📝 Logs are being saved to:"
            echo "   - Django: logs/django.log"
            echo "   - Cloudflare: logs/cloudflare.log"
            echo "=========================================="
            echo "⚠️  Press Ctrl+C to stop the server"
            echo "⚠️  اضغط Ctrl+C لإيقاف السيرفر"
            echo "==========================================${NC}"
            break
        fi
    fi
    if [ $i -eq 15 ]; then
        echo -e "${RED}❌ Could not get tunnel URL. Check logs/cloudflare.log${NC}"
        cat logs/cloudflare.log
        cleanup
        exit 1
    fi
    echo -e "${YELLOW}⏳ Waiting for URL... ($i/15)${NC}"
    sleep 2
done

# Keep script running and show live logs
echo -e "\n${BLUE}📊 Live Logs (Ctrl+C to stop):${NC}\n"
tail -f logs/django.log logs/cloudflare.log &
TAIL_PID=$!

# Wait for user to stop
wait $TUNNEL_PID

