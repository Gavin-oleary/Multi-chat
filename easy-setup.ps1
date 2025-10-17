# Multi-Model Chat - Easy Setup Script for Windows
# This script automates the Docker-based setup process

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Multi-Model Chat - Easy Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not found"
    }
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
    
    # Check if Docker daemon is running
    docker ps 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Docker Desktop is not running!" -ForegroundColor Red
        Write-Host "Please start Docker Desktop and run this script again." -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if .env exists
if (Test-Path ".env") {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
    $overwrite = Read-Host "Do you want to reconfigure your API keys? (y/N)"
    if ($overwrite -ne "y" -and $overwrite -ne "Y") {
        Write-Host "Skipping API key configuration..." -ForegroundColor Yellow
    } else {
        Remove-Item ".env"
        Copy-Item "env.example" ".env"
        Write-Host "✓ Reset .env file from template" -ForegroundColor Green
    }
} else {
    if (Test-Path "env.example") {
        Copy-Item "env.example" ".env"
        Write-Host "✓ Created .env file from template" -ForegroundColor Green
    } else {
        Write-Host "✗ env.example not found!" -ForegroundColor Red
        Write-Host "Please ensure you're in the project root directory." -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  API Key Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You'll need API keys for the AI providers you want to use." -ForegroundColor White
Write-Host "All providers offer FREE tiers!" -ForegroundColor Green
Write-Host ""
Write-Host "Get your API keys from:" -ForegroundColor White
Write-Host "  • OpenAI:      https://platform.openai.com/api-keys" -ForegroundColor Gray
Write-Host "  • Anthropic:   https://console.anthropic.com" -ForegroundColor Gray
Write-Host "  • Google:      https://makersuite.google.com/app/apikey" -ForegroundColor Gray
Write-Host "  • Grok:        https://x.ai/api" -ForegroundColor Gray
Write-Host "  • Perplexity:  https://www.perplexity.ai/settings/api" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Tip: You can add more keys later by editing the .env file" -ForegroundColor Cyan
Write-Host "💡 Tip: Press ENTER to skip any provider you don't want to use" -ForegroundColor Cyan
Write-Host ""

# Function to update .env file
function Update-EnvFile {
    param (
        [string]$key,
        [string]$value
    )
    
    if ($value -and $value -ne "") {
        $content = Get-Content ".env" -Raw
        $content = $content -replace "(?m)^$key=.*$", "$key=$value"
        Set-Content ".env" -Value $content -NoNewline
    }
}

# Collect API keys
$configureKeys = Read-Host "Would you like to configure API keys now? (Y/n)"
if ($configureKeys -ne "n" -and $configureKeys -ne "N") {
    Write-Host ""
    
    $openaiKey = Read-Host "Enter your OpenAI API key (or press ENTER to skip)"
    if ($openaiKey) { Update-EnvFile "OPENAI_API_KEY" $openaiKey }
    
    $anthropicKey = Read-Host "Enter your Anthropic API key (or press ENTER to skip)"
    if ($anthropicKey) { Update-EnvFile "ANTHROPIC_API_KEY" $anthropicKey }
    
    $googleKey = Read-Host "Enter your Google API key (or press ENTER to skip)"
    if ($googleKey) { Update-EnvFile "GOOGLE_API_KEY" $googleKey }
    
    $grokKey = Read-Host "Enter your Grok API key (or press ENTER to skip)"
    if ($grokKey) { Update-EnvFile "GROK_API_KEY" $grokKey }
    
    $perplexityKey = Read-Host "Enter your Perplexity API key (or press ENTER to skip)"
    if ($perplexityKey) { Update-EnvFile "PERPLEXITY_API_KEY" $perplexityKey }
    
    Write-Host ""
    Write-Host "✓ API keys saved to .env file" -ForegroundColor Green
} else {
    Write-Host "⚠️  Skipping API key configuration" -ForegroundColor Yellow
    Write-Host "You can add them later by editing the .env file" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Stop any existing containers
Write-Host "Stopping any existing containers..." -ForegroundColor Yellow
docker compose down 2>$null | Out-Null

# Pull latest images
Write-Host "Pulling Docker images (this may take a few minutes on first run)..." -ForegroundColor Yellow
docker compose pull

# Build and start containers
Write-Host "Building and starting containers..." -ForegroundColor Yellow
docker compose up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✓ Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your application is starting up..." -ForegroundColor White
    Write-Host "This may take 30-60 seconds for the first time." -ForegroundColor Gray
    Write-Host ""
    Write-Host "Access your application at:" -ForegroundColor White
    Write-Host "  • Frontend:  http://localhost:5173" -ForegroundColor Cyan
    Write-Host "  • Backend:   http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  • API Docs:  http://localhost:8000/api/v1/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor White
    Write-Host "  • View logs:    docker compose logs -f" -ForegroundColor Gray
    Write-Host "  • Stop app:     docker compose down" -ForegroundColor Gray
    Write-Host "  • Restart app:  docker compose restart" -ForegroundColor Gray
    Write-Host "  • Check status: docker compose ps" -ForegroundColor Gray
    Write-Host ""
    
    # Wait for services to be ready
    Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Check if backend is responding
    $maxAttempts = 12
    $attempt = 0
    $backendReady = $false
    
    while ($attempt -lt $maxAttempts -and -not $backendReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $backendReady = $true
            }
        } catch {
            Start-Sleep -Seconds 5
            $attempt++
            Write-Host "  Waiting for backend... ($attempt/$maxAttempts)" -ForegroundColor Gray
        }
    }
    
    if ($backendReady) {
        Write-Host "✓ Backend is ready!" -ForegroundColor Green
        Write-Host ""
        
        # Offer to open browser
        $openBrowser = Read-Host "Would you like to open the application in your browser? (Y/n)"
        if ($openBrowser -ne "n" -and $openBrowser -ne "N") {
            Start-Process "http://localhost:5173"
            Write-Host "✓ Opening browser..." -ForegroundColor Green
        }
    } else {
        Write-Host "⚠️  Backend is taking longer than expected to start" -ForegroundColor Yellow
        Write-Host "Check logs with: docker compose logs -f backend" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "Happy chatting! 🚀" -ForegroundColor Cyan
    Write-Host ""
    
} else {
    Write-Host ""
    Write-Host "✗ Failed to start containers" -ForegroundColor Red
    Write-Host "Check the error messages above for details." -ForegroundColor Yellow
    Write-Host "You can also check logs with: docker compose logs" -ForegroundColor Gray
    exit 1
}

