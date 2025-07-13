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

# Game constants
GRAVITY = 0.8
JUMP_FORCE = -18  # Increased jump force for higher jumps
GROUND_Y = SCREEN_HEIGHT - 100
OBSTACLE_SPEED = 4  # Reduced speed for easier timing
OBSTACLE_SPAWN_RATE = 0.015  # Reduced spawn rate for more manageable difficulty
MIN_OBSTACLE_SPACING = 300  # Minimum distance between obstacles

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class Cheetah:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.is_jumping = False
        self.is_on_ground = True
        self.animation_frame = 0
        self.animation_speed = 0.3
        self.rotation = 0
        self.trail_particles = []
        
    def update(self):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # Ground collision
        if self.y >= GROUND_Y - 40:
            self.y = GROUND_Y - 40
            self.velocity_y = 0
            self.is_on_ground = True
            self.is_jumping = False
        else:
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
            
        # Update trail particles
        for particle in self.trail_particles[:]:
            particle['life'] -= 1
            particle['x'] -= 2
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
                
        # Add trail particles when moving
        if not self.is_on_ground and random.random() < 0.3:
            self.trail_particles.append({
                'x': self.x - 20,
                'y': self.y + 20,
                'life': 10,
                'color': ORANGE
            })
    
    def jump(self):
        if self.is_on_ground:
            self.velocity_y = JUMP_FORCE
            self.is_jumping = True
            self.is_on_ground = False
            
    def draw(self, screen):
        # Draw trail particles
        for particle in self.trail_particles:
            alpha = int((particle['life'] / 10) * 255)
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), 3)
        
        # Draw cheetah body
        cheetah_surface = pygame.Surface((60, 40), pygame.SRCALPHA)
        
        # Body (orange with spots)
        pygame.draw.ellipse(cheetah_surface, ORANGE, (10, 15, 40, 20))
        
        # Spots
        spots = [(15, 18), (25, 16), (35, 20), (20, 25), (30, 22)]
        for spot in spots:
            pygame.draw.circle(cheetah_surface, BLACK, spot, 2)
        
        # Head
        pygame.draw.circle(cheetah_surface, ORANGE, (45, 20), 12)
        
        # Ears
        pygame.draw.circle(cheetah_surface, ORANGE, (50, 12), 4)
        pygame.draw.circle(cheetah_surface, ORANGE, (52, 15), 3)
        
        # Eyes
        pygame.draw.circle(cheetah_surface, BLACK, (48, 18), 2)
        
        # Nose
        pygame.draw.circle(cheetah_surface, BLACK, (55, 20), 1)
        
        # Legs
        pygame.draw.rect(cheetah_surface, ORANGE, (15, 30, 4, 10))
        pygame.draw.rect(cheetah_surface, ORANGE, (25, 30, 4, 10))
        pygame.draw.rect(cheetah_surface, ORANGE, (35, 30, 4, 10))
        pygame.draw.rect(cheetah_surface, ORANGE, (45, 30, 4, 10))
        
        # Tail
        tail_points = [(10, 20), (5, 15), (0, 20), (5, 25)]
        pygame.draw.polygon(cheetah_surface, ORANGE, tail_points)
        
        # Rotate the cheetah
        rotated_surface = pygame.transform.rotate(cheetah_surface, self.rotation)
        
        # Draw to screen
        screen.blit(rotated_surface, (self.x - rotated_surface.get_width()//2, 
                                     self.y - rotated_surface.get_height()//2))

class Obstacle:
    def __init__(self, x, obstacle_type="spike"):
        self.x = x
        self.obstacle_type = obstacle_type
        self.width = 30
        # Reduced heights for easier jumping
        if obstacle_type == "spike":
            self.height = 45  # Reduced from 60
        elif obstacle_type == "block":
            self.height = 50  # Reduced from 60
        elif obstacle_type == "flying_spike":
            self.height = 40  # Reduced from 60
        else:
            self.height = 50
        self.color = RED
        
    def update(self):
        self.x -= OBSTACLE_SPEED
        
    def draw(self, screen):
        if self.obstacle_type == "spike":
            # Draw spike
            points = [(self.x, GROUND_Y), (self.x + 15, GROUND_Y - self.height), (self.x + 30, GROUND_Y)]
            pygame.draw.polygon(screen, self.color, points)
        elif self.obstacle_type == "block":
            # Draw block
            pygame.draw.rect(screen, self.color, (self.x, GROUND_Y - self.height, self.width, self.height))
        elif self.obstacle_type == "flying_spike":
            # Draw flying spike (moved higher for easier passage)
            points = [(self.x, GROUND_Y - 250), (self.x + 15, GROUND_Y - 250 - self.height), (self.x + 30, GROUND_Y - 250)]
            pygame.draw.polygon(screen, self.color, points)
            
    def get_rect(self):
        if self.obstacle_type == "spike":
            return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)
        elif self.obstacle_type == "block":
            return pygame.Rect(self.x, GROUND_Y - self.height, self.width, self.height)
        elif self.obstacle_type == "flying_spike":
            return pygame.Rect(self.x, GROUND_Y - 250 - self.height, self.width, self.height)

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
        self.parallax_offset += OBSTACLE_SPEED * 0.5
        
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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Geometry Cheetah")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        
    def reset_game(self):
        self.cheetah = Cheetah(100, GROUND_Y - 40)
        self.obstacles = []
        self.background = Background()
        self.score = 0
        self.game_state = GameState.MENU
        self.high_score = 0
        self.game_start_time = 0  # Track when game starts for initial delay
        
    def spawn_obstacle(self):
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
        
        if can_spawn and random.random() < OBSTACLE_SPAWN_RATE:
            obstacle_type = random.choice(["spike", "block", "flying_spike"])
            self.obstacles.append(Obstacle(SCREEN_WIDTH + 50, obstacle_type))
    
    def check_collision(self):
        cheetah_rect = pygame.Rect(self.cheetah.x - 20, self.cheetah.y - 20, 40, 40)
        
        for obstacle in self.obstacles:
            if cheetah_rect.colliderect(obstacle.get_rect()):
                return True
        return False
    
    def update(self):
        if self.game_state == GameState.PLAYING:
            self.cheetah.update()
            self.background.update()
            
            # Spawn obstacles
            self.spawn_obstacle()
            
            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.x + obstacle.width < 0:
                    self.obstacles.remove(obstacle)
                    self.score += 1
            
            # Check collision
            if self.check_collision():
                self.game_state = GameState.GAME_OVER
                if self.score > self.high_score:
                    self.high_score = self.score
    
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.PLAYING:
            self.draw_game()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        self.background.draw(self.screen)
        
        # Title
        title = self.font.render("GEOMETRY CHEETAH", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instructions = self.small_font.render("Press SPACE to start", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH//2, 250))
        self.screen.blit(instructions, instructions_rect)
        
        instructions2 = self.small_font.render("Press SPACE to jump", True, WHITE)
        instructions2_rect = instructions2.get_rect(center=(SCREEN_WIDTH//2, 280))
        self.screen.blit(instructions2, instructions2_rect)
        
        # High score
        if self.high_score > 0:
            high_score_text = self.small_font.render(f"High Score: {self.high_score}", True, YELLOW)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, 350))
            self.screen.blit(high_score_text, high_score_rect)
    
    def draw_game(self):
        self.background.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw cheetah
        self.cheetah.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
    
    def draw_game_over(self):
        self.background.draw(self.screen)
        
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
        
        # High score
        if self.score >= self.high_score:
            high_score_text = self.font.render("NEW HIGH SCORE!", True, YELLOW)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH//2, 300))
            self.screen.blit(high_score_text, high_score_rect)
        
        # Restart instruction
        restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, 350))
        self.screen.blit(restart_text, restart_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GameState.MENU:
                        self.game_state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks()  # Record start time
                    elif self.game_state == GameState.PLAYING:
                        self.cheetah.jump()
                    elif self.game_state == GameState.GAME_OVER:
                        self.reset_game()
                        self.game_state = GameState.PLAYING
                        self.game_start_time = pygame.time.get_ticks()  # Record start time
        
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