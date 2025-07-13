import pygame
import random
import math
import os
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
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (205, 133, 63)
DARK_BLUE = (25, 25, 112)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
ROCK_GRAY = (120, 120, 120)
DARK_ROCK = (80, 80, 80)
LIGHT_ROCK = (160, 160, 160)
BUSH_GREEN = (34, 139, 34)
DARK_BUSH = (0, 100, 0)
LIGHT_BUSH = (50, 205, 50)

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

class PowerUpType(Enum):
    EXTRA_LIFE = 1
    FLYING = 2
    INVINCIBILITY = 3
    DOUBLE_JUMP = 4
    SLOW_TIME = 5
    MAGNET = 6

class Particle:
    def __init__(self, x, y, color, velocity_x=0, velocity_y=0, life=60):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.life = life
        self.max_life = life
        self.size = random.randint(2, 6)
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.1  # Gravity
        self.life -= 1
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class PowerUp:
    def __init__(self, x, y, power_type, level_settings):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.level_settings = level_settings
        self.collected = False
        self.animation_timer = 0
        self.bob_offset = 0
        
        # Set properties based on power-up type
        if power_type == PowerUpType.EXTRA_LIFE:
            self.color = RED
            self.size = 20
            self.symbol = "♥"
        elif power_type == PowerUpType.FLYING:
            self.color = CYAN
            self.size = 18
            self.symbol = "✈"
        elif power_type == PowerUpType.INVINCIBILITY:
            self.color = GOLD
            self.size = 22
            self.symbol = "★"
        elif power_type == PowerUpType.DOUBLE_JUMP:
            self.color = PURPLE
            self.size = 19
            self.symbol = "⚡"
        elif power_type == PowerUpType.SLOW_TIME:
            self.color = BLUE
            self.size = 20
            self.symbol = "⏰"
        elif power_type == PowerUpType.MAGNET:
            self.color = SILVER
            self.size = 18
            self.symbol = "🧲"
    
    def update(self):
        self.x -= self.level_settings.obstacle_speed
        self.animation_timer += 1
        self.bob_offset = math.sin(self.animation_timer * 0.1) * 5
    
    def draw(self, screen):
        if self.collected:
            return
            
        # Draw power-up with effects
        y_pos = self.y + self.bob_offset
        
        # Glow effect
        glow_radius = self.size + 5 + int(3 * math.sin(self.animation_timer * 0.2))
        pygame.draw.circle(screen, (*self.color, 100), (int(self.x), int(y_pos)), glow_radius)
        
        # Main power-up
        pygame.draw.circle(screen, self.color, (int(self.x), int(y_pos)), self.size)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(y_pos)), self.size, 2)
        
        # Symbol
        font = pygame.font.Font(None, 24)
        symbol_text = font.render(self.symbol, True, WHITE)
        symbol_rect = symbol_text.get_rect(center=(int(self.x), int(y_pos)))
        screen.blit(symbol_text, symbol_rect)
        
        # Sparkle effect
        if self.animation_timer % 20 < 10:
            sparkle_pos = (self.x + random.randint(-15, 15), y_pos + random.randint(-15, 15))
            pygame.draw.circle(screen, WHITE, (int(sparkle_pos[0]), int(sparkle_pos[1])), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.load_sounds()
        
    def load_sounds(self):
        try:
            self.create_jump_sound()
            self.create_land_sound()
            self.create_death_sound()
            self.create_score_sound()
            self.create_level_complete_sound()
            self.create_menu_select_sound()
            self.create_bounce_sound()
            self.create_powerup_sound()
        except Exception as e:
            print(f"Could not load sounds: {e}")
    
    def create_jump_sound(self):
        sample_rate = 44100
        duration = 0.2
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 400 + (i / samples) * 200
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        try:
            sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
                pygame.Surface((len(sound_array), 1, 3))
            ))
            self.sounds['jump'] = sound_surface
        except:
            pass
    
    def create_land_sound(self):
        sample_rate = 44100
        duration = 0.15
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 200 * math.exp(-i / (samples * 0.3))
            sample = int(32767 * 0.4 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        try:
            sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
                pygame.Surface((len(sound_array), 1, 3))
            ))
            self.sounds['land'] = sound_surface
        except:
            pass
    
    def create_death_sound(self):
        sample_rate = 44100
        duration = 0.5
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 600 * math.exp(-i / (samples * 0.5))
            sample = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        try:
            sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
                pygame.Surface((len(sound_array), 1, 3))
            ))
            self.sounds['death'] = sound_surface
        except:
            pass
    
    def create_score_sound(self):
        sample_rate = 44100
        duration = 0.1
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 800 + (i / samples) * 400
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        try:
            sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
                pygame.Surface((len(sound_array), 1, 3))
            ))
            self.sounds['score'] = sound_surface
        except:
            pass
    
    def create_level_complete_sound(self):
        sample_rate = 44100
        duration = 0.8
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 300 + (i / samples) * 600
            sample = int(32767 * 0.4 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        try:
            sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
                pygame.Surface((len(sound_array), 1, 3))
            ))
            self.sounds['level_complete'] = sound_surface
        except:
            pass
    
    def create_menu_select_sound(self):
        sample_rate = 44100
        duration = 0.1
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 500
            sample = int(32767 * 0.2 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        try:
            sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
                pygame.Surface((len(sound_array), 1, 3))
            ))
            self.sounds['menu_select'] = sound_surface
        except:
            pass
    
    def create_bounce_sound(self):
        sample_rate = 44100
        duration = 0.15
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 300 * math.exp(-i / (samples * 0.4))
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        try:
            sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
                pygame.Surface((len(sound_array), 1, 3))
            ))
            self.sounds['bounce'] = sound_surface
        except:
            pass
    
    def create_powerup_sound(self):
        sample_rate = 44100
        duration = 0.3
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 600 + (i / samples) * 300
            sample = int(32767 * 0.4 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        try:
            sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
                pygame.Surface((len(sound_array), 1, 3))
            ))
            self.sounds['powerup'] = sound_surface
        except:
            pass
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def start_music(self):
        """Start background music"""
        try:
            # Create a simple background music loop
            sample_rate = 44100
            duration = 2.0
            samples = int(sample_rate * duration)
            
            sound_array = []
            for i in range(samples):
                frequency = 200 + 100 * math.sin(i / (sample_rate * 0.5))
                sample = int(32767 * 0.1 * math.sin(2 * math.pi * frequency * i / sample_rate))
                sound_array.append(sample)
            
            music_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
                pygame.Surface((len(sound_array), 1, 3))
            ))
            music_surface.play(-1)  # Loop indefinitely
            self.music_playing = True
        except:
            pass
    
    def stop_music(self):
        """Stop background music"""
        self.music_playing = False

