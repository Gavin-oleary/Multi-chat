#!/bin/bash
# ========================================
# Multi-Model Chat - Easy Setup Wizard
# ========================================
# This script automatically sets up the Multi-Model Chat application using Docker

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${CYAN}$1${NC}"
}

print_success() {
    echo -e "  ${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "  ${YELLOW}ℹ${NC} $1"
}

print_error() {
    echo -e "  ${RED}✗${NC} $1"
}

clear
echo -e "${CYAN}================================================${NC}"
echo -e "${CYAN}  Multi-Model Chat - Easy Setup Wizard${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""

# ========================================
# Step 1: Check Docker
# ========================================
print_header "[1/6] Checking Docker..."

if ! command -v docker &> /dev/null; then
    print_error "Docker not found"
    echo ""
    echo -e "  ${YELLOW}Docker is required to run this application.${NC}"
    echo -e "  ${CYAN}Please install Docker from: https://docs.docker.com/get-docker/${NC}"
    echo ""
    
    # OS-specific instructions
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "  ${YELLOW}For macOS:${NC}"
        echo -e "  ${WHITE}brew install --cask docker${NC}"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "  ${YELLOW}For Linux:${NC}"
        echo -e "  ${WHITE}curl -fsSL https://get.docker.com | sh${NC}"
    fi
    
    echo ""
    echo -e "  ${YELLOW}After installing Docker, please run this script again.${NC}"
    exit 1
fi

DOCKER_VERSION=$(docker --version)
print_success "Docker found: $DOCKER_VERSION"

# ========================================
# Step 2: Check Docker is running
# ========================================
print_header "[2/6] Checking Docker service..."

if ! docker ps &> /dev/null; then
    print_error "Docker is not running"
    echo ""
    echo -e "  ${YELLOW}Please start Docker and try again.${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "  ${GRAY}Open Docker Desktop from Applications${NC}"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo -e "  ${GRAY}Try: sudo systemctl start docker${NC}"
    fi
    
    exit 1
fi

print_success "Docker is running"

# ========================================
# Step 3: Check for docker-compose
# ========================================
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    print_error "docker-compose not found"
    echo ""
    echo -e "  ${YELLOW}Please install docker-compose${NC}"
    exit 1
fi

# ========================================
# Step 4: Configure API Keys
# ========================================
print_header "[3/6] Setting up API keys..."

if [ -f ".env" ]; then
    print_info "Found existing .env file"
    read -p "  Do you want to keep your existing configuration? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        rm .env
        print_info "Removed existing .env file"
    else
        print_success "Using existing .env file"
        SKIP_CONFIG=true
    fi
fi

if [ ! -f ".env" ]; then
    echo ""
    echo -e "  ${CYAN}You need API keys from 5 AI providers to use all features.${NC}"
    echo -e "  ${GREEN}Don't worry - all these providers offer FREE API keys!${NC}"
    echo ""
    echo -e "  ${CYAN}Get your FREE API keys from:${NC}"
    echo -e "    1. OpenAI (ChatGPT)   → ${WHITE}https://platform.openai.com/api-keys${NC}"
    echo -e "    2. Anthropic (Claude) → ${WHITE}https://console.anthropic.com/${NC}"
    echo -e "    3. Google (Gemini)    → ${WHITE}https://makersuite.google.com/app/apikey${NC}"
    echo -e "    4. X.AI (Grok)        → ${WHITE}https://x.ai/api${NC}"
    echo -e "    5. Perplexity         → ${WHITE}https://www.perplexity.ai/settings/api${NC}"
    echo ""
    echo -e "  ${GRAY}Tip: Press Enter to skip a key. You can add it later by editing .env${NC}"
    echo ""
    
    read -p "  Enter OpenAI API Key: " OPENAI_KEY
    read -p "  Enter Anthropic API Key: " ANTHROPIC_KEY
    read -p "  Enter Google API Key: " GOOGLE_KEY
    read -p "  Enter Grok API Key (optional): " GROK_KEY
    read -p "  Enter Perplexity API Key (optional): " PERPLEXITY_KEY
    
    # Validate at least one key is provided
    if [ -z "$OPENAI_KEY" ] && [ -z "$ANTHROPIC_KEY" ] && [ -z "$GOOGLE_KEY" ]; then
        print_error "At least one API key (OpenAI, Anthropic, or Google) is required"
        echo ""
        echo -e "  ${YELLOW}Please get at least one API key and run this script again.${NC}"
        exit 1
    fi
    
    # Generate secure random password for database
    DB_PASSWORD=$(openssl rand -base64 24 2>/dev/null || cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 24 | head -n 1)
    
    # Create .env file
    cat > .env << EOF
