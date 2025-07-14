import pygame
import random
import sys
import math
import os
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Set up audio system
pygame.mixer.set_reserved(4)
pygame.mixer.music.set_volume(0.7)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.6
FLAP_STRENGTH = -12
PIPE_SPEED = 4
PIPE_GAP = 220
PIPE_WIDTH = 80
BIRD_SIZE = 35

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
DARK_GREEN = (0, 100, 0)
DARK_BLUE = (25, 25, 112)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (211, 211, 211)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Adventure")
clock = pygame.time.Clock()

def create_note(frequency, duration, sample_rate=44100):
    """Create a single musical note"""
    try:
        import numpy as np
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)
        wave = np.sin(2 * np.pi * frequency * t) * 0.3
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        return stereo_wave
    except:
        return None

def create_theme_song(theme):
    """Create theme-specific music"""
    try:
        import numpy as np

        # Musical notes (frequencies in Hz)
        notes = {
            'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
            'G3': 196.00, 'A3': 220.00, 'B3': 246.94, 'C4': 261.63,
            'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00,
            'A4': 440.00, 'B4': 493.88, 'C5': 523.25, 'D5': 587.33,
            'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00
        }

        # Theme-specific melodies
        theme_melodies = {
            'city': [
                ('C4', 0.3), ('E4', 0.3), ('G4', 0.3), ('C5', 0.3),
                ('G4', 0.3), ('E4', 0.3), ('C4', 0.3), ('G4', 0.3),
                ('A4', 0.3), ('C5', 0.3), ('E5', 0.3), ('A4', 0.3),
                ('G4', 0.3), ('E4', 0.3), ('C4', 0.3), ('G4', 0.3)
            ],
            'forest': [
                ('D4', 0.4), ('F4', 0.4), ('A4', 0.4), ('D5', 0.4),
                ('A4', 0.4), ('F4', 0.4), ('D4', 0.4), ('A4', 0.4),
                ('G4', 0.4), ('B4', 0.4), ('D5', 0.4), ('G4', 0.4),
                ('F4', 0.4), ('D4', 0.4), ('A4', 0.4), ('F4', 0.4)
            ],
            'mountains': [
                ('E4', 0.5), ('G4', 0.5), ('B4', 0.5), ('E5', 0.5),
                ('B4', 0.5), ('G4', 0.5), ('E4', 0.5), ('B4', 0.5),
                ('A4', 0.5), ('C5', 0.5), ('E5', 0.5), ('A4', 0.5),
                ('G4', 0.5), ('E4', 0.5), ('B4', 0.5), ('G4', 0.5)
            ],
            'desert': [
                ('F4', 0.6), ('A4', 0.6), ('C5', 0.6), ('F5', 0.6),
                ('C5', 0.6), ('A4', 0.6), ('F4', 0.6), ('C5', 0.6),
                ('B4', 0.6), ('D5', 0.6), ('F5', 0.6), ('B4', 0.6),
                ('A4', 0.6), ('F4', 0.6), ('C5', 0.6), ('A4', 0.6)
            ],
            'space': [
                ('G4', 0.7), ('B4', 0.7), ('D5', 0.7), ('G5', 0.7),
                ('D5', 0.7), ('B4', 0.7), ('G4', 0.7), ('D5', 0.7),
                ('C5', 0.7), ('E5', 0.7), ('G5', 0.7), ('C5', 0.7),
                ('B4', 0.7), ('G4', 0.7), ('D5', 0.7), ('B4', 0.7)
            ],
            'ocean': [
                ('A4', 0.4), ('C5', 0.4), ('E5', 0.4), ('A5', 0.4),
                ('E5', 0.4), ('C5', 0.4), ('A4', 0.4), ('E5', 0.4),
                ('D5', 0.4), ('F5', 0.4), ('A5', 0.4), ('D5', 0.4),
                ('C5', 0.4), ('A4', 0.4), ('E5', 0.4), ('C5', 0.4)
            ],
            'sunset': [
                ('B4', 0.5), ('D5', 0.5), ('F5', 0.5), ('B5', 0.5),
                ('F5', 0.5), ('D5', 0.5), ('B4', 0.5), ('F5', 0.5),
                ('E5', 0.5), ('G5', 0.5), ('B5', 0.5), ('E5', 0.5),
                ('D5', 0.5), ('B4', 0.5), ('F5', 0.5), ('D5', 0.5)
            ],
            'winter': [
                ('C5', 0.6), ('E5', 0.6), ('G5', 0.6), ('C6', 0.6),
                ('G5', 0.6), ('E5', 0.6), ('C5', 0.6), ('G5', 0.6),
                ('F5', 0.6), ('A5', 0.6), ('C6', 0.6), ('F5', 0.6),
                ('E5', 0.6), ('C5', 0.6), ('G5', 0.6), ('E5', 0.6)
            ],
            'volcano': [
                ('D5', 0.3), ('F5', 0.3), ('A5', 0.3), ('D6', 0.3),
                ('A5', 0.3), ('F5', 0.3), ('D5', 0.3), ('A5', 0.3),
                ('G5', 0.3), ('B5', 0.3), ('D6', 0.3), ('G5', 0.3),
                ('F5', 0.3), ('D5', 0.3), ('A5', 0.3), ('F5', 0.3)
            ],
            'neon_city': [
                ('E5', 0.4), ('G5', 0.4), ('B5', 0.4), ('E6', 0.4),
                ('B5', 0.4), ('G5', 0.4), ('E5', 0.4), ('B5', 0.4),
                ('A5', 0.4), ('C6', 0.4), ('E6', 0.4), ('A5', 0.4),
                ('G5', 0.4), ('E5', 0.4), ('B5', 0.4), ('G5', 0.4)
            ],
            'candy_land': [
                ('F5', 0.3), ('A5', 0.3), ('C6', 0.3), ('F6', 0.3),
                ('C6', 0.3), ('A5', 0.3), ('F5', 0.3), ('C6', 0.3),
                ('B5', 0.3), ('D6', 0.3), ('F6', 0.3), ('B5', 0.3),
                ('A5', 0.3), ('F5', 0.3), ('C6', 0.3), ('A5', 0.3)
            ],
            'underwater': [
                ('G5', 0.5), ('B5', 0.5), ('D6', 0.5), ('G6', 0.5),
                ('D6', 0.5), ('B5', 0.5), ('G5', 0.5), ('D6', 0.5),
                ('C6', 0.5), ('E6', 0.5), ('G6', 0.5), ('C6', 0.5),
                ('B5', 0.5), ('G5', 0.5), ('D6', 0.5), ('B5', 0.5)
            ],
            'cyberpunk': [
                ('A5', 0.4), ('C6', 0.4), ('E6', 0.4), ('A6', 0.4),
                ('E6', 0.4), ('C6', 0.4), ('A5', 0.4), ('E6', 0.4),
                ('D6', 0.4), ('F6', 0.4), ('A6', 0.4), ('D6', 0.4),
                ('C6', 0.4), ('A5', 0.4), ('E6', 0.4), ('C6', 0.4)
            ],
            'fantasy': [
                ('B5', 0.6), ('D6', 0.6), ('F6', 0.6), ('B6', 0.6),
                ('F6', 0.6), ('D6', 0.6), ('B5', 0.6), ('F6', 0.6),
                ('E6', 0.6), ('G6', 0.6), ('B6', 0.6), ('E6', 0.6),
                ('D6', 0.6), ('B5', 0.6), ('F6', 0.6), ('D6', 0.6)
            ],
            'steampunk': [
                ('C6', 0.5), ('E6', 0.5), ('G6', 0.5), ('C7', 0.5),
                ('G6', 0.5), ('E6', 0.5), ('C6', 0.5), ('G6', 0.5),
                ('F6', 0.5), ('A6', 0.5), ('C7', 0.5), ('F6', 0.5),
                ('E6', 0.5), ('C6', 0.5), ('G6', 0.5), ('E6', 0.5)
            ],
            'apocalypse': [
                ('D6', 0.7), ('F6', 0.7), ('A6', 0.7), ('D7', 0.7),
                ('A6', 0.7), ('F6', 0.7), ('D6', 0.7), ('A6', 0.7),
                ('G6', 0.7), ('B6', 0.7), ('D7', 0.7), ('G6', 0.7),
                ('F6', 0.7), ('D6', 0.7), ('A6', 0.7), ('F6', 0.7)
            ]
        }

        melody = theme_melodies.get(theme, theme_melodies['city'])
        sample_rate = 44100
        full_song = np.array([])

        for note_name, duration in melody:
            if note_name in notes:
                note_wave = create_note(notes[note_name], duration, sample_rate)
                if note_wave is not None:
                    if len(full_song) == 0:
                        full_song = note_wave
                    else:
                        full_song = np.vstack((full_song, note_wave))

        if len(full_song) > 0:
            sound = pygame.sndarray.make_sound(full_song)
            return sound
        return None
    except:
        return None


def create_flappy_bird_song():
    """Create the default Flappy Adventure theme song"""
    return create_theme_song('city')

def create_sound_effect(frequency, duration=100):
    """Create a simple sound effect"""
    try:
        import numpy as np
        sample_rate = 44100
        samples = int(sample_rate * duration / 1000)

        t = np.linspace(0, duration/1000, samples)
        wave = np.sin(2 * np.pi * frequency * t) * 0.5
        wave = (wave * 32767).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    except:
        return None

