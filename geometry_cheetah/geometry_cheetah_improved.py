import pygame
import random
import math
from enum import Enum

# Initialize Pygame
pygame.init()

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

class Level:
    def __init__(self, level_num, name, description, color):
        self.level_num = level_num
        self.name = name
        self.description = description
        self.color = color
        self.completed = False
        self.best_score = 0
        self.required_score = 0
        
        # Level-specific settings - EASIER PLATFORMS
        if level_num == 1:
            self.obstacle_speed = 4  # Reduced from 5
            self.obstacle_spawn_rate = 0.02  # Reduced from 0.025
            self.obstacle_types = ["spike", "block"]
            self.platform_types = ["normal", "wide"]  # Easier platforms
            self.platform_spawn_rate = 0.03  # More platforms
            self.required_score = 20  # Reduced from 25
            self.background_color = BLUE
        elif level_num == 2:
            self.obstacle_speed = 5  # Reduced from 7
            self.obstacle_spawn_rate = 0.025  # Reduced from 0.035
            self.obstacle_types = ["spike", "block", "flying_spike"]
            self.platform_types = ["normal", "wide", "moving_slow"]  # Easier moving platforms
            self.platform_spawn_rate = 0.04
            self.required_score = 35  # Reduced from 45
            self.background_color = PURPLE
        elif level_num == 3:
            self.obstacle_speed = 6  # Reduced from 9
            self.obstacle_spawn_rate = 0.03  # Reduced from 0.045
            self.obstacle_types = ["spike", "block", "flying_spike", "double_spike"]
            self.platform_types = ["normal", "wide", "moving_slow", "bouncy"]
            self.platform_spawn_rate = 0.05
            self.required_score = 50  # Reduced from 70
            self.background_color = RED
        elif level_num == 4:
            self.obstacle_speed = 7  # Reduced from 11
            self.obstacle_spawn_rate = 0.035  # Reduced from 0.055
            self.obstacle_types = ["spike", "block", "flying_spike", "double_spike", "moving_spike"]
            self.platform_types = ["normal", "wide", "moving_slow", "bouncy", "disappearing_slow"]
            self.platform_spawn_rate = 0.06
            self.required_score = 70  # Reduced from 100
            self.background_color = ORANGE
        elif level_num == 5:
            self.obstacle_speed = 8  # Reduced from 13
            self.obstacle_spawn_rate = 0.04  # Reduced from 0.065
            self.obstacle_types = ["spike", "block", "flying_spike", "double_spike", "moving_spike", "laser"]
            self.platform_types = ["normal", "wide", "moving_slow", "bouncy", "disappearing_slow", "teleport_slow"]
            self.platform_spawn_rate = 0.07
            self.required_score = 100  # Reduced from 150
            self.background_color = CYAN

class Cheetah:
    def __init__(self, x, y):
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
        
    def update(self, platforms):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Reset platform status
        self.is_on_platform = False
        self.current_platform = None
        
        # Check platform collisions with LARGER collision box for easier landing
        for platform in platforms:
            if self.check_platform_collision(platform):
                if self.velocity_y > 0:  # Falling down
                    self.y = platform.y - 40
                    self.velocity_y = 0
                    self.is_on_ground = True
                    self.is_jumping = False
                    self.is_on_platform = True
                    self.current_platform = platform
                    break
        
        # Ground collision (only if not on platform)
        if not self.is_on_platform and self.y >= GROUND_Y - 40:
            self.y = GROUND_Y - 40
            self.velocity_y = 0
            self.is_on_ground = True
            self.is_jumping = False
        elif not self.is_on_platform:
            self.is_on_ground = False
            
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
    
    def check_platform_collision(self, platform):
        # LARGER collision box for easier platform landing
        cheetah_rect = pygame.Rect(self.x - 25, self.y - 25, 50, 50)
        platform_rect = platform.get_rect()
        return cheetah_rect.colliderect(platform_rect)
    
    def jump(self):
        if self.is_on_ground or self.is_on_platform:
            # Special jump for bouncy platforms
            if self.current_platform and self.current_platform.platform_type == "bouncy":
                self.velocity_y = JUMP_FORCE * 1.3  # Slightly higher jump
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