# ========================================
# Multi-Model Chat - Configuration
# ========================================
# Generated by easy-setup.sh

# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$DB_PASSWORD
POSTGRES_DB=multichat
POSTGRES_PORT=5432

# Redis Configuration
REDIS_PORT=6379

# API Keys
OPENAI_API_KEY=$OPENAI_KEY
ANTHROPIC_API_KEY=$ANTHROPIC_KEY
GOOGLE_API_KEY=$GOOGLE_KEY
GROK_API_KEY=$GROK_KEY
PERPLEXITY_API_KEY=$PERPLEXITY_KEY

# Application Ports
BACKEND_PORT=8000
FRONTEND_PORT=5173

# Frontend Environment
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000

# Application Settings
DEBUG=false
CORS_ORIGINS=["http://localhost:5173"]
EOF
    
    print_success "Configuration saved to .env"
fi

# ========================================
# Step 5: Pull Docker images
# ========================================
print_header "[4/6] Downloading required components..."
print_info "This may take a few minutes on first run..."

if $COMPOSE_CMD pull > /dev/null 2>&1; then
    print_success "Components downloaded"
else
    print_error "Failed to download components"
    exit 1
fi

# ========================================
# Step 6: Start services
# ========================================
print_header "[5/6] Starting Multi-Model Chat..."

if $COMPOSE_CMD up -d > /dev/null 2>&1; then
    print_success "Services started"
else
    print_error "Failed to start services"
    echo ""
    echo -e "  ${YELLOW}Try running: $COMPOSE_CMD up${NC}"
    exit 1
fi

# ========================================
# Step 7: Wait for services to be ready
# ========================================
print_header "[6/6] Waiting for services to initialize..."

MAX_ATTEMPTS=60
ATTEMPT=0
HEALTHY=false

echo -n "  Checking health"

while [ $ATTEMPT -lt $MAX_ATTEMPTS ] && [ "$HEALTHY" = false ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        HEALTHY=true
    else
        echo -n "."
        sleep 2
        ATTEMPT=$((ATTEMPT + 1))
    fi
done

echo ""

if [ "$HEALTHY" = true ]; then
    print_success "All services are ready!"
else
    print_info "Services starting (may take a bit longer)"
    echo -e "  ${GRAY}You can check status with: $COMPOSE_CMD logs -f${NC}"
fi

# ========================================
# Success!
# ========================================
echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  ✓ Multi-Model Chat is Ready!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${CYAN}Access your chat application:${NC}"
echo -e "  🌐 Frontend:  ${WHITE}http://localhost:5173${NC}"
echo -e "  📖 API Docs:  ${WHITE}http://localhost:8000/api/v1/docs${NC}"
echo ""
echo -e "${CYAN}Useful commands:${NC}"
echo -e "  Stop:         ${WHITE}$COMPOSE_CMD down${NC}"
echo -e "  View logs:    ${WHITE}$COMPOSE_CMD logs -f${NC}"
echo -e "  Restart:      ${WHITE}$COMPOSE_CMD restart${NC}"
echo ""

# Open browser (macOS and some Linux systems)
read -p "Open in browser now? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    sleep 2
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "http://localhost:5173"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open "http://localhost:5173"
        fi
    fi
fi

echo ""
echo -e "${CYAN}Happy chatting! 🚀${NC}"
echo ""

