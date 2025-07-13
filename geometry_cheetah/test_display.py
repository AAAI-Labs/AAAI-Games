import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Display Test - Press any key to close")

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

print("Pygame initialized successfully!")
print("Window created!")
print("You should see a red window. Press any key to close.")

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            running = False
    
    # Fill screen with red
    screen.fill(RED)
    
    # Draw some text
    font = pygame.font.Font(None, 36)
    text = font.render("Display Test - Press any key to close", True, WHITE)
    text_rect = text.get_rect(center=(400, 300))
    screen.blit(text, text_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("Test completed!") 