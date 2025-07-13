#!/usr/bin/env python3
"""
Simple audio test for Flappy Bird
"""

import pygame
import numpy as np
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

print("🎵 Testing Audio System...")
print("=" * 30)

# Test 1: Check if mixer is working
try:
    pygame.mixer.get_init()
    print("✅ Pygame mixer initialized successfully")
except Exception as e:
    print(f"❌ Mixer initialization failed: {e}")

# Test 2: Create a simple beep sound
try:
    sample_rate = 44100
    duration = 0.5  # 0.5 seconds
    samples = int(sample_rate * duration)
    
    # Create a simple beep
    t = np.linspace(0, duration, samples)
    frequency = 440  # A4 note
    wave = np.sin(2 * np.pi * frequency * t) * 0.5
    wave = (wave * 32767).astype(np.int16)
    
    # Convert to stereo (2 channels)
    stereo_wave = np.column_stack((wave, wave))
    sound = pygame.sndarray.make_sound(stereo_wave)
    print("✅ Test sound created successfully")
    
    # Play the sound
    print("🔊 Playing test sound...")
    sound.play()
    time.sleep(1)  # Wait for sound to finish
    print("✅ Test sound played successfully")
    
except Exception as e:
    print(f"❌ Sound creation/playback failed: {e}")

# Test 3: Check system volume
try:
    # Try to get system volume info
    print("📊 Audio system info:")
    print(f"   - Sample rate: {pygame.mixer.get_init()[0]}")
    print(f"   - Format: {pygame.mixer.get_init()[1]}")
    print(f"   - Channels: {pygame.mixer.get_init()[2]}")
except Exception as e:
    print(f"❌ Could not get audio info: {e}")

print("\n🎮 If you heard a beep sound, audio is working!")
print("If you didn't hear anything, check your system volume and audio settings.")
print("\nPress Enter to continue...")
input()

pygame.quit() 