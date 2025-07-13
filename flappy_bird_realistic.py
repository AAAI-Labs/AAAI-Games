import pygame
import random
import sys
import math
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.6
FLAP_STRENGTH = -12
PIPE_SPEED = 4
PIPE_GAP = 220  # Increased gap for easier gameplay
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
pygame.display.set_caption("Flappy Bird - Realistic")
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.color = color
        self.life = 30
        self.max_life = 30
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1
        
    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        size = int(3 * (self.life / self.max_life))
        if size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class RealisticBird:
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
        # Add flap particles
        for _ in range(8):
            self.particles.append(Particle(self.x, self.y + BIRD_SIZE//2, (139, 69, 19)))
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
        
        # Update rotation
        if self.velocity < 0:
            self.rotation = -30
        else:
            self.rotation = min(90, self.rotation + 5)
            
        # Update wing animation
        self.wing_angle += 5 * self.wing_direction
        if self.wing_angle > 15 or self.wing_angle < -20:
            self.wing_direction *= -1
            
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
        
    def draw(self, screen):
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
            
        # Create a surface for the bird to rotate
        bird_surface = pygame.Surface((BIRD_SIZE + 20, BIRD_SIZE + 20), pygame.SRCALPHA)
        
        # Bird body (oval shape)
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
        
        # Bird wing (animated)
        wing_x = BIRD_SIZE//2 - 5
        wing_y = BIRD_SIZE//2 + 5
        wing_width = 20
        wing_height = 15
        
        # Wing base
        pygame.draw.ellipse(bird_surface, DARK_GRAY, (wing_x, wing_y, wing_width, wing_height))
        
        # Wing feathers (animated)
        feather_x = wing_x + wing_width//2
        feather_y = wing_y + wing_height//2
        feather_length = 15 + abs(self.wing_angle)
        
        # Draw multiple feathers
        for i in range(3):
            angle_offset = (i - 1) * 10 + self.wing_angle
            end_x = feather_x + math.cos(math.radians(angle_offset)) * feather_length
            end_y = feather_y + math.sin(math.radians(angle_offset)) * feather_length
            pygame.draw.line(bird_surface, GRAY, (feather_x, feather_y), (end_x, end_y), 2)
        
        # Bird tail
        tail_points = [(10, BIRD_SIZE//2), (0, BIRD_SIZE//2 - 8), (0, BIRD_SIZE//2 + 8)]
        pygame.draw.polygon(bird_surface, DARK_GRAY, tail_points)
        pygame.draw.polygon(bird_surface, BLACK, tail_points, 1)
        
        # Bird feet (when flying)
        if self.velocity > 0:
            foot_x = BIRD_SIZE//2
            foot_y = BIRD_SIZE + 5
            pygame.draw.line(bird_surface, ORANGE, (foot_x - 3, foot_y), (foot_x - 3, foot_y + 8), 2)
            pygame.draw.line(bird_surface, ORANGE, (foot_x + 3, foot_y), (foot_x + 3, foot_y + 8), 2)
        
        # Rotate the bird surface
        rotated_surface = pygame.transform.rotate(bird_surface, self.rotation)
        screen.blit(rotated_surface, (self.x - rotated_surface.get_width()//2 + BIRD_SIZE//2, 
                                     self.y - rotated_surface.get_height()//2 + BIRD_SIZE//2))
        
    def get_rect(self):
        return self.rect

class DynamicBackground:
    def __init__(self):
        self.current_theme = "city"
        self.themes = ["city", "forest", "mountains", "desert", "space"]
        self.theme_index = 0
        self.clouds = []
        self.buildings = []
        self.trees = []
        self.mountains = []
        self.stars = []
        self.score_threshold = 10  # Change theme every 10 points
        
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
            
    def update_theme(self, score):
        new_theme_index = min(score // self.score_threshold, len(self.themes) - 1)
        if new_theme_index != self.theme_index:
            self.theme_index = new_theme_index
            self.current_theme = self.themes[self.theme_index]
            
    def update(self):
        # Update clouds
        for cloud in self.clouds:
            cloud['x'] -= 1
            if cloud['x'] < -100:
                cloud['x'] = SCREEN_WIDTH + 100
                cloud['y'] = random.randint(50, 200)
                
        # Update stars twinkling
        for star in self.stars:
            star['twinkle'] = (star['twinkle'] + 1) % 200
                
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
            
    def draw_desert(self, screen):
        # Sky gradient (orange/yellow)
        for y in range(SCREEN_HEIGHT - 100):
            color_ratio = y / (SCREEN_HEIGHT - 100)
            r = int(135 + (255 - 135) * color_ratio)
            g = int(206 + (200 - 206) * color_ratio)
            b = int(235 + (100 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
            
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
            
    def draw_city_pipe(self, screen):
        # Building-like pipes with more realistic city style
        building_colors = [DARK_GRAY, GRAY, LIGHT_GRAY, (100, 100, 100)]
        color = random.choice(building_colors)
        
        # Top building
        pygame.draw.rect(screen, color, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)
        
        # Bottom building
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, color, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)
        
        # Building details - windows with different patterns
        window_colors = [YELLOW, LIGHT_BLUE, WHITE, (255, 255, 200)]
        
        # Top building windows (more realistic pattern)
        for row in range(3, (self.top_height - 20) // 25):
            for col in range(2):
                window_x = self.x + 10 + col * 25
                window_y = 15 + row * 25
                if window_y < self.top_height - 15:
                    # Random window colors for variety
                    window_color = random.choice(window_colors)
                    pygame.draw.rect(screen, window_color, (window_x, window_y, 15, 12))
                    pygame.draw.rect(screen, BLACK, (window_x, window_y, 15, 12), 1)
        
        # Bottom building windows
        for row in range(3, (self.bottom_height - 20) // 25):
            for col in range(2):
                window_x = self.x + 10 + col * 25
                window_y = bottom_y + 15 + row * 25
                if window_y < bottom_y + self.bottom_height - 15:
                    window_color = random.choice(window_colors)
                    pygame.draw.rect(screen, window_color, (window_x, window_y, 15, 12))
                    pygame.draw.rect(screen, BLACK, (window_x, window_y, 15, 12), 1)
        
        # Building tops (roofs)
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.top_height - 5, PIPE_WIDTH + 4, 5))
        pygame.draw.rect(screen, BLACK, (self.x - 2, bottom_y, PIPE_WIDTH + 4, 5))
        
        # Building entrances (bottom of buildings)
        entrance_width = 20
        entrance_height = 15
        pygame.draw.rect(screen, BLACK, (self.x + (PIPE_WIDTH - entrance_width) // 2, 
                                       self.top_height - entrance_height, 
                                       entrance_width, entrance_height))
        pygame.draw.rect(screen, BLACK, (self.x + (PIPE_WIDTH - entrance_width) // 2, 
                                       bottom_y + self.bottom_height, 
                                       entrance_width, entrance_height))
            
    def draw_forest_pipe(self, screen):
        # Tree-like pipes
        # Top pipe
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
        # Top pipe
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
        # Top pipe
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
        # Top pipe
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
        
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2, PIPE_WIDTH, self.bottom_height)
        return top_rect, bottom_rect

class Game:
    def __init__(self):
        self.bird = RealisticBird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.background = DynamicBackground()
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_started = False  # New: track if game has started
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 48)
        
        # Add initial pipes
        for i in range(3):
            self.pipes.append(Pipe(SCREEN_WIDTH + i * 300, self.background.current_theme))
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__init__()  # Reset game
                    elif not self.game_started:
                        self.game_started = True  # Start the game on first space press
                        self.bird.flap()
                    else:
                        self.bird.flap()
        return True
        
    def update(self):
        if not self.game_over and self.game_started:
            self.bird.update()
            self.background.update()
            self.background.update_theme(self.score)
            
            # Update pipes
            for pipe in self.pipes:
                pipe.update()
                
            # Remove off-screen pipes
            self.pipes = [pipe for pipe in self.pipes if pipe.x > -PIPE_WIDTH]
            
            # Add new pipes with current theme
            if len(self.pipes) < 3:
                self.pipes.append(Pipe(SCREEN_WIDTH + 300, self.background.current_theme))
                
            # Check collisions
            bird_rect = self.bird.get_rect()
            
            # Check if bird hits the ground or ceiling
            if self.bird.y <= 0 or self.bird.y >= SCREEN_HEIGHT - BIRD_SIZE:
                self.game_over = True
                
            # Check pipe collisions
            for pipe in self.pipes:
                top_rect, bottom_rect = pipe.get_rects()
                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                    self.game_over = True
                    
            # Update score
            for pipe in self.pipes:
                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                    
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
                    
    def draw(self):
        # Draw background
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
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(screen, self.background.current_theme)
            
        # Draw bird
        self.bird.draw(screen)
        
        # Draw score
        score_text = self.font.render(str(self.score), True, WHITE)
        score_text.set_alpha(200)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
        
        # Draw high score
        high_score_text = self.small_font.render(f"Best: {self.high_score}", True, WHITE)
        high_score_text.set_alpha(150)
        screen.blit(high_score_text, (10, 10))
        
        # Draw current theme
        theme_text = self.small_font.render(f"Theme: {self.background.current_theme.title()}", True, WHITE)
        theme_text.set_alpha(150)
        screen.blit(theme_text, (10, 40))
        
        # Draw start screen
        if not self.game_started and not self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Title
            title_text = self.font.render("FLAPPY BIRD", True, YELLOW)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))
            
            # Instructions
            instruction1 = self.medium_font.render("Press SPACE to start", True, WHITE)
            instruction2 = self.small_font.render("Flap to fly through the gaps!", True, WHITE)
            instruction3 = self.small_font.render("Watch the backgrounds change as you progress", True, WHITE)
            
            screen.blit(instruction1, (SCREEN_WIDTH // 2 - instruction1.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(instruction2, (SCREEN_WIDTH // 2 - instruction2.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(instruction3, (SCREEN_WIDTH // 2 - instruction3.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
            
            # Bird preview (static)
            self.bird.draw(screen)
            
        # Draw game over message
        elif self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.medium_font.render("Press SPACE to restart", True, WHITE)
            final_score_text = self.medium_font.render(f"Score: {self.score}", True, WHITE)
            
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
            
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