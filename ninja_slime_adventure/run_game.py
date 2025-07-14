#!/usr/bin/env python3
"""
Ninja Slime Adventure Game Launcher
Activates virtual environment and runs the game
"""

import os
import sys
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Activate virtual environment and run the game
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(script_dir, 'ninja_slime_env', 'Scripts', 'activate.bat')
        python_exe = os.path.join(script_dir, 'ninja_slime_env', 'Scripts', 'python.exe')
    else:  # Unix/Linux/macOS
        activate_script = os.path.join(script_dir, 'ninja_slime_env', 'bin', 'activate')
        python_exe = os.path.join(script_dir, 'ninja_slime_env', 'bin', 'python3')
    
    # Check if virtual environment exists
    if not os.path.exists(python_exe):
        print("Virtual environment not found. Please run setup_env.sh first.")
        sys.exit(1)
    
    # Run the game
    game_script = os.path.join(script_dir, 'ninja_slime_adventure.py')
    
    try:
        subprocess.run([python_exe, game_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running game: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main() 