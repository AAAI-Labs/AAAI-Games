#!/usr/bin/env python3
"""
Geometry Cheetah - Enhanced Background Edition Launcher
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
    print("🏃 GEOMETRY CHEETAH - ENHANCED BACKGROUND EDITION 🏃")
    print("=" * 70)
    
    # Check pygame
    if not check_pygame():
        print("\nPlease install pygame first:")
        print("pip install pygame")
        return
    
    print("\nStarting Geometry Cheetah Enhanced Background Edition...")
    print("Features:")
    print("- Multiple parallax background layers")
    print("- Dynamic aurora effects and lightning")
    print("- Detailed clouds and atmospheric effects")
    print("- Mountain ranges with snow caps")
    print("- Twinkling stars and particle systems")
    print("- Level-specific color themes")
    print("- All power-ups and enhanced gameplay")
    print("\nControls:")
    print("- SPACE: Jump / Select / Confirm")
    print("- UP/DOWN arrows: Navigate level select")
    print("- ESC: Return to level select")
    print("- Close window to quit")
    print("=" * 70)
    
    try:
        # Run the game
        game_script = "geometry_cheetah_background.py"
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