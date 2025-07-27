@echo off
setlocal

REM create a virtual environment if it doesn't exist
if not exist ".venv\Scripts\activate.bat" (
    python -m venv .venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activating the virtual environment
call .venv\Scripts\activate.bat

REM Installing requirements
pip install --upgrade pip
pip install -r requirements.txt

REM Running main.py from examples folder
python -m examples.main

endlocal
pause
