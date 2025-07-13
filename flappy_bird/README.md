# Flappy Bird Enhanced

A Python implementation of Flappy Bird using Pygame with enhanced graphics and features.

## Features

- Smooth bird animation with rotation
- Particle effects when flapping
- Animated background with moving clouds
- Score tracking with high score memory
- Beautiful graphics and smooth gameplay

## Setup

### Option 1: Quick Setup (Recommended)
```bash
chmod +x setup_env.sh
./setup_env.sh
```

### Option 2: Manual Setup
1. **Activate the virtual environment:**
   ```bash
   source flappy_bird_env/bin/activate
   ```

2. **Install dependencies (if needed):**
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

### Option 1: Use the Game Launcher (Recommended)
```bash
python3 run_game.py
```
Then choose:
- **1** for Basic Flappy Bird
- **2** for Enhanced Flappy Bird (recommended)

### Option 2: Run Directly
```bash
python3 flappy_bird_enhanced.py
```

2. **Controls:**
   - Press **SPACE** to flap and fly upward
   - Navigate through the green pipes
   - Avoid hitting pipes, ground, or ceiling
   - Press **SPACE** to restart when game over

## Files

- `flappy_bird_enhanced.py` - Main game file with enhanced features
- `flappy_bird.py` - Original basic version
- `run_game.py` - Game launcher (choose between versions)
- `setup_env.sh` - Automated environment setup script
- `requirements.txt` - Python dependencies
- `flappy_bird_env/` - Virtual environment with pygame installed 