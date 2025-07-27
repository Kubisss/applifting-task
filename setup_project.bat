@echo off
setlocal

REM Vytvoření virtuálního prostředí
if not exist ".venv\Scripts\activate.bat" (
    python -m venv .venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Aktivace virtuálního prostředí
call .venv\Scripts\activate.bat

REM Instalace požadavků
pip install --upgrade pip
pip install -r requirements.txt

REM Spuštění main.py ze složky examples
python -m examples.main

endlocal
pause
