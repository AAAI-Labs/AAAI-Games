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
        
        sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
            pygame.Surface((len(sound_array), 1, 3))
        ))
        self.sounds['jump'] = sound_surface
    
    def create_land_sound(self):
        sample_rate = 44100
        duration = 0.15
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 200 * math.exp(-i / (samples * 0.3))
            sample = int(32767 * 0.4 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
            pygame.Surface((len(sound_array), 1, 3))
        ))
        self.sounds['land'] = sound_surface
    
    def create_death_sound(self):
        sample_rate = 44100
        duration = 0.5
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 600 * math.exp(-i / (samples * 0.5))
            sample = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
            pygame.Surface((len(sound_array), 1, 3))
        ))
        self.sounds['death'] = sound_surface
    
    def create_score_sound(self):
        sample_rate = 44100
        duration = 0.1
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 800 + 200 * math.sin(i / samples * 4 * math.pi)
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
            pygame.Surface((len(sound_array), 1, 3))
        ))
        self.sounds['score'] = sound_surface
    
    def create_level_complete_sound(self):
        sample_rate = 44100
        duration = 0.8
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            if i < samples // 3:
                frequency = 523
            elif i < 2 * samples // 3:
                frequency = 659
            else:
                frequency = 784
            sample = int(32767 * 0.4 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
            pygame.Surface((len(sound_array), 1, 3))
        ))
        self.sounds['level_complete'] = sound_surface
    
    def create_menu_select_sound(self):
        sample_rate = 44100
        duration = 0.1
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 300
            sample = int(32767 * 0.2 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
            pygame.Surface((len(sound_array), 1, 3))
        ))
        self.sounds['menu_select'] = sound_surface
    
    def create_bounce_sound(self):
        sample_rate = 44100
        duration = 0.15
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 600 * math.exp(-i / (samples * 0.2))
            sample = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
            pygame.Surface((len(sound_array), 1, 3))
        ))
        self.sounds['bounce'] = sound_surface
    
    def create_powerup_sound(self):
        sample_rate = 44100
        duration = 0.3
        samples = int(sample_rate * duration)
        
        sound_array = []
        for i in range(samples):
            frequency = 600 + 400 * math.sin(i / samples * 6 * math.pi)
            sample = int(32767 * 0.4 * math.sin(2 * math.pi * frequency * i / sample_rate))
            sound_array.append(sample)
        
        sound_surface = pygame.sndarray.make_sound(pygame.surfarray.pixels3d(
            pygame.Surface((len(sound_array), 1, 3))
        ))
        self.sounds['powerup'] = sound_surface
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def start_music(self):
        if not self.music_playing:
            try:
                self.music_playing = True
            except:
                pass
    
    def stop_music(self):
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
        
        if level_num == 1:
            self.obstacle_speed = 4
            self.obstacle_spawn_rate = 0.02
            self.obstacle_types = ["spike", "block"]
            self.platform_types = ["normal", "wide"]
            self.platform_spawn_rate = 0.03
            self.powerup_spawn_rate = 0.008  # Power-ups spawn occasionally
            self.required_score = 20
            self.background_color = BLUE
        elif level_num == 2:
            self.obstacle_speed = 5
            self.obstacle_spawn_rate = 0.025
            self.obstacle_types = ["spike", "block", "flying_spike"]
            self.platform_types = ["normal", "wide", "moving_slow"]
            self.platform_spawn_rate = 0.04
            self.powerup_spawn_rate = 0.01
            self.required_score = 35
            self.background_color = PURPLE
        elif level_num == 3:
            self.obstacle_speed = 6
            self.obstacle_spawn_rate = 0.03
            self.obstacle_types = ["spike", "block", "flying_spike", "double_spike"]
            self.platform_types = ["normal", "wide", "moving_slow", "bouncy"]
            self.platform_spawn_rate = 0.05
            self.powerup_spawn_rate = 0.012
            self.required_score = 50
            self.background_color = RED
        elif level_num == 4:
            self.obstacle_speed = 7
            self.obstacle_spawn_rate = 0.035
            self.obstacle_types = ["spike", "block", "flying_spike", "double_spike", "moving_spike"]
            self.platform_types = ["normal", "wide", "moving_slow", "bouncy", "disappearing_slow"]
            self.platform_spawn_rate = 0.06
            self.powerup_spawn_rate = 0.015
            self.required_score = 70
            self.background_color = ORANGE
        elif level_num == 5:
            self.obstacle_speed = 8
            self.obstacle_spawn_rate = 0.04
            self.obstacle_types = ["spike", "block", "flying_spike", "double_spike", "moving_spike", "laser"]
            self.platform_types = ["normal", "wide", "moving_slow", "bouncy", "disappearing_slow", "teleport_slow"]
            self.platform_spawn_rate = 0.07
            self.powerup_spawn_rate = 0.018
            self.required_score = 100
            self.background_color = CYAN