class Level:
    def __init__(self, level_num, name, description, color):
        self.level_num = level_num
        self.name = name
        self.description = description
        self.background_color = color
        self.completed = False
        self.best_score = 0
        self.required_score = 15
        
        # Level-specific settings
        if level_num == 1:  # Tutorial
            self.obstacle_speed = 3
            self.obstacle_spawn_rate = 0.02
            self.platform_spawn_rate = 0.03
            self.powerup_spawn_rate = 0.01
            self.obstacle_types = ["small_rock"]
            self.platform_types = ["normal"]
        elif level_num == 2:  # Speed Run
            self.obstacle_speed = 4
            self.obstacle_spawn_rate = 0.025
            self.platform_spawn_rate = 0.035
            self.powerup_spawn_rate = 0.015
            self.obstacle_types = ["small_rock", "spiky_bush"]
            self.platform_types = ["normal", "small"]
        elif level_num == 3:  # Chaos
            self.obstacle_speed = 4.5
            self.obstacle_spawn_rate = 0.03
            self.platform_spawn_rate = 0.04
            self.powerup_spawn_rate = 0.02
            self.obstacle_types = ["small_rock", "large_rock", "spiky_bush"]
            self.platform_types = ["normal", "small", "moving"]
        elif level_num == 4:  # Insanity
            self.obstacle_speed = 5
            self.obstacle_spawn_rate = 0.035
            self.platform_spawn_rate = 0.045
            self.powerup_spawn_rate = 0.025
            self.obstacle_types = ["small_rock", "large_rock", "spiky_bush", "rock_cluster", "moving_rock"]
            self.platform_types = ["normal", "small", "moving", "disappearing"]
        elif level_num == 5:  # Master
            self.obstacle_speed = 6
            self.obstacle_spawn_rate = 0.04
            self.platform_spawn_rate = 0.05
            self.powerup_spawn_rate = 0.03
            self.obstacle_types = ["small_rock", "large_rock", "spiky_bush", "rock_cluster", "moving_rock", "boulder"]
            self.platform_types = ["normal", "small", "moving", "disappearing", "bouncy", "teleport"]

