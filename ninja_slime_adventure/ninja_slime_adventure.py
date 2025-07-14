import pygame
import random
import sys
import time
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 100, 0)
BROWN = (139, 69, 19)

# Game states
MENU = "menu"
PLAYING = "playing"
WORDLE_PUZZLE = "wordle"
TIC_TAC_TOE_PUZZLE = "tictactoe"
GAME_OVER = "game_over"
VICTORY = "victory"

class NinjaSlime:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        self.jump_speed = -15
        self.vel_y = 0
        self.on_ground = False
        self.health = 100
        self.max_health = 100
        self.keys_collected = 0
        self.master_rescued = False
        
    def update(self, platforms: List[pygame.Rect], gravity: float = 0.8):
        # Horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            
        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_speed
            self.on_ground = False
            
        # Apply gravity
        self.vel_y += gravity
        self.y += self.vel_y
        
        # Platform collision
        self.on_ground = False
        slime_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            if slime_rect.colliderect(platform):
                if self.vel_y > 0:  # Falling
                    self.y = platform.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping
                    self.y = platform.bottom
                    self.vel_y = 0
                    
        # Keep slime on screen
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True
            
    def draw(self, screen):
        # Draw slime body (green blob)
        pygame.draw.ellipse(screen, LIGHT_GREEN, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, DARK_GREEN, (self.x, self.y, self.width, self.height), 2)
        
        # Draw ninja mask (black bandana)
        pygame.draw.ellipse(screen, BLACK, (self.x + 5, self.y + 5, 30, 15))
        
        # Draw eyes
        pygame.draw.circle(screen, WHITE, (self.x + 12, self.y + 12), 3)
        pygame.draw.circle(screen, WHITE, (self.x + 28, self.y + 12), 3)
        pygame.draw.circle(screen, BLACK, (self.x + 12, self.y + 12), 1)
        pygame.draw.circle(screen, BLACK, (self.x + 28, self.y + 12), 1)
        
        # Draw health bar
        health_width = 40
        health_height = 5
        health_x = self.x
        health_y = self.y - 10
        health_ratio = self.health / self.max_health
        
        pygame.draw.rect(screen, RED, (health_x, health_y, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (health_x, health_y, health_width * health_ratio, health_height))

class Platform:
    def __init__(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int] = BROWN):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

class Key:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.collected = False
        
    def draw(self, screen):
        if not self.collected:
            # Draw key
            pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
            pygame.draw.circle(screen, YELLOW, (self.x + 10, self.y + 10), 8)
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

