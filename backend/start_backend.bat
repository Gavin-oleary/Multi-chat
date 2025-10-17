@echo off 
echo Starting backend server... 
call venv\Scripts\activate 
pip install -q -r requirements.txt 
echo Starting FastAPI server... 
python -m uvicorn app.main:app --reload
pause 
