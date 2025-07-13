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

A Python implementation of the classic Flappy Bird game using Pygame, featuring both basic and enhanced versions with modern graphics and effects.

### 🚀 Quick Start

#### Option 1: Using Virtual Environment (Recommended)
1. **Setup Virtual Environment:**
   ```bash
   ./setup_env.sh
   ```
   
2. **Activate Environment:**
   ```bash
   source flappy_bird_env/bin/activate
   ```

3. **Run the Game:**
   ```bash
   python run_game.py
   ```

#### Option 2: Direct Installation
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Game:**
   ```bash
   python run_game.py
   ```
   
   Or run directly:
   ```bash
   python flappy_bird.py          # Basic version
   python flappy_bird_enhanced.py # Enhanced version
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

### 🛠️ Technical Details

- **Engine:** Pygame 2.5.0+
- **Language:** Python 3.6+
- **Architecture:** Object-oriented design with separate classes for Bird, Pipe, Background, and Game
- **Performance:** 60 FPS gameplay
- **Cross-platform:** Works on Windows, macOS, and Linux

### 📁 Project Structure

```
Games/
├── geometry_cheetah/           # Geometry Cheetah game
│   ├── geometry_cheetah.py     # Main game file
│   ├── run_game.py            # Game launcher
│   ├── setup_env.sh           # Environment setup script
│   ├── requirements.txt       # Dependencies
│   └── README.md              # Game documentation
├── flappy_bird/               # Flappy Bird game
│   ├── flappy_bird.py         # Basic Flappy Bird game
│   ├── flappy_bird_enhanced.py # Enhanced version with effects
│   ├── run_game.py            # Game launcher
│   ├── setup_env.sh           # Environment setup script
│   ├── requirements.txt       # Dependencies
│   └── README.md              # Game documentation
├── requirements.txt           # Main project dependencies
└── README.md                  # This file
```

### 🎮 Controls

| Action | Key |
|--------|-----|
| Flap/Restart | SPACE |
| Quit Game | Close Window |

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
   pip install pygame
   ```

2. **Check Python version:**
   ```bash
   python --version  # Should be 3.6 or higher
   ```

3. **Run with verbose output:**
   ```bash
   python -v flappy_bird.py
   ```

### 🎯 Future Enhancements

Potential features to add:
- Sound effects and background music
- Power-ups and special abilities
- Multiple bird characters
- Level progression with increasing difficulty
- Online leaderboards
- Mobile touch controls

### 📝 License

This project is part of AAAI Labs educational content.

---

**Happy Gaming! 🐦✨**
