#!/usr/bin/env python3
"""
Flappy Bird Game Launcher
Choose between basic, enhanced, realistic, and music versions
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
    print("3. Realistic Flappy Bird (Realistic bird + dynamic backgrounds)")
    print("4. Flappy Bird with Song (Classic melody + dynamic themes)")
    print("5. Flappy Bird with Music (Enhanced audio + effects)")
    print("6. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                print("\n🚀 Launching Basic Flappy Bird...")
                subprocess.run([sys.executable, "flappy_bird.py"])
                break
            elif choice == "2":
                print("\n🚀 Launching Enhanced Flappy Bird...")
                subprocess.run([sys.executable, "flappy_bird_enhanced.py"])
                break
            elif choice == "3":
                print("\n🚀 Launching Realistic Flappy Bird...")
                subprocess.run([sys.executable, "flappy_bird_realistic.py"])
                break
            elif choice == "4":
                print("\n🎵 Launching Flappy Bird with Song...")
                music_path = os.path.join("flappy bird with music", "flappy_bird_with_song.py")
                if os.path.exists(music_path):
                    subprocess.run([sys.executable, music_path])
                else:
                    print("❌ Music version not found. Please check the 'flappy bird with music' folder.")
                break
            elif choice == "5":
                print("\n🎵 Launching Flappy Bird with Music...")
                music_path = os.path.join("flappy bird with music", "flappy_bird_with_music.py")
                if os.path.exists(music_path):
                    subprocess.run([sys.executable, music_path])
                else:
                    print("❌ Music version not found. Please check the 'flappy bird with music' folder.")
                break
            elif choice == "6":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    main() 