# Minecraft 2D Game

A 2D Minecraft-inspired game built with Python and Pygame featuring procedural terrain generation, block placement/breaking, inventory system, and survival mechanics.

## Features

### Core Gameplay

- **Procedural Terrain Generation**: Uses Perlin noise to create realistic, varied landscapes
- **Block System**: 12 different block types including ores, trees, and natural resources
- **Building & Mining**: Break blocks with left-click, place blocks with right-click
- **Inventory System**: Collect and manage different block types
- **Survival Mechanics**: Health and hunger systems

### Block Types

- **Natural Blocks**: Grass, Dirt, Stone, Sand, Water
- **Ores**: Coal, Iron, Gold, Diamond (with different hardness levels)
- **Vegetation**: Wood, Leaves
- **Special**: Water (unbreakable)

### World Generation

- **Procedural Height Map**: Creates realistic terrain variations
- **Ore Distribution**: Different ores spawn at different depths
- **Tree Generation**: Randomly placed trees with trunks and leaves
- **Layered Terrain**: Grass on top, dirt below, stone and ores deeper

### Player Features

- **Movement**: Smooth horizontal movement with jumping
- **Physics**: Gravity and collision detection
- **Health System**: 100 health points with visual health bar
- **Hunger System**: Gradually decreases over time
- **Inventory Management**: Select different blocks for placement

## Controls

### Movement

- **WASD** or **Arrow Keys**: Move left/right
- **Space** or **W/Up**: Jump
- **ESC**: Pause/Resume game

### Block Interaction

- **Left Mouse Button**: Break blocks
- **Right Mouse Button**: Place blocks
- **1-5 Keys**: Select block type for placement
  - **1**: Dirt
  - **2**: Stone
  - **3**: Wood
  - **4**: Leaves
  - **5**: Sand

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the game files**
2. **Navigate to the game directory**:

   ```bash
   cd minecraft_game
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game**:

   ```bash
   python minecraft_2d.py
   ```

## Game Mechanics

### Block Breaking

- Different blocks have different "health" values
- Stone and ores require multiple hits to break
- Breaking blocks adds them to your inventory

### Block Placement

- Select a block type using number keys (1-5)
- Right-click to place blocks in empty spaces
- Blocks are consumed from inventory when placed

### Survival Elements

- **Health**: Starts at 100, can be lost from various actions
- **Hunger**: Gradually decreases, affects gameplay
- **Inventory Management**: Limited space for collected blocks

### World Exploration

- **Horizontal Scrolling**: Camera follows player movement
- **Procedural Generation**: Each world is unique
- **Resource Distribution**: Ores are more common deeper underground

## Technical Details

### Performance

- **Optimized Rendering**: Only renders visible blocks
- **Efficient Collision Detection**: Tile-based collision system
- **Smooth 60 FPS**: Optimized game loop

### World Size

- **Width**: 100 tiles (3,200 pixels)
- **Height**: 50 tiles (1,600 pixels)
- **Tile Size**: 32x32 pixels

### File Structure

```
minecraft_game/
├── minecraft_2d.py      # Main game file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Future Enhancements

Potential features for future versions:

- **Crafting System**: Combine blocks to create tools and items
- **Enemies**: Hostile mobs and combat system
- **Day/Night Cycle**: Dynamic lighting and time system
- **Save/Load System**: Persist world changes
- **Multiplayer**: Network play with other players
- **More Block Types**: Additional materials and decorative blocks
- **Sound Effects**: Audio feedback for actions
- **Particle Effects**: Visual feedback for breaking/placing blocks

## Troubleshooting

### Common Issues

**Game won't start:**

- Ensure Python 3.7+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify pygame is working: `python -c "import pygame; print('Pygame OK')"`

**Performance issues:**

- Close other applications to free up system resources
- Reduce screen resolution if needed
- Ensure graphics drivers are up to date

**Controls not responding:**

- Make sure the game window is focused
- Check that your keyboard/mouse are working properly
- Try pressing ESC to unpause if the game appears frozen

## Credits

- **Engine**: Pygame
- **Noise Generation**: noise library (Perlin noise)
- **Graphics**: Custom pixel art and colors
- **Game Design**: Inspired by Minecraft

## License

This project is open source and available under the MIT License.
