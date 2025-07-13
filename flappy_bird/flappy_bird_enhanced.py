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
PIPE_GAP = 180
PIPE_WIDTH = 80
BIRD_SIZE = 25

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

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Enhanced")
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
        color = (*self.color, alpha)
        size = int(3 * (self.life / self.max_life))
        if size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.rect = pygame.Rect(x, y, BIRD_SIZE, BIRD_SIZE)
        self.rotation = 0
        self.particles = []
        
    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.rotation = -30
        # Add flap particles
        for _ in range(5):
            self.particles.append(Particle(self.x, self.y + BIRD_SIZE//2, YELLOW))
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
        
        # Update rotation
        if self.velocity < 0:
            self.rotation = -30
        else:
            self.rotation = min(90, self.rotation + 5)
            
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
        
    def draw(self, screen):
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
            
        # Create a surface for the bird to rotate
        bird_surface = pygame.Surface((BIRD_SIZE, BIRD_SIZE), pygame.SRCALPHA)
        
        # Draw bird body
        pygame.draw.circle(bird_surface, YELLOW, (BIRD_SIZE//2, BIRD_SIZE//2), BIRD_SIZE//2)
        pygame.draw.circle(bird_surface, BLACK, (BIRD_SIZE//2, BIRD_SIZE//2), BIRD_SIZE//2, 2)
        
        # Draw bird eye
        pygame.draw.circle(bird_surface, BLACK, (BIRD_SIZE//2 + 5, BIRD_SIZE//2 - 5), 3)
        pygame.draw.circle(bird_surface, WHITE, (BIRD_SIZE//2 + 6, BIRD_SIZE//2 - 6), 1)
        
        # Draw bird wing
        pygame.draw.ellipse(bird_surface, ORANGE, (BIRD_SIZE//2 - 15, BIRD_SIZE//2 + 5, 15, 10))
        
        # Draw bird beak
        pygame.draw.polygon(bird_surface, ORANGE, [(BIRD_SIZE//2 + 10, BIRD_SIZE//2), 
                                                  (BIRD_SIZE//2 + 20, BIRD_SIZE//2 - 3),
                                                  (BIRD_SIZE//2 + 20, BIRD_SIZE//2 + 3)])
        
        # Rotate the bird surface
        rotated_surface = pygame.transform.rotate(bird_surface, self.rotation)
        screen.blit(rotated_surface, (self.x - rotated_surface.get_width()//2 + BIRD_SIZE//2, 
                                     self.y - rotated_surface.get_height()//2 + BIRD_SIZE//2))
        
    def get_rect(self):
        return self.rect

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(150, SCREEN_HEIGHT - 150)
        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_height = SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, DARK_GREEN, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)
        
        # Top pipe cap
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.top_height - 20, PIPE_WIDTH + 10, 20))
        pygame.draw.rect(screen, BLACK, (self.x - 5, self.top_height - 20, PIPE_WIDTH + 10, 20), 3)
        
        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, DARK_GREEN, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)
        
        # Bottom pipe cap
        pygame.draw.rect(screen, GREEN, (self.x - 5, bottom_y, PIPE_WIDTH + 10, 20))
        pygame.draw.rect(screen, BLACK, (self.x - 5, bottom_y, PIPE_WIDTH + 10, 20), 3)
        
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2, PIPE_WIDTH, self.bottom_height)
        return top_rect, bottom_rect

class Background:
    def __init__(self):
        self.clouds = []
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(50, 200),
                'size': random.randint(30, 80)
            })
            
    def update(self):
        for cloud in self.clouds:
            cloud['x'] -= 1
            if cloud['x'] < -100:
                cloud['x'] = SCREEN_WIDTH + 100
                cloud['y'] = random.randint(50, 200)
                
    def draw(self, screen):
        # Sky gradient
        for y in range(SCREEN_HEIGHT - 50):
            color_ratio = y / (SCREEN_HEIGHT - 50)
            r = int(135 + (200 - 135) * color_ratio)
            g = int(206 + (230 - 206) * color_ratio)
            b = int(235 + (255 - 235) * color_ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
            
        # Draw clouds
        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (cloud['x'], cloud['y']), cloud['size'])
            pygame.draw.circle(screen, WHITE, (cloud['x'] + cloud['size']//2, cloud['y']), cloud['size']//2)
            pygame.draw.circle(screen, WHITE, (cloud['x'] - cloud['size']//2, cloud['y']), cloud['size']//2)

class Game:
    def __init__(self):
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.background = Background()
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 48)
        
        # Add initial pipes
        for i in range(3):
            self.pipes.append(Pipe(SCREEN_WIDTH + i * 300))
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__init__()  # Reset game
                    else:
                        self.bird.flap()
        return True
        
    def update(self):
        if not self.game_over:
            self.bird.update()
            self.background.update()
            
            # Update pipes
            for pipe in self.pipes:
                pipe.update()
                
            # Remove off-screen pipes
            self.pipes = [pipe for pipe in self.pipes if pipe.x > -PIPE_WIDTH]
            
            # Add new pipes
            if len(self.pipes) < 3:
                self.pipes.append(Pipe(SCREEN_WIDTH + 300))
                
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
        
        # Draw ground with grass texture
        pygame.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        for i in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(screen, DARK_GREEN, (i, SCREEN_HEIGHT - 50), (i + 10, SCREEN_HEIGHT - 50), 3)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(screen)
            
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
        
        # Draw game over message
        if self.game_over:
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