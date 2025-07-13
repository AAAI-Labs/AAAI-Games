# AAAI Labs (Antoni & Ariana's AI Labs): Games

## 🎮 Games Collection

### 🏃 Geometry Cheetah Game

A Geometry Dash-style game featuring a bouncing cheetah character! Jump over obstacles, collect points, and try to achieve the highest score possible.

#### 🚀 Quick Start
```bash
cd geometry_cheetah
./setup_env.sh
source geometry_cheetah_env/bin/activate
python run_game.py
```

#### 🎯 How to Play
- **Press SPACE** to make the cheetah jump
- **Avoid obstacles** by timing your jumps perfectly
- **Try to get the highest score possible!**

#### 🎨 Features
- **Bouncing Cheetah Character** with realistic physics
- **Multiple Obstacle Types**: spikes, blocks, and flying spikes
- **Beautiful Graphics**: gradient sky, animated clouds, stars, and particle effects
- **Smooth Animations**: cheetah rotation, trail particles, and parallax backgrounds

---

### 🐦 Flappy Bird Game

A Python implementation of the classic Flappy Bird game using Pygame, featuring multiple versions from basic graphics to enhanced audio experiences.

### 🚀 Quick Start

#### Option 1: Using Virtual Environment (Recommended)
1. **Setup Virtual Environment:**
   ```bash
   ./setup_env.sh
   ```
   
2. **Activate Environment:**
   ```bash
   source flappy_bird_env_py3/bin/activate  # For Python 3 (recommended)
   # or
   source flappy_bird_env/bin/activate      # For Python 2
   ```

3. **Run the Game:**
   ```bash
   python3 run_game.py
   ```

#### Option 2: Direct Installation
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Game:**
   ```bash
   python3 run_game.py
   ```
   
   Or run directly:
   ```bash
   python3 flappy_bird.py              # Basic version
   python3 flappy_bird_enhanced.py     # Enhanced version
   python3 flappy_bird_realistic.py    # Realistic version
   ```

### 🎯 How to Play

- **Press SPACE** to make the bird flap and fly upward
- **Avoid the pipes** by flying through the gaps
- **Don't hit the ground or ceiling**
- **Try to get the highest score possible!**
- **Press SPACE** to restart when game over

### 🎨 Game Features

#### Basic Version (`flappy_bird.py`)
- Simple, clean graphics
- Classic Flappy Bird gameplay
- Score tracking
- Game over screen with restart option

#### Enhanced Version (`flappy_bird_enhanced.py`)
- **Beautiful sky gradient background**
- **Animated clouds** moving across the screen
- **Particle effects** when the bird flaps
- **Bird rotation** based on velocity
- **Enhanced pipe graphics** with caps
- **High score tracking**
- **Semi-transparent game over overlay**
- **Grass texture** on the ground
- **Smooth animations** and visual effects

#### Realistic Version (`flappy_bird_realistic.py`)
- **Realistic bird design** with detailed features (beak, eyes, wings, tail, feet)
- **Animated wing flapping** with feather details
- **Dynamic backgrounds** that change as you progress:
  - 🏙️ **City** (0-9 points): Urban skyline with buildings and lit windows
  - 🌲 **Forest** (10-19 points): Green forest with trees and nature
  - 🏔️ **Mountains** (20-29 points): Mountain ranges with snow caps
  - 🏜️ **Desert** (30-39 points): Sandy desert with dunes and cacti
  - 🚀 **Space** (40+ points): Cosmic space with stars and planets
- **Theme-specific pipes** that match each environment
- **Particle effects** with realistic colors
- **Progressive difficulty** - backgrounds change every 10 points
- **Current theme indicator** on screen

### 🎵 Music Versions

Located in the `flappy bird with music/` folder:

#### Flappy Bird with Song (`flappy_bird_with_song.py`)
- **Classic Flappy Bird melody** playing in the background
- **Dynamic backgrounds** that change as you progress
- **Theme-specific pipe designs**
- **Sound effects** for flapping, scoring, and crashing
- **Theme change sound effects**

#### Flappy Bird with Music (`flappy_bird_with_music.py`)
- **Enhanced audio** with background music
- **Multiple sound effects**
- **Particle effects**
- **Animated backgrounds**

### 🛠️ Technical Details

- **Engine:** Pygame 2.5.0+
- **Language:** Python 3.6+
- **Architecture:** Object-oriented design with separate classes for Bird, Pipe, Background, and Game
- **Performance:** 60 FPS gameplay
- **Cross-platform:** Works on Windows, macOS, and Linux

### 📁 Project Structure

```
Games/
├── flappy_bird.py              # Basic Flappy Bird game
├── flappy_bird_enhanced.py     # Enhanced version with effects
├── flappy_bird_realistic.py    # Realistic version with dynamic backgrounds
├── run_game.py                 # Game launcher (includes music versions)
├── setup_env.sh                # Environment setup script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── flappy bird with music/     # Music versions folder
    ├── flappy_bird_with_song.py    # Classic melody version
    ├── flappy_bird_with_music.py   # Enhanced audio version
    ├── test_audio.py              # Audio testing script
    ├── requirements.txt           # Dependencies
    └── README.md                  # Music versions documentation
```

### 🎮 Controls

| Action | Key |
|--------|-----|
| Flap/Restart | SPACE |
| Quit Game | Q |
| Restart | R |

### 🔧 Customization

You can easily modify game parameters in the constants section of each file:

- `GRAVITY`: How fast the bird falls
- `FLAP_STRENGTH`: How much the bird jumps when flapping
- `PIPE_SPEED`: How fast pipes move
- `PIPE_GAP`: Size of the gap between pipes
- `SCREEN_WIDTH/HEIGHT`: Game window size

### 🐛 Troubleshooting

If you encounter issues:

1. **Make sure Pygame is installed:**
   ```bash
   pip install pygame numpy
   ```

2. **Check Python version:**
   ```bash
   python3 --version  # Should be 3.6 or higher
   ```

3. **For audio issues:**
   ```bash
   cd "flappy bird with music"
   python3 test_audio.py
   ```

4. **Run with verbose output:**
   ```bash
   python3 -v flappy_bird.py
   ```

### 🎯 Future Enhancements

Potential features to add:
- Power-ups and special abilities
- Multiple bird characters
- Level progression with increasing difficulty
- Online leaderboards
- Mobile touch controls
- More music tracks and sound effects

### 📝 License

This project is part of AAAI Labs educational content.

---

**Happy Gaming! 🐦✨🎵**
