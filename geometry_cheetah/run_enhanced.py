#!/usr/bin/env python3
"""
Geometry Cheetah Enhanced Game Launcher
A Geometry Dash-style game featuring a bouncing cheetah character with multiple levels.
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import pygame
        print(f"✓ Pygame {pygame.version.ver} is installed")
        return True
    except ImportError:
        print("✗ Pygame is not installed")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame>=2.5.0"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def main():
    """Main launcher function."""
    print("=" * 60)
    print("🏃 GEOMETRY CHEETAH - ENHANCED EDITION 🏃")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("geometry_cheetah_enhanced.py"):
        print("Error: geometry_cheetah_enhanced.py not found in current directory")
        print("Please run this script from the geometry_cheetah directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\nInstalling missing dependencies...")
        if not install_dependencies():
            print("Failed to install dependencies. Please install pygame manually:")
            print("pip install pygame>=2.5.0")
            return
    
    print("\nStarting Geometry Cheetah Enhanced...")
    print("Features:")
    print("- 5 unique levels with increasing difficulty")
    print("- Different obstacle types per level")
    print("- Level progression system")
    print("- Score tracking for each level")
    print("\nControls:")
    print("- SPACE: Jump / Select / Confirm")
    print("- UP/DOWN arrows: Navigate level select")
    print("- ESC: Return to level select")
    print("- Close window to quit")
    print("\n" + "=" * 60)
    
    # Import and run the game
    try:
        from geometry_cheetah_enhanced import Game
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        print("Please make sure all dependencies are installed correctly")

if __name__ == "__main__":
    main() 