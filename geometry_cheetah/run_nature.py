#!/usr/bin/env python3
"""
Geometry Cheetah - Nature Edition Launcher
"""

import os
import sys
import subprocess

def check_pygame():
    """Check if pygame is installed"""
    try:
        import pygame
        print(f"✓ Pygame {pygame.version.ver} is installed")
        return True
    except ImportError:
        print("❌ Pygame is not installed")
        return False

def main():
    print("=" * 70)
    print("🏃 GEOMETRY CHEETAH - NATURE EDITION 🏃")
    print("=" * 70)
    
    # Check pygame
    if not check_pygame():
        print("\nPlease install pygame first:")
        print("pip install pygame")
        return
    
    print("\nStarting Geometry Cheetah Nature Edition...")
    print("Features:")
    print("- Detailed rocks with realistic textures and shading")
    print("- Spiky bushes with animated swaying and thorns")
    print("- Rock clusters with varied rock types")
    print("- Moving rocks with trail effects")
    print("- Massive boulders with cracks and moss")
    print("- Enhanced backgrounds with parallax effects")
    print("- All power-ups and enhanced gameplay")
    print("\nControls:")
    print("- SPACE: Jump / Select / Confirm")
    print("- UP/DOWN arrows: Navigate level select")
    print("- ESC: Return to level select")
    print("- Close window to quit")
    print("=" * 70)
    
    try:
        # Run the game
        game_script = "geometry_cheetah_nature.py"
        if os.path.exists(game_script):
            subprocess.run([sys.executable, game_script])
        else:
            print(f"❌ Error: {game_script} not found")
            print("Please make sure you're in the correct directory")
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running game: {e}")
        print("Please make sure all dependencies are installed correctly")

if __name__ == "__main__":
    main() 