#!/bin/bash

# Kontrola, zda je nainstalovaný Python 3.13
if ! command -v python3.13 &> /dev/null
then
    echo "Python 3.13 nebyl nalezen. Instaluji přes Homebrew..."
    brew install python@3.13
fi

# Vytvoření venv s Pythonem 3.13
echo "Vytvářím venv s Pythonem 3.13..."
python3.13 -m venv venv_py313

# Aktivace prostředí
echo "Aktivuji prostředí..."
source venv_py313/bin/activate

# Vytvoření requirements.txt (pokud neexistuje)
cat > requirements.txt <<EOL
annotated-types==0.7.0
anyio==4.9.0
certifi==2025.7.14
colorama==0.4.6
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
iniconfig==2.1.0
packaging==25.0
pluggy==1.6.0
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
pytest==8.4.1
pytest-asyncio==1.1.0
sniffio==1.3.1
typing-inspection==0.4.1
typing_extensions==4.14.1
EOL

# Instalace balíčků
echo "Instaluji balíčky z requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Hotovo! Aktivuj prostředí příkazem: source venv_py313/bin/activate"
