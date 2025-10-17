#!/bin/bash
# Multi-Model Chat - Easy Setup Script for Mac/Linux
# This script automates the Docker-based setup process

# Colors for output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;90m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================"
echo -e "  Multi-Model Chat - Easy Setup"
echo -e "========================================${NC}"
echo ""

# Check if Docker is installed and running
echo -e "${YELLOW}Checking Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed!${NC}"
    echo -e "${YELLOW}Please install Docker Desktop from: https://www.docker.com/products/docker-desktop${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"

# Check if Docker daemon is running
if ! docker ps &> /dev/null; then
    echo -e "${RED}✗ Docker Desktop is not running!${NC}"
    echo -e "${YELLOW}Please start Docker Desktop and run this script again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file already exists${NC}"
    read -p "Do you want to reconfigure your API keys? (y/N): " overwrite
    if [[ $overwrite == "y" || $overwrite == "Y" ]]; then
        rm .env
        cp env.example .env
        echo -e "${GREEN}✓ Reset .env file from template${NC}"
    else
        echo -e "${YELLOW}Skipping API key configuration...${NC}"
    fi
else
    if [ -f "env.example" ]; then
        cp env.example .env
        echo -e "${GREEN}✓ Created .env file from template${NC}"
    else
        echo -e "${RED}✗ env.example not found!${NC}"
        echo -e "${YELLOW}Please ensure you're in the project root directory.${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${CYAN}========================================"
echo -e "  API Key Configuration"
echo -e "========================================${NC}"
echo ""
echo -e "${WHITE}You'll need API keys for the AI providers you want to use.${NC}"
echo -e "${GREEN}All providers offer FREE tiers!${NC}"
echo ""
echo -e "${WHITE}Get your API keys from:${NC}"
echo -e "${GRAY}  • OpenAI:      https://platform.openai.com/api-keys${NC}"
echo -e "${GRAY}  • Anthropic:   https://console.anthropic.com${NC}"
echo -e "${GRAY}  • Google:      https://makersuite.google.com/app/apikey${NC}"
echo -e "${GRAY}  • Grok:        https://x.ai/api${NC}"
echo -e "${GRAY}  • Perplexity:  https://www.perplexity.ai/settings/api${NC}"
echo ""
echo -e "${CYAN}💡 Tip: You can add more keys later by editing the .env file${NC}"
echo -e "${CYAN}💡 Tip: Press ENTER to skip any provider you don't want to use${NC}"
echo ""

# Function to update .env file
update_env_file() {
    local key=$1
    local value=$2
    
    if [ -n "$value" ]; then
        # Use sed to replace the line (works on both Mac and Linux)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/^${key}=.*$/${key}=${value}/" .env
        else
            # Linux
            sed -i "s/^${key}=.*$/${key}=${value}/" .env
        fi
    fi
}

# Collect API keys
read -p "Would you like to configure API keys now? (Y/n): " configure_keys
if [[ $configure_keys != "n" && $configure_keys != "N" ]]; then
    echo ""
    
    read -p "Enter your OpenAI API key (or press ENTER to skip): " openai_key
    [ -n "$openai_key" ] && update_env_file "OPENAI_API_KEY" "$openai_key"
    
    read -p "Enter your Anthropic API key (or press ENTER to skip): " anthropic_key
    [ -n "$anthropic_key" ] && update_env_file "ANTHROPIC_API_KEY" "$anthropic_key"
    
    read -p "Enter your Google API key (or press ENTER to skip): " google_key
    [ -n "$google_key" ] && update_env_file "GOOGLE_API_KEY" "$google_key"
    
    read -p "Enter your Grok API key (or press ENTER to skip): " grok_key
    [ -n "$grok_key" ] && update_env_file "GROK_API_KEY" "$grok_key"
    
    read -p "Enter your Perplexity API key (or press ENTER to skip): " perplexity_key
    [ -n "$perplexity_key" ] && update_env_file "PERPLEXITY_API_KEY" "$perplexity_key"
    
    echo ""
    echo -e "${GREEN}✓ API keys saved to .env file${NC}"
else
    echo -e "${YELLOW}⚠️  Skipping API key configuration${NC}"
    echo -e "${GRAY}You can add them later by editing the .env file${NC}"
fi

echo ""
echo -e "${CYAN}========================================"
echo -e "  Starting Application"
echo -e "========================================${NC}"
echo ""

# Stop any existing containers
echo -e "${YELLOW}Stopping any existing containers...${NC}"
docker compose down &> /dev/null

# Pull latest images
echo -e "${YELLOW}Pulling Docker images (this may take a few minutes on first run)...${NC}"
docker compose pull

# Build and start containers
echo -e "${YELLOW}Building and starting containers...${NC}"
docker compose up -d --build

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================"
    echo -e "  ✓ Setup Complete!"
    echo -e "========================================${NC}"
    echo ""
    echo -e "${WHITE}Your application is starting up...${NC}"
    echo -e "${GRAY}This may take 30-60 seconds for the first time.${NC}"
    echo ""
    echo -e "${WHITE}Access your application at:${NC}"
    echo -e "${CYAN}  • Frontend:  http://localhost:5173${NC}"
    echo -e "${CYAN}  • Backend:   http://localhost:8000${NC}"
    echo -e "${CYAN}  • API Docs:  http://localhost:8000/api/v1/docs${NC}"
    echo ""
    echo -e "${WHITE}Useful commands:${NC}"
    echo -e "${GRAY}  • View logs:    docker compose logs -f${NC}"
    echo -e "${GRAY}  • Stop app:     docker compose down${NC}"
    echo -e "${GRAY}  • Restart app:  docker compose restart${NC}"
    echo -e "${GRAY}  • Check status: docker compose ps${NC}"
    echo ""
    
    # Wait for services to be ready
    echo -e "${YELLOW}Waiting for services to be ready...${NC}"
    sleep 10
    
    # Check if backend is responding
    max_attempts=12
    attempt=0
    backend_ready=false
    
    while [ $attempt -lt $max_attempts ] && [ "$backend_ready" = false ]; do
        if curl -s -f http://localhost:8000 > /dev/null 2>&1; then
            backend_ready=true
        else
            sleep 5
            attempt=$((attempt + 1))
            echo -e "${GRAY}  Waiting for backend... ($attempt/$max_attempts)${NC}"
        fi
    done
    
    if [ "$backend_ready" = true ]; then
        echo -e "${GREEN}✓ Backend is ready!${NC}"
        echo ""
        
        # Offer to open browser
        read -p "Would you like to open the application in your browser? (Y/n): " open_browser
        if [[ $open_browser != "n" && $open_browser != "N" ]]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open http://localhost:5173 &> /dev/null
            elif command -v open &> /dev/null; then
                open http://localhost:5173
            fi
            echo -e "${GREEN}✓ Opening browser...${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Backend is taking longer than expected to start${NC}"
        echo -e "${GRAY}Check logs with: docker compose logs -f backend${NC}"
    fi
    
    echo ""
    echo -e "${CYAN}Happy chatting! 🚀${NC}"
    echo ""
    
else
    echo ""
    echo -e "${RED}✗ Failed to start containers${NC}"
    echo -e "${YELLOW}Check the error messages above for details.${NC}"
    echo -e "${GRAY}You can also check logs with: docker compose logs${NC}"
    exit 1
fi