class Platform:
    def __init__(self, x, y, platform_type="normal", level_settings=None):
        self.x = x
        self.y = y
        self.platform_type = platform_type
        self.level_settings = level_settings or Level(1, "Tutorial", "Easy level", BLUE)
        self.movement_timer = 0
        self.original_y = y
        self.visible = True
        self.teleport_timer = 0
        
        # Set properties based on platform type - EASIER PLATFORMS
        if platform_type == "normal":
            self.width = 100  # Increased from 80
            self.height = 25  # Increased from 20
            self.color = GREEN
        elif platform_type == "wide":
            self.width = 120  # New wide platform
            self.height = 30
            self.color = LIME
        elif platform_type == "moving_slow":
            self.width = 90  # Increased from 70
            self.height = 25  # Increased from 18
            self.color = CYAN
        elif platform_type == "disappearing_slow":
            self.width = 80  # Increased from 60
            self.height = 22  # Increased from 16
            self.color = YELLOW
            self.disappear_timer = 0
        elif platform_type == "bouncy":
            self.width = 95  # Increased from 75
            self.height = 25  # Increased from 20
            self.color = PINK
        elif platform_type == "teleport_slow":
            self.width = 85  # Increased from 65
            self.height = 22  # Increased from 17
            self.color = PURPLE
        
    def update(self):
        self.x -= self.level_settings.obstacle_speed
        self.movement_timer += 1
        
        # Special movement for moving platforms - SLOWER
        if self.platform_type == "moving_slow":
            self.y = self.original_y + math.sin(self.movement_timer * 0.05) * 30  # Slower movement
            
        # Disappearing platform logic - SLOWER
        elif self.platform_type == "disappearing_slow":
            self.disappear_timer += 1
            if self.disappear_timer > 180:  # Disappear after 3 seconds (was 2)
                self.visible = False
                
        # Teleport platform logic - SLOWER
        elif self.platform_type == "teleport_slow":
            self.teleport_timer += 1
            if self.teleport_timer > 240:  # Teleport every 4 seconds (was 3)
                self.y = random.randint(GROUND_Y - 250, GROUND_Y - 80)
                self.teleport_timer = 0
            
    def draw(self, screen):
        if not self.visible:
            return
            
        # Draw platform with better graphics
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Add platform border for better visibility
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)
        
        # Add special effects
        if self.platform_type == "disappearing_slow":
            # Add warning effect
            if self.disappear_timer > 150:  # Flash when about to disappear
                if self.disappear_timer % 30 < 15:  # Slower flashing
                    pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height), 3)
                    
        elif self.platform_type == "bouncy":
            # Add bounce effect
            pygame.draw.rect(screen, WHITE, (self.x + 5, self.y + 5, self.width - 10, 8))
            pygame.draw.rect(screen, PINK, (self.x + 8, self.y + 8, self.width - 16, 4))
            
        elif self.platform_type == "teleport_slow":
            # Add teleport effect
            if self.teleport_timer > 200:  # Flash before teleporting
                if self.teleport_timer % 20 < 10:  # Slower flashing
                    pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 3)
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Rest of the classes remain the same as in the ultimate version
class Obstacle:
    def __init__(self, x, obstacle_type="spike", level_settings=None):
        self.x = x
        self.obstacle_type = obstacle_type
        self.level_settings = level_settings or Level(1, "Tutorial", "Easy level", BLUE)
        self.width = 30
        self.movement_timer = 0
        self.original_y = 0
        
        # Set properties based on obstacle type
        if obstacle_type == "spike":
            self.height = 45
            self.color = RED
        elif obstacle_type == "block":
            self.height = 50
            self.color = RED
        elif obstacle_type == "flying_spike":
            self.height = 40
            self.color = RED
            self.y_offset = -250
        elif obstacle_type == "double_spike":
            self.height = 45
            self.color = PURPLE
            self.width = 60
        elif obstacle_type == "moving_spike":
            self.height = 45
            self.color = CYAN
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
        
        # Special movement for moving obstacles
        if self.obstacle_type == "moving_spike":
            self.y_offset = math.sin(self.movement_timer * 0.1) * 30
            
    def draw(self, screen):
        if self.obstacle_type == "spike":
            points = [(self.x, GROUND_Y), (self.x + 15, GROUND_Y - self.height), (self.x + 30, GROUND_Y)]
            pygame.draw.polygon(screen, self.color, points)
        elif self.obstacle_type == "block":
            pygame.draw.rect(screen, self.color, (self.x, GROUND_Y - self.height, self.width, self.height))
        elif self.obstacle_type == "flying_spike":
            points = [(self.x, GROUND_Y + self.y_offset), (self.x + 15, GROUND_Y + self.y_offset - self.height), (self.x + 30, GROUND_Y + self.y_offset)]
            pygame.draw.polygon(screen, self.color, points)
        elif self.obstacle_type == "double_spike":
            points1 = [(self.x, GROUND_Y), (self.x + 15, GROUND_Y - self.height), (self.x + 30, GROUND_Y)]
            points2 = [(self.x + 30, GROUND_Y), (self.x + 45, GROUND_Y - self.height), (self.x + 60, GROUND_Y)]
            pygame.draw.polygon(screen, self.color, points1)
            pygame.draw.polygon(screen, self.color, points2)
        elif self.obstacle_type == "moving_spike":
            points = [(self.x, GROUND_Y + self.y_offset), (self.x + 15, GROUND_Y + self.y_offset - self.height), (self.x + 30, GROUND_Y + self.y_offset)]
            pygame.draw.polygon(screen, self.color, points)
        elif self.obstacle_type == "laser":
            pygame.draw.rect(screen, self.color, (self.x, GROUND_Y + self.y_offset, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x, GROUND_Y + self.y_offset, self.width, 2))
            
    def get_rect(self):
        if self.obstacle_type == "spike":
            return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)
        elif self.obstacle_type == "block":
            return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)
        elif self.obstacle_type == "flying_spike":
            return pygame.Rect(self.x, GROUND_Y + self.y_offset - self.height, self.width, self.height)
        elif self.obstacle_type == "double_spike":
            return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)
        elif self.obstacle_type == "moving_spike":
            return pygame.Rect(self.x, GROUND_Y + self.y_offset - self.height, self.width, self.height)
        elif self.obstacle_type == "laser":
            return pygame.Rect(self.x, GROUND_Y + self.y_offset, self.width, self.height)

