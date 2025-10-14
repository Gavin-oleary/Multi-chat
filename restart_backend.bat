@echo off
echo Restarting backend server...
echo.
echo Please close the backend window if it's still open, then press any key to continue...
pause

cd backend
call backendv\Scripts\activate
echo Starting FastAPI server...
python -m app.main
pause
