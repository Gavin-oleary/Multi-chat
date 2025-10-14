[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Root = (Get-Location)
)

Write-Host "Scaffolding project structure under '$Root'..." -ForegroundColor Cyan

# Ensure root exists
if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
    throw "Root path '$Root' does not exist or is not a directory."
}

$directories = @(
    "backend",
    "backend/app",
    "backend/app/api",
    "backend/app/api/v1",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/services",
    "backend/app/clients",
    "backend/app/utils",
    "backend/alembic",
    "backend/alembic/versions",
    "backend/tests",
    "backend/tests/test_api",
    "backend/tests/test_services",
    "backend/tests/test_clients",
    "frontend",
    "frontend/public",
    "frontend/src",
    "frontend/src/components",
    "frontend/src/components/Chat",
    "frontend/src/components/Sidebar",
    "frontend/src/components/common",
    "frontend/src/pages",
    "frontend/src/services",
    "frontend/src/store",
    "frontend/src/hooks",
    "frontend/src/utils",
    "frontend/src/styles"
)

$files = @(
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/config.py",
    "backend/app/database.py",
    "backend/app/api/__init__.py",
    "backend/app/api/deps.py",
    "backend/app/api/v1/__init__.py",
    "backend/app/api/v1/router.py",
    "backend/app/api/v1/conversations.py",
    "backend/app/api/v1/messages.py",
    "backend/app/api/v1/chat.py",
    "backend/app/models/__init__.py",
    "backend/app/models/conversation.py",
    "backend/app/models/message.py",
    "backend/app/models/user.py",
    "backend/app/schemas/__init__.py",
    "backend/app/schemas/conversation.py",
    "backend/app/schemas/message.py",
    "backend/app/schemas/chat.py",
    "backend/app/services/__init__.py",
    "backend/app/services/conversation_service.py",
    "backend/app/services/chat_service.py",
    "backend/app/clients/__init__.py",
    "backend/app/clients/base.py",
    "backend/app/clients/claude.py",
    "backend/app/clients/openai.py",
    "backend/app/clients/gemini.py",
    "backend/app/clients/grok.py",
    "backend/app/clients/perplexity.py",
    "backend/app/utils/__init__.py",
    "backend/app/utils/helpers.py",
    "backend/alembic/env.py",
    "backend/tests/__init__.py",
    "backend/tests/conftest.py",
    "backend/.env.example",
    "backend/.env",
    "backend/requirements.txt",
    "backend/alembic.ini",
    "backend/README.md",
    "frontend/public/favicon.ico",
    "frontend/src/main.jsx",
    "frontend/src/App.jsx",
    "frontend/src/components/Chat/ChatInput.jsx",
    "frontend/src/components/Chat/ModelResponse.jsx",
    "frontend/src/components/Chat/ModelGrid.jsx",
    "frontend/src/components/Chat/MessageBubble.jsx",
    "frontend/src/components/Sidebar/ConversationList.jsx",
    "frontend/src/components/Sidebar/ConversationItem.jsx",
    "frontend/src/components/common/Button.jsx",
    "frontend/src/components/common/Loading.jsx",
    "frontend/src/components/common/ErrorBoundary.jsx",
    "frontend/src/pages/ChatPage.jsx",
    "frontend/src/pages/ConversationPage.jsx",
    "frontend/src/services/api.js",
    "frontend/src/store/chatStore.js",
    "frontend/src/store/conversationStore.js",
    "frontend/src/hooks/useChat.js",
    "frontend/src/hooks/useConversations.js",
    "frontend/src/utils/helpers.js",
    "frontend/src/styles/index.css",
    "frontend/.env.example",
    "frontend/.env",
    "frontend/.gitignore",
    "frontend/index.html",
    "frontend/package.json",
    "frontend/vite.config.js",
    "frontend/README.md",
    ".gitignore",
    "docker-compose.yml",
    "README.md",
    "LICENSE"
)

foreach ($dir in $directories) {
    $fullPath = Join-Path -Path $Root -ChildPath $dir
    if (-not (Test-Path -LiteralPath $fullPath -PathType Container)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "Created directory: $dir"
    }
}

foreach ($file in $files) {
    $fullPath = Join-Path -Path $Root -ChildPath $file
    $parent = Split-Path -Path $fullPath -Parent
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
        Write-Host "Created directory (from file list): $(Resolve-Path -Relative $parent)"
    }
    if (-not (Test-Path -LiteralPath $fullPath)) {
        New-Item -ItemType File -Path $fullPath -Force | Out-Null
        Write-Host "Created file: $file"
    }
}

Write-Host "Scaffold complete." -ForegroundColor Green