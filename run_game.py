#!/usr/bin/env python3
"""
Flappy Bird Game Launcher
Choose between basic and enhanced versions
"""

import sys
import subprocess
import os

def main():
    print("=" * 50)
    print("🎮 FLAPPY BIRD GAME LAUNCHER 🎮")
    print("=" * 50)
    print()
    print("Choose your game version:")
    print("1. Basic Flappy Bird (Simple graphics)")
    print("2. Enhanced Flappy Bird (Better graphics, particles, effects)")
    print("3. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\n🚀 Launching Basic Flappy Bird...")
                subprocess.run([sys.executable, "flappy_bird.py"])
                break
            elif choice == "2":
                print("\n🚀 Launching Enhanced Flappy Bird...")
                subprocess.run([sys.executable, "flappy_bird_enhanced.py"])
                break
            elif choice == "3":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    main() 