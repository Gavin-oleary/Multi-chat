@echo off
echo Starting Multi-Model Chat Client...
echo.

REM Check if backend .env exists
if not exist "backend\.env" (
    echo Error: backend\.env not found!
    echo Please copy backend\.env.example to backend\.env and configure your API keys.
    pause
    exit /b 1
)

REM Check if frontend .env exists
if not exist "frontend\.env" (
    echo Warning: frontend\.env not found. Creating from example...
    copy "frontend\.env.example" "frontend\.env"
)

REM Create backend startup script
echo @echo off > backend\start_backend.bat
echo echo Starting backend server... >> backend\start_backend.bat
echo call venv\Scripts\activate >> backend\start_backend.bat
echo pip install -q -r requirements.txt >> backend\start_backend.bat
echo echo Running database initialization... >> backend\start_backend.bat
echo python init_db.py >> backend\start_backend.bat
echo echo Starting FastAPI server... >> backend\start_backend.bat
echo python -m app.main >> backend\start_backend.bat
echo pause >> backend\start_backend.bat

REM Create frontend startup script
echo @echo off > frontend\start_frontend.bat
echo echo Starting frontend server... >> frontend\start_frontend.bat
echo if not exist node_modules ( >> frontend\start_frontend.bat
echo     echo Installing dependencies... >> frontend\start_frontend.bat
echo     npm install >> frontend\start_frontend.bat
echo ) >> frontend\start_frontend.bat
echo echo Starting development server... >> frontend\start_frontend.bat
echo npm run dev >> frontend\start_frontend.bat
echo pause >> frontend\start_frontend.bat

echo Starting Backend in new window...
start "Multi-Model Chat - Backend" cmd /k "cd backend && start_backend.bat"

timeout /t 3 /nobreak > nul

echo Starting Frontend in new window...
start "Multi-Model Chat - Frontend" cmd /k "cd frontend && start_frontend.bat"

echo.
echo Setup complete!
echo Backend API Docs: http://localhost:8000/api/v1/docs
echo Frontend App: http://localhost:5173
echo.
pause