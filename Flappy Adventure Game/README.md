# Flappy Adventure 🎵

This folder contains the musical versions of the Flappy Adventure game with enhanced audio features.

## Files Included

- **`flappy_bird_with_song.py`** - The main game with the classic Flappy Adventure melody
- **`flappy_bird_with_music.py`** - Enhanced version with background music and sound effects
- **`test_audio.py`** - Audio testing script to verify sound functionality
- **`requirements.txt`** - Python dependencies
- **`README.md`** - This file

## Features

### flappy_bird_with_song.py

- Classic Flappy Adventure gameplay
- The iconic Flappy Adventure melody playing in the background
- Dynamic backgrounds that change as you progress
- Theme-specific pipe designs
- Sound effects for flapping, scoring, and crashing

### flappy_bird_with_music.py

- Enhanced audio with background music
- Multiple sound effects
- Particle effects
- Animated backgrounds

## Setup Instructions

1. **Create a Python 3 virtual environment:**

   ```bash
   python3 -m venv flappy_bird_env_py3
   source flappy_bird_env_py3/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**

   ```bash
   python3 flappy_bird_with_song.py
   ```

## Controls

- **Spacebar** or **Mouse Click** - Make the bird flap
- **R** - Restart the game
- **Q** - Quit the game

## Audio Features

The game includes:

- Background music (classic Flappy Adventure melody)
- Flap sound effects
- Score sound effects
- Crash sound effects
- Theme change sound effects

## Troubleshooting

If you don't hear audio:

1. Check your system volume
2. Run `python3 test_audio.py` to test audio functionality
3. Make sure pygame is properly installed: `pip install pygame`

## Game Progression

As you progress through the game, you'll experience:

- **City Theme** (0-10 points) - Urban skyline background
- **Forest Theme** (10-20 points) - Lush green forest
- **Mountain Theme** (20-30 points) - Snowy mountain peaks
- **Desert Theme** (30-40 points) - Sandy desert landscape
- **Space Theme** (40+ points) - Cosmic space background

Each theme comes with unique pipe designs and background music that adapts to the environment.

Enjoy playing Flappy Adventure! 🎮🎵