class Background:
    def __init__(self, level_color=BLUE):
        self.clouds = []
        self.stars = []
        self.parallax_offset = 0
        self.level_color = level_color
        
        # Generate clouds
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 200),
                'size': random.randint(30, 80)
            })
            
        # Generate stars
        for _ in range(20):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 300),
                'brightness': random.randint(100, 255),
                'twinkle_speed': random.uniform(0.02, 0.05)
            })
        
    def update(self):
        # Update parallax offset
        self.parallax_offset += 0.5
        
        # Update clouds
        for cloud in self.clouds:
            cloud['x'] -= 0.5
            if cloud['x'] + cloud['size'] < 0:
                cloud['x'] = SCREEN_WIDTH + cloud['size']
                cloud['y'] = random.randint(50, 200)
        
        # Update stars
        for star in self.stars:
            star['brightness'] += math.sin(pygame.time.get_ticks() * star['twinkle_speed']) * 10
            star['brightness'] = max(50, min(255, star['brightness']))
        
    def draw(self, screen):
        # Draw gradient sky
        for y in range(SCREEN_HEIGHT):
            # Create gradient from level color to darker shade
            ratio = y / SCREEN_HEIGHT
            r = int(self.level_color[0] * (1 - ratio * 0.5))
            g = int(self.level_color[1] * (1 - ratio * 0.5))
            b = int(self.level_color[2] * (1 - ratio * 0.5))
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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Cheetah - Improved Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 72)
        
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
        self.cheetah = Cheetah(100, GROUND_Y - 40)
        self.obstacles = []
        self.platforms = []
        self.background = Background(self.levels[self.current_level - 1].background_color)
        self.score = 0
        self.game_state = GameState.MENU
        self.game_start_time = 0
        
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
    
    def spawn_platform(self):
        current_level_data = self.levels[self.current_level - 1]
        
        # Don't spawn platforms for the first 3 seconds of gameplay
        if hasattr(self, 'game_start_time'):
            time_since_start = pygame.time.get_ticks() - self.game_start_time
            if time_since_start < 3000:  # 3 seconds delay
                return
        
        # Check if we can spawn a new platform
        can_spawn = True
        for platform in self.platforms:
            if platform.x > SCREEN_WIDTH - 400:  # More spacing for platforms
                can_spawn = False
                break
        
        if can_spawn and random.random() < current_level_data.platform_spawn_rate:
            platform_type = random.choice(current_level_data.platform_types)
            platform_y = random.randint(GROUND_Y - 300, GROUND_Y - 100)
            self.platforms.append(Platform(SCREEN_WIDTH + 50, platform_y, platform_type, current_level_data))
    
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
            self.cheetah.update(self.platforms)
            self.background.update()
            
            # Spawn obstacles and platforms
            self.spawn_obstacle()
            self.spawn_platform()
            
            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.x + obstacle.width < 0:
                    self.obstacles.remove(obstacle)
                    self.score += 1
            
            # Update platforms
            for platform in self.platforms[:]:
                platform.update()
                if platform.x + platform.width < 0:
                    self.platforms.remove(platform)
                    self.score += 1
            
            # Check collision
            if self.check_collision():
                self.game_state = GameState.GAME_OVER
                current_level_data = self.levels[self.current_level - 1]
                if self.score > current_level_data.best_score:
                    current_level_data.best_score = self.score
            
            # Check level completion
            current_level_data = self.levels[self.current_level - 1]
            if self.score >= current_level_data.required_score:
                current_level_data.completed = True
                self.game_state = GameState.LEVEL_COMPLETE
    
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
    
    def draw_menu(self):
        self.background.draw(self.screen)
        
        # Title
        title = self.title_font.render("GEOMETRY CHEETAH", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 120))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("Improved Edition", True, YELLOW)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 180))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Instructions
        instructions = self.small_font.render("Press SPACE to select level", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH//2, 280))
        self.screen.blit(instructions, instructions_rect)
        
        instructions2 = self.small_font.render("Press SPACE to jump", True, WHITE)
        instructions2_rect = instructions2.get_rect(center=(SCREEN_WIDTH//2, 310))
        self.screen.blit(instructions2, instructions2_rect)
        
        # Level progress
        completed_levels = sum(1 for level in self.levels if level.completed)
        progress_text = self.small_font.render(f"Levels Completed: {completed_levels}/{len(self.levels)}", True, CYAN)
        progress_rect = progress_text.get_rect(center=(SCREEN_WIDTH//2, 380))
        self.screen.blit(progress_text, progress_rect)
    
    def draw_level_select(self):
        self.background.draw(self.screen)
        
        # Title
        title = self.font.render("SELECT LEVEL", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        # Draw level buttons
        for i, level in enumerate(self.levels):
            y_pos = 150 + i * 80
            color = level.color if i + 1 == self.selected_level else GRAY
            
            # Level button background
            button_rect = pygame.Rect(200, y_pos - 20, 800, 60)
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, WHITE, button_rect, 3)
            
            # Level info
            level_text = self.font.render(f"Level {level.level_num}: {level.name}", True, WHITE)
            self.screen.blit(level_text, (220, y_pos - 10))
            
            desc_text = self.small_font.render(level.description, True, WHITE)
            self.screen.blit(desc_text, (220, y_pos + 15))
            
            # Completion status
            if level.completed:
                status_text = self.small_font.render("✓ COMPLETED", True, GREEN)
                self.screen.blit(status_text, (900, y_pos + 5))
            else:
                status_text = self.small_font.render(f"Score: {level.required_score}", True, YELLOW)
                self.screen.blit(status_text, (900, y_pos + 5))
        
        # Instructions
        instructions = self.small_font.render("Use UP/DOWN arrows to select, SPACE to start", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH//2, 550))
        self.screen.blit(instructions, instructions_rect)
    
    def draw_game(self):
        self.background.draw(self.screen)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw cheetah
        self.cheetah.draw(self.screen)
        
        # Draw score and level info
        current_level_data = self.levels[self.current_level - 1]
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        level_text = self.small_font.render(f"Level {self.current_level}: {current_level_data.name}", True, current_level_data.color)
        self.screen.blit(level_text, (20, 60))
        
        required_text = self.small_font.render(f"Required: {current_level_data.required_score}", True, YELLOW)
        self.screen.blit(required_text, (20, 85))
    
    def draw_game_over(self):
        self.background.draw(self.screen)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw cheetah
        self.cheetah.draw(self.screen)
        
        # Game over overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(score_text, score_rect)
        
        # Level info
        current_level_data = self.levels[self.current_level - 1]
        level_text = self.small_font.render(f"Level {self.current_level}: {current_level_data.name}", True, current_level_data.color)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 280))
        self.screen.blit(level_text, level_rect)
        
        # Best score
        if self.score >= current_level_data.best_score:
            best_score_text = self.font.render("NEW BEST SCORE!", True, YELLOW)
            best_score_rect = best_score_text.get_rect(center=(SCREEN_WIDTH//2, 320))
            self.screen.blit(best_score_text, best_score_rect)
        
        # Restart instruction
        restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, 370))
        self.screen.blit(restart_text, restart_rect)
        
        # Level select instruction
        select_text = self.small_font.render("Press ESC for level select", True, WHITE)
        select_rect = select_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(select_text, select_rect)
    
    def draw_level_complete(self):
        self.background.draw(self.screen)
        
        # Level complete overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Success text
        success_text = self.title_font.render("LEVEL COMPLETE!", True, GREEN)
        success_rect = success_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(success_text, success_rect)
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 280))
        self.screen.blit(score_text, score_rect)
        
        # Level info
        current_level_data = self.levels[self.current_level - 1]
        level_text = self.small_font.render(f"Level {self.current_level}: {current_level_data.name}", True, current_level_data.color)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 320))
        self.screen.blit(level_text, level_rect)
        
        # Next level instruction
        if self.current_level < len(self.levels):
            next_text = self.small_font.render("Press SPACE for next level", True, WHITE)
            next_rect = next_text.get_rect(center=(SCREEN_WIDTH//2, 360))
            self.screen.blit(next_text, next_rect)
        else:
            final_text = self.font.render("ALL LEVELS COMPLETED!", True, YELLOW)
            final_rect = final_text.get_rect(center=(SCREEN_WIDTH//2, 360))
            self.screen.blit(final_text, final_rect)
        
        # Menu instruction
        menu_text = self.small_font.render("Press ESC for level select", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(menu_text, menu_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GameState.MENU:
                        self.game_state = GameState.LEVEL_SELECT
                    elif self.game_state == GameState.LEVEL_SELECT:
                        self.current_level = self.selected_level
                        self.reset_game()
                        self.game_state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks()
                    elif self.game_state == GameState.PLAYING:
                        self.cheetah.jump()
                    elif self.game_state == GameState.GAME_OVER:
                        self.reset_game()
                        self.game_state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks()
                    elif self.game_state == GameState.LEVEL_COMPLETE:
                        if self.current_level < len(self.levels):
                            self.current_level += 1
                            self.reset_game()
                            self.game_state = GameState.PLAYING
                            self.game_start_time = pygame.time.get_ticks()
                        else:
                            self.game_state = GameState.LEVEL_SELECT
                
                elif event.key == pygame.K_ESCAPE:
                    if self.game_state in [GameState.GAME_OVER, GameState.LEVEL_COMPLETE]:
                        self.game_state = GameState.LEVEL_SELECT
                
                elif event.key in [pygame.K_UP, pygame.K_DOWN] and self.game_state == GameState.LEVEL_SELECT:
                    if event.key == pygame.K_UP:
                        self.selected_level = max(1, self.selected_level - 1)
                    else:
                        self.selected_level = min(len(self.levels), self.selected_level + 1)
        
        return True
    
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