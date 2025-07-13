#!/bin/bash

# Geometry Cheetah Environment Setup Script

echo "🏃 Setting up Geometry Cheetah environment..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv geometry_cheetah_env

# Activate virtual environment
echo "Activating virtual environment..."
source geometry_cheetah_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "✅ Environment setup complete!"
echo ""
echo "To run the game:"
echo "1. Activate the environment: source geometry_cheetah_env/bin/activate"
echo "2. Run the game: python run_game.py"
echo ""
echo "Or use the quick launcher: ./run_game.py" 