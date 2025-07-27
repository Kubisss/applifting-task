#!/bin/bash

# Check if Python 3.13 is installed
if ! command -v python3.13 &> /dev/null
then
    echo "Python 3.13 not found. Installing via Homebrew..."
    brew install python@3.13
fi

# Create a virtual environment
echo "Creating venv with Python 3.13..."
python3.13 -m venv venv_py313

echo "Activating the environment..."
source venv_py313/bin/activate

# Install requirements
echo "Installing packages from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Done! Activate the environment with: source venv_py313/bin/activate"