class PowerUpCheetah:
    def __init__(self, x, y, audio_manager):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.on_ground = False
        self.jump_count = 0
        self.max_jumps = 1
        self.audio_manager = audio_manager
        self.invincible = False
        self.invincible_timer = 0
        self.lives = 3
        
        # Power-up states
        self.flying = False
        self.flying_timer = 0
        self.slow_time = False
        self.slow_time_timer = 0
        self.magnet = False
        self.magnet_timer = 0
        
        # Animation
        self.animation_timer = 0
        self.rotation = 0
        self.trail_particles = []
        
    def update(self, platforms, powerups):
        # Apply gravity (unless flying)
        if not self.flying:
            self.velocity_y += GRAVITY
        else:
            # Flying mode - slower gravity
            self.velocity_y += GRAVITY * 0.3
        
        # Apply slow time effect
        if self.slow_time:
            self.velocity_y *= 0.7
        
        # Update position
        self.y += self.velocity_y
        
        # Check ground collision
        if self.y >= GROUND_Y - 40:
            self.y = GROUND_Y - 40
            self.velocity_y = 0
            self.on_ground = True
            self.jump_count = 0
            if not self.flying:
                self.flying = False
        
        # Check platform collisions
        self.on_ground = False
        for platform in platforms:
            if self.check_platform_collision(platform):
                self.on_ground = True
                self.jump_count = 0
                if not self.flying:
                    self.flying = False
                break
        
        # Check power-up collisions
        for powerup in powerups:
            if self.check_powerup_collision(powerup):
                self.collect_powerup(powerup)
        
        # Update power-up timers
        if self.flying:
            self.flying_timer -= 1
            if self.flying_timer <= 0:
                self.flying = False
        
        if self.slow_time:
            self.slow_time_timer -= 1
            if self.slow_time_timer <= 0:
                self.slow_time = False
        
        if self.magnet:
            self.magnet_timer -= 1
            if self.magnet_timer <= 0:
                self.magnet = False
        
        if self.invincible:
            self.invincible_timer -= 1
        
        # Update animation
        self.animation_timer += 1
        
        # Update rotation based on velocity
        target_rotation = -self.velocity_y * 2
        self.rotation += (target_rotation - self.rotation) * 0.1
        
        # Update trail particles
        for particle in self.trail_particles[:]:
            particle.update()
            if particle.life <= 0:
                self.trail_particles.remove(particle)
        
        # Add new trail particles
        if abs(self.velocity_y) > 2:
            for _ in range(2):
                particle = Particle(
                    self.x + random.randint(-10, 10),
                    self.y + random.randint(-10, 10),
                    (255, 200, 100),
                    random.uniform(-1, 1),
                    random.uniform(-2, 2),
                    30
                )
                self.trail_particles.append(particle)
    
    def check_platform_collision(self, platform):
        # IMPROVED collision detection with better platform landing
        cheetah_rect = pygame.Rect(self.x - 25, self.y - 25, 50, 50)
        platform_rect = platform.get_rect()
        
        if cheetah_rect.colliderect(platform_rect):
            # Check if cheetah is above the platform
            if self.velocity_y > 0 and self.y < platform.y:
                self.y = platform.y - 25
                self.velocity_y = 0
                self.audio_manager.play_sound('land')
                return True
        return False
    
    def check_powerup_collision(self, powerup):
        cheetah_rect = pygame.Rect(self.x - 20, self.y - 20, 40, 40)
        powerup_rect = powerup.get_rect()
        return cheetah_rect.colliderect(powerup_rect)
    
    def collect_powerup(self, powerup):
        if powerup.collected:
            return
            
        powerup.collected = True
        self.audio_manager.play_sound('powerup')
        
        if powerup.power_type == PowerUpType.EXTRA_LIFE:
            self.lives += 1
        elif powerup.power_type == PowerUpType.FLYING:
            self.flying = True
            self.flying_timer = 180  # 3 seconds
        elif powerup.power_type == PowerUpType.INVINCIBILITY:
            self.make_invincible(180)  # 3 seconds
        elif powerup.power_type == PowerUpType.DOUBLE_JUMP:
            self.max_jumps = 2
        elif powerup.power_type == PowerUpType.SLOW_TIME:
            self.slow_time = True
            self.slow_time_timer = 120  # 2 seconds
        elif powerup.power_type == PowerUpType.MAGNET:
            self.magnet = True
            self.magnet_timer = 240  # 4 seconds
    
    def jump(self):
        if self.flying:
            return
            
        if self.on_ground or self.jump_count < self.max_jumps:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False
            self.jump_count += 1
            self.audio_manager.play_sound('jump')
    
    def fly_up(self):
        if self.flying:
            self.velocity_y = -8
    
    def fly_down(self):
        if self.flying:
            self.velocity_y = 8
    
    def make_invincible(self, duration=60):
        self.invincible = True
        self.invincible_timer = duration
    
    def draw(self, screen):
        # Draw trail particles with effects
        for particle in self.trail_particles:
            particle.draw(screen)
        
        # Create cheetah surface
        cheetah_surface = pygame.Surface((80, 60), pygame.SRCALPHA)
        
        # Body (main shape)
        body_color = (255, 200, 100)
        pygame.draw.ellipse(cheetah_surface, body_color, (10, 20, 50, 30))
        
        # Head
        head_color = (255, 180, 80)
        pygame.draw.circle(cheetah_surface, head_color, (55, 25), 15)
        
        # Ears
        ear_color = (255, 160, 60)
        pygame.draw.circle(cheetah_surface, ear_color, (50, 15), 8)
        pygame.draw.circle(cheetah_surface, ear_color, (60, 15), 8)
        pygame.draw.circle(cheetah_surface, PINK, (50, 15), 4)
        pygame.draw.circle(cheetah_surface, PINK, (60, 15), 4)
        
        # Eyes
        eye_color = (50, 50, 50)
        pygame.draw.circle(cheetah_surface, eye_color, (52, 22), 3)
        pygame.draw.circle(cheetah_surface, eye_color, (58, 22), 3)
        
        # Eye highlights
        pygame.draw.circle(cheetah_surface, WHITE, (51, 21), 1)
        pygame.draw.circle(cheetah_surface, WHITE, (57, 21), 1)
        
        # Blinking animation
        if self.animation_timer % 60 < 50:
            pygame.draw.circle(cheetah_surface, WHITE, (52, 22), 1)
            pygame.draw.circle(cheetah_surface, WHITE, (58, 22), 1)
        
        # Nose
        pygame.draw.circle(cheetah_surface, BLACK, (65, 25), 2)
        
        # Mouth
        pygame.draw.arc(cheetah_surface, BLACK, (60, 20, 10, 10), 0, 3.14, 2)
        
        # Spots/patterns
        spot_color = (200, 150, 50)
        pygame.draw.circle(cheetah_surface, spot_color, (20, 25), 3)
        pygame.draw.circle(cheetah_surface, spot_color, (30, 30), 2)
        pygame.draw.circle(cheetah_surface, spot_color, (40, 28), 3)
        pygame.draw.circle(cheetah_surface, spot_color, (25, 35), 2)
        
        # Legs
        leg_color = (255, 180, 80)
        pygame.draw.rect(cheetah_surface, leg_color, (15, 40, 6, 15))
        pygame.draw.rect(cheetah_surface, leg_color, (25, 40, 6, 15))
        pygame.draw.rect(cheetah_surface, leg_color, (35, 40, 6, 15))
        pygame.draw.rect(cheetah_surface, leg_color, (45, 40, 6, 15))
        
        # Tail (animated)
        tail_wag = math.sin(self.animation_timer * 0.2) * 5
        tail_points = [(10, 30), (5 + tail_wag, 25), (0 + tail_wag * 2, 20)]
        pygame.draw.lines(cheetah_surface, body_color, False, tail_points, 4)
        
        # Tail tip
        tail_tip = (0 + tail_wag * 2, 20)
        pygame.draw.circle(cheetah_surface, BLACK, (tail_tip[0], tail_tip[1]), 3)
        pygame.draw.circle(cheetah_surface, WHITE, (tail_tip[0]-1, tail_tip[1]-1), 1)
        
        # Rotate the cheetah
        rotated_surface = pygame.transform.rotate(cheetah_surface, self.rotation)
        
        # Apply invincibility effect
        if self.invincible and self.invincible_timer % 10 < 5:
            pass  # Skip drawing to create flash effect
        else:
            screen.blit(rotated_surface, (self.x - rotated_surface.get_width()//2, 
                                         self.y - rotated_surface.get_height()//2))

class Platform:
    def __init__(self, x, y, platform_type="normal", level_settings=None):
        self.x = x
        self.y = y
        self.platform_type = platform_type
        self.level_settings = level_settings
        self.width = 80
        self.height = 20
        self.movement_timer = 0
        self.disappear_timer = 0
        self.visible = True
        self.bounce_force = -15
        
        # Set properties based on platform type
        if platform_type == "normal":
            self.color = GREEN
            self.width = 100
        elif platform_type == "small":
            self.color = LIME
            self.width = 60
        elif platform_type == "moving":
            self.color = CYAN
            self.width = 80
            self.start_y = y
            self.movement_range = 50
        elif platform_type == "disappearing":
            self.color = ORANGE
            self.width = 80
            self.disappear_timer = 180  # 3 seconds
        elif platform_type == "bouncy":
            self.color = PINK
            self.width = 80
            self.bounce_force = -20
        elif platform_type == "teleport":
            self.color = PURPLE
            self.width = 80
            self.teleport_timer = 0
    
    def update(self):
        self.x -= self.level_settings.obstacle_speed
        self.movement_timer += 1
        
        # Special movement for moving platforms
        if self.platform_type == "moving":
            self.y = self.start_y + math.sin(self.movement_timer * 0.05) * self.movement_range
        
        # Disappearing platform logic
        if self.platform_type == "disappearing":
            self.disappear_timer -= 1
            if self.disappear_timer <= 0:
                self.visible = False
        
        # Teleport platform logic
        if self.platform_type == "teleport":
            self.teleport_timer += 1
            if self.teleport_timer > 120:  # Every 2 seconds
                self.teleport_timer = 0
                self.visible = not self.visible
    
    def draw(self, screen):
        if not self.visible:
            return
            
        # Draw platform with effects
        if self.platform_type == "bouncy":
            # Bouncy platform with spring effect
            spring_offset = math.sin(self.movement_timer * 0.3) * 3
            pygame.draw.rect(screen, self.color, (self.x, self.y + spring_offset, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x, self.y + spring_offset, self.width, self.height), 2)
            
            # Draw spring coils
            for i in range(0, self.width, 10):
                coil_y = self.y + spring_offset + self.height + 5
                pygame.draw.circle(screen, SILVER, (int(self.x + i), int(coil_y)), 3)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)
        
        # Platform type indicators
        if self.platform_type == "disappearing":
            # Warning effect
            if self.disappear_timer < 60:
                warning_color = RED if self.disappear_timer % 20 < 10 else ORANGE
                pygame.draw.rect(screen, warning_color, (self.x, self.y, self.width, self.height), 3)
        elif self.platform_type == "teleport":
            # Teleport effect
            if self.visible:
                teleport_color = PURPLE if self.teleport_timer % 40 < 20 else WHITE
                pygame.draw.rect(screen, teleport_color, (self.x, self.y, self.width, self.height), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class NatureObstacle:
    def __init__(self, x, obstacle_type="small_rock", level_settings=None):
        self.x = x
        self.obstacle_type = obstacle_type
        self.level_settings = level_settings
        self.width = 40
        self.height = 50
        self.y_offset = 0
        self.movement_timer = 0
        self.animation_timer = 0
        
        # Set properties based on obstacle type
        if obstacle_type == "small_rock":
            self.width = 35
            self.height = 45
        elif obstacle_type == "large_rock":
            self.width = 60
            self.height = 70
        elif obstacle_type == "spiky_bush":
            self.width = 50
            self.height = 60
        elif obstacle_type == "rock_cluster":
            self.width = 80
            self.height = 55
        elif obstacle_type == "moving_rock":
            self.width = 45
            self.height = 50
            self.y_offset = random.randint(-30, 30)
        elif obstacle_type == "boulder":
            self.width = 70
            self.height = 80
        
    def update(self):
        self.x -= self.level_settings.obstacle_speed
        self.movement_timer += 1
        self.animation_timer += 1
        
        # Special movement for moving rocks
        if self.obstacle_type == "moving_rock":
            self.y_offset = math.sin(self.movement_timer * 0.08) * 25
            
    def draw_small_rock(self, screen):
        """Draw a detailed small rock"""
        base_y = GROUND_Y - self.height
        
        # Main rock body
        rock_points = [
            (self.x, base_y + self.height),
            (self.x + 10, base_y + self.height - 10),
            (self.x + 20, base_y + self.height - 25),
            (self.x + 30, base_y + self.height - 35),
            (self.x + 35, base_y + self.height - 40),
            (self.x + 30, base_y + self.height - 45),
            (self.x + 20, base_y + self.height - 40),
            (self.x + 10, base_y + self.height - 30),
            (self.x, base_y + self.height - 20)
        ]
        
        # Draw rock with shading
        pygame.draw.polygon(screen, ROCK_GRAY, rock_points)
        pygame.draw.polygon(screen, DARK_ROCK, rock_points, 2)
        
        # Add rock details
        for i in range(3):
            detail_x = self.x + random.randint(5, 30)
            detail_y = base_y + random.randint(10, 40)
            pygame.draw.circle(screen, DARK_ROCK, (detail_x, detail_y), 2)
        
        # Add highlights
        highlight_points = [
            (self.x + 5, base_y + self.height - 15),
            (self.x + 15, base_y + self.height - 25),
            (self.x + 25, base_y + self.height - 35)
        ]
        for point in highlight_points:
            pygame.draw.circle(screen, LIGHT_ROCK, point, 1)
    
    def draw_large_rock(self, screen):
        """Draw a detailed large rock"""
        base_y = GROUND_Y - self.height
        
        # Main rock body with more complex shape
        rock_points = [
            (self.x, base_y + self.height),
            (self.x + 15, base_y + self.height - 15),
            (self.x + 30, base_y + self.height - 25),
            (self.x + 45, base_y + self.height - 35),
            (self.x + 60, base_y + self.height - 40),
            (self.x + 55, base_y + self.height - 50),
            (self.x + 45, base_y + self.height - 60),
            (self.x + 35, base_y + self.height - 65),
            (self.x + 20, base_y + self.height - 70),
            (self.x + 10, base_y + self.height - 60),
            (self.x + 5, base_y + self.height - 45),
            (self.x, base_y + self.height - 30)
        ]
        
        # Draw rock with shading
        pygame.draw.polygon(screen, ROCK_GRAY, rock_points)
        pygame.draw.polygon(screen, DARK_ROCK, rock_points, 3)
        
        # Add detailed rock texture
        for i in range(8):
            detail_x = self.x + random.randint(5, 55)
            detail_y = base_y + random.randint(15, 65)
            detail_size = random.randint(1, 3)
            pygame.draw.circle(screen, DARK_ROCK, (detail_x, detail_y), detail_size)
        
        # Add moss/lichen details
        moss_points = [
            (self.x + 10, base_y + self.height - 20),
            (self.x + 25, base_y + self.height - 35),
            (self.x + 40, base_y + self.height - 45)
        ]
        for point in moss_points:
            pygame.draw.circle(screen, DARK_GREEN, point, 3)
            pygame.draw.circle(screen, LIGHT_GREEN, (point[0]-1, point[1]-1), 1)
        
        # Add highlights
        highlight_points = [
            (self.x + 8, base_y + self.height - 25),
            (self.x + 20, base_y + self.height - 40),
            (self.x + 35, base_y + self.height - 50)
        ]
        for point in highlight_points:
            pygame.draw.circle(screen, LIGHT_ROCK, point, 2)
    
    def draw_spiky_bush(self, screen):
        """Draw a detailed spiky bush"""
        base_y = GROUND_Y - self.height
        
        # Bush base
        bush_base = pygame.Rect(self.x + 10, base_y + self.height - 20, 30, 20)
        pygame.draw.ellipse(screen, DARK_BUSH, bush_base)
        pygame.draw.ellipse(screen, BLACK, bush_base, 2)
        
        # Main bush body
        bush_points = [
            (self.x + 15, base_y + self.height - 25),
            (self.x + 25, base_y + self.height - 40),
            (self.x + 35, base_y + self.height - 50),
            (self.x + 40, base_y + self.height - 60),
            (self.x + 35, base_y + self.height - 55),
            (self.x + 25, base_y + self.height - 45),
            (self.x + 15, base_y + self.height - 35)
        ]
        
        pygame.draw.polygon(screen, BUSH_GREEN, bush_points)
        pygame.draw.polygon(screen, DARK_BUSH, bush_points, 2)
        
        # Draw spikes/thorns
        spike_positions = [
            (self.x + 20, base_y + self.height - 30),
            (self.x + 30, base_y + self.height - 45),
            (self.x + 35, base_y + self.height - 55),
            (self.x + 25, base_y + self.height - 40),
            (self.x + 15, base_y + self.height - 25)
        ]
        
        for spike_pos in spike_positions:
            # Spike shape
            spike_points = [
                (spike_pos[0], spike_pos[1]),
                (spike_pos[0] - 3, spike_pos[1] - 8),
                (spike_pos[0] + 3, spike_pos[1] - 8)
            ]
            pygame.draw.polygon(screen, DARK_BUSH, spike_points)
            pygame.draw.polygon(screen, BLACK, spike_points, 1)
        
        # Add bush details
        for i in range(5):
            detail_x = self.x + random.randint(10, 40)
            detail_y = base_y + random.randint(25, 55)
            detail_size = random.randint(1, 2)
            pygame.draw.circle(screen, LIGHT_BUSH, (detail_x, detail_y), detail_size)
        
        # Animated swaying effect
        sway_offset = math.sin(self.animation_timer * 0.1) * 2
        sway_points = [
            (self.x + 20 + sway_offset, base_y + self.height - 35),
            (self.x + 30 + sway_offset, base_y + self.height - 50),
            (self.x + 25 + sway_offset, base_y + self.height - 45)
        ]
        for point in sway_points:
            pygame.draw.circle(screen, LIGHT_BUSH, (int(point[0]), int(point[1])), 1)
    
    def draw_rock_cluster(self, screen):
        """Draw a cluster of small rocks"""
        base_y = GROUND_Y - self.height
        
        # Draw multiple rocks in a cluster
        rock_positions = [
            (self.x + 10, base_y + self.height - 20),
            (self.x + 25, base_y + self.height - 35),
            (self.x + 40, base_y + self.height - 25),
            (self.x + 55, base_y + self.height - 40),
            (self.x + 20, base_y + self.height - 45)
        ]
        
        for i, pos in enumerate(rock_positions):
            rock_size = random.randint(8, 15)
            rock_points = [
                (pos[0], pos[1] + rock_size),
                (pos[0] + rock_size//2, pos[1] + rock_size//2),
                (pos[0] + rock_size, pos[1] + rock_size),
                (pos[0] + rock_size, pos[1]),
                (pos[0] + rock_size//2, pos[1] - rock_size//2),
                (pos[0], pos[1])
            ]
            
            # Vary rock colors slightly
            rock_color = (ROCK_GRAY[0] + random.randint(-20, 20),
                         ROCK_GRAY[1] + random.randint(-20, 20),
                         ROCK_GRAY[2] + random.randint(-20, 20))
            
            pygame.draw.polygon(screen, rock_color, rock_points)
            pygame.draw.polygon(screen, DARK_ROCK, rock_points, 1)
            
            # Add rock details
            for j in range(2):
                detail_x = pos[0] + random.randint(2, rock_size-2)
                detail_y = pos[1] + random.randint(2, rock_size-2)
                pygame.draw.circle(screen, DARK_ROCK, (detail_x, detail_y), 1)
    
    def draw_moving_rock(self, screen):
        """Draw a moving rock with animation"""
        base_y = GROUND_Y - self.height + self.y_offset
        
        # Main rock body
        rock_points = [
            (self.x, base_y + self.height),
            (self.x + 15, base_y + self.height - 15),
            (self.x + 30, base_y + self.height - 25),
            (self.x + 45, base_y + self.height - 30),
            (self.x + 40, base_y + self.height - 45),
            (self.x + 25, base_y + self.height - 50),
            (self.x + 10, base_y + self.height - 40),
            (self.x, base_y + self.height - 25)
        ]
        
        pygame.draw.polygon(screen, ROCK_GRAY, rock_points)
        pygame.draw.polygon(screen, DARK_ROCK, rock_points, 2)
        
        # Add movement trail effect
        trail_alpha = int(100 * abs(math.sin(self.movement_timer * 0.1)))
        trail_points = [(p[0] - 5, p[1]) for p in rock_points]
        trail_surface = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        pygame.draw.polygon(trail_surface, (*ROCK_GRAY, trail_alpha), trail_points)
        screen.blit(trail_surface, (self.x - 5, base_y - 5))
        
        # Add rock details
        for i in range(4):
            detail_x = self.x + random.randint(5, 40)
            detail_y = base_y + random.randint(10, 45)
            pygame.draw.circle(screen, DARK_ROCK, (detail_x, detail_y), 2)
    
    def draw_boulder(self, screen):
        """Draw a massive boulder"""
        base_y = GROUND_Y - self.height
        
        # Main boulder body
        boulder_points = [
            (self.x, base_y + self.height),
            (self.x + 20, base_y + self.height - 20),
            (self.x + 40, base_y + self.height - 35),
            (self.x + 60, base_y + self.height - 45),
            (self.x + 70, base_y + self.height - 50),
            (self.x + 65, base_y + self.height - 65),
            (self.x + 55, base_y + self.height - 75),
            (self.x + 40, base_y + self.height - 80),
            (self.x + 25, base_y + self.height - 75),
            (self.x + 15, base_y + self.height - 65),
            (self.x + 10, base_y + self.height - 50),
            (self.x, base_y + self.height - 35)
        ]
        
        # Draw boulder with multiple layers for depth
        pygame.draw.polygon(screen, DARK_ROCK, boulder_points)
        pygame.draw.polygon(screen, ROCK_GRAY, boulder_points, 3)
        
        # Add massive rock texture
        for i in range(12):
            detail_x = self.x + random.randint(5, 65)
            detail_y = base_y + random.randint(20, 75)
            detail_size = random.randint(2, 4)
            detail_color = random.choice([DARK_ROCK, LIGHT_ROCK, ROCK_GRAY])
            pygame.draw.circle(screen, detail_color, (detail_x, detail_y), detail_size)
        
        # Add cracks and fissures
        crack_points = [
            (self.x + 15, base_y + self.height - 30),
            (self.x + 25, base_y + self.height - 45),
            (self.x + 35, base_y + self.height - 55)
        ]
        for i in range(len(crack_points) - 1):
            pygame.draw.line(screen, BLACK, crack_points[i], crack_points[i+1], 2)
        
        # Add moss patches
        moss_positions = [
            (self.x + 10, base_y + self.height - 25),
            (self.x + 45, base_y + self.height - 60),
            (self.x + 30, base_y + self.height - 40)
        ]
        for moss_pos in moss_positions:
            pygame.draw.circle(screen, DARK_GREEN, moss_pos, 4)
            pygame.draw.circle(screen, LIGHT_GREEN, (moss_pos[0]-1, moss_pos[1]-1), 2)
        
        # Add highlights
        highlight_points = [
            (self.x + 5, base_y + self.height - 30),
            (self.x + 20, base_y + self.height - 50),
            (self.x + 40, base_y + self.height - 65)
        ]
        for point in highlight_points:
            pygame.draw.circle(screen, LIGHT_ROCK, point, 3)
    
    def draw(self, screen):
        if self.obstacle_type == "small_rock":
            self.draw_small_rock(screen)
        elif self.obstacle_type == "large_rock":
            self.draw_large_rock(screen)
        elif self.obstacle_type == "spiky_bush":
            self.draw_spiky_bush(screen)
        elif self.obstacle_type == "rock_cluster":
            self.draw_rock_cluster(screen)
        elif self.obstacle_type == "moving_rock":
            self.draw_moving_rock(screen)
        elif self.obstacle_type == "boulder":
            self.draw_boulder(screen)
            
    def get_rect(self):
        if self.obstacle_type == "moving_rock":
            return pygame.Rect(self.x, GROUND_Y + self.y_offset - self.height, self.width, self.height)
        else:
            return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)

class EnhancedBackground:
    def __init__(self, level_color=BLUE):
        self.level_color = level_color
        self.parallax_offset = 0
        
        # Multiple background layers
        self.far_mountains = []
        self.mountains = []
        self.hills = []
        self.clouds = []
        self.stars = []
        self.particles = []
        self.lightning_flashes = []
        self.aurora_effect = []
        
        # Generate far mountains (slowest parallax)
        for _ in range(8):
            self.far_mountains.append({
                'x': random.randint(-200, SCREEN_WIDTH + 200),
                'y': random.randint(100, 250),
                'width': random.randint(100, 300),
                'height': random.randint(50, 150),
                'color': (max(0, level_color[0] - 100), max(0, level_color[1] - 100), max(0, level_color[2] - 100))
            })
        
        # Generate mountains (medium parallax)
        for _ in range(6):
            self.mountains.append({
                'x': random.randint(-100, SCREEN_WIDTH + 100),
                'y': random.randint(150, 300),
                'width': random.randint(80, 200),
                'height': random.randint(60, 120),
                'color': (max(0, level_color[0] - 50), max(0, level_color[1] - 50), max(0, level_color[2] - 50))
            })
        
        # Generate hills (faster parallax)
        for _ in range(10):
            self.hills.append({
                'x': random.randint(-50, SCREEN_WIDTH + 50),
                'y': random.randint(200, 350),
                'width': random.randint(60, 150),
                'height': random.randint(30, 80),
                'color': (max(0, level_color[0] - 30), max(0, level_color[1] - 30), max(0, level_color[2] - 30))
            })
        
        # Generate clouds
        for _ in range(8):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(30, 180),
                'size': random.randint(40, 120),
                'speed': random.uniform(0.3, 0.8),
                'opacity': random.randint(150, 255)
            })
        
        # Generate stars
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(20, 200),
                'brightness': random.randint(100, 255),
                'twinkle_speed': random.uniform(0.01, 0.03),
                'size': random.randint(1, 3)
            })
        
        # Generate aurora effect
        for _ in range(20):
            self.aurora_effect.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 150),
                'width': random.randint(100, 300),
                'height': random.randint(20, 60),
                'color': (random.randint(0, 255), random.randint(100, 255), random.randint(100, 255)),
                'speed': random.uniform(0.1, 0.3),
                'opacity': random.randint(30, 100)
            })
        
        # Generate floating particles
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.2, 0.2),
                'size': random.randint(1, 4),
                'color': (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)),
                'life': random.randint(100, 300)
            })
        
    def update(self):
        # Update parallax offset
        self.parallax_offset += 1
        
        # Update far mountains (slowest)
        for mountain in self.far_mountains:
            mountain['x'] -= 0.2
            if mountain['x'] + mountain['width'] < -100:
                mountain['x'] = SCREEN_WIDTH + 100
                mountain['y'] = random.randint(100, 250)
        
        # Update mountains (medium)
        for mountain in self.mountains:
            mountain['x'] -= 0.5
            if mountain['x'] + mountain['width'] < -100:
                mountain['x'] = SCREEN_WIDTH + 100
                mountain['y'] = random.randint(150, 300)
        
        # Update hills (faster)
        for hill in self.hills:
            hill['x'] -= 1.0
            if hill['x'] + hill['width'] < -50:
                hill['x'] = SCREEN_WIDTH + 50
                hill['y'] = random.randint(200, 350)
        
        # Update clouds
        for cloud in self.clouds:
            cloud['x'] -= cloud['speed']
            if cloud['x'] + cloud['size'] < -cloud['size']:
                cloud['x'] = SCREEN_WIDTH + cloud['size']
                cloud['y'] = random.randint(30, 180)
                cloud['opacity'] = random.randint(150, 255)
        
        # Update stars
        for star in self.stars:
            star['brightness'] += math.sin(pygame.time.get_ticks() * star['twinkle_speed']) * 15
            star['brightness'] = max(50, min(255, star['brightness']))
        
        # Update aurora effect
        for aurora in self.aurora_effect:
            aurora['x'] -= aurora['speed']
            if aurora['x'] + aurora['width'] < -aurora['width']:
                aurora['x'] = SCREEN_WIDTH + aurora['width']
                aurora['opacity'] = random.randint(30, 100)
        
        # Update particles
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if particle['life'] <= 0 or particle['x'] < -10 or particle['x'] > SCREEN_WIDTH + 10:
                particle['x'] = random.randint(0, SCREEN_WIDTH)
                particle['y'] = random.randint(0, SCREEN_HEIGHT)
                particle['life'] = random.randint(100, 300)
        
        # Random lightning effect
        if random.random() < 0.001:  # Very rare
            self.lightning_flashes.append({
                'timer': 10,
                'intensity': random.randint(100, 200)
            })
        
        # Update lightning
        for flash in self.lightning_flashes[:]:
            flash['timer'] -= 1
            if flash['timer'] <= 0:
                self.lightning_flashes.remove(flash)
        
    def draw(self, screen):
        # Draw gradient sky with multiple layers
        for y in range(SCREEN_HEIGHT):
            # Create complex gradient
            ratio = y / SCREEN_HEIGHT
            
            # Base gradient
            r = int(self.level_color[0] * (1 - ratio * 0.6))
            g = int(self.level_color[1] * (1 - ratio * 0.6))
            b = int(self.level_color[2] * (1 - ratio * 0.6))
            
            # Add atmospheric scattering effect
            atmospheric_blue = int(100 * (1 - ratio))
            r = min(255, r + atmospheric_blue // 3)
            g = min(255, g + atmospheric_blue // 3)
            b = min(255, b + atmospheric_blue)
            
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw aurora effect
        for aurora in self.aurora_effect:
            aurora_surface = pygame.Surface((aurora['width'], aurora['height']), pygame.SRCALPHA)
            for i in range(aurora['height']):
                alpha = int(aurora['opacity'] * (1 - i / aurora['height']))
                color = (*aurora['color'], alpha)
                pygame.draw.line(aurora_surface, color, (0, i), (aurora['width'], i))
            screen.blit(aurora_surface, (aurora['x'], aurora['y']))
        
        # Draw stars with twinkling
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])
            
            # Add star sparkles
            if random.random() < 0.1:
                sparkle_pos = (star['x'] + random.randint(-5, 5), star['y'] + random.randint(-5, 5))
                pygame.draw.circle(screen, WHITE, (int(sparkle_pos[0]), int(sparkle_pos[1])), 1)
        
        # Draw far mountains
        for mountain in self.far_mountains:
            points = [
                (mountain['x'], mountain['y'] + mountain['height']),
                (mountain['x'] + mountain['width'] // 2, mountain['y']),
                (mountain['x'] + mountain['width'], mountain['y'] + mountain['height'])
            ]
            pygame.draw.polygon(screen, mountain['color'], points)
            
            # Add snow caps
            snow_points = [
                (mountain['x'] + mountain['width'] // 2 - 10, mountain['y'] + 5),
                (mountain['x'] + mountain['width'] // 2, mountain['y']),
                (mountain['x'] + mountain['width'] // 2 + 10, mountain['y'] + 5)
            ]
            pygame.draw.polygon(screen, WHITE, snow_points)
        
        # Draw mountains
        for mountain in self.mountains:
            points = [
                (mountain['x'], mountain['y'] + mountain['height']),
                (mountain['x'] + mountain['width'] // 2, mountain['y']),
                (mountain['x'] + mountain['width'], mountain['y'] + mountain['height'])
            ]
            pygame.draw.polygon(screen, mountain['color'], points)
        
        # Draw hills
        for hill in self.hills:
            points = [
                (hill['x'], hill['y'] + hill['height']),
                (hill['x'] + hill['width'] // 2, hill['y']),
                (hill['x'] + hill['width'], hill['y'] + hill['height'])
            ]
            pygame.draw.polygon(screen, hill['color'], points)
        
        # Draw clouds with depth
        for cloud in self.clouds:
            cloud_color = (cloud['opacity'], cloud['opacity'], cloud['opacity'])
            
            # Main cloud body
            pygame.draw.circle(screen, cloud_color, (int(cloud['x']), int(cloud['y'])), cloud['size'])
            pygame.draw.circle(screen, cloud_color, (int(cloud['x'] - cloud['size'] * 0.7), int(cloud['y'])), int(cloud['size'] * 0.8))
            pygame.draw.circle(screen, cloud_color, (int(cloud['x'] + cloud['size'] * 0.7), int(cloud['y'])), int(cloud['size'] * 0.8))
            pygame.draw.circle(screen, cloud_color, (int(cloud['x']), int(cloud['y'] - cloud['size'] * 0.5)), int(cloud['size'] * 0.6))
        
        # Draw floating particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 300))
            particle_color = (*particle['color'], alpha)
            pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])
        
        # Lightning effect
        for flash in self.lightning_flashes:
            lightning_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            lightning_color = (255, 255, 255, flash['intensity'])
            lightning_surface.fill(lightning_color)
            screen.blit(lightning_surface, (0, 0))
        
        # Draw ground with detailed texture
        ground_gradient = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
        for y in range(SCREEN_HEIGHT - GROUND_Y):
            ratio = y / (SCREEN_HEIGHT - GROUND_Y)
            r = int(50 * (1 - ratio * 0.5))
            g = int(200 * (1 - ratio * 0.3))
            b = int(50 * (1 - ratio * 0.5))
            pygame.draw.line(ground_gradient, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        screen.blit(ground_gradient, (0, GROUND_Y))
        
        # Draw detailed grass texture
        for i in range(0, SCREEN_WIDTH, 15):
            grass_height = random.randint(3, 8)
            grass_color = (random.randint(40, 80), random.randint(180, 220), random.randint(40, 80))
            pygame.draw.line(screen, grass_color, (i, GROUND_Y), (i + random.randint(-3, 3), GROUND_Y - grass_height), 2)
        
        # Draw ground details
        for i in range(0, SCREEN_WIDTH, 50):
            detail_x = i + random.randint(-20, 20)
            detail_y = GROUND_Y + random.randint(0, 20)
            detail_size = random.randint(2, 5)
            detail_color = (random.randint(80, 120), random.randint(60, 100), random.randint(20, 40))
            pygame.draw.circle(screen, detail_color, (detail_x, detail_y), detail_size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Cheetah - Nature Edition")
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
        self.cheetah = PowerUpCheetah(100, GROUND_Y - 40, self.audio_manager)
        self.obstacles = []
        self.platforms = []
        self.powerups = []
        self.background = EnhancedBackground(self.levels[self.current_level - 1].background_color)
        self.score = 0
        self.game_state = GameState.MENU
        self.game_start_time = 0
        self.last_score = 0
        
    def spawn_obstacle(self):
        current_level_data = self.levels[self.current_level - 1]
        
        if hasattr(self, 'game_start_time'):
            time_since_start = pygame.time.get_ticks() - self.game_start_time
            if time_since_start < 2000:
                return
        
        can_spawn = True
        for obstacle in self.obstacles:
            if obstacle.x > SCREEN_WIDTH - MIN_OBSTACLE_SPACING:
                can_spawn = False
                break
        
        if can_spawn and random.random() < current_level_data.obstacle_spawn_rate:
            obstacle_type = random.choice(current_level_data.obstacle_types)
            self.obstacles.append(NatureObstacle(SCREEN_WIDTH + 50, obstacle_type, current_level_data))
    
    def spawn_platform(self):
        current_level_data = self.levels[self.current_level - 1]
        
        if hasattr(self, 'game_start_time'):
            time_since_start = pygame.time.get_ticks() - self.game_start_time
            if time_since_start < 3000:
                return
        
        can_spawn = True
        for platform in self.platforms:
            if platform.x > SCREEN_WIDTH - 400:
                can_spawn = False
                break
        
        if can_spawn and random.random() < current_level_data.platform_spawn_rate:
            platform_type = random.choice(current_level_data.platform_types)
            platform_y = random.randint(GROUND_Y - 300, GROUND_Y - 100)
            self.platforms.append(Platform(SCREEN_WIDTH + 50, platform_y, platform_type, current_level_data))
    
    def spawn_powerup(self):
        current_level_data = self.levels[self.current_level - 1]
        
        if hasattr(self, 'game_start_time'):
            time_since_start = pygame.time.get_ticks() - self.game_start_time
            if time_since_start < 5000:  # Wait 5 seconds before spawning power-ups
                return
        
        can_spawn = True
        for powerup in self.powerups:
            if powerup.x > SCREEN_WIDTH - 600:
                can_spawn = False
                break
        
        if can_spawn and random.random() < current_level_data.powerup_spawn_rate:
            powerup_type = random.choice(list(PowerUpType))
            powerup_y = random.randint(GROUND_Y - 350, GROUND_Y - 150)
            self.powerups.append(PowerUp(SCREEN_WIDTH + 50, powerup_y, powerup_type, current_level_data))
    
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
            self.cheetah.update(self.platforms, self.powerups)
            self.background.update()
            
            self.spawn_obstacle()
            self.spawn_platform()
            self.spawn_powerup()
            
            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.x + obstacle.width < 0:
                    self.obstacles.remove(obstacle)
                    self.score += 1
            
            for platform in self.platforms[:]:
                platform.update()
                if platform.x + platform.width < 0:
                    self.platforms.remove(platform)
                    self.score += 1
            
            for powerup in self.powerups[:]:
                powerup.update()
                if powerup.x + powerup.size < 0:
                    self.powerups.remove(powerup)
            
            if self.score > self.last_score:
                self.audio_manager.play_sound('score')
                self.last_score = self.score
            
            if self.check_collision():
                self.cheetah.lives -= 1
                if self.cheetah.lives <= 0:
                    self.audio_manager.play_sound('death')
                    self.game_state = GameState.GAME_OVER
                    current_level_data = self.levels[self.current_level - 1]
                    if self.score > current_level_data.best_score:
                        current_level_data.best_score = self.score
                else:
                    # Reset cheetah position but keep power-ups
                    self.cheetah.x = 100
                    self.cheetah.y = GROUND_Y - 40
                    self.cheetah.velocity_y = 0
                    self.cheetah.make_invincible(120)  # 2 seconds of invincibility
            
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
        
        # Handle flying controls
        keys = pygame.key.get_pressed()
        if self.game_state == GameState.PLAYING and self.cheetah.flying:
            if keys[pygame.K_UP]:
                self.cheetah.fly_up()
            elif keys[pygame.K_DOWN]:
                self.cheetah.fly_down()
        
        return True
    
    def draw(self):
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
    
    def draw_menu(self):
        # Draw animated background
        self.background.draw(self.screen)
        
        # Title with glow effect
        title_text = self.title_font.render("GEOMETRY CHEETAH", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Glow effect
        for i in range(5):
            glow_color = (100, 100, 255, 50 - i * 10)
            glow_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
            glow_surface.fill(glow_color)
            self.screen.blit(glow_surface, (title_rect.x - i, title_rect.y - i))
        
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font.render("Nature Edition", True, GREEN)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Instructions
        instruction1 = self.small_font.render("Press SPACE to start", True, WHITE)
        instruction1_rect = instruction1.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(instruction1, instruction1_rect)
        
        instruction2 = self.small_font.render("Experience nature-themed obstacles!", True, WHITE)
        instruction2_rect = instruction2.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(instruction2, instruction2_rect)
        
        # Features list
        features = [
            "🪨 Detailed rocks with realistic textures",
            "🌿 Spiky bushes with animated swaying",
            "🏔️ Rock clusters and moving boulders",
            "🌟 Enhanced backgrounds with parallax",
            "✨ All power-ups and enhanced gameplay",
            "🎨 Nature-themed obstacle designs"
        ]
        
        for i, feature in enumerate(features):
            feature_text = self.small_font.render(feature, True, WHITE)
            feature_rect = feature_text.get_rect(center=(SCREEN_WIDTH // 2, 450 + i * 25))
            self.screen.blit(feature_text, feature_rect)
    
    def draw_level_select(self):
        # Draw animated background
        self.background.draw(self.screen)
        
        # Title
        title_text = self.font.render("Select Level", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Level options
        for i, level in enumerate(self.levels):
            y_pos = 200 + i * 80
            color = WHITE if i + 1 == self.selected_level else GRAY
            
            # Level background
            level_bg_color = (*level.background_color, 100)
            level_surface = pygame.Surface((400, 60), pygame.SRCALPHA)
            level_surface.fill(level_bg_color)
            self.screen.blit(level_surface, (SCREEN_WIDTH // 2 - 200, y_pos - 10))
            
            # Level text
            level_text = self.font.render(f"Level {level.level_num}: {level.name}", True, color)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(level_text, level_rect)
            
            # Description
            desc_text = self.small_font.render(level.description, True, color)
            desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 25))
            self.screen.blit(desc_text, desc_rect)
            
            # Best score
            if level.best_score > 0:
                score_text = self.small_font.render(f"Best: {level.best_score}", True, GOLD)
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2 + 150, y_pos + 10))
                self.screen.blit(score_text, score_rect)
            
            # Completion indicator
            if level.completed:
                complete_text = self.small_font.render("✓", True, GREEN)
                complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2 - 150, y_pos + 10))
                self.screen.blit(complete_text, complete_rect)
        
        # Instructions
        instruction1 = self.small_font.render("Use UP/DOWN arrows to select, SPACE to start", True, WHITE)
        instruction1_rect = instruction1.get_rect(center=(SCREEN_WIDTH // 2, 550))
        self.screen.blit(instruction1, instruction1_rect)
    
    def draw_game(self):
        # Draw enhanced background
        self.background.draw(self.screen)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Draw nature obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw power-ups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw cheetah
        self.cheetah.draw(self.screen)
        
        # Draw UI
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        # Lives
        lives_text = self.font.render(f"Lives: {self.cheetah.lives}", True, WHITE)
        self.screen.blit(lives_text, (20, 60))
        
        # Level info
        current_level_data = self.levels[self.current_level - 1]
        level_text = self.small_font.render(f"Level {self.current_level}: {current_level_data.name}", True, WHITE)
        self.screen.blit(level_text, (20, 100))
        
        # Power-up indicators
        y_offset = 130
        if self.cheetah.flying:
            flying_text = self.small_font.render("FLYING", True, CYAN)
            self.screen.blit(flying_text, (20, y_offset))
            y_offset += 25
        if self.cheetah.invincible:
            invincible_text = self.small_font.render("INVINCIBLE", True, GOLD)
            self.screen.blit(invincible_text, (20, y_offset))
            y_offset += 25
        if self.cheetah.slow_time:
            slow_text = self.small_font.render("SLOW TIME", True, BLUE)
            self.screen.blit(slow_text, (20, y_offset))
            y_offset += 25
        if self.cheetah.magnet:
            magnet_text = self.small_font.render("MAGNET", True, SILVER)
            self.screen.blit(magnet_text, (20, y_offset))
    
    def draw_game_over(self):
        # Draw background
        self.background.draw(self.screen)
        
        # Game over text
        game_over_text = self.title_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(score_text, score_rect)
        
        # Instructions
        instruction1 = self.small_font.render("Press SPACE to retry", True, WHITE)
        instruction1_rect = instruction1.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(instruction1, instruction1_rect)
        
        instruction2 = self.small_font.render("Press ESC for level select", True, WHITE)
        instruction2_rect = instruction2.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(instruction2, instruction2_rect)
    
    def draw_level_complete(self):
        # Draw background
        self.background.draw(self.screen)
        
        # Level complete text
        complete_text = self.title_font.render("LEVEL COMPLETE!", True, GREEN)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(complete_text, complete_rect)
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        self.screen.blit(score_text, score_rect)
        
        # Next level or game complete
        if self.current_level < len(self.levels):
            next_text = self.small_font.render("Press SPACE for next level", True, WHITE)
        else:
            next_text = self.small_font.render("All levels completed! Press SPACE for menu", True, WHITE)
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(next_text, next_rect)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 