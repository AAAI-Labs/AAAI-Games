#!/usr/bin/env python3
"""
Geometry Cheetah Improved Game Launcher
A Geometry Dash-style game featuring a bouncing cheetah character with easier platforms and better graphics.
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
    print("=" * 70)
    print("🏃 GEOMETRY CHEETAH - IMPROVED EDITION 🏃")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists("geometry_cheetah_improved.py"):
        print("Error: geometry_cheetah_improved.py not found in current directory")
        print("Please run this script from the geometry_cheetah directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\nInstalling missing dependencies...")
        if not install_dependencies():
            print("Failed to install dependencies. Please install pygame manually:")
            print("pip install pygame>=2.5.0")
            return
    
    print("\nStarting Geometry Cheetah Improved...")
    print("Features:")
    print("- 5 balanced levels with easier platforms")
    print("- 6 platform types designed for easier jumping")
    print("- Much better-looking cheetah character")
    print("- Larger collision boxes for easier platform landing")
    print("- Slower moving platforms and longer disappearing timers")
    print("- Platform-based gameplay like Geometry Dash")
    print("\nControls:")
    print("- SPACE: Jump / Select / Confirm")
    print("- UP/DOWN arrows: Navigate level select")
    print("- ESC: Return to level select")
    print("- Close window to quit")
    print("\n" + "=" * 70)
    
    # Import and run the game
    try:
        from geometry_cheetah_improved import Game
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        print("Please make sure all dependencies are installed correctly")

if __name__ == "__main__":
    main() 