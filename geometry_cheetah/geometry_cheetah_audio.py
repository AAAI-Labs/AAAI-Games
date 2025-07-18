import pygame
import random
import math
import os
import numpy as np
from enum import Enum

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (150, 100, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
LIME = (50, 255, 50)
BROWN = (139, 69, 19)
DARK_ORANGE = (255, 140, 0)
LIGHT_ORANGE = (255, 200, 100)

# Game constants
GRAVITY = 0.8
JUMP_FORCE = -18
GROUND_Y = SCREEN_HEIGHT - 100
MIN_OBSTACLE_SPACING = 250

class GameState(Enum):
    MENU = 1
    LEVEL_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4
    LEVEL_COMPLETE = 5

class Background:
    def __init__(self):
        self.clouds = []
        self.stars = []
        self.parallax_offset = 0
        
        # Generate clouds
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 200),
                'size': random.randint(30, 80)
            })
            
        # Generate stars
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, 300),
                'brightness': random.randint(100, 255)
            })
    
    def update(self):
        # Update parallax offset
        self.parallax_offset += 2 * 0.5
        
        # Update clouds
        for cloud in self.clouds:
            cloud['x'] -= 1
            if cloud['x'] + cloud['size'] < 0:
                cloud['x'] = SCREEN_WIDTH + cloud['size']
                cloud['y'] = random.randint(50, 200)
                
        # Update stars
        for star in self.stars:
            star['x'] -= 0.5
            if star['x'] < 0:
                star['x'] = SCREEN_WIDTH
                star['y'] = random.randint(0, 300)
    
    def draw(self, screen):
        # Draw gradient sky
        for y in range(300):
            color_ratio = y / 300
            r = int(100 + color_ratio * 50)
            g = int(150 + color_ratio * 100)
            b = int(255 - color_ratio * 100)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw stars
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), 1)
        
        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (int(cloud['x']), int(cloud['y'])), cloud['size'])
            pygame.draw.circle(screen, WHITE, (int(cloud['x'] - 20), int(cloud['y'])), cloud['size'] - 10)
            pygame.draw.circle(screen, WHITE, (int(cloud['x'] + 20), int(cloud['y'])), cloud['size'] - 10)
        
        # Draw ground
        pygame.draw.rect(screen, GREEN, (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
        
        # Draw grass texture
        for i in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(screen, (50, 200, 50), (i, GROUND_Y), (i + 10, GROUND_Y - 5), 2)

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.load_sounds()
        
    def load_sounds(self):
        """Load all sound effects"""
        try:
            # Create simple sound effects using pygame's built-in sound generation
            self.create_jump_sound()
            self.create_land_sound()
            self.create_death_sound()
            self.create_score_sound()
            self.create_level_complete_sound()
            self.create_menu_select_sound()
            self.create_bounce_sound()
        except Exception as e:
            print(f"Could not load sounds: {e}")
    
    def create_jump_sound(self):
        """Create a jump sound effect"""
        sample_rate = 44100
        duration = 0.2
        samples = int(sample_rate * duration)
        sound_array = np.zeros((samples, 2), dtype=np.int16)  # Stereo
        for i in range(samples):
            frequency = 400 + (i / samples) * 200  # Rising frequency
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array[i, 0] = sample
            sound_array[i, 1] = sample
        self.sounds['jump'] = pygame.sndarray.make_sound(sound_array)
    
    def create_land_sound(self):
        """Create a landing sound effect"""
        sample_rate = 44100
        duration = 0.15
        samples = int(sample_rate * duration)
        sound_array = np.zeros((samples, 2), dtype=np.int16)
        for i in range(samples):
            frequency = 200 * math.exp(-i / (samples * 0.3))  # Decaying frequency
            sample = int(32767 * 0.4 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array[i, 0] = sample
            sound_array[i, 1] = sample
        self.sounds['land'] = pygame.sndarray.make_sound(sound_array)
    
    def create_death_sound(self):
        """Create a death sound effect"""
        sample_rate = 44100
        duration = 0.5
        samples = int(sample_rate * duration)
        sound_array = np.zeros((samples, 2), dtype=np.int16)
        for i in range(samples):
            frequency = 600 * math.exp(-i / (samples * 0.5))  # Descending frequency
            sample = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array[i, 0] = sample
            sound_array[i, 1] = sample
        self.sounds['death'] = pygame.sndarray.make_sound(sound_array)
    
    def create_score_sound(self):
        """Create a score sound effect"""
        sample_rate = 44100
        duration = 0.1
        samples = int(sample_rate * duration)
        sound_array = np.zeros((samples, 2), dtype=np.int16)
        for i in range(samples):
            frequency = 800 + 200 * math.sin(i / samples * 4 * math.pi)
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array[i, 0] = sample
            sound_array[i, 1] = sample
        self.sounds['score'] = pygame.sndarray.make_sound(sound_array)
    
    def create_level_complete_sound(self):
        """Create a level complete sound effect"""
        sample_rate = 44100
        duration = 0.8
        samples = int(sample_rate * duration)
        sound_array = np.zeros((samples, 2), dtype=np.int16)
        for i in range(samples):
            if i < samples // 3:
                frequency = 523  # C note
            elif i < 2 * samples // 3:
                frequency = 659  # E note
            else:
                frequency = 784  # G note
            sample = int(32767 * 0.4 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array[i, 0] = sample
            sound_array[i, 1] = sample
        self.sounds['level_complete'] = pygame.sndarray.make_sound(sound_array)
    
    def create_menu_select_sound(self):
        """Create a menu selection sound effect"""
        sample_rate = 44100
        duration = 0.1
        samples = int(sample_rate * duration)
        sound_array = np.zeros((samples, 2), dtype=np.int16)
        for i in range(samples):
            frequency = 300
            sample = int(32767 * 0.2 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array[i, 0] = sample
            sound_array[i, 1] = sample
        self.sounds['menu_select'] = pygame.sndarray.make_sound(sound_array)
    
    def create_bounce_sound(self):
        """Create a bounce sound effect"""
        sample_rate = 44100
        duration = 0.15
        samples = int(sample_rate * duration)
        sound_array = np.zeros((samples, 2), dtype=np.int16)
        for i in range(samples):
            frequency = 600 * math.exp(-i / (samples * 0.2))
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array[i, 0] = sample
            sound_array[i, 1] = sample
        self.sounds['bounce'] = pygame.sndarray.make_sound(sound_array)
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def start_music(self):
        """Start background music"""
        if not self.music_playing:
            # Create a fun background music loop
            self.create_background_music()
            self.music_playing = True
    
    def create_background_music(self):
        """Create a fun background music loop"""
        sample_rate = 44100
        duration = 2.0  # 2 second loop
        samples = int(sample_rate * duration)
        
        # Create a fun upbeat melody
        music_array = np.zeros((samples, 2), dtype=np.int16)
        
        # Define a simple melody (C major scale)
        melody_notes = [
            (523, 0.2),   # C
            (587, 0.2),   # D
            (659, 0.2),   # E
            (698, 0.2),   # F
            (784, 0.2),   # G
            (880, 0.2),   # A
            (988, 0.2),   # B
            (1047, 0.2),  # C (octave)
            (988, 0.2),   # B
            (880, 0.2),   # A
            (784, 0.2),   # G
            (698, 0.2),   # F
            (659, 0.2),   # E
            (587, 0.2),   # D
            (523, 0.2),   # C
        ]
        
        sample_index = 0
        for note_freq, note_duration in melody_notes:
            note_samples = int(sample_rate * note_duration)
            for i in range(note_samples):
                if sample_index < samples:
                    # Create a pleasant sine wave with some harmonics
                    t = i / sample_rate
                    sample = int(32767 * 0.15 * (
                        math.sin(2 * math.pi * note_freq * t) +
                        0.3 * math.sin(2 * math.pi * note_freq * 2 * t) +  # Second harmonic
                        0.1 * math.sin(2 * math.pi * note_freq * 3 * t)    # Third harmonic
                    ))
                    music_array[sample_index, 0] = sample
                    music_array[sample_index, 1] = sample
                    sample_index += 1
        
        # Fill remaining samples with silence or repeat
        while sample_index < samples:
            music_array[sample_index, 0] = 0
            music_array[sample_index, 1] = 0
            sample_index += 1
        
        # Create the music sound and play it in a loop
        self.background_music = pygame.sndarray.make_sound(music_array)
        self.background_music.play(-1)  # -1 means loop indefinitely
    
    def stop_music(self):
        """Stop background music"""
        if self.music_playing:
            if hasattr(self, 'background_music'):
                self.background_music.stop()
            self.music_playing = False

class Level:
    def __init__(self, level_num, name, description, color):
        self.level_num = level_num
        self.name = name
        self.description = description
        self.color = color
        self.completed = False
        self.best_score = 0
        self.required_score = 0
        
        # Level-specific settings - NATURE THEMED OBSTACLES
        if level_num == 1:
            self.obstacle_speed = 4
            self.obstacle_spawn_rate = 0.02
            self.obstacle_types = ["thorny_bush", "rock"]
            self.platform_types = ["normal", "wide"]
            self.platform_spawn_rate = 0.03
            self.required_score = 20
            self.background_color = BLUE
        elif level_num == 2:
            self.obstacle_speed = 5
            self.obstacle_spawn_rate = 0.025
            self.obstacle_types = ["thorny_bush", "rock", "flying_bush"]
            self.platform_types = ["normal", "wide", "moving_slow"]
            self.platform_spawn_rate = 0.04
            self.required_score = 35
            self.background_color = PURPLE
        elif level_num == 3:
            self.obstacle_speed = 6
            self.obstacle_spawn_rate = 0.03
            self.obstacle_types = ["thorny_bush", "rock", "flying_bush", "double_bush"]
            self.platform_types = ["normal", "wide", "moving_slow", "bouncy"]
            self.platform_spawn_rate = 0.05
            self.required_score = 50
            self.background_color = RED
        elif level_num == 4:
            self.obstacle_speed = 7
            self.obstacle_spawn_rate = 0.035
            self.obstacle_types = ["thorny_bush", "rock", "flying_bush", "double_bush", "moving_rock"]
            self.platform_types = ["normal", "wide", "moving_slow", "bouncy", "disappearing_slow"]
            self.platform_spawn_rate = 0.06
            self.required_score = 70
            self.background_color = ORANGE
        elif level_num == 5:
            self.obstacle_speed = 8
            self.obstacle_spawn_rate = 0.04
            self.obstacle_types = ["thorny_bush", "rock", "flying_bush", "double_bush", "moving_rock", "laser"]
            self.platform_types = ["normal", "wide", "moving_slow", "bouncy", "disappearing_slow", "teleport_slow"]
            self.platform_spawn_rate = 0.07
            self.required_score = 100
            self.background_color = CYAN

class Cheetah:
    def __init__(self, x, y, audio_manager):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.is_on_ground = True
        self.is_on_platform = False
        self.animation_frame = 0
        self.animation_speed = 0.3
        self.rotation = 0
        self.trail_particles = []
        self.invincible = False
        self.invincible_timer = 0
        self.current_platform = None
        self.audio_manager = audio_manager
        self.was_on_platform = False  # Track platform state for sound effects
        
    def update(self, clouds):  # Changed from platforms to clouds
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Reset platform status
        self.is_on_platform = False
        self.current_platform = None
        
        # Check cloud collisions with LARGER collision box for easier landing
        for cloud in clouds:
            if self.check_cloud_collision(cloud):  # Changed from check_platform_collision
                if self.velocity_y > 0:  # Falling down
                    self.y = cloud.y - 40
                    self.velocity_y = 0
                    self.is_on_ground = True
                    self.is_jumping = False
                    self.is_on_platform = True
                    self.current_platform = cloud
                    
                    # Play landing sound if just landed on cloud
                    if not self.was_on_platform:
                        self.audio_manager.play_sound('land')
                    break
        
        # Ground collision (only if not on platform)
        if not self.is_on_platform and self.y >= GROUND_Y - 40:
            self.y = GROUND_Y - 40
            self.velocity_y = 0
            self.is_on_ground = True
            self.is_jumping = False
            
            # No sound effect for ground landing
        elif not self.is_on_platform:
            self.is_on_ground = False
        
        # Update platform state tracking
        self.was_on_platform = self.is_on_platform
            
        # Update animation
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 4:
            self.animation_frame = 0
            
        # Update rotation based on velocity
        if self.velocity_y < 0:
            self.rotation = -15
        elif self.velocity_y > 0:
            self.rotation = 15
        else:
            self.rotation = 0
            
        # Update invincibility
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
            
        # Update trail particles
        for particle in self.trail_particles[:]:
            particle['life'] -= 1
            particle['x'] -= 2
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
                
        # Add trail particles when moving
        if not self.is_on_ground and not self.is_on_platform and random.random() < 0.3:
            self.trail_particles.append({
                'x': self.x - 20,
                'y': self.y + 20,
                'life': 10,
                'color': ORANGE
            })
    
    def check_cloud_collision(self, cloud):  # Changed from check_platform_collision
        # LARGER collision box for easier cloud landing
        cheetah_rect = pygame.Rect(self.x - 25, self.y - 25, 50, 50)
        cloud_rect = cloud.get_rect()
        return cheetah_rect.colliderect(cloud_rect)
    
    def jump(self):
        if self.is_on_ground or self.is_on_platform:
            # Play jump sound
            self.audio_manager.play_sound('jump')
            
            # Special jump for bouncy clouds
            if self.current_platform and self.current_platform.cloud_type == "bouncy_cloud":  # Changed from platform_type
                self.velocity_y = JUMP_FORCE * 1.3  # Slightly higher jump
                self.audio_manager.play_sound('bounce')  # Play bounce sound for bouncy clouds
            else:
                self.velocity_y = JUMP_FORCE
            self.is_jumping = True
            self.is_on_ground = False
            self.is_on_platform = False
            
    def make_invincible(self, duration=60):
        self.invincible = True
        self.invincible_timer = duration
            
    def draw(self, screen):
        # Draw trail particles
        for particle in self.trail_particles:
            alpha = int((particle['life'] / 10) * 255)
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), 3)
        
        # Draw IMPROVED cheetah with better graphics
        cheetah_surface = pygame.Surface((80, 50), pygame.SRCALPHA)
        
        # Body (gradient orange with better shape)
        pygame.draw.ellipse(cheetah_surface, DARK_ORANGE, (15, 20, 45, 25))
        pygame.draw.ellipse(cheetah_surface, ORANGE, (18, 22, 39, 19))
        
        # Spots (more realistic)
        spots = [(20, 25), (30, 23), (40, 27), (25, 30), (35, 28), (45, 25)]
        for spot in spots:
            pygame.draw.circle(cheetah_surface, BLACK, spot, 3)
            pygame.draw.circle(cheetah_surface, DARK_GRAY, (spot[0]-1, spot[1]-1), 1)
        
        # Head (larger and more detailed)
        pygame.draw.circle(cheetah_surface, DARK_ORANGE, (55, 25), 15)
        pygame.draw.circle(cheetah_surface, ORANGE, (57, 27), 12)
        
        # Ears (more realistic)
        pygame.draw.circle(cheetah_surface, DARK_ORANGE, (62, 15), 6)
        pygame.draw.circle(cheetah_surface, DARK_ORANGE, (65, 18), 5)
        pygame.draw.circle(cheetah_surface, PINK, (63, 16), 3)
        pygame.draw.circle(cheetah_surface, PINK, (66, 19), 2)
        
        # Eyes (more expressive)
        pygame.draw.circle(cheetah_surface, WHITE, (60, 23), 4)
        pygame.draw.circle(cheetah_surface, WHITE, (63, 23), 4)
        pygame.draw.circle(cheetah_surface, BLACK, (61, 24), 2)
        pygame.draw.circle(cheetah_surface, BLACK, (64, 24), 2)
        pygame.draw.circle(cheetah_surface, WHITE, (61.5, 23.5), 1)
        pygame.draw.circle(cheetah_surface, WHITE, (64.5, 23.5), 1)
        
        # Nose
        pygame.draw.circle(cheetah_surface, BLACK, (68, 25), 2)
        
        # Mouth
        pygame.draw.arc(cheetah_surface, BLACK, (65, 25, 6, 4), 0, 3.14, 2)
        
        # Legs (more detailed)
        pygame.draw.rect(cheetah_surface, DARK_ORANGE, (20, 35, 5, 12))
        pygame.draw.rect(cheetah_surface, DARK_ORANGE, (30, 35, 5, 12))
        pygame.draw.rect(cheetah_surface, DARK_ORANGE, (40, 35, 5, 12))
        pygame.draw.rect(cheetah_surface, DARK_ORANGE, (50, 35, 5, 12))
        
        # Paws
        pygame.draw.circle(cheetah_surface, BLACK, (22, 47), 2)
        pygame.draw.circle(cheetah_surface, BLACK, (32, 47), 2)
        pygame.draw.circle(cheetah_surface, BLACK, (42, 47), 2)
        pygame.draw.circle(cheetah_surface, BLACK, (52, 47), 2)
        
        # Tail (more detailed)
        tail_points = [(15, 25), (8, 20), (2, 25), (8, 30), (15, 28)]
        pygame.draw.polygon(cheetah_surface, DARK_ORANGE, tail_points)
        pygame.draw.polygon(cheetah_surface, ORANGE, [(12, 25), (8, 22), (5, 25), (8, 28)])
        
        # Tail tip
        pygame.draw.circle(cheetah_surface, BLACK, (3, 25), 2)
        
        # Rotate the cheetah
        rotated_surface = pygame.transform.rotate(cheetah_surface, self.rotation)
        
        # Apply invincibility effect
        if self.invincible and self.invincible_timer % 10 < 5:
            # Make cheetah flash when invincible
            pass  # Skip drawing to create flash effect
        else:
            # Draw to screen
            screen.blit(rotated_surface, (self.x - rotated_surface.get_width()//2, 
                                         self.y - rotated_surface.get_height()//2))

class CloudPlatform:
    def __init__(self, x, y, cloud_type="small_cloud", level_settings=None):
        self.x = x
        self.y = y
        self.cloud_type = cloud_type
        self.level_settings = level_settings or Level(1, "Tutorial", "Easy level", BLUE)
        self.movement_timer = 0
        self.original_y = y
        self.visible = True
        self.bounce_timer = 0
        self.lightning_timer = 0
        self.trail_particles = []
        
        # Set properties based on cloud type
        if cloud_type == "small_cloud":
            self.width = 80
            self.height = 40
            self.color = WHITE
            self.speed = 2
        elif cloud_type == "medium_cloud":
            self.width = 120
            self.height = 50
            self.color = WHITE
            self.speed = 1.5
        elif cloud_type == "large_cloud":
            self.width = 160
            self.height = 60
            self.color = WHITE
            self.speed = 1
        elif cloud_type == "moving_cloud":
            self.width = 100
            self.height = 45
            self.color = CYAN
            self.speed = 2.5
            self.movement_range = 50
        elif cloud_type == "disappearing_cloud":
            self.width = 90
            self.height = 42
            self.color = YELLOW
            self.speed = 2
            self.disappear_timer = 0
            self.warning_timer = 0
        elif cloud_type == "bouncy_cloud":
            self.width = 95
            self.height = 45
            self.color = PINK
            self.speed = 2
            self.bounce_strength = 1.5
        elif cloud_type == "storm_cloud":
            self.width = 140
            self.height = 55
            self.color = DARK_GRAY
            self.speed = 1.8
            self.lightning_active = False
        
    def update(self):
        self.x -= self.level_settings.obstacle_speed
        self.movement_timer += 1
        
        # Update trail particles
        for particle in self.trail_particles[:]:
            particle['life'] -= 1
            particle['x'] -= 1
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
        
        # Add trail particles for moving clouds
        if self.cloud_type == "moving_cloud" and random.random() < 0.3:
            self.trail_particles.append({
                'x': self.x + self.width,
                'y': self.y + self.height//2,
                'life': 15,
                'color': CYAN
            })
        
        # Special movement for moving clouds
        if self.cloud_type == "moving_cloud":
            self.y = self.original_y + math.sin(self.movement_timer * 0.05) * self.movement_range
        
        # Disappearing cloud logic
        elif self.cloud_type == "disappearing_cloud":
            self.disappear_timer += 1
            self.warning_timer += 1
            if self.disappear_timer > 180:  # Disappear after 3 seconds
                self.visible = False
        
        # Bouncy cloud animation
        elif self.cloud_type == "bouncy_cloud":
            self.bounce_timer += 1
            bounce_offset = math.sin(self.bounce_timer * 0.2) * 3
            self.y = self.original_y + bounce_offset
        
        # Storm cloud lightning
        elif self.cloud_type == "storm_cloud":
            self.lightning_timer += 1
            if self.lightning_timer > 120:  # Lightning every 2 seconds
                self.lightning_active = True
                self.lightning_timer = 0
            elif self.lightning_timer > 10:
                self.lightning_active = False
    
    def draw_small_cloud(self, screen):
        # Draw small fluffy cloud
        pygame.draw.circle(screen, self.color, (self.x + 20, self.y + 20), 15)
        pygame.draw.circle(screen, self.color, (self.x + 35, self.y + 15), 12)
        pygame.draw.circle(screen, self.color, (self.x + 50, self.y + 20), 15)
        pygame.draw.circle(screen, self.color, (self.x + 35, self.y + 30), 10)
        
        # Add shadow
        shadow_color = (200, 200, 200)
        pygame.draw.circle(screen, shadow_color, (self.x + 22, self.y + 22), 13)
        pygame.draw.circle(screen, shadow_color, (self.x + 37, self.y + 17), 10)
        pygame.draw.circle(screen, shadow_color, (self.x + 52, self.y + 22), 13)
        pygame.draw.circle(screen, shadow_color, (self.x + 37, self.y + 32), 8)
    
    def draw_medium_cloud(self, screen):
        # Draw medium cloud with more detail
        pygame.draw.circle(screen, self.color, (self.x + 25, self.y + 25), 20)
        pygame.draw.circle(screen, self.color, (self.x + 45, self.y + 20), 18)
        pygame.draw.circle(screen, self.color, (self.x + 65, self.y + 25), 20)
        pygame.draw.circle(screen, self.color, (self.x + 85, self.y + 20), 15)
        pygame.draw.circle(screen, self.color, (self.x + 45, self.y + 35), 15)
        pygame.draw.circle(screen, self.color, (self.x + 65, self.y + 35), 12)
        
        # Add shadow
        shadow_color = (200, 200, 200)
        pygame.draw.circle(screen, shadow_color, (self.x + 27, self.y + 27), 18)
        pygame.draw.circle(screen, shadow_color, (self.x + 47, self.y + 22), 16)
        pygame.draw.circle(screen, shadow_color, (self.x + 67, self.y + 27), 18)
        pygame.draw.circle(screen, shadow_color, (self.x + 87, self.y + 22), 13)
        pygame.draw.circle(screen, shadow_color, (self.x + 47, self.y + 37), 13)
        pygame.draw.circle(screen, shadow_color, (self.x + 67, self.y + 37), 10)
    
    def draw_large_cloud(self, screen):
        # Draw large cloud with maximum detail
        pygame.draw.circle(screen, self.color, (self.x + 30, self.y + 30), 25)
        pygame.draw.circle(screen, self.color, (self.x + 55, self.y + 25), 23)
        pygame.draw.circle(screen, self.color, (self.x + 80, self.y + 30), 25)
        pygame.draw.circle(screen, self.color, (self.x + 105, self.y + 25), 20)
        pygame.draw.circle(screen, self.color, (self.x + 130, self.y + 30), 22)
        pygame.draw.circle(screen, self.color, (self.x + 55, self.y + 40), 18)
        pygame.draw.circle(screen, self.color, (self.x + 80, self.y + 40), 20)
        pygame.draw.circle(screen, self.color, (self.x + 105, self.y + 40), 15)
        
        # Add shadow
        shadow_color = (200, 200, 200)
        pygame.draw.circle(screen, shadow_color, (self.x + 32, self.y + 32), 23)
        pygame.draw.circle(screen, shadow_color, (self.x + 57, self.y + 27), 21)
        pygame.draw.circle(screen, shadow_color, (self.x + 82, self.y + 32), 23)
        pygame.draw.circle(screen, shadow_color, (self.x + 107, self.y + 27), 18)
        pygame.draw.circle(screen, shadow_color, (self.x + 132, self.y + 32), 20)
        pygame.draw.circle(screen, shadow_color, (self.x + 57, self.y + 42), 16)
        pygame.draw.circle(screen, shadow_color, (self.x + 82, self.y + 42), 18)
        pygame.draw.circle(screen, shadow_color, (self.x + 107, self.y + 42), 13)
    
    def draw_moving_cloud(self, screen):
        # Draw moving cloud with trail effect
        self.draw_medium_cloud(screen)
        
        # Draw trail particles
        for particle in self.trail_particles:
            alpha = particle['life'] / 15
            color = (*particle['color'], int(255 * alpha))
            pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), 3)
    
    def draw_disappearing_cloud(self, screen):
        # Draw disappearing cloud with warning effect
        self.draw_small_cloud(screen)
        
        # Warning effect when about to disappear
        if self.warning_timer > 150:
            if self.warning_timer % 30 < 15:
                pygame.draw.circle(screen, RED, (self.x + self.width//2, self.y + self.height//2), 25, 3)
    
    def draw_bouncy_cloud(self, screen):
        # Draw bouncy cloud with spring effect
        self.draw_medium_cloud(screen)
        
        # Add spring effect
        spring_color = (255, 255, 255)
        pygame.draw.rect(screen, spring_color, (self.x + 10, self.y + 10, self.width - 20, 8))
        pygame.draw.rect(screen, PINK, (self.x + 15, self.y + 12, self.width - 30, 4))
    
    def draw_storm_cloud(self, screen):
        # Draw storm cloud with lightning
        storm_color = (100, 100, 100)
        pygame.draw.circle(screen, storm_color, (self.x + 35, self.y + 30), 25)
        pygame.draw.circle(screen, storm_color, (self.x + 60, self.y + 25), 23)
        pygame.draw.circle(screen, storm_color, (self.x + 85, self.y + 30), 25)
        pygame.draw.circle(screen, storm_color, (self.x + 110, self.y + 25), 20)
        pygame.draw.circle(screen, storm_color, (self.x + 60, self.y + 40), 18)
        pygame.draw.circle(screen, storm_color, (self.x + 85, self.y + 40), 20)
        
        # Lightning effect
        if self.lightning_active:
            lightning_points = [
                (self.x + 20, self.y + 10),
                (self.x + 40, self.y + 25),
                (self.x + 30, self.y + 35),
                (self.x + 50, self.y + 45),
                (self.x + 70, self.y + 35),
                (self.x + 90, self.y + 45),
                (self.x + 110, self.y + 35)
            ]
            pygame.draw.lines(screen, YELLOW, False, lightning_points, 3)
    
    def draw(self, screen):
        if not self.visible:
            return
        
        # Draw based on cloud type
        if self.cloud_type == "small_cloud":
            self.draw_small_cloud(screen)
        elif self.cloud_type == "medium_cloud":
            self.draw_medium_cloud(screen)
        elif self.cloud_type == "large_cloud":
            self.draw_large_cloud(screen)
        elif self.cloud_type == "moving_cloud":
            self.draw_moving_cloud(screen)
        elif self.cloud_type == "disappearing_cloud":
            self.draw_disappearing_cloud(screen)
        elif self.cloud_type == "bouncy_cloud":
            self.draw_bouncy_cloud(screen)
        elif self.cloud_type == "storm_cloud":
            self.draw_storm_cloud(screen)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle:
    def __init__(self, x, obstacle_type="thorny_bush", level_settings=None):
        self.x = x
        self.obstacle_type = obstacle_type
        self.level_settings = level_settings or Level(1, "Tutorial", "Easy level", BLUE)
        self.width = 40
        self.movement_timer = 0
        self.original_y = 0
        self.animation_frame = 0
        
        # Set properties based on obstacle type
        if obstacle_type == "thorny_bush":
            self.height = 60
            self.color = GREEN
        elif obstacle_type == "rock":
            self.height = 50
            self.color = GRAY
        elif obstacle_type == "flying_bush":
            self.height = 55
            self.color = GREEN
            self.y_offset = -250
        elif obstacle_type == "double_bush":
            self.height = 60
            self.color = DARK_GRAY
            self.width = 80
        elif obstacle_type == "moving_rock":
            self.height = 50
            self.color = BROWN
            self.original_y = GROUND_Y - self.height
            self.y_offset = 0
        elif obstacle_type == "laser":
            self.height = 5
            self.color = YELLOW
            self.width = 100
            self.y_offset = -200
        
    def update(self):
        self.x -= self.level_settings.obstacle_speed
        self.movement_timer += 1
        self.animation_frame += 0.2
        
        # Special movement for moving obstacles
        if self.obstacle_type == "moving_rock":
            self.y_offset = math.sin(self.movement_timer * 0.1) * 30
        
    def draw(self, screen):
        if self.obstacle_type == "thorny_bush":
            self.draw_thorny_bush(screen)
        elif self.obstacle_type == "rock":
            self.draw_rock(screen)
        elif self.obstacle_type == "flying_bush":
            self.draw_flying_bush(screen)
        elif self.obstacle_type == "double_bush":
            self.draw_double_bush(screen)
        elif self.obstacle_type == "moving_rock":
            self.draw_moving_rock(screen)
        elif self.obstacle_type == "laser":
            pygame.draw.rect(screen, self.color, (self.x, GROUND_Y + self.y_offset, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x, GROUND_Y + self.y_offset, self.width, 2))
    
    def draw_thorny_bush(self, screen):
        """Draw a detailed thorny bush with animated swaying"""
        sway_offset = math.sin(self.animation_frame) * 3
        
        # Main bush body (multiple overlapping circles)
        bush_center_x = self.x + self.width // 2 + sway_offset
        bush_center_y = GROUND_Y - self.height // 2
        
        # Draw main bush body
        pygame.draw.circle(screen, GREEN, (bush_center_x, bush_center_y), 25)
        pygame.draw.circle(screen, (50, 150, 50), (bush_center_x - 8, bush_center_y - 5), 20)
        pygame.draw.circle(screen, (50, 150, 50), (bush_center_x + 8, bush_center_y - 5), 20)
        
        # Draw thorns (sharp points)
        thorns = [
            (bush_center_x - 15, bush_center_y - 15),
            (bush_center_x + 15, bush_center_y - 15),
            (bush_center_x - 10, bush_center_y - 25),
            (bush_center_x + 10, bush_center_y - 25),
            (bush_center_x, bush_center_y - 30),
            (bush_center_x - 20, bush_center_y - 5),
            (bush_center_x + 20, bush_center_y - 5)
        ]
        
        for thorn in thorns:
            # Draw thorn point
            pygame.draw.circle(screen, DARK_GRAY, (int(thorn[0]), int(thorn[1])), 3)
            # Draw thorn outline
            pygame.draw.circle(screen, BLACK, (int(thorn[0]), int(thorn[1])), 3, 1)
    
    def draw_rock(self, screen):
        """Draw a detailed rock with texture"""
        rock_rect = pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)
        
        # Main rock body
        pygame.draw.ellipse(screen, GRAY, rock_rect)
        pygame.draw.ellipse(screen, DARK_GRAY, rock_rect, 2)
        
        # Rock texture (cracks and details)
        center_x = self.x + self.width // 2
        center_y = GROUND_Y - self.height // 2
        
        # Draw cracks
        pygame.draw.line(screen, DARK_GRAY, (center_x - 10, center_y - 15), (center_x + 5, center_y + 10), 2)
        pygame.draw.line(screen, DARK_GRAY, (center_x - 5, center_y - 20), (center_x + 10, center_y - 5), 1)
        pygame.draw.line(screen, DARK_GRAY, (center_x + 5, center_y - 10), (center_x - 5, center_y + 15), 1)
        
        # Draw highlights
        pygame.draw.circle(screen, (200, 200, 200), (center_x - 8, center_y - 10), 3)
        pygame.draw.circle(screen, (180, 180, 180), (center_x + 8, center_y - 8), 2)
    
    def draw_flying_bush(self, screen):
        """Draw a flying thorny bush"""
        bush_center_x = self.x + self.width // 2
        bush_center_y = GROUND_Y + self.y_offset - self.height // 2
        
        # Main bush body
        pygame.draw.circle(screen, GREEN, (bush_center_x, bush_center_y), 25)
        pygame.draw.circle(screen, (50, 150, 50), (bush_center_x - 8, bush_center_y - 5), 20)
        pygame.draw.circle(screen, (50, 150, 50), (bush_center_x + 8, bush_center_y - 5), 20)
        
        # Flying thorns (more aggressive)
        thorns = [
            (bush_center_x - 18, bush_center_y - 18),
            (bush_center_x + 18, bush_center_y - 18),
            (bush_center_x - 12, bush_center_y - 28),
            (bush_center_x + 12, bush_center_y - 28),
            (bush_center_x, bush_center_y - 32),
            (bush_center_x - 22, bush_center_y - 8),
            (bush_center_x + 22, bush_center_y - 8)
        ]
        
        for thorn in thorns:
            pygame.draw.circle(screen, DARK_GRAY, (int(thorn[0]), int(thorn[1])), 4)
            pygame.draw.circle(screen, BLACK, (int(thorn[0]), int(thorn[1])), 4, 1)
    
    def draw_double_bush(self, screen):
        """Draw two thorny bushes side by side"""
        # First bush
        bush1_x = self.x + 20
        bush1_y = GROUND_Y - self.height // 2
        
        pygame.draw.circle(screen, GREEN, (bush1_x, bush1_y), 25)
        pygame.draw.circle(screen, (50, 150, 50), (bush1_x - 8, bush1_y - 5), 20)
        pygame.draw.circle(screen, (50, 150, 50), (bush1_x + 8, bush1_y - 5), 20)
        
        # Second bush
        bush2_x = self.x + 60
        bush2_y = GROUND_Y - self.height // 2
        
        pygame.draw.circle(screen, GREEN, (bush2_x, bush2_y), 25)
        pygame.draw.circle(screen, (50, 150, 50), (bush2_x - 8, bush2_y - 5), 20)
        pygame.draw.circle(screen, (50, 150, 50), (bush2_x + 8, bush2_y - 5), 20)
        
        # Thorns for both bushes
        thorns1 = [(bush1_x - 15, bush1_y - 15), (bush1_x + 15, bush1_y - 15), (bush1_x, bush1_y - 30)]
        thorns2 = [(bush2_x - 15, bush2_y - 15), (bush2_x + 15, bush2_y - 15), (bush2_x, bush2_y - 30)]
        
        for thorn in thorns1 + thorns2:
            pygame.draw.circle(screen, DARK_GRAY, (int(thorn[0]), int(thorn[1])), 3)
            pygame.draw.circle(screen, BLACK, (int(thorn[0]), int(thorn[1])), 3, 1)
    
    def draw_moving_rock(self, screen):
        """Draw a moving rock with enhanced details"""
        rock_rect = pygame.Rect(self.x, GROUND_Y + self.y_offset - self.height, self.width, self.height)
        
        # Main rock body
        pygame.draw.ellipse(screen, BROWN, rock_rect)
        pygame.draw.ellipse(screen, DARK_GRAY, rock_rect, 2)
        
        # Rock texture
        center_x = self.x + self.width // 2
        center_y = GROUND_Y + self.y_offset - self.height // 2
        
        # Dynamic cracks based on movement
        crack_offset = int(math.sin(self.movement_timer * 0.2) * 2)
        pygame.draw.line(screen, DARK_GRAY, (center_x - 10 + crack_offset, center_y - 15), (center_x + 5, center_y + 10), 2)
        pygame.draw.line(screen, DARK_GRAY, (center_x - 5, center_y - 20), (center_x + 10, center_y - 5), 1)
        
        # Highlights
        pygame.draw.circle(screen, (200, 200, 200), (center_x - 8, center_y - 10), 3)
        pygame.draw.circle(screen, (180, 180, 180), (center_x + 8, center_y - 8), 2)
        
    def get_rect(self):
        if self.obstacle_type == "thorny_bush":
            return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)
        elif self.obstacle_type == "rock":
            return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)
        elif self.obstacle_type == "flying_bush":
            return pygame.Rect(self.x, GROUND_Y + self.y_offset - self.height, self.width, self.height)
        elif self.obstacle_type == "double_bush":
            return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)
        elif self.obstacle_type == "moving_rock":
            return pygame.Rect(self.x, GROUND_Y + self.y_offset - self.height, self.width, self.height)
        elif self.obstacle_type == "laser":
            return pygame.Rect(self.x, GROUND_Y + self.y_offset, self.width, self.height)

# Rest of the classes (Platform, Obstacle, Background) remain the same as in improved version
# but with audio integration added to the Game class

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Cheetah - Audio Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 72)
        
        # Initialize audio manager
        self.audio_manager = AudioManager()
        
        # Initialize levels
        self.levels = [
            Level(1, "Tutorial", "Easy level to get started", BLUE),
            Level(2, "Speed Run", "Faster obstacles and flying spikes", PURPLE),
            Level(3, "Chaos", "Multiple obstacle types", RED),
            Level(4, "Insanity", "Moving obstacles and double spikes", ORANGE),
            Level(5, "Master", "Ultimate challenge with lasers", CYAN)
        ]
        
        self.current_level = 1
        self.selected_level = 1
        
        self.reset_game()
        
    def reset_game(self):
        self.cheetah = Cheetah(100, GROUND_Y - 40, self.audio_manager)
        self.obstacles = []
        self.clouds = []  # Changed from platforms to clouds
        self.background = Background()
        self.score = 0
        self.game_state = GameState.MENU
        self.game_start_time = 0
        self.last_score = 0  # Track score changes for sound effects
        
    def spawn_obstacle(self):
        current_level_data = self.levels[self.current_level - 1]
        
        # Don't spawn obstacles for the first 2 seconds of gameplay
        if hasattr(self, 'game_start_time'):
            time_since_start = pygame.time.get_ticks() - self.game_start_time
            if time_since_start < 2000:  # 2 seconds delay
                return
        
        # Check if we can spawn a new obstacle (respect minimum spacing)
        can_spawn = True
        for obstacle in self.obstacles:
            if obstacle.x > SCREEN_WIDTH - MIN_OBSTACLE_SPACING:
                can_spawn = False
                break
        
        if can_spawn and random.random() < current_level_data.obstacle_spawn_rate:
            obstacle_type = random.choice(current_level_data.obstacle_types)
            self.obstacles.append(Obstacle(SCREEN_WIDTH + 50, obstacle_type, current_level_data))
    
    def spawn_cloud(self):  # Changed from spawn_platform
        current_level_data = self.levels[self.current_level - 1]
        
        # Don't spawn clouds for the first 3 seconds of gameplay
        if hasattr(self, 'game_start_time'):
            time_since_start = pygame.time.get_ticks() - self.game_start_time
            if time_since_start < 3000:  # 3 seconds delay
                return
        
        # Check if we can spawn a new cloud
        can_spawn = True
        for cloud in self.clouds:
            if cloud.x > SCREEN_WIDTH - 400:  # More spacing for clouds
                can_spawn = False
                break
        
        if can_spawn and random.random() < current_level_data.platform_spawn_rate:
            cloud_type = random.choice(["small_cloud", "medium_cloud", "large_cloud", "moving_cloud", "disappearing_cloud", "bouncy_cloud", "storm_cloud"])
            cloud_y = random.randint(GROUND_Y - 300, GROUND_Y - 100)
            self.clouds.append(CloudPlatform(SCREEN_WIDTH + 50, cloud_y, cloud_type, current_level_data))
    
    def check_collision(self):
        if self.cheetah.invincible:
            return False
            
        cheetah_rect = pygame.Rect(self.cheetah.x - 20, self.cheetah.y - 20, 40, 40)
        
        for obstacle in self.obstacles:
            if cheetah_rect.colliderect(obstacle.get_rect()):
                return True
        return False
    
    def update(self):
        if self.game_state == GameState.PLAYING:
            self.cheetah.update(self.clouds)  # Changed from platforms to clouds
            self.background.update()
            
            # Spawn obstacles and clouds
            self.spawn_obstacle()
            self.spawn_cloud()  # Changed from spawn_platform
            
            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.x + obstacle.width < 0:
                    self.obstacles.remove(obstacle)
                    self.score += 1
            
            # Update clouds
            for cloud in self.clouds[:]:
                cloud.update()
                if cloud.x + cloud.width < 0:
                    self.clouds.remove(cloud)
                    self.score += 1
            
            # Play score sound when score increases
            if self.score > self.last_score:
                self.audio_manager.play_sound('score')
                self.last_score = self.score
            
            # Check collision
            if self.check_collision():
                self.audio_manager.play_sound('death')
                self.game_state = GameState.GAME_OVER
                current_level_data = self.levels[self.current_level - 1]
                if self.score > current_level_data.best_score:
                    current_level_data.best_score = self.score
            
            # Check level completion
            current_level_data = self.levels[self.current_level - 1]
            if self.score >= current_level_data.required_score:
                current_level_data.completed = True
                self.audio_manager.play_sound('level_complete')
                self.game_state = GameState.LEVEL_COMPLETE
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GameState.MENU:
                        self.audio_manager.play_sound('menu_select')
                        self.game_state = GameState.LEVEL_SELECT
                    elif self.game_state == GameState.LEVEL_SELECT:
                        self.audio_manager.play_sound('menu_select')
                        self.current_level = self.selected_level
                        self.reset_game()
                        self.game_state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks()
                        self.audio_manager.start_music()
                    elif self.game_state == GameState.PLAYING:
                        self.cheetah.jump()
                    elif self.game_state == GameState.GAME_OVER:
                        self.audio_manager.play_sound('menu_select')
                        self.reset_game()
                        self.game_state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks()
                        self.audio_manager.start_music()
                    elif self.game_state == GameState.LEVEL_COMPLETE:
                        if self.current_level < len(self.levels):
                            self.audio_manager.play_sound('menu_select')
                            self.current_level += 1
                            self.reset_game()
                            self.game_state = GameState.PLAYING
                            self.game_start_time = pygame.time.get_ticks()
                            self.audio_manager.start_music()
                        else:
                            self.game_state = GameState.LEVEL_SELECT
                
                elif event.key == pygame.K_ESCAPE:
                    if self.game_state in [GameState.GAME_OVER, GameState.LEVEL_COMPLETE]:
                        self.audio_manager.play_sound('menu_select')
                        self.game_state = GameState.LEVEL_SELECT
                
                elif event.key in [pygame.K_UP, pygame.K_DOWN] and self.game_state == GameState.LEVEL_SELECT:
                    if event.key == pygame.K_UP:
                        self.selected_level = max(1, self.selected_level - 1)
                    else:
                        self.selected_level = min(len(self.levels), self.selected_level + 1)
                    self.audio_manager.play_sound('menu_select')
        
        return True
    
    def draw(self):
        self.screen.fill(BLACK)
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.LEVEL_SELECT:
            self.draw_level_select()
        elif self.game_state == GameState.PLAYING:
            self.draw_game()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.game_state == GameState.LEVEL_COMPLETE:
            self.draw_level_complete()
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def draw_menu(self):
        self.background.draw(self.screen)
        text = self.font.render("AUDIO EDITION - MENU", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 50))

    def draw_level_select(self):
        self.background.draw(self.screen)
        text = self.font.render("Select Level", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))

    def draw_game(self):
        self.background.draw(self.screen)
        text = self.font.render("Game Running", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH//2 - 150, 20))
        self.cheetah.draw(self.screen)
        # Draw obstacles and platforms if they exist
        for obstacle in getattr(self, 'obstacles', []):
            if hasattr(obstacle, 'draw'):
                obstacle.draw(self.screen)
        for cloud in getattr(self, 'clouds', []): # Changed from platforms to clouds
            if hasattr(cloud, 'draw'):
                cloud.draw(self.screen)

    def draw_game_over(self):
        self.background.draw(self.screen)
        text = self.font.render("GAME OVER", True, RED)
        self.screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))

    def draw_level_complete(self):
        self.background.draw(self.screen)
        text = self.font.render("LEVEL COMPLETE!", True, GREEN)
        self.screen.blit(text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 50))

# Add the missing classes (Platform, Obstacle, Background) here
# They would be the same as in the improved version

if __name__ == "__main__":
    game = Game()
    game.run() 