# Create sounds
try:
    flap_sound = create_sound_effect(800, 150)
    score_sound = create_sound_effect(1200, 200)
    crash_sound = create_sound_effect(200, 500)
    theme_change_sound = create_sound_effect(600, 300)
    background_song = create_flappy_bird_song()

    print("🎵 Sound effects created successfully!")
    if background_song:
        print("🎼 Flappy Adventure song created successfully!")
    else:
        print("❌ Could not create background song")
except Exception as e:
    print(f"❌ Error creating sounds: {e}")
    flap_sound = None
    score_sound = None
    crash_sound = None
    theme_change_sound = None
    background_song = None

class Particle:
    def __init__(self, x, y, color, particle_type="trail"):
        self.x = x
        self.y = y
        self.particle_type = particle_type

        if particle_type == "trail":
            # Trail particles move backward and fade
            self.vx = random.uniform(-8, -2)
            self.vy = random.uniform(-2, 2)
            self.life = 45
            self.max_life = 45
            self.fade_rate = 0.95
        else:
            # Flap particles explode outward
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-5, -1)
            self.life = 30
            self.max_life = 30
            self.fade_rate = 0.9

        self.color = color
        self.alpha = 255

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.particle_type == "trail":
            self.vy += 0.1  # Gentle gravity for trail
        else:
            self.vy += 0.2  # Normal gravity for flap particles

        self.life -= 1
        self.alpha = int(255 * (self.life / self.max_life))

    def draw(self, screen):
        if self.life > 0:
            if self.particle_type == "trail":
                # Trail particles are bigger and more visible
                size = int(8 * (self.life / self.max_life))  # Increased from 4 to 8
                if size > 0:
                    # Create a trail effect with multiple larger circles
                    for i in range(3):
                        offset = i * 4  # Increased offset for bigger particles
                        alpha = max(0, self.alpha - (i * 40))
                        if alpha > 0:
                            trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                            trail_surface.set_alpha(alpha)
                            pygame.draw.circle(trail_surface, self.color, (size, size), size)
                            screen.blit(trail_surface, (int(self.x - size + offset), int(self.y - size)))
            else:
                # Regular flap particles - made bigger
                size = int(6 * (self.life / self.max_life))  # Increased from 3 to 6
                if size > 0:
                    particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    particle_surface.set_alpha(self.alpha)
                    pygame.draw.circle(particle_surface, self.color, (size, size), size)
                    screen.blit(particle_surface, (int(self.x - size), int(self.y - size)))

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.rect = pygame.Rect(x, y, BIRD_SIZE, BIRD_SIZE)
        self.rotation = 0
        self.particles = []
        self.wing_angle = 0
        self.wing_direction = 1

    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.rotation = -30
        self.wing_angle = -20
        for _ in range(8):
            self.particles.append(Particle(self.x, self.y + BIRD_SIZE//2, (139, 69, 19), "flap"))

        if flap_sound:
            flap_sound.play()

    def update(self, speed_boost=False, pipe_speed=None):
        # Apply gravity (reduced if speed boost is active)
        gravity = GRAVITY * 0.7 if speed_boost else GRAVITY

        # Always apply gravity and allow normal movement
        self.velocity += gravity
        self.y += self.velocity
        self.rect.y = self.y

        if self.velocity < 0:
            self.rotation = -30
        else:
            self.rotation = min(90, self.rotation + 5)

        self.wing_angle += 5 * self.wing_direction
        if self.wing_angle > 15 or self.wing_angle < -20:
            self.wing_direction *= -1

        # Add trail particles continuously
        if random.random() < 0.3:  # 30% chance per frame
            trail_color = (139, 69, 19) if not speed_boost else (255, 215, 0)  # Gold trail during speed boost
            self.particles.append(Particle(self.x, self.y + BIRD_SIZE//2, trail_color, "trail"))

        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

        bird_surface = pygame.Surface((BIRD_SIZE + 20, BIRD_SIZE + 20), pygame.SRCALPHA)

        # Bird body
        pygame.draw.ellipse(bird_surface, BROWN, (10, 10, BIRD_SIZE, BIRD_SIZE))
        pygame.draw.ellipse(bird_surface, BLACK, (10, 10, BIRD_SIZE, BIRD_SIZE), 2)

        # Bird head
        head_radius = BIRD_SIZE // 3
        pygame.draw.circle(bird_surface, BROWN, (BIRD_SIZE + 5, BIRD_SIZE//2), head_radius)
        pygame.draw.circle(bird_surface, BLACK, (BIRD_SIZE + 5, BIRD_SIZE//2), head_radius, 2)

        # Bird eye
        eye_x = BIRD_SIZE + 5 + head_radius - 5
        eye_y = BIRD_SIZE//2 - 3
        pygame.draw.circle(bird_surface, BLACK, (eye_x, eye_y), 4)
        pygame.draw.circle(bird_surface, WHITE, (eye_x + 1, eye_y - 1), 2)
        pygame.draw.circle(bird_surface, BLACK, (eye_x + 2, eye_y - 1), 1)

        # Bird beak
        beak_points = [(BIRD_SIZE + 5 + head_radius, BIRD_SIZE//2),
                       (BIRD_SIZE + 5 + head_radius + 12, BIRD_SIZE//2 - 4),
                       (BIRD_SIZE + 5 + head_radius + 12, BIRD_SIZE//2 + 4)]
        pygame.draw.polygon(bird_surface, ORANGE, beak_points)
        pygame.draw.polygon(bird_surface, BLACK, beak_points, 1)

        # Bird wing
        wing_x = BIRD_SIZE//2 - 5
        wing_y = BIRD_SIZE//2 + 5
        wing_width = 20
        wing_height = 15

        pygame.draw.ellipse(bird_surface, DARK_GRAY, (wing_x, wing_y, wing_width, wing_height))

        feather_x = wing_x + wing_width//2
        feather_y = wing_y + wing_height//2
        feather_length = 15 + abs(self.wing_angle)

        for i in range(3):
            angle_offset = (i - 1) * 10 + self.wing_angle
            end_x = feather_x + math.cos(math.radians(angle_offset)) * feather_length
            end_y = feather_y + math.sin(math.radians(angle_offset)) * feather_length
            pygame.draw.line(bird_surface, GRAY, (feather_x, feather_y), (end_x, end_y), 2)

        # Bird tail
        tail_points = [(10, BIRD_SIZE//2), (0, BIRD_SIZE//2 - 8), (0, BIRD_SIZE//2 + 8)]
        pygame.draw.polygon(bird_surface, DARK_GRAY, tail_points)
        pygame.draw.polygon(bird_surface, BLACK, tail_points, 1)

        if self.velocity > 0:
            foot_x = BIRD_SIZE//2
            foot_y = BIRD_SIZE + 5
            pygame.draw.line(bird_surface, ORANGE, (foot_x - 3, foot_y), (foot_x - 3, foot_y + 8), 2)
            pygame.draw.line(bird_surface, ORANGE, (foot_x + 3, foot_y), (foot_x + 3, foot_y + 8), 2)

        rotated_surface = pygame.transform.rotate(bird_surface, self.rotation)
        screen.blit(rotated_surface, (self.x - rotated_surface.get_width()//2 + BIRD_SIZE//2,
                                     self.y - rotated_surface.get_height()//2 + BIRD_SIZE//2))

    def get_rect(self):
        return self.rect

class Background:
    def __init__(self):
        self.current_theme = "city"
        self.themes = ["city", "forest", "mountains", "desert", "space", "ocean", "sunset", "winter", "volcano", "neon_city", "candy_land", "underwater", "cyberpunk", "fantasy", "steampunk", "apocalypse"]
        self.theme_index = 0
        self.clouds = []
        self.buildings = []
        self.trees = []
        self.mountains = []
        self.stars = []
        self.bubbles = []
        self.snowflakes = []
        self.lava_particles = []
        self.neon_lights = []
        self.candy_elements = []
        self.seaweed = []
        self.cyber_effects = []
        self.magical_particles = []
        self.steam_clouds = []
        self.dust_particles = []
        self.score_threshold = 8  # Reduced to cycle through themes faster

        # Initialize clouds
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 200),
                'size': random.randint(30, 80)
            })

        # Initialize buildings for city
        self.generate_buildings()

        # Initialize trees for forest
        self.generate_trees()

        # Initialize mountains
        self.generate_mountains()

        # Initialize stars for space
        self.generate_stars()

        # Initialize bubbles for ocean
        self.generate_bubbles()

        # Initialize snowflakes for winter
        self.generate_snowflakes()

        # Initialize lava particles for volcano
        self.generate_lava_particles()

        # Initialize neon lights for neon city
        self.generate_neon_lights()

        # Initialize candy elements for candy land
        self.generate_candy_elements()

        # Initialize seaweed for underwater
        self.generate_seaweed()

        # Initialize cyber effects for cyberpunk
        self.generate_cyber_effects()

        # Initialize magical particles for fantasy
        self.generate_magical_particles()

        # Initialize steam clouds for steampunk
        self.generate_steam_clouds()

        # Initialize dust particles for apocalypse
        self.generate_dust_particles()

    def generate_buildings(self):
        self.buildings = []
        for i in range(0, SCREEN_WIDTH + 100, 80):
            height = random.randint(100, 300)
            self.buildings.append({
                'x': i,
                'height': height,
                'color': random.choice([DARK_GRAY, GRAY, LIGHT_GRAY])
            })

    def generate_trees(self):
        self.trees = []
        for i in range(0, SCREEN_WIDTH + 100, 60):
            height = random.randint(80, 150)
            self.trees.append({
                'x': i,
                'height': height,
                'trunk_color': BROWN,
                'leaves_color': DARK_GREEN
            })

    def generate_mountains(self):
        self.mountains = []
        for i in range(0, SCREEN_WIDTH + 200, 150):
            height = random.randint(150, 250)
            self.mountains.append({
                'x': i,
                'height': height,
                'color': DARK_GRAY
            })

    def generate_stars(self):
        self.stars = []
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - 100),
                'size': random.randint(1, 3),
                'twinkle': random.randint(0, 100)
            })

    def generate_bubbles(self):
        self.bubbles = []
        for _ in range(10):
            self.bubbles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT),
                'size': random.randint(10, 20),
                'speed': random.uniform(0.5, 1.5)
            })

    def generate_snowflakes(self):
        self.snowflakes = []
        for _ in range(20):
            self.snowflakes.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - 100),
                'size': random.randint(5, 10),
                'speed': random.uniform(0.3, 0.8)
            })

    def generate_lava_particles(self):
        self.lava_particles = []
        for _ in range(10):
            self.lava_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT),
                'size': random.randint(5, 15),
                'speed': random.uniform(0.5, 1.5),
                'color': (255, 100, 0) # Reddish lava
            })

    def generate_neon_lights(self):
        self.neon_lights = []
        for _ in range(10):
            self.neon_lights.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - 100),
                'size': random.randint(10, 20),
                'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            })

    def generate_candy_elements(self):
        self.candy_elements = []
        for _ in range(10):
            self.candy_elements.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - 100),
                'type': random.choice(['heart', 'star', 'diamond', 'candy_cane']),
                'color': random.choice([RED, YELLOW, PURPLE, GOLD]),
                'size': random.randint(10, 20)
            })

    def generate_seaweed(self):
        self.seaweed = []
        for _ in range(15):
            self.seaweed.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'height': random.randint(50, 150),
                'color': (0, 150, 0),
                'sway': random.uniform(0, 6.28)
            })

    def generate_cyber_effects(self):
        self.cyber_effects = []
        for _ in range(20):
            self.cyber_effects.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - 100),
                'type': random.choice(['glitch', 'data_stream', 'hologram']),
                'color': (0, 255, 255),
                'size': random.randint(5, 15),
                'speed': random.uniform(1, 3)
            })

    def generate_magical_particles(self):
        self.magical_particles = []
        for _ in range(25):
            self.magical_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - 100),
                'color': random.choice([(255, 0, 255), (0, 255, 255), (255, 255, 0), (255, 0, 128)]),
                'size': random.randint(3, 8),
                'sparkle': random.randint(0, 100)
            })

    def generate_steam_clouds(self):
        self.steam_clouds = []
        for _ in range(12):
            self.steam_clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT - 50),
                'size': random.randint(20, 40),
                'opacity': random.randint(100, 200),
                'rise_speed': random.uniform(0.5, 1.5)
            })

    def generate_dust_particles(self):
        self.dust_particles = []
        for _ in range(30):
            self.dust_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT - 100),
                'size': random.randint(2, 6),
                'drift_speed': random.uniform(0.2, 0.8),
                'color': (139, 69, 19)
            })

    def update_theme(self, score):
        new_theme_index = min(score // self.score_threshold, len(self.themes) - 1)
        if new_theme_index != self.theme_index:
            self.theme_index = new_theme_index
            self.current_theme = self.themes[self.theme_index]
            if theme_change_sound:
                theme_change_sound.play()

    def update(self, pipe_speed):
        # Update clouds
        for cloud in self.clouds:
            cloud['x'] -= pipe_speed // 2  # Clouds move faster with speed boost
            if cloud['x'] < -100:
                cloud['x'] = SCREEN_WIDTH + 100
                cloud['y'] = random.randint(50, 200)

        # Update buildings (city theme)
        for building in self.buildings:
            building['x'] -= pipe_speed // 3
            if building['x'] < -100:
                building['x'] = SCREEN_WIDTH + 100
                building['height'] = random.randint(100, 300)

        # Update trees (forest theme)
        for tree in self.trees:
            tree['x'] -= pipe_speed // 3
            if tree['x'] < -100:
                tree['x'] = SCREEN_WIDTH + 100
                tree['height'] = random.randint(80, 150)

        # Update mountains
        for mountain in self.mountains:
            mountain['x'] -= pipe_speed // 4
            if mountain['x'] < -200:
                mountain['x'] = SCREEN_WIDTH + 200
                mountain['height'] = random.randint(150, 250)

        # Update stars twinkling
        for star in self.stars:
            star['twinkle'] = (star['twinkle'] + 1) % 200

        # Update bubbles
        for bubble in self.bubbles:
            bubble['y'] -= bubble['speed']
            if bubble['y'] < -bubble['size']:
                bubble['y'] = SCREEN_HEIGHT + bubble['size']
                bubble['x'] = random.randint(0, SCREEN_WIDTH)

        # Update snowflakes
        for snowflake in self.snowflakes:
            snowflake['y'] -= snowflake['speed']
            if snowflake['y'] < -snowflake['size']:
                snowflake['y'] = SCREEN_HEIGHT + snowflake['size']
                snowflake['x'] = random.randint(0, SCREEN_WIDTH)

        # Update lava particles
        for lava_particle in self.lava_particles:
            lava_particle['y'] -= lava_particle['speed']
            if lava_particle['y'] < -lava_particle['size']:
                lava_particle['y'] = SCREEN_HEIGHT + lava_particle['size']
                lava_particle['x'] = random.randint(0, SCREEN_WIDTH)

        # Update neon lights
        for neon_light in self.neon_lights:
            neon_light['y'] -= 0.5 # Slight upward movement
            if neon_light['y'] < -neon_light['size']:
                neon_light['y'] = SCREEN_HEIGHT + neon_light['size']
                neon_light['x'] = random.randint(0, SCREEN_WIDTH)

        # Update candy elements
        for candy_element in self.candy_elements:
            candy_element['y'] -= 0.8 # Slight upward movement
            if candy_element['y'] < -20:
                candy_element['y'] = SCREEN_HEIGHT + 20
                candy_element['x'] = random.randint(0, SCREEN_WIDTH)

        # Update seaweed swaying
        for seaweed in self.seaweed:
            seaweed['sway'] += 0.02
            seaweed['x'] -= pipe_speed // 4
            if seaweed['x'] < -50:
                seaweed['x'] = SCREEN_WIDTH + 50
                seaweed['height'] = random.randint(50, 150)

        # Update cyber effects
        for effect in self.cyber_effects:
            effect['y'] -= effect['speed']
            if effect['y'] < -effect['size']:
                effect['y'] = SCREEN_HEIGHT + effect['size']
                effect['x'] = random.randint(0, SCREEN_WIDTH)

        # Update magical particles
        for particle in self.magical_particles:
            particle['sparkle'] = (particle['sparkle'] + 1) % 200
            particle['y'] -= 0.5
            if particle['y'] < -particle['size']:
                particle['y'] = SCREEN_HEIGHT + particle['size']
                particle['x'] = random.randint(0, SCREEN_WIDTH)

        # Update steam clouds
        for steam in self.steam_clouds:
            steam['y'] -= steam['rise_speed']
            if steam['y'] < -steam['size']:
                steam['y'] = SCREEN_HEIGHT + steam['size']
                steam['x'] = random.randint(0, SCREEN_WIDTH)

        # Update dust particles
        for dust in self.dust_particles:
            dust['x'] -= dust['drift_speed']
            if dust['x'] < -dust['size']:
                dust['x'] = SCREEN_WIDTH + dust['size']
                dust['y'] = random.randint(0, SCREEN_HEIGHT - 100)

    def draw(self, screen):
        if self.current_theme == "city":
            self.draw_city(screen)
        elif self.current_theme == "forest":
            self.draw_forest(screen)
        elif self.current_theme == "mountains":
            self.draw_mountains(screen)
        elif self.current_theme == "desert":
            self.draw_desert(screen)
        elif self.current_theme == "space":
            self.draw_space(screen)
        elif self.current_theme == "ocean":
            self.draw_ocean(screen)
        elif self.current_theme == "sunset":
            self.draw_sunset(screen)
        elif self.current_theme == "winter":
            self.draw_winter(screen)
        elif self.current_theme == "volcano":
            self.draw_volcano(screen)
        elif self.current_theme == "neon_city":
            self.draw_neon_city(screen)
        elif self.current_theme == "candy_land":
            self.draw_candy_land(screen)
        elif self.current_theme == "underwater":
            self.draw_underwater(screen)
        elif self.current_theme == "cyberpunk":
            self.draw_cyberpunk(screen)
        elif self.current_theme == "fantasy":
            self.draw_fantasy(screen)
        elif self.current_theme == "steampunk":
            self.draw_steampunk(screen)
        elif self.current_theme == "apocalypse":
            self.draw_apocalypse(screen)

    def draw_city(self, screen):
        # Sky gradient
        for y in range(SCREEN_HEIGHT - 100):
            color_ratio = y / (SCREEN_HEIGHT - 100)
            r = int(135 + (100 - 135) * color_ratio)
            g = int(206 + (150 - 206) * color_ratio)
            b = int(235 + (200 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Draw buildings
        for building in self.buildings:
            pygame.draw.rect(screen, building['color'],
                           (building['x'], SCREEN_HEIGHT - 100 - building['height'],
                            60, building['height']))
            pygame.draw.rect(screen, BLACK,
                           (building['x'], SCREEN_HEIGHT - 100 - building['height'],
                            60, building['height']), 2)

            # Windows
            for window_y in range(building['height'] - 20, 0, 30):
                for window_x in range(10, 50, 15):
                    if random.random() > 0.3:  # Some windows lit
                        pygame.draw.rect(screen, YELLOW,
                                       (building['x'] + window_x,
                                        SCREEN_HEIGHT - 100 - building['height'] + window_y,
                                        8, 8))

        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])
            pygame.draw.circle(screen, WHITE, (cloud['x'] + cloud['size']//2, cloud['y']), cloud['size']//2)
            pygame.draw.circle(screen, WHITE, (cloud['x'] - cloud['size']//2, cloud['y']), cloud['size']//2)

    def draw_forest(self, screen):
        # Sky gradient (greener)
        for y in range(SCREEN_HEIGHT - 100):
            color_ratio = y / (SCREEN_HEIGHT - 100)
            r = int(135 + (50 - 135) * color_ratio)
            g = int(206 + (200 - 206) * color_ratio)
            b = int(235 + (100 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Draw trees
        for tree in self.trees:
            # Tree trunk
            pygame.draw.rect(screen, tree['trunk_color'],
                           (tree['x'] + 20, SCREEN_HEIGHT - 100 - tree['height'],
                            20, tree['height']))
            # Tree leaves
            pygame.draw.circle(screen, tree['leaves_color'],
                             (tree['x'] + 30, SCREEN_HEIGHT - 100 - tree['height'] + 20), 40)
            pygame.draw.circle(screen, tree['leaves_color'],
                             (tree['x'] + 15, SCREEN_HEIGHT - 100 - tree['height'] + 40), 30)
            pygame.draw.circle(screen, tree['leaves_color'],
                             (tree['x'] + 45, SCREEN_HEIGHT - 100 - tree['height'] + 40), 30)

        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

    def draw_mountains(self, screen):
        # Sky gradient (purple-ish)
        for y in range(SCREEN_HEIGHT - 100):
            color_ratio = y / (SCREEN_HEIGHT - 100)
            r = int(135 + (100 - 135) * color_ratio)
            g = int(206 + (150 - 206) * color_ratio)
            b = int(235 + (200 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_HEIGHT, y))

        # Draw mountains
        for mountain in self.mountains:
            points = [(mountain['x'], SCREEN_HEIGHT - 100),
                     (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                     (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
            pygame.draw.polygon(screen, mountain['color'], points)
            pygame.draw.polygon(screen, BLACK, points, 2)

        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

    def draw_desert(self, screen):
        # Sky gradient (orange/yellow)
        for y in range(SCREEN_HEIGHT - 100):
            color_ratio = y / (SCREEN_HEIGHT - 100)
            r = int(135 + (255 - 135) * color_ratio)
            g = int(206 + (200 - 206) * color_ratio)
            b = int(235 + (100 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_HEIGHT, y))

        # Draw sand dunes
        for i in range(0, SCREEN_WIDTH + 100, 100):
            points = [(i, SCREEN_HEIGHT - 100),
                     (i + 50, SCREEN_HEIGHT - 150),
                     (i + 100, SCREEN_HEIGHT - 100)]
            pygame.draw.polygon(screen, GOLD, points)
            pygame.draw.polygon(screen, BLACK, points, 1)

    def draw_space(self, screen):
        # Dark space background
        screen.fill(DARK_BLUE)

        # Draw stars
        for star in self.stars:
            brightness = 255 if star['twinkle'] < 100 else 128
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (star['x'], star['y']), star['size'])

        # Draw planets
        pygame.draw.circle(screen, PURPLE, (100, 100), 30)
        pygame.draw.circle(screen, ORANGE, (600, 150), 25)
        pygame.draw.circle(screen, LIGHT_BLUE, (700, 80), 20)

    def draw_ocean(self, screen):
        # Blue ocean background
        screen.fill(DARK_BLUE)

        # Draw water gradient
        for y in range(SCREEN_HEIGHT - 100, SCREEN_HEIGHT):
            color_ratio = (SCREEN_HEIGHT - y) / (SCREEN_HEIGHT - (SCREEN_HEIGHT - 100))
            r = int(135 + (100 - 135) * color_ratio)
            g = int(206 + (150 - 206) * color_ratio)
            b = int(235 + (200 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Draw bubbles
        for bubble in self.bubbles:
            pygame.draw.circle(screen, WHITE, (bubble['x'], bubble['y']), bubble['size'])

        # Draw fish (example)
        for i in range(0, SCREEN_WIDTH, 100):
            pygame.draw.circle(screen, WHITE, (i + 50, SCREEN_HEIGHT - 100 - 50), 20)

    def draw_sunset(self, screen):
        # Orange sunset background
        screen.fill(DARK_GRAY)

        # Draw sky gradient
        for y in range(SCREEN_HEIGHT - 100):
            color_ratio = y / (SCREEN_HEIGHT - 100)
            r = int(135 + (255 - 135) * color_ratio)
            g = int(206 + (200 - 206) * color_ratio)
            b = int(235 + (100 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Draw mountains
        for mountain in self.mountains:
            points = [(mountain['x'], SCREEN_HEIGHT - 100),
                     (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                     (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
            pygame.draw.polygon(screen, mountain['color'], points)
            pygame.draw.polygon(screen, BLACK, points, 2)

        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

    def draw_winter(self, screen):
        # White winter background
        screen.fill(WHITE)

        # Draw snowflakes
        for snowflake in self.snowflakes:
            pygame.draw.circle(screen, WHITE, (snowflake['x'], snowflake['y']), snowflake['size'])

        # Draw mountains
        for mountain in self.mountains:
            points = [(mountain['x'], SCREEN_HEIGHT - 100),
                     (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                     (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
            pygame.draw.polygon(screen, mountain['color'], points)
            pygame.draw.polygon(screen, BLACK, points, 2)

        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

    def draw_volcano(self, screen):
        # Red volcanic background
        screen.fill(RED)

        # Draw lava particles
        for lava_particle in self.lava_particles:
            pygame.draw.circle(screen, lava_particle['color'], (lava_particle['x'], lava_particle['y']), lava_particle['size'])

        # Draw mountains
        for mountain in self.mountains:
            points = [(mountain['x'], SCREEN_HEIGHT - 100),
                     (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                     (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
            pygame.draw.polygon(screen, mountain['color'], points)
            pygame.draw.polygon(screen, BLACK, points, 2)

        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

    def draw_neon_city(self, screen):
        # Dark blue background with neon lights
        screen.fill(DARK_BLUE)

        # Draw neon lights
        for neon_light in self.neon_lights:
            pygame.draw.circle(screen, neon_light['color'], (neon_light['x'], neon_light['y']), neon_light['size'])

        # Draw buildings
        for building in self.buildings:
            pygame.draw.rect(screen, building['color'],
                           (building['x'], SCREEN_HEIGHT - 100 - building['height'],
                            60, building['height']))
            pygame.draw.rect(screen, BLACK,
                           (building['x'], SCREEN_HEIGHT - 100 - building['height'],
                            60, building['height']), 2)

            # Windows
            for window_y in range(building['height'] - 20, 0, 30):
                for window_x in range(10, 50, 15):
                    if random.random() > 0.3:  # Some windows lit
                        pygame.draw.rect(screen, YELLOW,
                                       (building['x'] + window_x,
                                        SCREEN_HEIGHT - 100 - building['height'] + window_y,
                                        8, 8))

        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

    def draw_candy_land(self, screen):
        # Pink candy land background
        screen.fill(PURPLE)

        # Draw candy elements
        for candy_element in self.candy_elements:
            if candy_element['type'] == 'heart':
                pygame.draw.circle(screen, candy_element['color'], (candy_element['x'], candy_element['y']), candy_element['size'])
            elif candy_element['type'] == 'star':
                pygame.draw.circle(screen, candy_element['color'], (candy_element['x'], candy_element['y']), candy_element['size'])
            elif candy_element['type'] == 'diamond':
                pygame.draw.rect(screen, candy_element['color'], (candy_element['x'], candy_element['y'], candy_element['size'], candy_element['size']))
            elif candy_element['type'] == 'candy_cane':
                pygame.draw.line(screen, candy_element['color'], (candy_element['x'], candy_element['y']), (candy_element['x'] + candy_element['size'], candy_element['y'] + candy_element['size']), 3)

        # Draw mountains
        for mountain in self.mountains:
            points = [(mountain['x'], SCREEN_HEIGHT - 100),
                     (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                     (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
            pygame.draw.polygon(screen, mountain['color'], points)
            pygame.draw.polygon(screen, BLACK, points, 2)

        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

    def draw_underwater(self, screen):
        # Deep blue underwater background
        for y in range(SCREEN_HEIGHT - 100):
            color_ratio = y / (SCREEN_HEIGHT - 100)
            r = int(0 + (0 - 0) * color_ratio)
            g = int(50 + (100 - 50) * color_ratio)
            b = int(150 + (255 - 150) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Draw seaweed
        for seaweed in self.seaweed:
            sway_offset = math.sin(seaweed['sway']) * 10
            points = [
                (seaweed['x'] + sway_offset, SCREEN_HEIGHT - 100),
                (seaweed['x'] + sway_offset + 5, SCREEN_HEIGHT - 100 - seaweed['height']//2),
                (seaweed['x'] + sway_offset, SCREEN_HEIGHT - 100 - seaweed['height'])
            ]
            pygame.draw.polygon(screen, seaweed['color'], points)
            pygame.draw.polygon(screen, (0, 100, 0), points, 2)

        # Draw bubbles
        for bubble in self.bubbles:
            pygame.draw.circle(screen, (255, 255, 255, 100), (bubble['x'], bubble['y']), bubble['size'])
            pygame.draw.circle(screen, (200, 200, 255), (bubble['x'], bubble['y']), bubble['size'], 1)

    def draw_cyberpunk(self, screen):
        # Dark purple cyberpunk background
        screen.fill((25, 0, 50))

        # Draw cyber effects
        for effect in self.cyber_effects:
            if effect['type'] == 'glitch':
                # Glitch effect - random lines
                for _ in range(3):
                    x1 = effect['x'] + random.randint(-effect['size'], effect['size'])
                    y1 = effect['y'] + random.randint(-effect['size'], effect['size'])
                    x2 = effect['x'] + random.randint(-effect['size'], effect['size'])
                    y2 = effect['y'] + random.randint(-effect['size'], effect['size'])
                    pygame.draw.line(screen, effect['color'], (x1, y1), (x2, y2), 2)
            elif effect['type'] == 'data_stream':
                # Data stream effect
                for i in range(5):
                    y_offset = i * 10
                    pygame.draw.circle(screen, effect['color'], (effect['x'], effect['y'] + y_offset), 2)
            elif effect['type'] == 'hologram':
                # Hologram effect
                pygame.draw.circle(screen, effect['color'], (effect['x'], effect['y']), effect['size'])
                pygame.draw.circle(screen, (255, 255, 255), (effect['x'], effect['y']), effect['size'], 2)

        # Draw neon buildings
        for building in self.buildings:
            neon_color = (random.randint(100, 255), 0, random.randint(100, 255))
            pygame.draw.rect(screen, (20, 20, 20), (building['x'], SCREEN_HEIGHT - 100 - building['height'], 60, building['height']))
            pygame.draw.rect(screen, neon_color, (building['x'], SCREEN_HEIGHT - 100 - building['height'], 60, building['height']), 3)

    def draw_fantasy(self, screen):
        # Magical gradient background
        for y in range(SCREEN_HEIGHT - 100):
            color_ratio = y / (SCREEN_HEIGHT - 100)
            r = int(100 + (200 - 100) * color_ratio)
            g = int(50 + (100 - 50) * color_ratio)
            b = int(150 + (255 - 150) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Draw magical particles
        for particle in self.magical_particles:
            sparkle_alpha = int(128 + 127 * math.sin(particle['sparkle'] * 0.1))
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            particle_surface.set_alpha(sparkle_alpha)
            pygame.draw.circle(particle_surface, particle['color'], (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))

        # Draw floating islands (mountains)
        for mountain in self.mountains:
            # Island base
            points = [(mountain['x'], SCREEN_HEIGHT - 100),
                     (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                     (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
            pygame.draw.polygon(screen, (139, 69, 19), points)  # Brown base
            pygame.draw.polygon(screen, (34, 139, 34), points)  # Green top
            pygame.draw.polygon(screen, BLACK, points, 2)

    def draw_steampunk(self, screen):
        # Brown steampunk background
        screen.fill((139, 69, 19))

        # Draw steam clouds
        for steam in self.steam_clouds:
            steam_surface = pygame.Surface((steam['size'] * 2, steam['size'] * 2), pygame.SRCALPHA)
            steam_surface.set_alpha(steam['opacity'])
            pygame.draw.circle(steam_surface, (200, 200, 200), (steam['size'], steam['size']), steam['size'])
            screen.blit(steam_surface, (steam['x'] - steam['size'], steam['y'] - steam['size']))

        # Draw mechanical buildings
        for building in self.buildings:
            # Metal building
            pygame.draw.rect(screen, (100, 100, 100), (building['x'], SCREEN_HEIGHT - 100 - building['height'], 60, building['height']))
            pygame.draw.rect(screen, (50, 50, 50), (building['x'], SCREEN_HEIGHT - 100 - building['height'], 60, building['height']), 3)

            # Gears and pipes
            for i in range(3):
                gear_y = SCREEN_HEIGHT - 100 - building['height'] + 20 + i * 30
                if gear_y < SCREEN_HEIGHT - 100:
                    pygame.draw.circle(screen, (80, 80, 80), (building['x'] + 30, gear_y), 8)
                    pygame.draw.circle(screen, (60, 60, 60), (building['x'] + 30, gear_y), 8, 2)

    def draw_apocalypse(self, screen):
        # Dark apocalyptic background
        screen.fill((40, 40, 40))

        # Draw dust particles
        for dust in self.dust_particles:
            pygame.draw.circle(screen, dust['color'], (dust['x'], dust['y']), dust['size'])

        # Draw destroyed buildings
        for building in self.buildings:
            # Broken building
            height = building['height'] - random.randint(0, 50)
            pygame.draw.rect(screen, (60, 60, 60), (building['x'], SCREEN_HEIGHT - 100 - height, 60, height))
            pygame.draw.rect(screen, (30, 30, 30), (building['x'], SCREEN_HEIGHT - 100 - height, 60, height), 2)

            # Broken windows
            for i in range(2):
                window_x = building['x'] + 15 + i * 25
                window_y = SCREEN_HEIGHT - 100 - height + 20
                if window_y < SCREEN_HEIGHT - 100:
                    pygame.draw.rect(screen, (20, 20, 20), (window_x, window_y, 15, 12))
                    pygame.draw.rect(screen, (10, 10, 10), (window_x, window_y, 15, 12), 1)

class Pipe:
    def __init__(self, x, theme="city"):
        self.x = x
        self.theme = theme
        self.gap_y = random.randint(150, SCREEN_HEIGHT - 150)
        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_height = SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen, theme):
        if theme == "city":
            self.draw_city_pipe(screen)
        elif theme == "forest":
            self.draw_forest_pipe(screen)
        elif theme == "mountains":
            self.draw_mountain_pipe(screen)
        elif theme == "desert":
            self.draw_desert_pipe(screen)
        elif theme == "space":
            self.draw_space_pipe(screen)
        elif theme == "ocean":
            self.draw_ocean_pipe(screen)
        elif theme == "sunset":
            self.draw_sunset_pipe(screen)
        elif theme == "winter":
            self.draw_winter_pipe(screen)
        elif theme == "volcano":
            self.draw_volcano_pipe(screen)
        elif theme == "neon_city":
            self.draw_neon_city_pipe(screen)
        elif theme == "candy_land":
            self.draw_candy_land_pipe(screen)
        elif theme == "underwater":
            self.draw_underwater_pipe(screen)
        elif theme == "cyberpunk":
            self.draw_cyberpunk_pipe(screen)
        elif theme == "fantasy":
            self.draw_fantasy_pipe(screen)
        elif theme == "steampunk":
            self.draw_steampunk_pipe(screen)
        elif theme == "apocalypse":
            self.draw_apocalypse_pipe(screen)

    def draw_city_pipe(self, screen):
        # Building-like pipes
        building_colors = [DARK_GRAY, GRAY, LIGHT_GRAY, (100, 100, 100)]
        color = random.choice(building_colors)

        # Top building
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom building
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Windows
        window_colors = [YELLOW, LIGHT_BLUE, WHITE, (255, 255, 200)]
        for row in range(3, (self.top_height - 20) // 25):
            for col in range(2):
                window_x = self.x + 10 + col * 25
                window_y = 15 + row * 25
                if window_y < self.top_height - 15:
                    window_color = random.choice(window_colors)
                    pygame.draw.rect(screen, window_color, (window_x, window_y, 15, 12))
                    pygame.draw.rect(screen, BLACK, (window_x, window_y, 15, 12), 1)

        for row in range(3, (self.bottom_height - 20) // 25):
            for col in range(2):
                window_x = self.x + 10 + col * 25
                window_y = bottom_y + 15 + row * 25
                if window_y < bottom_y + self.bottom_height - 15:
                    window_color = random.choice(window_colors)
                    pygame.draw.rect(screen, window_color, (window_x, window_y, 15, 12))
                    pygame.draw.rect(screen, BLACK, (window_x, window_y, 15, 12), 1)

    def draw_forest_pipe(self, screen):
        # Tree-like pipes
        pygame.draw.rect(screen, BROWN, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Tree top
        pygame.draw.circle(screen, DARK_GREEN, (self.x + PIPE_WIDTH//2, self.top_height - 20), 30)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, BROWN, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Tree top
        pygame.draw.circle(screen, DARK_GREEN, (self.x + PIPE_WIDTH//2, bottom_y + 20), 30)

    def draw_mountain_pipe(self, screen):
        # Rock-like pipes
        color = DARK_GRAY
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Snow caps
        pygame.draw.rect(screen, WHITE, (self.x - 5, self.top_height - 15, PIPE_WIDTH + 10, 15))
        pygame.draw.rect(screen, WHITE, (self.x - 5, bottom_y, PIPE_WIDTH + 10, 15))

    def draw_desert_pipe(self, screen):
        # Sand-like pipes
        color = GOLD
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Cactus details
        for y in range(20, self.top_height - 20, 40):
            pygame.draw.rect(screen, DARK_GREEN, (self.x + 15, y, 10, 20))
        for y in range(bottom_y + 20, bottom_y + self.bottom_height - 20, 40):
            pygame.draw.rect(screen, DARK_GREEN, (self.x + 15, y, 10, 20))

    def draw_space_pipe(self, screen):
        # Space station-like pipes
        color = SILVER
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, WHITE, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, WHITE, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Lights
        for y in range(10, self.top_height - 10, 20):
            pygame.draw.circle(screen, RED, (self.x + 10, y), 3)
            pygame.draw.circle(screen, BLUE, (self.x + PIPE_WIDTH - 10, y), 3)
        for y in range(bottom_y + 10, bottom_y + self.bottom_height - 10, 20):
            pygame.draw.circle(screen, RED, (self.x + 10, y), 3)
            pygame.draw.circle(screen, BLUE, (self.x + PIPE_WIDTH - 10, y), 3)

    def draw_ocean_pipe(self, screen):
        # Ocean-like pipes
        color = LIGHT_BLUE
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Fish
        for i in range(0, PIPE_WIDTH, 10):
            pygame.draw.circle(screen, WHITE, (self.x + i + 5, bottom_y + 50), 10)

    def draw_sunset_pipe(self, screen):
        # Sunset-like pipes
        color = ORANGE
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Sun
        pygame.draw.circle(screen, YELLOW, (self.x + PIPE_WIDTH//2, self.top_height - 50), 40)
        pygame.draw.circle(screen, YELLOW, (self.x + PIPE_WIDTH//2, self.top_height - 50), 30)

    def draw_winter_pipe(self, screen):
        # Winter-like pipes
        color = WHITE
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Snowflake
        pygame.draw.circle(screen, WHITE, (self.x + PIPE_WIDTH//2, self.top_height - 50), 20)

    def draw_volcano_pipe(self, screen):
        # Volcano-like pipes
        color = RED
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Lava
        pygame.draw.rect(screen, (255, 100, 0), (self.x - 5, self.top_height - 15, PIPE_WIDTH + 10, 15))
        pygame.draw.rect(screen, (255, 100, 0), (self.x - 5, bottom_y, PIPE_WIDTH + 10, 15))

    def draw_neon_city_pipe(self, screen):
        # Neon city-like pipes
        color = SILVER
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, WHITE, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, WHITE, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Lights
        for y in range(10, self.top_height - 10, 20):
            pygame.draw.circle(screen, RED, (self.x + 10, y), 3)
            pygame.draw.circle(screen, BLUE, (self.x + PIPE_WIDTH - 10, y), 3)
        for y in range(bottom_y + 10, bottom_y + self.bottom_height - 10, 20):
            pygame.draw.circle(screen, RED, (self.x + 10, y), 3)
            pygame.draw.circle(screen, BLUE, (self.x + PIPE_WIDTH - 10, y), 3)

    def draw_candy_land_pipe(self, screen):
        # Candy land-like pipes
        color = PURPLE
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, WHITE, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, WHITE, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Candy cane
        pygame.draw.line(screen, WHITE, (self.x + PIPE_WIDTH//2, self.top_height - 50), (self.x + PIPE_WIDTH//2 + 10, self.top_height - 50 + 10), 3)

    def draw_underwater_pipe(self, screen):
        # Coral-like pipes
        color = (255, 182, 193)  # Light coral
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Coral details
        for i in range(0, self.top_height - 20, 30):
            pygame.draw.circle(screen, (255, 20, 147), (self.x + 20, i + 20), 8)
            pygame.draw.circle(screen, (255, 105, 180), (self.x + 40, i + 30), 6)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Coral details
        for i in range(0, self.bottom_height - 20, 30):
            pygame.draw.circle(screen, (255, 20, 147), (self.x + 20, bottom_y + i + 20), 8)
            pygame.draw.circle(screen, (255, 105, 180), (self.x + 40, bottom_y + i + 30), 6)

    def draw_cyberpunk_pipe(self, screen):
        # Cyberpunk pipes with neon effects
        color = (20, 20, 20)
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, (0, 255, 255), (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Circuit patterns
        for i in range(0, self.top_height - 10, 20):
            pygame.draw.line(screen, (0, 255, 255), (self.x + 10, i + 10), (self.x + PIPE_WIDTH - 10, i + 10), 2)
            pygame.draw.circle(screen, (255, 0, 255), (self.x + 20, i + 10), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, (0, 255, 255), (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Circuit patterns
        for i in range(0, self.bottom_height - 10, 20):
            pygame.draw.line(screen, (0, 255, 255), (self.x + 10, bottom_y + i + 10), (self.x + PIPE_WIDTH - 10, bottom_y + i + 10), 2)
            pygame.draw.circle(screen, (255, 0, 255), (self.x + 20, bottom_y + i + 10), 3)

    def draw_fantasy_pipe(self, screen):
        # Crystal-like pipes
        color = (138, 43, 226)  # Blue violet
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Crystal facets
        for i in range(0, self.top_height - 20, 25):
            points = [(self.x + 10, i + 10), (self.x + 30, i + 5), (self.x + 50, i + 10), (self.x + 30, i + 20)]
            pygame.draw.polygon(screen, (255, 255, 255), points)
            pygame.draw.polygon(screen, (138, 43, 226), points, 2)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Crystal facets
        for i in range(0, self.bottom_height - 20, 25):
            points = [(self.x + 10, bottom_y + i + 10), (self.x + 30, bottom_y + i + 5), (self.x + 50, bottom_y + i + 10), (self.x + 30, bottom_y + i + 20)]
            pygame.draw.polygon(screen, (255, 255, 255), points)
            pygame.draw.polygon(screen, (138, 43, 226), points, 2)

    def draw_steampunk_pipe(self, screen):
        # Brass steampunk pipes
        color = (205, 133, 63)  # Peru (brass-like)
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, (139, 69, 19), (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Rivets and bolts
        for i in range(0, self.top_height - 10, 30):
            pygame.draw.circle(screen, (139, 69, 19), (self.x + 10, i + 15), 4)
            pygame.draw.circle(screen, (139, 69, 19), (self.x + PIPE_WIDTH - 10, i + 15), 4)
            pygame.draw.circle(screen, (139, 69, 19), (self.x + PIPE_WIDTH//2, i + 15), 4)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, (139, 69, 19), (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Rivets and bolts
        for i in range(0, self.bottom_height - 10, 30):
            pygame.draw.circle(screen, (139, 69, 19), (self.x + 10, bottom_y + i + 15), 4)
            pygame.draw.circle(screen, (139, 69, 19), (self.x + PIPE_WIDTH - 10, bottom_y + i + 15), 4)
            pygame.draw.circle(screen, (139, 69, 19), (self.x + PIPE_WIDTH//2, bottom_y + i + 15), 4)

    def draw_apocalypse_pipe(self, screen):
        # Rusty apocalyptic pipes
        color = (139, 69, 19)  # Saddle brown
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, (101, 67, 33), (self.x, 0, PIPE_WIDTH, self.top_height), 3)

        # Rust spots
        for i in range(0, self.top_height - 10, 20):
            rust_x = self.x + random.randint(5, PIPE_WIDTH - 15)
            rust_y = i + random.randint(5, 15)
            pygame.draw.circle(screen, (139, 0, 0), (rust_x, rust_y), 3)

        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, (101, 67, 33), (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)

        # Rust spots
        for i in range(0, self.bottom_height - 10, 20):
            rust_x = self.x + random.randint(5, PIPE_WIDTH - 15)
            rust_y = bottom_y + i + random.randint(5, 15)
            pygame.draw.circle(screen, (139, 0, 0), (rust_x, rust_y), 3)

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2, PIPE_WIDTH, self.bottom_height)
        return top_rect, bottom_rect

class Powerup:
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.powerup_type = powerup_type
        self.rect = pygame.Rect(x, y, 40, 40)
        self.collected = False
        self.animation_time = 0

        # Powerup types and their properties
        self.powerup_data = {
            'health': {'color': RED, 'symbol': '♥', 'duration': 0},
            'speed': {'color': BLUE, 'symbol': '⚡', 'duration': 5000},
            'invincible': {'color': YELLOW, 'symbol': '★', 'duration': 5000},
            'double_points': {'color': GOLD, 'symbol': '2×', 'duration': 4000}
        }

    def update(self, pipe_speed):
        self.x -= pipe_speed
        self.rect.x = self.x
        self.animation_time += 1

        if self.x < -50:
            self.collected = True

    def draw(self, screen):
        if not self.collected:
            data = self.powerup_data[self.powerup_type]

            # Animated floating effect
            float_offset = math.sin(self.animation_time * 0.1) * 3

            # Draw powerup background (bigger)
            pygame.draw.circle(screen, data['color'],
                             (int(self.x + 15), int(self.y + 15 + float_offset)), 20)
            pygame.draw.circle(screen, WHITE,
                             (int(self.x + 15), int(self.y + 15 + float_offset)), 20, 3)

            # Draw symbol (bigger font)
            symbol_font = pygame.font.Font(None, 36)
            symbol_text = symbol_font.render(data['symbol'], True, WHITE)
            symbol_rect = symbol_text.get_rect(center=(self.x + 15, self.y + 15 + float_offset))
            screen.blit(symbol_text, symbol_rect)

            # Draw sparkle effect
            if self.animation_time % 20 < 10:
                for i in range(4):
                    angle = (self.animation_time * 5 + i * 90) * math.pi / 180
                    sparkle_x = self.x + 15 + math.cos(angle) * 20
                    sparkle_y = self.y + 15 + float_offset + math.sin(angle) * 20
                    pygame.draw.circle(screen, WHITE, (int(sparkle_x), int(sparkle_y)), 2)


class Game:
    def __init__(self):
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.powerups = []
        self.background = Background()
        self.score = 0
        self.high_score = self.load_high_score()
        self.lives = 3
        self.game_over = False
        self.game_started = False
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 48)

        # Powerup effects
        self.speed_boost = False
        self.invincible = False
        self.double_points = False
        self.powerup_timers = {}
        self.last_collision_time = 0  # Track last collision to prevent rapid consecutive collisions
        self.pipe_speed = PIPE_SPEED

        # Music management
        self.current_theme_song = None
        self.change_theme_music('city')  # Start with city theme music

        for i in range(3):
            self.pipes.append(Pipe(SCREEN_WIDTH + i * 300, self.background.current_theme))

        # Add initial powerup
        self.spawn_powerup()

    def change_theme_music(self, theme):
        """Change the background music based on the current theme"""
        try:
            # Stop current music if playing
            if self.current_theme_song:
                self.current_theme_song.stop()

            # Create and play new theme music
            self.current_theme_song = create_theme_song(theme)
            if self.current_theme_song:
                self.current_theme_song.play(-1)  # Loop indefinitely
                print(f"🎵 Now playing {theme} theme music!")
        except Exception as e:
            print(f"❌ Error changing theme music: {e}")

    def spawn_powerup(self):
        """Spawn a random powerup"""
        if len(self.powerups) < 2:  # Max 2 powerups at once
            powerup_types = ['health', 'speed', 'invincible', 'double_points']
            powerup_type = random.choice(powerup_types)

            # Spawn powerup in a random position
            x = SCREEN_WIDTH + random.randint(100, 300)
            y = random.randint(100, SCREEN_HEIGHT - 200)

            self.powerups.append(Powerup(x, y, powerup_type))

    def apply_powerup(self, powerup_type):
        """Apply powerup effect"""
        powerup_data = {
            'health': {'color': RED, 'symbol': '♥', 'duration': 0},
            'speed': {'color': BLUE, 'symbol': '⚡', 'duration': 5000},
            'invincible': {'color': YELLOW, 'symbol': '★', 'duration': 5000},
            'double_points': {'color': GOLD, 'symbol': '2×', 'duration': 4000}
        }

        data = powerup_data[powerup_type]

        if powerup_type == 'health':
            self.lives += 1  # No cap on lives
            print("❤️ Health restored!")

        elif powerup_type == 'speed':
            self.speed_boost = True
            self.invincible = True  # Speed boost now includes invincibility
            self.powerup_timers['speed'] = pygame.time.get_ticks() + data['duration']
            self.powerup_timers['invincible'] = pygame.time.get_ticks() + data['duration']
            print("⚡ Speed boost with invincibility activated!")

        elif powerup_type == 'invincible':
            self.invincible = True
            self.powerup_timers['invincible'] = pygame.time.get_ticks() + data['duration']
            print("🛡️ Invincibility activated!")

        elif powerup_type == 'double_points':
            self.double_points = True
            self.powerup_timers['double_points'] = pygame.time.get_ticks() + data['duration']
            print("2× Double points activated!")

        # Play powerup sound
        if score_sound:
            score_sound.play()

    def update_powerup_timers(self):
        """Update powerup timers and deactivate expired effects"""
        current_time = pygame.time.get_ticks()

        for effect, end_time in list(self.powerup_timers.items()):
            if current_time > end_time:
                if effect == 'speed':
                    self.speed_boost = False
                    # Always add 4 seconds of invincibility after speed boost ends
                    self.invincible = True
                    self.powerup_timers['invincible'] = current_time + 4000  # 4000ms = 4 seconds
                    print("Speed boost ended! 4 seconds of invincibility granted!")
                elif effect == 'invincible':
                    self.invincible = False
                    print("Invincible effect ended!")
                elif effect == 'double_points':
                    self.double_points = False
                    print("Double_Points effect ended!")

                del self.powerup_timers[effect]
                if effect != 'invincible':  # Don't print for invincible since we handle it above
                    print(f"{effect.title()} effect ended!")

    def load_high_score(self):
        """Load high score from file"""
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        """Save high score to file"""
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except Exception as e:
            print(f"Could not save high score: {e}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__init__()
                    elif not self.game_started:
                        self.game_started = True
                        self.bird.flap()
                    else:
                        self.bird.flap()
        return True

    def get_pipe_speed(self):
        return PIPE_SPEED * 2 if self.speed_boost else PIPE_SPEED

    def update(self):
        if not self.game_over and self.game_started:
            # Update powerup timers
            self.update_powerup_timers()

            # Apply powerup effects to bird
            current_pipe_speed = self.get_pipe_speed()
            self.bird.update(speed_boost=self.speed_boost, pipe_speed=current_pipe_speed)
            self.background.update(current_pipe_speed)

            # Check if theme changed and update music
            old_theme = self.background.current_theme
            self.background.update_theme(self.score)
            if self.background.current_theme != old_theme:
                self.change_theme_music(self.background.current_theme)

            # Update pipes
            for pipe in self.pipes:
                pipe.x -= self.get_pipe_speed()

            self.pipes = [pipe for pipe in self.pipes if pipe.x > -PIPE_WIDTH]

            if len(self.pipes) < 3:
                self.pipes.append(Pipe(SCREEN_WIDTH + 300, self.background.current_theme))

            # Update powerups
            for powerup in self.powerups:
                powerup.update(self.get_pipe_speed())
            self.powerups = [p for p in self.powerups if not p.collected]

            # Spawn new powerups occasionally
            if random.random() < 0.005:  # 0.5% chance per frame
                self.spawn_powerup()

            bird_rect = self.bird.get_rect()

            # Check for powerup collection
            for powerup in self.powerups[:]:  # Copy list to avoid modification during iteration
                if bird_rect.colliderect(powerup.rect):
                    self.apply_powerup(powerup.powerup_type)
                    powerup.collected = True
                    self.powerups.remove(powerup)
                    if score_sound:
                        score_sound.play()

            # Check for collisions (only if not invincible)
            current_time = pygame.time.get_ticks()
            collision_detected = False

            # Only check collisions if enough time has passed since last collision
            if not self.invincible and (current_time - self.last_collision_time) > 500:  # 500ms delay
                # Check boundary collisions first
                if self.bird.y <= 0 or self.bird.y >= SCREEN_HEIGHT - BIRD_SIZE:
                    self.lives -= 1
                    collision_detected = True
                    self.last_collision_time = current_time
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        # Reset bird position and velocity
                        self.bird.x = 100
                        self.bird.y = SCREEN_HEIGHT // 2
                        self.bird.velocity = 0
                    if crash_sound:
                        crash_sound.play()

                # Check pipe collisions (only if no boundary collision was detected)
                if not collision_detected:
                    for pipe in self.pipes:
                        top_rect, bottom_rect = pipe.get_rects()
                        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                            self.lives -= 1
                            collision_detected = True
                            self.last_collision_time = current_time
                            if self.lives <= 0:
                                self.game_over = True
                            else:
                                # Reset bird position and velocity
                                self.bird.x = 100
                                self.bird.y = SCREEN_HEIGHT // 2
                                self.bird.velocity = 0
                            if crash_sound:
                                crash_sound.play()
                            break

            # Score points
            for pipe in self.pipes:
                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    points = 2 if self.double_points else 1
                    self.score += points
                    if score_sound:
                        score_sound.play()

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def draw(self):
        self.background.draw(screen)

        # Draw ground based on theme
        if self.background.current_theme == "city":
            pygame.draw.rect(screen, DARK_GRAY, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        elif self.background.current_theme == "forest":
            pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            # Add grass
            for i in range(0, SCREEN_WIDTH, 20):
                pygame.draw.line(screen, DARK_GREEN, (i, SCREEN_HEIGHT - 100), (i + 10, SCREEN_HEIGHT - 100), 3)
        elif self.background.current_theme == "mountains":
            pygame.draw.rect(screen, DARK_GRAY, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        elif self.background.current_theme == "desert":
            pygame.draw.rect(screen, GOLD, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        elif self.background.current_theme == "space":
            pygame.draw.rect(screen, DARK_BLUE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        elif self.background.current_theme == "ocean":
            pygame.draw.rect(screen, DARK_BLUE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            # Draw water gradient
            for y in range(SCREEN_HEIGHT - 100, SCREEN_HEIGHT):
                color_ratio = (SCREEN_HEIGHT - y) / (SCREEN_HEIGHT - (SCREEN_HEIGHT - 100))
                r = int(135 + (100 - 135) * color_ratio)
                g = int(206 + (150 - 206) * color_ratio)
                b = int(235 + (200 - 235) * color_ratio)
                pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        elif self.background.current_theme == "sunset":
            pygame.draw.rect(screen, DARK_GRAY, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            # Draw sky gradient
            for y in range(SCREEN_HEIGHT - 100):
                color_ratio = y / (SCREEN_HEIGHT - 100)
                r = int(135 + (255 - 135) * color_ratio)
                g = int(206 + (200 - 206) * color_ratio)
                b = int(235 + (100 - 235) * color_ratio)
                pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

            # Draw mountains
            for mountain in self.background.mountains:
                points = [(mountain['x'], SCREEN_HEIGHT - 100),
                         (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                         (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
                pygame.draw.polygon(screen, mountain['color'], points)
                pygame.draw.polygon(screen, BLACK, points, 2)

            # Draw clouds
            for cloud in self.background.clouds:
                pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

        elif self.background.current_theme == "winter":
            pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            # Draw snowflakes
            for snowflake in self.background.snowflakes:
                pygame.draw.circle(screen, WHITE, (snowflake['x'], snowflake['y']), snowflake['size'])

            # Draw mountains
            for mountain in self.background.mountains:
                points = [(mountain['x'], SCREEN_HEIGHT - 100),
                         (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                         (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
                pygame.draw.polygon(screen, mountain['color'], points)
                pygame.draw.polygon(screen, BLACK, points, 2)

            # Draw clouds
            for cloud in self.background.clouds:
                pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

        elif self.background.current_theme == "volcano":
            pygame.draw.rect(screen, RED, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            # Draw lava particles
            for lava_particle in self.background.lava_particles:
                pygame.draw.circle(screen, lava_particle['color'], (lava_particle['x'], lava_particle['y']), lava_particle['size'])

            # Draw mountains
            for mountain in self.background.mountains:
                points = [(mountain['x'], SCREEN_HEIGHT - 100),
                         (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                         (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
                pygame.draw.polygon(screen, mountain['color'], points)
                pygame.draw.polygon(screen, BLACK, points, 2)

            # Draw clouds
            for cloud in self.background.clouds:
                pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

        elif self.background.current_theme == "neon_city":
            pygame.draw.rect(screen, DARK_BLUE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            # Draw neon lights
            for neon_light in self.background.neon_lights:
                pygame.draw.circle(screen, neon_light['color'], (neon_light['x'], neon_light['y']), neon_light['size'])

            # Draw buildings
            for building in self.background.buildings:
                pygame.draw.rect(screen, building['color'],
                               (building['x'], SCREEN_HEIGHT - 100 - building['height'],
                                60, building['height']))
                pygame.draw.rect(screen, BLACK,
                               (building['x'], SCREEN_HEIGHT - 100 - building['height'],
                                60, building['height']), 2)

                # Windows
                for window_y in range(building['height'] - 20, 0, 30):
                    for window_x in range(10, 50, 15):
                        if random.random() > 0.3:  # Some windows lit
                            pygame.draw.rect(screen, YELLOW,
                                           (building['x'] + window_x,
                                            SCREEN_HEIGHT - 100 - building['height'] + window_y,
                                            8, 8))

            # Draw clouds
            for cloud in self.background.clouds:
                pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

        elif self.background.current_theme == "candy_land":
            pygame.draw.rect(screen, PURPLE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            # Draw candy elements
            for candy_element in self.background.candy_elements:
                if candy_element['type'] == 'heart':
                    pygame.draw.circle(screen, candy_element['color'], (candy_element['x'], candy_element['y']), candy_element['size'])
                elif candy_element['type'] == 'star':
                    pygame.draw.circle(screen, candy_element['color'], (candy_element['x'], candy_element['y']), candy_element['size'])
                elif candy_element['type'] == 'diamond':
                    pygame.draw.rect(screen, candy_element['color'], (candy_element['x'], candy_element['y'], candy_element['size'], candy_element['size']))
                elif candy_element['type'] == 'candy_cane':
                    pygame.draw.line(screen, candy_element['color'], (candy_element['x'], candy_element['y']), (candy_element['x'] + candy_element['size'], candy_element['y'] + candy_element['size']), 3)

            # Draw mountains
            for mountain in self.background.mountains:
                points = [(mountain['x'], SCREEN_HEIGHT - 100),
                         (mountain['x'] + 75, SCREEN_HEIGHT - 100 - mountain['height']),
                         (mountain['x'] + 150, SCREEN_HEIGHT - 100)]
                pygame.draw.polygon(screen, mountain['color'], points)
                pygame.draw.polygon(screen, BLACK, points, 2)

            # Draw clouds
            for cloud in self.background.clouds:
                pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])

        for pipe in self.pipes:
            pipe.draw(screen, self.background.current_theme)

        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(screen)

        self.bird.draw(screen)

        # Draw score
        score_text = self.font.render(str(self.score), True, WHITE)
        score_text.set_alpha(200)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))

        # Draw lives with heart symbols
        if self.lives <= 6:
            heart_symbols = "♥" * self.lives
            lives_text = self.small_font.render(f"Lives: {heart_symbols}", True, GOLD)
        else:
            lives_text = self.small_font.render(f"Lives: {self.lives} ♥", True, GOLD)
        lives_text.set_alpha(200)
        screen.blit(lives_text, (SCREEN_WIDTH - 200, 10))

        # Draw high score
        high_score_text = self.small_font.render(f"Best: {self.high_score}", True, WHITE)
        high_score_text.set_alpha(150)
        screen.blit(high_score_text, (10, 10))

        # Draw theme
        theme_text = self.small_font.render(f"Theme: {self.background.current_theme.title()}", True, WHITE)
        theme_text.set_alpha(150)
        screen.blit(theme_text, (10, 40))

        # Draw active powerup effects
        effect_y = 70
        for effect, end_time in self.powerup_timers.items():
            remaining_time = max(0, (end_time - pygame.time.get_ticks()) / 1000)
            if remaining_time > 0:
                effect_symbols = {
                    'speed': '⚡',
                    'invincible': '★',
                    'double_points': '2×'
                }
                effect_text = self.small_font.render(
                    f"{effect_symbols.get(effect, effect)} {remaining_time:.1f}s",
                    True, YELLOW
                )
                screen.blit(effect_text, (10, effect_y))
                effect_y += 25

        # Draw invincibility effect on bird
        if self.invincible:
            # Create a pulsing shield effect
            shield_alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.01))
            shield_surface = pygame.Surface((BIRD_SIZE + 20, BIRD_SIZE + 20), pygame.SRCALPHA)
            shield_surface.set_alpha(shield_alpha)
            pygame.draw.circle(shield_surface, YELLOW, (BIRD_SIZE//2 + 10, BIRD_SIZE//2 + 10), BIRD_SIZE//2 + 15, 3)
            screen.blit(shield_surface, (self.bird.x - 10, self.bird.y - 10))

        if not self.game_started and not self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            title_text = self.font.render("FLAPPY ADVENTURE", True, YELLOW)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))

            instruction1 = self.medium_font.render("Press SPACE to start", True, WHITE)
            instruction2 = self.small_font.render("🎵 Now with the Flappy Adventure song!", True, WHITE)
            instruction3 = self.small_font.render("Listen to the classic melody", True, WHITE)
            instruction4 = self.small_font.render("💎 Collect powerups for special abilities!", True, WHITE)

            screen.blit(instruction1, (SCREEN_WIDTH // 2 - instruction1.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(instruction2, (SCREEN_WIDTH // 2 - instruction2.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(instruction3, (SCREEN_WIDTH // 2 - instruction3.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
            screen.blit(instruction4, (SCREEN_WIDTH // 2 - instruction4.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

            self.bird.draw(screen)

        elif self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.medium_font.render("Press SPACE to restart", True, WHITE)
            final_score_text = self.medium_font.render(f"Score: {self.score}", True, WHITE)
            high_score_text = self.medium_font.render(f"Best: {self.high_score}", True, GOLD)

            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

            # Show new high score celebration
            if self.score == self.high_score and self.score > 0:
                new_record_text = self.medium_font.render("🏆 NEW RECORD! 🏆", True, YELLOW)
                screen.blit(new_record_text, (SCREEN_WIDTH // 2 - new_record_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))

        pygame.display.flip()

def main():
    game = Game()
    running = True

    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()