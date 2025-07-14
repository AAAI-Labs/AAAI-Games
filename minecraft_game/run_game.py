#!/usr/bin/env python3
"""
Minecraft 2D Game Launcher
Checks dependencies and launches the game
"""

import sys
import importlib


def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = ['pygame', 'numpy', 'noise']
    missing_packages = []

    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")

    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False

    return True


def main():
    print("Minecraft 2D Game Launcher")
    print("=" * 30)

    if not check_dependencies():
        sys.exit(1)

    print("\nStarting Minecraft 2D...")
    print("Press Ctrl+C to exit")

    try:
        # Import and run the game
        from minecraft_2d import Game
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame closed by user")
    except Exception as e:
        print(f"Error running game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()