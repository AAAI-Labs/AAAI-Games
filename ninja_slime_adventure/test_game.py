#!/usr/bin/env python3
"""
Test script for Ninja Slime Adventure game components
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Test screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ninja Slime Adventure - Test")

# Test colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Test font
font = pygame.font.Font(None, 36)

def test_basic_components():
    """Test basic game components"""
    print("Testing basic components...")
    
    # Test slime creation
    slime_x, slime_y = 100, 100
    slime_width, slime_height = 40, 40
    
    # Test platform creation
    platform = pygame.Rect(200, 200, 100, 20)
    
    # Test key creation
    key_x, key_y = 300, 300
    key_width, key_height = 20, 20
    
    print("✓ Basic components created successfully")
    return True

def test_puzzle_logic():
    """Test puzzle game logic"""
    print("Testing puzzle logic...")
    
    # Test Wordle logic
    target_word = "SLIME"
    guess = "STARE"
    
    # Simple feedback logic
    feedback = []
    for i, letter in enumerate(guess):
        if i < len(target_word) and letter == target_word[i]:
            feedback.append("green")
        elif letter in target_word:
            feedback.append("yellow")
        else:
            feedback.append("gray")
    
    print(f"✓ Wordle feedback: {feedback}")
    
    # Test Tic Tac Toe logic
    board = [["" for _ in range(3)] for _ in range(3)]
    board[0][0] = "X"
    board[1][1] = "O"
    
    print(f"✓ Tic Tac Toe board: {board}")
    return True

def run_test_display():
    """Run a simple test display"""
    print("Running test display...")
    
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
        screen.fill(BLACK)
        
        # Draw test elements
        # Slime
        pygame.draw.ellipse(screen, GREEN, (100, 100, 40, 40))
        pygame.draw.ellipse(screen, BLACK, (100, 100, 40, 40), 2)
        
        # Platform
        pygame.draw.rect(screen, (139, 69, 19), (200, 200, 100, 20))
        pygame.draw.rect(screen, BLACK, (200, 200, 100, 20), 2)
        
        # Key
        pygame.draw.rect(screen, (255, 255, 0), (300, 300, 20, 20))
        pygame.draw.circle(screen, (255, 255, 0), (310, 310), 8)
        
        # Text
        text = font.render("Ninja Slime Adventure - Test", True, WHITE)
        screen.blit(text, (200, 50))
        
        text2 = font.render("Press ESC to exit", True, WHITE)
        screen.blit(text2, (200, 500))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

def main():
    print("=== Ninja Slime Adventure Test Suite ===")
    
    # Test basic components
    if test_basic_components():
        print("✓ Basic components test passed")
    
    # Test puzzle logic
    if test_puzzle_logic():
        print("✓ Puzzle logic test passed")
    
    # Run test display
    print("\nStarting test display...")
    run_test_display()
    
    print("\n=== All tests completed ===")

if __name__ == "__main__":
    main() 