#!/usr/bin/env python3
"""
Simplified Minecraft 2D Game with better visibility
"""

import pygame
import random
import noise
from enum import Enum
from typing import Tuple

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SIZE = 32
WORLD_WIDTH = 50  # Smaller world for testing
WORLD_HEIGHT = 30
PLAYER_SPEED = 5
GRAVITY = 0.8
JUMP_FORCE = -15

# Colors
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
DIRT_BROWN = (139, 69, 19)
STONE_GRAY = (105, 105, 105)
WOOD_BROWN = (160, 82, 45)
LEAF_GREEN = (0, 128, 0)
WATER_BLUE = (0, 105, 148)
PLAYER_RED = (255, 0, 0)

class BlockType(Enum):
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    WOOD = 4
    LEAVES = 5

class Block:
    def __init__(self, block_type: BlockType, x: int, y: int):
        self.type = block_type
        self.x = x
        self.y = y

    def get_color(self) -> Tuple[int, int, int]:
        color_map = {
            BlockType.GRASS: GRASS_GREEN,
            BlockType.DIRT: DIRT_BROWN,
            BlockType.STONE: STONE_GRAY,
            BlockType.WOOD: WOOD_BROWN,
            BlockType.LEAVES: LEAF_GREEN,
        }
        return color_map.get(self.type, (0, 0, 0))

class Player:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE * 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False

    def update(self, world, keys):
        # Horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
        else:
            self.velocity_x *= 0.8

        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False

        # Apply gravity
        self.velocity_y += GRAVITY

        # Update position
        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y

        # Collision detection
        self.on_ground = False

        # Check horizontal collision
        if not self.check_collision(world, new_x, self.y):
            self.x = new_x
        else:
            self.velocity_x = 0

        # Check vertical collision
        if not self.check_collision(world, self.x, new_y):
            self.y = new_y
        else:
            if self.velocity_y > 0:
                self.on_ground = True
            self.velocity_y = 0

        # Keep player in world bounds
        self.x = max(0, min(self.x, WORLD_WIDTH * TILE_SIZE - self.width))
        self.y = max(0, min(self.y, WORLD_HEIGHT * TILE_SIZE - self.height))

    def check_collision(self, world, x, y):
        left_tile = int(x // TILE_SIZE)
        right_tile = int((x + self.width - 1) // TILE_SIZE)
        top_tile = int(y // TILE_SIZE)
        bottom_tile = int((y + self.height - 1) // TILE_SIZE)

        for tile_x in range(left_tile, right_tile + 1):
            for tile_y in range(top_tile, bottom_tile + 1):
                if (0 <= tile_x < WORLD_WIDTH and 0 <= tile_y < WORLD_HEIGHT and
                    world[tile_x][tile_y].type != BlockType.AIR):
                    return True
        return False

class World:
    def __init__(self):
        self.blocks = [[Block(BlockType.AIR, x, y) for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]
        self.generate_terrain()

    def generate_terrain(self):
        # Simple terrain generation
        for x in range(WORLD_WIDTH):
            # Create a simple flat surface
            surface_height = WORLD_HEIGHT // 2

            for y in range(WORLD_HEIGHT):
                if y > surface_height:
                    if y == surface_height + 1:
                        self.blocks[x][y] = Block(BlockType.GRASS, x, y)
                    elif y < surface_height + 3:
                        self.blocks[x][y] = Block(BlockType.DIRT, x, y)
                    else:
                        self.blocks[x][y] = Block(BlockType.STONE, x, y)

class Game:
    def __init__(self):
        print("Initializing game...")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minecraft 2D - Simple Version")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        print("Creating world...")
        self.world = World()
        self.player = Player(100, 100)
        self.camera_x = 0

        self.running = True
        print("Game initialized successfully!")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(self.world.blocks, keys)

        # Update camera to follow player
        target_camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_x = max(0, min(target_camera_x, WORLD_WIDTH * TILE_SIZE - SCREEN_WIDTH))

    def draw(self):
        # Clear screen
        self.screen.fill(SKY_BLUE)

        # Draw world
        start_x = max(0, int(self.camera_x // TILE_SIZE))
        end_x = min(WORLD_WIDTH, start_x + SCREEN_WIDTH // TILE_SIZE + 2)

        for x in range(start_x, end_x):
            for y in range(WORLD_HEIGHT):
                block = self.world.blocks[x][y]
                if block.type != BlockType.AIR:
                    screen_x = x * TILE_SIZE - self.camera_x
                    screen_y = y * TILE_SIZE

                    if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
                        color = block.get_color()
                        rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        # Draw player
        player_rect = pygame.Rect(self.player.x - self.camera_x, self.player.y,
                                self.player.width, self.player.height)
        pygame.draw.rect(self.screen, PLAYER_RED, player_rect)

        # Draw UI
        self.draw_ui()

        # Update display
        pygame.display.flip()

    def draw_ui(self):
        # Draw instructions
        instructions = [
            "Minecraft 2D - Simple Version",
            "WASD/Arrows: Move",
            "Space: Jump",
            "ESC: Exit"
        ]

        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, (0, 0, 0))
            self.screen.blit(text, (10, 10 + i * 25))

        # Draw player position
        pos_text = self.font.render(f"Player: ({int(self.player.x)}, {int(self.player.y)})", True, (0, 0, 0))
        self.screen.blit(pos_text, (10, SCREEN_HEIGHT - 30))

    def run(self):
        print("Starting game loop...")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        print("Game ended")
        pygame.quit()

if __name__ == "__main__":
    print("Starting Minecraft 2D Simple...")
    game = Game()
    game.run()