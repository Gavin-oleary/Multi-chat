@echo off
echo ============================================
echo Database Setup Script (FIRST TIME ONLY!)
echo ============================================
echo.
echo WARNING: This will DROP all existing data!
echo Only run this for initial setup or to reset the database.
echo.
set /p confirm="Type 'YES' to continue or anything else to cancel: "

if not "%confirm%"=="YES" (
    echo.
    echo Cancelled. No changes made.
    pause
    exit /b 0
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Dropping and recreating database tables...
python -c "import asyncio; from app.database import Base, engine; asyncio.run((lambda: engine.begin()).__call__()).__aenter__().run_sync(Base.metadata.drop_all)"

echo.
echo Running database initialization...
python init_db.py

echo.
echo ============================================
echo Database setup complete!
echo ============================================
echo.
echo You can now start the backend with:
echo   start_backend.bat
echo.
pause

