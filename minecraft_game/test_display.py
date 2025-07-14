#!/usr/bin/env python3
"""
Simple test to check if pygame display is working
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Display Test")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)

def main():
    print("Starting display test...")
    print("You should see a window with colored rectangles and text")

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear screen
        screen.fill(WHITE)

        # Draw some test shapes
        pygame.draw.rect(screen, RED, (100, 100, 100, 100))
        pygame.draw.rect(screen, GREEN, (250, 100, 100, 100))
        pygame.draw.rect(screen, BLUE, (400, 100, 100, 100))

        # Draw text
        text = font.render("Display Test - Press ESC to exit", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text, text_rect)

        # Draw instructions
        instructions = font.render("If you can see this, pygame is working!", True, BLACK)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(instructions, instructions_rect)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("Display test completed")

if __name__ == "__main__":
    main()