class PowerUpCheetah:
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
        self.was_on_platform = False
        self.eye_blink_timer = 0
        self.tail_wag_timer = 0
        self.ear_twitch_timer = 0
        self.glow_effect = 0
        
        # Power-up states
        self.lives = 3
        self.flying = False
        self.flying_timer = 0
        self.double_jump_available = False
        self.double_jump_used = False
        self.slow_time = False
        self.slow_time_timer = 0
        self.magnet = False
        self.magnet_timer = 0
        self.active_powerups = []
        
    def update(self, platforms, powerups):
        # Apply gravity (unless flying)
        if not self.flying:
            self.velocity_y += GRAVITY
        else:
            # Flying mode - controlled vertical movement
            self.velocity_y = 0
        
        self.y += self.velocity_y
        
        # Reset platform status
        self.is_on_platform = False
        self.current_platform = None
        
        # Check platform collisions
        for platform in platforms:
            if self.check_platform_collision(platform):
                if self.velocity_y > 0:  # Falling down
                    self.y = platform.y - 40
                    self.velocity_y = 0
                    self.is_on_ground = True
                    self.is_jumping = False
                    self.is_on_platform = True
                    self.current_platform = platform
                    
                    if not self.was_on_platform:
                        self.audio_manager.play_sound('land')
                        # Reset double jump when landing
                        self.double_jump_used = False
                    break
        
        # Ground collision
        if not self.is_on_platform and self.y >= GROUND_Y - 40:
            self.y = GROUND_Y - 40
            self.velocity_y = 0
            self.is_on_ground = True
            self.is_jumping = False
            
            if not self.was_on_platform:
                self.audio_manager.play_sound('land')
                self.double_jump_used = False
        elif not self.is_on_platform:
            self.is_on_ground = False
        
        # Update platform state tracking
        self.was_on_platform = self.is_on_platform
        
        # Check power-up collisions
        for powerup in powerups:
            if not powerup.collected and self.check_powerup_collision(powerup):
                self.collect_powerup(powerup)
        
        # Update power-up timers
        if self.flying:
            self.flying_timer -= 1
            if self.flying_timer <= 0:
                self.flying = False
                self.active_powerups.remove("Flying")
        
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
                if "Invincibility" in self.active_powerups:
                    self.active_powerups.remove("Invincibility")
        
        if self.slow_time:
            self.slow_time_timer -= 1
            if self.slow_time_timer <= 0:
                self.slow_time = False
                self.active_powerups.remove("Slow Time")
        
        if self.magnet:
            self.magnet_timer -= 1
            if self.magnet_timer <= 0:
                self.magnet = False
                self.active_powerups.remove("Magnet")
        
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
            
        # Update animation timers
        self.eye_blink_timer += 1
        self.tail_wag_timer += 1
        self.ear_twitch_timer += 1
        self.glow_effect = (self.glow_effect + 1) % 60
            
        # Update trail particles
        for particle in self.trail_particles[:]:
            particle['life'] -= 1
            particle['x'] -= 2
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
                
        # Add trail particles when moving
        if not self.is_on_ground and not self.is_on_platform and random.random() < 0.3:
            color = CYAN if self.flying else ORANGE
            self.trail_particles.append({
                'x': self.x - 20,
                'y': self.y + 20,
                'life': 10,
                'color': color
            })
    
    def check_platform_collision(self, platform):
        cheetah_rect = pygame.Rect(self.x - 25, self.y - 25, 50, 50)
        platform_rect = platform.get_rect()
        
        if (self.velocity_y > 0 and 
            cheetah_rect.colliderect(platform_rect) and
            self.y < platform.y):
            return True
        return False
    
    def check_powerup_collision(self, powerup):
        cheetah_rect = pygame.Rect(self.x - 25, self.y - 25, 50, 50)
        powerup_rect = powerup.get_rect()
        return cheetah_rect.colliderect(powerup_rect)
    
    def collect_powerup(self, powerup):
        powerup.collected = True
        self.audio_manager.play_sound('powerup')
        
        if powerup.power_type == PowerUpType.EXTRA_LIFE:
            self.lives += 1
            self.active_powerups.append("Extra Life")
        elif powerup.power_type == PowerUpType.FLYING:
            self.flying = True
            self.flying_timer = 300  # 5 seconds at 60 FPS
            self.active_powerups.append("Flying")
        elif powerup.power_type == PowerUpType.INVINCIBILITY:
            self.invincible = True
            self.invincible_timer = 180  # 3 seconds
            self.active_powerups.append("Invincibility")
        elif powerup.power_type == PowerUpType.DOUBLE_JUMP:
            self.double_jump_available = True
            self.double_jump_used = False
            self.active_powerups.append("Double Jump")
        elif powerup.power_type == PowerUpType.SLOW_TIME:
            self.slow_time = True
            self.slow_time_timer = 180  # 3 seconds
            self.active_powerups.append("Slow Time")
        elif powerup.power_type == PowerUpType.MAGNET:
            self.magnet = True
            self.magnet_timer = 240  # 4 seconds
            self.active_powerups.append("Magnet")
    
    def jump(self):
        if self.is_on_ground or self.is_on_platform:
            self.audio_manager.play_sound('jump')
            
            if self.current_platform and self.current_platform.platform_type == "bouncy":
                self.velocity_y = JUMP_FORCE * 1.3
                self.audio_manager.play_sound('bounce')
            else:
                self.velocity_y = JUMP_FORCE
            self.is_jumping = True
            self.is_on_ground = False
            self.is_on_platform = False
            self.double_jump_used = False
        elif self.double_jump_available and not self.double_jump_used:
            # Double jump
            self.velocity_y = JUMP_FORCE * 0.8
            self.double_jump_used = True
            self.audio_manager.play_sound('jump')
    
    def fly_up(self):
        if self.flying:
            self.velocity_y = -5
    
    def fly_down(self):
        if self.flying:
            self.velocity_y = 5
    
    def make_invincible(self, duration=60):
        self.invincible = True
        self.invincible_timer = duration
            
    def draw(self, screen):
        # Draw trail particles with effects
        for particle in self.trail_particles:
            alpha = int((particle['life'] / 10) * 255)
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(screen, (255, 200, 100, alpha//2), (int(particle['x']), int(particle['y'])), 6)
            pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), 3)
        
        # Draw cheetah with power-up effects
        cheetah_surface = pygame.Surface((100, 60), pygame.SRCALPHA)
        
        # Power-up glow effects
        if self.flying:
            glow_color = CYAN
        elif self.invincible:
            glow_color = GOLD
        elif self.slow_time:
            glow_color = BLUE
        elif self.magnet:
            glow_color = SILVER
        else:
            glow_color = (255, 200, 100)
        
        glow_intensity = int(20 + 10 * math.sin(self.glow_effect * 0.1))
        pygame.draw.ellipse(cheetah_surface, (*glow_color, glow_intensity), (10, 15, 80, 50))
        
        # Body with gradient and shading
        pygame.draw.ellipse(cheetah_surface, DARK_ORANGE, (15, 20, 50, 30))
        pygame.draw.ellipse(cheetah_surface, ORANGE, (18, 22, 44, 24))
        pygame.draw.ellipse(cheetah_surface, LIGHT_ORANGE, (20, 24, 40, 20))
        
        # Muscle definition
        pygame.draw.ellipse(cheetah_surface, DARK_ORANGE, (25, 25, 15, 8))
        pygame.draw.ellipse(cheetah_surface, DARK_ORANGE, (35, 28, 12, 6))
        
        # Spots
        spots = [
            (22, 28), (30, 26), (38, 30), (26, 32), (34, 30), (42, 28),
            (20, 25), (28, 23), (36, 27), (24, 29), (32, 27), (40, 25)
        ]
        for spot in spots:
            pygame.draw.circle(cheetah_surface, DARK_BROWN, (spot[0]+1, spot[1]+1), 4)
            pygame.draw.circle(cheetah_surface, BLACK, spot, 3)
            pygame.draw.circle(cheetah_surface, DARK_GRAY, (spot[0]-1, spot[1]-1), 1)
        
        # Head
        pygame.draw.circle(cheetah_surface, DARK_ORANGE, (60, 30), 18)
        pygame.draw.circle(cheetah_surface, ORANGE, (62, 32), 15)
        pygame.draw.circle(cheetah_surface, LIGHT_ORANGE, (64, 34), 12)
        
        # Ears
        ear_twitch = math.sin(self.ear_twitch_timer * 0.1) * 2
        pygame.draw.circle(cheetah_surface, DARK_ORANGE, (70, 18 + ear_twitch), 8)
        pygame.draw.circle(cheetah_surface, DARK_ORANGE, (74, 22 + ear_twitch), 7)
        pygame.draw.circle(cheetah_surface, PINK, (71, 19 + ear_twitch), 5)
        pygame.draw.circle(cheetah_surface, PINK, (75, 23 + ear_twitch), 4)
        pygame.draw.circle(cheetah_surface, WHITE, (72, 20 + ear_twitch), 2)
        pygame.draw.circle(cheetah_surface, WHITE, (76, 24 + ear_twitch), 2)
        
        # Eyes
        blink = self.eye_blink_timer > 100 and self.eye_blink_timer < 105
        if not blink:
            pygame.draw.circle(cheetah_surface, WHITE, (65, 28), 6)
            pygame.draw.circle(cheetah_surface, WHITE, (68, 28), 6)
            pygame.draw.circle(cheetah_surface, GOLD, (66, 29), 3)
            pygame.draw.circle(cheetah_surface, GOLD, (69, 29), 3)
            pygame.draw.circle(cheetah_surface, BLACK, (66, 30), 2)
            pygame.draw.circle(cheetah_surface, BLACK, (69, 30), 2)
            pygame.draw.circle(cheetah_surface, WHITE, (65.5, 28.5), 1)
            pygame.draw.circle(cheetah_surface, WHITE, (68.5, 28.5), 1)
        else:
            pygame.draw.ellipse(cheetah_surface, BLACK, (62, 26, 6, 2))
            pygame.draw.ellipse(cheetah_surface, BLACK, (65, 26, 6, 2))
        
        # Nose and mouth
        pygame.draw.circle(cheetah_surface, BLACK, (78, 30), 3)
        pygame.draw.circle(cheetah_surface, PINK, (79, 31), 1)
        pygame.draw.arc(cheetah_surface, BLACK, (70, 30, 8, 6), 0, 3.14, 2)
        pygame.draw.circle(cheetah_surface, PINK, (74, 33), 1)
        
        # Whiskers
        whisker_points = [(75, 28), (85, 26), (75, 29), (85, 29), (75, 30), (85, 32)]
        for i in range(0, len(whisker_points), 2):
            pygame.draw.line(cheetah_surface, WHITE, whisker_points[i], whisker_points[i+1], 1)
        
        # Legs
        leg_positions = [(22, 40), (32, 40), (42, 40), (52, 40)]
        for pos in leg_positions:
            pygame.draw.rect(cheetah_surface, DARK_ORANGE, (pos[0], pos[1], 6, 15))
            pygame.draw.rect(cheetah_surface, ORANGE, (pos[0]+1, pos[1]+1, 4, 13))
            pygame.draw.rect(cheetah_surface, DARK_ORANGE, (pos[0]+1, pos[1]+15, 4, 8))
            pygame.draw.rect(cheetah_surface, ORANGE, (pos[0]+2, pos[1]+16, 2, 6))
        
        # Paws
        paw_positions = [(24, 53), (34, 53), (44, 53), (54, 53)]
        for pos in paw_positions:
            pygame.draw.circle(cheetah_surface, BLACK, pos, 3)
            pygame.draw.circle(cheetah_surface, DARK_GRAY, (pos[0]-1, pos[1]-1), 1)
        
        # Tail
        tail_wag = math.sin(self.tail_wag_timer * 0.2) * 5
        tail_base = (18, 30)
        tail_mid = (10, 25 + tail_wag)
        tail_tip = (2, 30 + tail_wag * 2)
        
        pygame.draw.polygon(cheetah_surface, DARK_BROWN, [
            (tail_base[0]+2, tail_base[1]+2), 
            (tail_mid[0]+2, tail_mid[1]+2), 
            (tail_tip[0]+2, tail_tip[1]+2),
            (tail_mid[0]+2, tail_base[1]+2)
        ])
        
        pygame.draw.polygon(cheetah_surface, DARK_ORANGE, [tail_base, tail_mid, tail_tip, (tail_mid[0], tail_base[1])])
        pygame.draw.polygon(cheetah_surface, ORANGE, [
            (tail_base[0]+2, tail_base[1]+2), 
            (tail_mid[0]+2, tail_mid[1]+2), 
            (tail_tip[0]+2, tail_tip[1]+2),
            (tail_mid[0]+2, tail_base[1]+2)
        ])
        
        tail_spots = [(12, 27), (8, 28), (4, 29)]
        for spot in tail_spots:
            pygame.draw.circle(cheetah_surface, BLACK, (spot[0] + tail_wag//2, spot[1]), 2)
        
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

# Rest of the classes (Platform, Obstacle, Background) would be included here
# They would be the same as in previous versions

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Cheetah - Power-Ups Edition")
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
        self.background = Background(self.levels[self.current_level - 1].background_color)
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
            self.obstacles.append(Obstacle(SCREEN_WIDTH + 50, obstacle_type, current_level_data))
    
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
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

# Add the missing classes (Platform, Obstacle, Background) here
# They would be the same as in previous versions

if __name__ == "__main__":
    game = Game()
    game.run() 