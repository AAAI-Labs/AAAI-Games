#!/bin/bash

# Flappy Bird Game - Virtual Environment Setup Script

echo "🎮 Flappy Bird Game - Environment Setup"
echo "======================================"

# Check if Python 3 virtual environment exists
if [ ! -d "flappy_bird_env_py3" ]; then
    echo "📦 Creating Python 3 virtual environment..."
    python3 -m venv flappy_bird_env_py3
    echo "✅ Python 3 virtual environment created!"
else
    echo "✅ Python 3 virtual environment already exists!"
fi

# Check if Python 2 virtual environment exists
if [ ! -d "flappy_bird_env" ]; then
    echo "📦 Creating Python 2 virtual environment..."
    python3 -m venv flappy_bird_env
    echo "✅ Python 2 virtual environment created!"
else
    echo "✅ Python 2 virtual environment already exists!"
fi

# Activate Python 3 virtual environment and install dependencies
echo "🔧 Activating Python 3 virtual environment..."
source flappy_bird_env_py3/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install pygame numpy

echo ""
echo "🎉 Setup complete! Your virtual environments are ready."
echo ""
echo "To activate the Python 3 environment (recommended for music versions):"
echo "  source flappy_bird_env_py3/bin/activate"
echo ""
echo "To activate the Python 2 environment:"
echo "  source flappy_bird_env/bin/activate"
echo ""
echo "To run the game launcher:"
echo "  python3 run_game.py"
echo ""
echo "To run music versions directly:"
echo "  cd 'flappy bird with music'"
echo "  source ../flappy_bird_env_py3/bin/activate"
echo "  python3 flappy_bird_with_song.py"
echo ""
echo "To deactivate the environment:"
echo "  deactivate" 