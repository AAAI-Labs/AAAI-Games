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
WORLD_WIDTH = 100
WORLD_HEIGHT = 50
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
SAND_YELLOW = (238, 203, 173)
COAL_BLACK = (47, 47, 47)
IRON_GRAY = (169, 169, 169)
GOLD_YELLOW = (255, 215, 0)
DIAMOND_BLUE = (185, 242, 255)

class BlockType(Enum):
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    WOOD = 4
    LEAVES = 5
    WATER = 6
    SAND = 7
    COAL_ORE = 8
    IRON_ORE = 9
    GOLD_ORE = 10
    DIAMOND_ORE = 11


class Block:
    def __init__(self, block_type: BlockType, x: int, y: int):
        self.type = block_type
        self.x = x
        self.y = y
        self.health = self.get_max_health()
        self.breakable = block_type != BlockType.AIR

    def get_max_health(self) -> int:
        health_map = {
            BlockType.GRASS: 1,
            BlockType.DIRT: 1,
            BlockType.STONE: 3,
            BlockType.WOOD: 2,
            BlockType.LEAVES: 1,
            BlockType.WATER: 999,  # Unbreakable
            BlockType.SAND: 1,
            BlockType.COAL_ORE: 2,
            BlockType.IRON_ORE: 3,
            BlockType.GOLD_ORE: 3,
            BlockType.DIAMOND_ORE: 4
        }
        return health_map.get(self.type, 1)

    def get_color(self) -> Tuple[int, int, int]:
        color_map = {
            BlockType.GRASS: GRASS_GREEN,
            BlockType.DIRT: DIRT_BROWN,
            BlockType.STONE: STONE_GRAY,
            BlockType.WOOD: WOOD_BROWN,
            BlockType.LEAVES: LEAF_GREEN,
            BlockType.WATER: WATER_BLUE,
            BlockType.SAND: SAND_YELLOW,
            BlockType.COAL_ORE: COAL_BLACK,
            BlockType.IRON_ORE: IRON_GRAY,
            BlockType.GOLD_ORE: GOLD_YELLOW,
            BlockType.DIAMOND_ORE: DIAMOND_BLUE
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
        self.inventory = {block_type: 0 for block_type in BlockType if block_type != BlockType.AIR}
        self.selected_block = BlockType.DIRT
        self.health = 100
        self.max_health = 100
        self.hunger = 100
        self.max_hunger = 100

    def update(self, world, keys):
        # Horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
        else:
            self.velocity_x *= 0.8  # Friction

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

        # Decrease hunger over time
        if random.random() < 0.001:  # Very slow hunger decrease
            self.hunger = max(0, self.hunger - 1)

    def check_collision(self, world, x, y):
        # Get the tiles the player would occupy
        left_tile = int(x // TILE_SIZE)
        right_tile = int((x + self.width - 1) // TILE_SIZE)
        top_tile = int(y // TILE_SIZE)
        bottom_tile = int((y + self.height - 1) // TILE_SIZE)

        # Check if any of these tiles are solid
        for tile_x in range(left_tile, right_tile + 1):
            for tile_y in range(top_tile, bottom_tile + 1):
                if (0 <= tile_x < WORLD_WIDTH and 0 <= tile_y < WORLD_HEIGHT and
                    world[tile_x][tile_y].type != BlockType.AIR and
                    world[tile_x][tile_y].type != BlockType.WATER):
                    return True
        return False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class World:
    def __init__(self):
        self.blocks = [[Block(BlockType.AIR, x, y) for y in range(WORLD_HEIGHT)] for x in range(WORLD_WIDTH)]
        self.generate_terrain()

    def generate_terrain(self):
        # Generate height map using noise
        scale = 50.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        height_map = []
        for x in range(WORLD_WIDTH):
            height = noise.pnoise1(
                x / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity
            )
            height = int((height + 1) * 0.5 * (WORLD_HEIGHT * 0.6)) + int(WORLD_HEIGHT * 0.2)
            height_map.append(height)

        # Generate terrain layers
        for x in range(WORLD_WIDTH):
            surface_height = height_map[x]

            for y in range(WORLD_HEIGHT):
                if y > surface_height:
                    # Underground
                    if y == surface_height + 1:
                        self.blocks[x][y] = Block(BlockType.GRASS, x, y)
                    elif y < surface_height + 4:
                        self.blocks[x][y] = Block(BlockType.DIRT, x, y)
                    else:
                        # Generate ores
                        ore_chance = random.random()
                        if ore_chance < 0.05:  # 5% chance for diamond
                            self.blocks[x][y] = Block(BlockType.DIAMOND_ORE, x, y)
                        elif ore_chance < 0.15:  # 10% chance for gold
                            self.blocks[x][y] = Block(BlockType.GOLD_ORE, x, y)
                        elif ore_chance < 0.35:  # 20% chance for iron
                            self.blocks[x][y] = Block(BlockType.IRON_ORE, x, y)
                        elif ore_chance < 0.65:  # 30% chance for coal
                            self.blocks[x][y] = Block(BlockType.COAL_ORE, x, y)
                        else:
                            self.blocks[x][y] = Block(BlockType.STONE, x, y)
                elif y == WORLD_HEIGHT - 1:
                    # Water at bottom
                    self.blocks[x][y] = Block(BlockType.WATER, x, y)

        # Generate trees
        for x in range(5, WORLD_WIDTH - 5):
            if random.random() < 0.1:  # 10% chance for tree
                tree_height = random.randint(3, 6)
                tree_x = x
                tree_y = surface_height

                # Check if there's grass here
                if (tree_y < WORLD_HEIGHT and
                    self.blocks[tree_x][tree_y].type == BlockType.GRASS):

                    # Generate trunk
                    for i in range(tree_height):
                        if tree_y - i >= 0:
                            self.blocks[tree_x][tree_y - i] = Block(
                                BlockType.WOOD, tree_x, tree_y - i
                            )

                    # Generate leaves
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            leaf_x = tree_x + dx
                            leaf_y = tree_y - tree_height + dy
                            if (0 <= leaf_x < WORLD_WIDTH and
                                0 <= leaf_y < WORLD_HEIGHT and
                                self.blocks[leaf_x][leaf_y].type == BlockType.AIR):
                                self.blocks[leaf_x][leaf_y] = Block(
                                    BlockType.LEAVES, leaf_x, leaf_y
                                )


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minecraft 2D")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        self.world = World()
        self.player = Player(100, 100)
        self.camera_x = 0

        self.running = True
        self.paused = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_1:
                    self.player.selected_block = BlockType.DIRT
                elif event.key == pygame.K_2:
                    self.player.selected_block = BlockType.STONE
                elif event.key == pygame.K_3:
                    self.player.selected_block = BlockType.WOOD
                elif event.key == pygame.K_4:
                    self.player.selected_block = BlockType.LEAVES
                elif event.key == pygame.K_5:
                    self.player.selected_block = BlockType.SAND
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click - break block
                    self.break_block()
                elif event.button == 3:  # Right click - place block
                    self.place_block()

    def break_block(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x = int((mouse_x + self.camera_x) // TILE_SIZE)
        world_y = int(mouse_y // TILE_SIZE)

        if (0 <= world_x < WORLD_WIDTH and 0 <= world_y < WORLD_HEIGHT):
            block = self.world.blocks[world_x][world_y]
            if block.breakable:
                block.health -= 1
                if block.health <= 0:
                    # Add to inventory
                    self.player.inventory[block.type] += 1
                    # Replace with air
                    self.world.blocks[world_x][world_y] = Block(BlockType.AIR, world_x, world_y)

    def place_block(self):
        if self.player.inventory[self.player.selected_block] > 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_x = int((mouse_x + self.camera_x) // TILE_SIZE)
            world_y = int(mouse_y // TILE_SIZE)

            if (0 <= world_x < WORLD_WIDTH and 0 <= world_y < WORLD_HEIGHT):
                if self.world.blocks[world_x][world_y].type == BlockType.AIR:
                    self.world.blocks[world_x][world_y] = Block(self.player.selected_block, world_x, world_y)
                    self.player.inventory[self.player.selected_block] -= 1

    def update(self):
        if not self.paused:
            keys = pygame.key.get_pressed()
            self.player.update(self.world.blocks, keys)

            # Update camera to follow player
            target_camera_x = self.player.x - SCREEN_WIDTH // 2
            self.camera_x = max(0, min(target_camera_x, WORLD_WIDTH * TILE_SIZE - SCREEN_WIDTH))

    def draw(self):
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
                        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Border

        # Draw player
        player_rect = pygame.Rect(self.player.x - self.camera_x, self.player.y,
                                self.player.width, self.player.height)
        pygame.draw.rect(self.screen, (255, 0, 0), player_rect)

        # Draw UI
        self.draw_ui()

        pygame.display.flip()

    def draw_ui(self):
        # Health bar
        health_width = 200
        health_height = 20
        health_x = 10
        health_y = 10

        pygame.draw.rect(self.screen, (255, 0, 0), (health_x, health_y, health_width, health_height))
        current_health_width = int((self.player.health / self.player.max_health) * health_width)
        pygame.draw.rect(self.screen, (0, 255, 0), (health_x, health_y, current_health_width, health_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (health_x, health_y, health_width, health_height), 2)

        health_text = self.font.render(
            f"Health: {self.player.health}/{self.player.max_health}", True, (0, 0, 0)
        )
        self.screen.blit(health_text, (health_x + 5, health_y + 2))

        # Hunger bar
        hunger_y = health_y + health_height + 10
        pygame.draw.rect(self.screen, (139, 69, 19), (health_x, hunger_y, health_width, health_height))
        current_hunger_width = int((self.player.hunger / self.player.max_hunger) * health_width)
        pygame.draw.rect(self.screen, (255, 255, 0), (health_x, hunger_y, current_hunger_width, health_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (health_x, hunger_y, health_width, health_height), 2)

        hunger_text = self.font.render(
            f"Hunger: {self.player.hunger}/{self.player.max_hunger}", True, (0, 0, 0)
        )
        self.screen.blit(hunger_text, (health_x + 5, hunger_y + 2))

        # Inventory
        inventory_y = hunger_y + health_height + 20
        inventory_text = self.font.render("Inventory:", True, (0, 0, 0))
        self.screen.blit(inventory_text, (health_x, inventory_y))

        y_offset = inventory_y + 25
        for i, (block_type, count) in enumerate(self.player.inventory.items()):
            if count > 0:
                color = Block(block_type, 0, 0).get_color()
                pygame.draw.rect(self.screen, color, (health_x, y_offset + i * 20, 15, 15))
                pygame.draw.rect(self.screen, (0, 0, 0), (health_x, y_offset + i * 20, 15, 15), 1)

                text = self.small_font.render(f"{block_type.name}: {count}", True, (0, 0, 0))
                self.screen.blit(text, (health_x + 20, y_offset + i * 20))

        # Selected block
        selected_y = SCREEN_HEIGHT - 50
        selected_text = self.font.render(
            f"Selected: {self.player.selected_block.name}", True, (0, 0, 0)
        )
        self.screen.blit(selected_text, (10, selected_y))

        # Controls
        controls_text = self.small_font.render(
            "Controls: WASD/Arrows=Move, Space=Jump, 1-5=Select Block, LMB=Break, RMB=Place",
            True, (0, 0, 0)
        )
        self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 25))

        if self.paused:
            pause_text = self.font.render("PAUSED - Press ESC to resume", True, (255, 0, 0))
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()