class Master:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.rescued = False
        
    def draw(self, screen):
        if not self.rescued:
            # Draw master (wizard)
            pygame.draw.ellipse(screen, PURPLE, (self.x, self.y, self.width, self.height))
            pygame.draw.ellipse(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
            
            # Draw wizard hat
            pygame.draw.polygon(screen, BLUE, [(self.x + 10, self.y), (self.x + 25, self.y - 20), (self.x + 40, self.y)])
            pygame.draw.polygon(screen, BLACK, [(self.x + 10, self.y), (self.x + 25, self.y - 20), (self.x + 40, self.y)], 2)
            
            # Draw eyes
            pygame.draw.circle(screen, WHITE, (self.x + 15, self.y + 15), 3)
            pygame.draw.circle(screen, WHITE, (self.x + 35, self.y + 15), 3)
            pygame.draw.circle(screen, BLACK, (self.x + 15, self.y + 15), 1)
            pygame.draw.circle(screen, BLACK, (self.x + 35, self.y + 15), 1)

class WordlePuzzle:
    def __init__(self):
        self.words = ["SLIME", "NINJA", "MASTER", "DUNGEON", "RESCUE", "PUZZLE", "GAME", "ADVENTURE"]
        self.target_word = random.choice(self.words)
        self.guesses = []
        self.max_guesses = 6
        self.current_guess = ""
        self.game_won = False
        self.game_over = False
        
    def add_letter(self, letter: str):
        if len(self.current_guess) < len(self.target_word) and not self.game_over:
            self.current_guess += letter.upper()
            
    def remove_letter(self):
        if self.current_guess and not self.game_over:
            self.current_guess = self.current_guess[:-1]
            
    def submit_guess(self):
        if len(self.current_guess) == len(self.target_word) and not self.game_over:
            self.guesses.append(self.current_guess)
            if self.current_guess == self.target_word:
                self.game_won = True
                self.game_over = True
            elif len(self.guesses) >= self.max_guesses:
                self.game_over = True
            self.current_guess = ""
            
    def get_feedback(self, guess: str) -> List[str]:
        feedback = []
        target_letters = list(self.target_word)
        guess_letters = list(guess)
        
        # Check for correct letters in correct positions
        for i in range(len(guess_letters)):
            if i < len(target_letters) and guess_letters[i] == target_letters[i]:
                feedback.append("green")
                target_letters[i] = None
            else:
                feedback.append("gray")
                
        # Check for correct letters in wrong positions
        for i in range(len(guess_letters)):
            if feedback[i] == "gray" and guess_letters[i] in target_letters:
                feedback[i] = "yellow"
                target_letters[target_letters.index(guess_letters[i])] = None
                
        return feedback
        
    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, DARK_GRAY, (200, 100, 800, 600))
        pygame.draw.rect(screen, WHITE, (200, 100, 800, 600), 3)
        
        # Draw title
        font_large = pygame.font.Font(None, 48)
        title = font_large.render("WORDLE PUZZLE", True, WHITE)
        screen.blit(title, (400, 120))
        
        # Draw target word length hint
        font_medium = pygame.font.Font(None, 32)
        hint = font_medium.render(f"Guess the {len(self.target_word)}-letter word!", True, WHITE)
        screen.blit(hint, (350, 160))
        
        # Draw guesses
        font_small = pygame.font.Font(None, 36)
        y_offset = 220
        for i, guess in enumerate(self.guesses):
            feedback = self.get_feedback(guess)
            x_offset = 350
            for j, letter in enumerate(guess):
                color = WHITE
                if feedback[j] == "green":
                    color = GREEN
                elif feedback[j] == "yellow":
                    color = YELLOW
                elif feedback[j] == "gray":
                    color = GRAY
                    
                letter_surface = font_small.render(letter, True, BLACK)
                pygame.draw.rect(screen, color, (x_offset, y_offset, 40, 40))
                pygame.draw.rect(screen, BLACK, (x_offset, y_offset, 40, 40), 2)
                screen.blit(letter_surface, (x_offset + 10, y_offset + 8))
                x_offset += 50
            y_offset += 60
            
        # Draw current guess
        if not self.game_over:
            x_offset = 350
            for i, letter in enumerate(self.current_guess):
                letter_surface = font_small.render(letter, True, BLACK)
                pygame.draw.rect(screen, WHITE, (x_offset, y_offset, 40, 40))
                pygame.draw.rect(screen, BLACK, (x_offset, y_offset, 40, 40), 2)
                screen.blit(letter_surface, (x_offset + 10, y_offset + 8))
                x_offset += 50
                
        # Draw remaining empty boxes
        for i in range(len(self.current_guess), len(self.target_word)):
            pygame.draw.rect(screen, WHITE, (x_offset, y_offset, 40, 40))
            pygame.draw.rect(screen, BLACK, (x_offset, y_offset, 40, 40), 2)
            x_offset += 50
            
        # Draw instructions
        font_small = pygame.font.Font(None, 24)
        instructions = [
            "Type letters to guess the word",
            "Press ENTER to submit",
            "Press BACKSPACE to delete",
            "Press ESC to exit puzzle"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, WHITE)
            screen.blit(text, (250, 500 + i * 30))
            
        # Draw game over message
        if self.game_over:
            font_large = pygame.font.Font(None, 48)
            if self.game_won:
                message = font_large.render("PUZZLE SOLVED!", True, GREEN)
            else:
                message = font_large.render(f"Game Over! Word was: {self.target_word}", True, RED)
            screen.blit(message, (350, 650))

