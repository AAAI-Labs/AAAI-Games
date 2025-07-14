#!/usr/bin/env python3
"""
Geometry Cheetah Beautiful Game Launcher
A Geometry Dash-style game featuring a stunningly beautiful cheetah character with enhanced graphics.
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
    print("🏃 GEOMETRY CHEETAH - BEAUTIFUL EDITION 🏃")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists("geometry_cheetah_beautiful.py"):
        print("Error: geometry_cheetah_beautiful.py not found in current directory")
        print("Please run this script from the geometry_cheetah directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\nInstalling missing dependencies...")
        if not install_dependencies():
            print("Failed to install dependencies. Please install pygame manually:")
            print("pip install pygame>=2.5.0")
            return
    
    print("\nStarting Geometry Cheetah Beautiful Edition...")
    print("Features:")
    print("- STUNNING cheetah with realistic details and animations")
    print("- Blinking eyes, wagging tail, and twitching ears")
    print("- Muscle definition and realistic fur patterns")
    print("- Glowing trail particles and visual effects")
    print("- Whiskers, detailed paws, and expressive features")
    print("- Fun background music and cool sound effects")
    print("- Fixed platform glitches and improved collision detection")
    print("- 5 balanced levels with easier platforms")
    print("- Platform-based gameplay like Geometry Dash")
    print("\nControls:")
    print("- SPACE: Jump / Select / Confirm")
    print("- UP/DOWN arrows: Navigate level select")
    print("- ESC: Return to level select")
    print("- Close window to quit")
    print("\n" + "=" * 70)
    
    # Import and run the game
    try:
        from geometry_cheetah_beautiful import Game
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        print("Please make sure all dependencies are installed correctly")

if __name__ == "__main__":
    main() 