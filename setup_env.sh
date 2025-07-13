#!/bin/bash

# Flappy Bird Game - Virtual Environment Setup Script

echo "🎮 Flappy Bird Game - Environment Setup"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "flappy_bird_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv flappy_bird_env
    echo "✅ Virtual environment created!"
else
    echo "✅ Virtual environment already exists!"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source flappy_bird_env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install pygame

echo ""
echo "🎉 Setup complete! Your virtual environment is ready."
echo ""
echo "To activate the environment manually:"
echo "  source flappy_bird_env/bin/activate"
echo ""
echo "To run the game:"
echo "  python run_game.py"
echo ""
echo "To deactivate the environment:"
echo "  deactivate" 