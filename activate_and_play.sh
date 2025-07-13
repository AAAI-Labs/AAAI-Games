#!/bin/bash

# Flappy Bird Game - Activate and Play Script

echo "🎮 Activating Flappy Bird Environment..."
echo "======================================"

# Navigate to the game directory
cd /Users/antoniluong/AAAI/Games

# Activate the virtual environment
source flappy_bird_env_py3/bin/activate

echo "✅ Virtual environment activated!"
echo "🐍 Python version: $(python3 --version)"
echo "🎵 Starting Flappy Bird with Music..."
echo ""

# Run the game
python3 flappy_bird_with_music.py 