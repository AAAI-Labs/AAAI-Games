#!/usr/bin/env python3
"""
Minecraft 2D with forced window visibility
"""

import pygame
import os

# Force window to be visible and centered
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minecraft 2D - VISIBLE WINDOW")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
DIRT_BROWN = (139, 69, 19)
STONE_GRAY = (105, 105, 105)

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def main():
    print("Starting Minecraft 2D Visible...")
    print("Window should be centered and visible")
    print("Press ESC to exit")

    running = True
    clock = pygame.time.Clock()

    # Force window to front
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear screen
        screen.fill(SKY_BLUE)

        # Draw a simple Minecraft-style scene
        # Ground
        pygame.draw.rect(screen, GRASS_GREEN, (0, 400, SCREEN_WIDTH, 200))

        # Some blocks
        pygame.draw.rect(screen, DIRT_BROWN, (100, 350, 50, 50))  # Dirt
        pygame.draw.rect(screen, STONE_GRAY, (200, 350, 50, 50))  # Stone
        pygame.draw.rect(screen, (160, 82, 45), (300, 350, 50, 50))  # Wood

        # Player (red square)
        pygame.draw.rect(screen, RED, (350, 300, 30, 60))

        # Text
        text = font.render("Minecraft 2D - Can you see this?", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text, text_rect)

        instructions = font.render("Press ESC to exit", True, BLACK)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(instructions, instructions_rect)

        # More visible instructions
        help_text = small_font.render("If you can see this window, pygame is working!", True, BLACK)
        help_rect = help_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(help_text, help_rect)

        # Draw a bright border to make it obvious
        pygame.draw.rect(screen, RED, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("Game ended")

if __name__ == "__main__":
    main()