class TicTacToePuzzle:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_won = False
        self.game_over = False
        self.winner = None
        
    def make_move(self, row: int, col: int):
        if self.board[row][col] == "" and not self.game_over:
            self.board[row][col] = self.current_player
            
            # Check for win
            if self.check_winner(row, col):
                self.game_won = True
                self.game_over = True
                self.winner = self.current_player
            elif self.is_board_full():
                self.game_over = True
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                
    def check_winner(self, row: int, col: int) -> bool:
        player = self.board[row][col]
        
        # Check row
        if all(self.board[row][i] == player for i in range(3)):
            return True
            
        # Check column
        if all(self.board[i][col] == player for i in range(3)):
            return True
            
        # Check diagonals
        if row == col and all(self.board[i][i] == player for i in range(3)):
            return True
            
        if row + col == 2 and all(self.board[i][2-i] == player for i in range(3)):
            return True
            
        return False
        
    def is_board_full(self) -> bool:
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))
        
    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, DARK_GRAY, (200, 100, 800, 600))
        pygame.draw.rect(screen, WHITE, (200, 100, 800, 600), 3)
        
        # Draw title
        font_large = pygame.font.Font(None, 48)
        title = font_large.render("TIC TAC TOE PUZZLE", True, WHITE)
        screen.blit(title, (400, 120))
        
        # Draw board
        board_x = 400
        board_y = 200
        cell_size = 100
        
        for i in range(3):
            for j in range(3):
                x = board_x + j * cell_size
                y = board_y + i * cell_size
                
                # Draw cell
                pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size))
                pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size), 2)
                
                # Draw X or O
                if self.board[i][j]:
                    font_large = pygame.font.Font(None, 72)
                    color = BLUE if self.board[i][j] == "X" else RED
                    text = font_large.render(self.board[i][j], True, color)
                    text_rect = text.get_rect(center=(x + cell_size//2, y + cell_size//2))
                    screen.blit(text, text_rect)
                    
        # Draw current player
        font_medium = pygame.font.Font(None, 32)
        player_text = font_medium.render(f"Current Player: {self.current_player}", True, WHITE)
        screen.blit(player_text, (350, 350))
        
        # Draw instructions
        font_small = pygame.font.Font(None, 24)
        instructions = [
            "Click on a cell to make a move",
            "You are X, computer is O",
            "Get 3 in a row to win!",
            "Press ESC to exit puzzle"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, WHITE)
            screen.blit(text, (250, 450 + i * 30))
            
        # Draw game over message
        if self.game_over:
            font_large = pygame.font.Font(None, 48)
            if self.game_won:
                if self.winner == "X":
                    message = font_large.render("YOU WIN!", True, GREEN)
                else:
                    message = font_large.render("Computer wins!", True, RED)
            else:
                message = font_large.render("It's a tie!", True, YELLOW)
            screen.blit(message, (450, 550))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ninja Slime Adventure")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        
        self.game_state = MENU
        self.slime = NinjaSlime(100, SCREEN_HEIGHT - 100)
        
        # Create platforms
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Ground
            Platform(300, 600, 200, 20),
            Platform(600, 500, 200, 20),
            Platform(900, 400, 200, 20),
            Platform(150, 300, 200, 20),
            Platform(450, 200, 200, 20),
            Platform(750, 150, 200, 20),
        ]
        
        # Create keys
        self.keys = [
            Key(350, 570),
            Key(650, 470),
            Key(950, 370),
            Key(200, 270),
            Key(500, 170),
        ]
        
        # Create master
        self.master = Master(800, 120)
        
        # Create puzzles
        self.wordle_puzzle = WordlePuzzle()
        self.tictactoe_puzzle = TicTacToePuzzle()
        
        # Puzzle triggers
        self.puzzle_triggers = [
            pygame.Rect(400, 580, 100, 20),  # Wordle trigger
            pygame.Rect(700, 480, 100, 20),  # Tic Tac Toe trigger
        ]
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state in [WORDLE_PUZZLE, TIC_TAC_TOE_PUZZLE]:
                        self.game_state = PLAYING
                    elif self.game_state == MENU:
                        return False
                        
                if self.game_state == WORDLE_PUZZLE:
                    if event.key == pygame.K_RETURN:
                        self.wordle_puzzle.submit_guess()
                        if self.wordle_puzzle.game_won:
                            self.slime.keys_collected += 1
                            self.game_state = PLAYING
                    elif event.key == pygame.K_BACKSPACE:
                        self.wordle_puzzle.remove_letter()
                    elif event.unicode.isalpha():
                        self.wordle_puzzle.add_letter(event.unicode)
                        
                elif self.game_state == TIC_TAC_TOE_PUZZLE:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = PLAYING
                        
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_state == TIC_TAC_TOE_PUZZLE:
                mouse_pos = pygame.mouse.get_pos()
                board_x = 400
                board_y = 200
                cell_size = 100
                
                for i in range(3):
                    for j in range(3):
                        x = board_x + j * cell_size
                        y = board_y + i * cell_size
                        if x <= mouse_pos[0] <= x + cell_size and y <= mouse_pos[1] <= y + cell_size:
                            if self.tictactoe_puzzle.board[i][j] == "":
                                self.tictactoe_puzzle.make_move(i, j)
                                if not self.tictactoe_puzzle.game_over:
                                    # Computer move
                                    self.make_computer_move()
                                    
        return True
        
    def make_computer_move(self):
        # Simple AI: find first empty cell
        for i in range(3):
            for j in range(3):
                if self.tictactoe_puzzle.board[i][j] == "":
                    self.tictactoe_puzzle.make_move(i, j)
                    return
                    
    def update(self):
        if self.game_state == PLAYING:
            self.slime.update([p.rect for p in self.platforms])
            
            # Check key collection
            slime_rect = pygame.Rect(self.slime.x, self.slime.y, self.slime.width, self.slime.height)
            for key in self.keys:
                if not key.collected:
                    key_rect = pygame.Rect(key.x, key.y, key.width, key.height)
                    if slime_rect.colliderect(key_rect):
                        key.collected = True
                        self.slime.keys_collected += 1
                        
            # Check puzzle triggers
            for i, trigger in enumerate(self.puzzle_triggers):
                if slime_rect.colliderect(trigger):
                    if i == 0:  # Wordle
                        self.game_state = WORDLE_PUZZLE
                        self.wordle_puzzle = WordlePuzzle()  # Reset puzzle
                    elif i == 1:  # Tic Tac Toe
                        self.game_state = TIC_TAC_TOE_PUZZLE
                        self.tictactoe_puzzle = TicTacToePuzzle()  # Reset puzzle
                        
            # Check master rescue
            master_rect = pygame.Rect(self.master.x, self.master.y, self.master.width, self.master.height)
            if slime_rect.colliderect(master_rect) and self.slime.keys_collected >= 3:
                self.master.rescued = True
                self.slime.master_rescued = True
                self.game_state = VICTORY
                
    def draw(self):
        self.screen.fill(BLACK)
        
        if self.game_state == MENU:
            self.draw_menu()
        elif self.game_state == PLAYING:
            self.draw_game()
        elif self.game_state == WORDLE_PUZZLE:
            self.wordle_puzzle.draw(self.screen)
        elif self.game_state == TIC_TAC_TOE_PUZZLE:
            self.tictactoe_puzzle.draw(self.screen)
        elif self.game_state == VICTORY:
            self.draw_victory()
            
        pygame.display.flip()
        
    def draw_menu(self):
        # Draw title
        title = self.font_large.render("NINJA SLIME ADVENTURE", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        # Draw subtitle
        subtitle = self.font.render("Rescue your master from the dungeon!", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 280))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw instructions
        instructions = [
            "Use ARROW KEYS or WASD to move",
            "SPACEBAR to jump",
            "Collect keys and solve puzzles",
            "Rescue your master to win!",
            "",
            "Press any key to start"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 400 + i * 40))
            self.screen.blit(text, text_rect)
            
    def draw_game(self):
        # Draw background (dungeon)
        pygame.draw.rect(self.screen, DARK_GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Draw some dungeon decorations
        for i in range(0, SCREEN_WIDTH, 100):
            pygame.draw.rect(self.screen, GRAY, (i, 0, 2, SCREEN_HEIGHT))
            
        # Draw platforms
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # Draw keys
        for key in self.keys:
            key.draw(self.screen)
            
        # Draw master
        self.master.draw(self.screen)
        
        # Draw puzzle triggers (invisible but functional)
        # for trigger in self.puzzle_triggers:
        #     pygame.draw.rect(self.screen, RED, trigger)
            
        # Draw slime
        self.slime.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
    def draw_ui(self):
        # Draw keys collected
        keys_text = self.font.render(f"Keys: {self.slime.keys_collected}/5", True, WHITE)
        self.screen.blit(keys_text, (10, 10))
        
        # Draw health
        health_text = self.font.render(f"Health: {self.slime.health}", True, WHITE)
        self.screen.blit(health_text, (10, 50))
        
        # Draw instructions
        instructions = [
            "Arrow Keys/WASD: Move",
            "Space: Jump",
            "Collect keys and solve puzzles!",
            "Need 3 keys to rescue master"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH - 300, 10 + i * 30))
            
    def draw_victory(self):
        # Draw victory screen
        self.screen.fill(GREEN)
        
        victory_text = self.font_large.render("VICTORY!", True, WHITE)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(victory_text, victory_rect)
        
        subtitle = self.font.render("You rescued your master!", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 380))
        self.screen.blit(subtitle, subtitle_rect)
        
        restart_text = self.font.render("Press any key to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, 450))
        self.screen.blit(restart_text, restart_rect)
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 