#!/bin/bash

# Ninja Slime Adventure Environment Setup Script

echo "Setting up Ninja Slime Adventure environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "ninja_slime_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ninja_slime_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source ninja_slime_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "Environment setup complete!"
echo ""
echo "To run the game:"
echo "  source ninja_slime_env/bin/activate && python3 ninja_slime_adventure.py"
echo "  or"
echo "  python3 run_game.py" 