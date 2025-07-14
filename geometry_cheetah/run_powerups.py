#!/usr/bin/env python3
"""
Geometry Cheetah Power-Ups Game Launcher
A Geometry Dash-style game featuring a bouncing cheetah character with exciting power-ups!
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
    print("🏃 GEOMETRY CHEETAH - POWER-UPS EDITION 🏃")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists("geometry_cheetah_powerups.py"):
        print("Error: geometry_cheetah_powerups.py not found in current directory")
        print("Please run this script from the geometry_cheetah directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\nInstalling missing dependencies...")
        if not install_dependencies():
            print("Failed to install dependencies. Please install pygame manually:")
            print("pip install pygame>=2.5.0")
            return
    
    print("\nStarting Geometry Cheetah Power-Ups Edition...")
    print("Features:")
    print("- 6 EXCITING POWER-UPS to collect and use:")
    print("  ♥ Extra Life - Get an additional life")
    print("  ✈ Flying - Fly through the air for 5 seconds")
    print("  ★ Invincibility - Become invincible for 3 seconds")
    print("  ⚡ Double Jump - Jump twice in the air")
    print("  ⏰ Slow Time - Slow down obstacles for 3 seconds")
    print("  🧲 Magnet - Attract power-ups for 4 seconds")
    print("- Multiple lives system (3 lives to start)")
    print("- Power-up spawn throughout levels")
    print("- Beautiful cheetah with enhanced graphics")
    print("- Fun background music and cool sound effects")
    print("- Fixed platform glitches and improved collision detection")
    print("- 5 balanced levels with easier platforms")
    print("- Platform-based gameplay like Geometry Dash")
    print("\nControls:")
    print("- SPACE: Jump / Select / Confirm")
    print("- UP/DOWN arrows: Navigate level select")
    print("- UP/DOWN arrows: Control flying when flying power-up is active")
    print("- ESC: Return to level select")
    print("- Close window to quit")
    print("\n" + "=" * 70)
    
    # Import and run the game
    try:
        from geometry_cheetah_powerups import Game
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        print("Please make sure all dependencies are installed correctly")

if __name__ == "__main__":
    main() 