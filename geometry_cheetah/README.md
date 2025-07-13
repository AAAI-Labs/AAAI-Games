# 🏃 Geometry Cheetah

A Geometry Dash-style game featuring a bouncing cheetah character! Jump over obstacles, collect points, and try to achieve the highest score possible.

## 🎮 Game Features

- **Bouncing Cheetah Character**: Control a cute animated cheetah with realistic physics
- **Multiple Obstacle Types**: Spikes, blocks, and flying spikes to avoid
- **Beautiful Graphics**: Gradient sky, animated clouds, stars, and particle effects
- **Smooth Animations**: Cheetah rotation, trail particles, and parallax backgrounds
- **Score System**: Track your score and compete for high scores
- **Modern UI**: Clean menus and game over screens

## 🚀 Quick Start

### Option 1: Using Virtual Environment (Recommended)
1. **Setup Virtual Environment:**
   ```bash
   ./setup_env.sh
   ```
   
2. **Activate Environment:**
   ```bash
   source geometry_cheetah_env/bin/activate
   ```

3. **Run the Game:**
   ```bash
   python run_game.py
   ```

### Option 2: Using the Launcher
```bash
python run_game.py
```

### Option 3: Direct Run
```bash
python geometry_cheetah.py
```

### Option 4: Manual Installation
```bash
pip install -r requirements.txt
python geometry_cheetah.py
```

## 🎯 How to Play

- **Press SPACE** to make the cheetah jump
- **Avoid obstacles** by timing your jumps perfectly
- **Don't hit the ground or ceiling**
- **Try to get the highest score possible!**
- **Press SPACE** to restart when game over

## 🎨 Game Elements

### Cheetah Character
- **Realistic Physics**: Gravity affects the cheetah's movement
- **Dynamic Rotation**: The cheetah tilts based on its velocity
- **Trail Particles**: Orange particles follow the cheetah when jumping
- **Animated Design**: Detailed cheetah with spots, ears, and tail

### Obstacles
- **Ground Spikes**: Triangular spikes on the ground
- **Blocks**: Rectangular obstacles to jump over
- **Flying Spikes**: Spikes suspended in the air

### Environment
- **Gradient Sky**: Beautiful blue gradient background
- **Animated Clouds**: White clouds that move across the screen
- **Twinkling Stars**: Stars that twinkle in the night sky
- **Grass Ground**: Green ground with grass texture

## 🛠️ Technical Details

- **Engine**: Pygame 2.5.0+
- **Language**: Python 3.6+
- **Architecture**: Object-oriented design with separate classes
- **Performance**: 60 FPS smooth gameplay
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🎮 Controls

| Action | Key |
|--------|-----|
| Jump/Restart | SPACE |
| Quit Game | Close Window |

## 🔧 Customization

You can easily modify game parameters in the constants section:

- `GRAVITY`: How fast the cheetah falls
- `JUMP_FORCE`: How high the cheetah jumps
- `OBSTACLE_SPEED`: How fast obstacles move
- `OBSTACLE_SPAWN_RATE`: How often obstacles appear
- `SCREEN_WIDTH/HEIGHT`: Game window size

## 🐛 Troubleshooting

If you encounter issues:

1. **Make sure Pygame is installed:**
   ```bash
   pip install pygame>=2.5.0
   ```

2. **Check Python version:**
   ```bash
   python --version  # Should be 3.6 or higher
   ```

3. **Run with verbose output:**
   ```bash
   python -v geometry_cheetah.py
   ```

## 🎯 Future Enhancements

Potential features to add:
- Sound effects and background music
- Power-ups and special abilities
- Multiple cheetah skins
- Level progression with increasing difficulty
- Online leaderboards
- Mobile touch controls
- More obstacle types and patterns

## 📝 License

This project is part of AAAI Labs educational content.

---

**Happy Gaming! 🏃✨** 