import pygame
import random
import sys
import os
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_GAP = 200
PIPE_WIDTH = 80
BIRD_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.rect = pygame.Rect(x, y, BIRD_SIZE, BIRD_SIZE)
        
    def flap(self):
        self.velocity = FLAP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
        
    def draw(self, screen):
        # Draw bird body
        pygame.draw.circle(screen, YELLOW, (self.x + BIRD_SIZE//2, self.y + BIRD_SIZE//2), BIRD_SIZE//2)
        # Draw bird eye
        pygame.draw.circle(screen, BLACK, (self.x + BIRD_SIZE//2 + 5, self.y + BIRD_SIZE//2 - 5), 3)
        # Draw bird wing
        pygame.draw.ellipse(screen, ORANGE, (self.x - 5, self.y + 5, 15, 10))
        
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
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top_height), 3)
        
        # Bottom pipe
        bottom_y = self.gap_y + PIPE_GAP // 2
        pygame.draw.rect(screen, GREEN, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height))
        pygame.draw.rect(screen, BLACK, (self.x, bottom_y, PIPE_WIDTH, self.bottom_height), 3)
        
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        bottom_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2, PIPE_WIDTH, self.bottom_height)
        return top_rect, bottom_rect

class Game:
    def __init__(self):
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
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
                    
    def draw(self):
        # Draw background
        screen.fill(BLUE)
        
        # Draw ground
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(screen)
            
        # Draw bird
        self.bird.draw(screen)
        
        # Draw score
        score_text = self.font.render(str(self.score), True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
            
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
    # Define ORANGE color that was missing
    ORANGE = (255, 165, 0)
    main() 