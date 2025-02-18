import pygame
import random
import heapq

# initialise PyGame
pygame.init()

# CONSTANTS
WIDTH = 600
HEIGHT = 650
CELL_SIZE = 30
BLACK = (0, 0, 0)
BLUE = (162, 212, 255)
RED = (255, 196, 0)
BACKGROUND_COLOUR = (22,33,43)
LINES_COLOUR = (51,77,100)
PLAYER_SIZE = 10
MAX_TRAIL_LENGTH = 50
FPS = 60
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # Transparent surface created for trail
trail_alpha = 50
pygame.display.set_caption("TRON GAME")

game_over = False # 'Game over check' variable created with boolean value - originally falsy

import pygame
import heapq

class TronAI:
    def __init__(self, grid_size, walls, player_pos, opponent_pos):
        self.grid_size = grid_size  # (width, height)
        self.walls = walls  # Set of occupied positions
        self.player_pos = player_pos  # AI player position
        self.opponent_pos = opponent_pos  # Opponent position


class Move:
    def __init__(self, x, y, speed = CELL_SIZE // 5, direction = None):
        # Initialise Move class
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction

        self.trail = [] # Keep track of position - prevent self collision
        self.max_trail_length = MAX_TRAIL_LENGTH # Limit length of trail


    def update_position(self):
        # Checking if self.direction has been given a value
        if self.direction is None:
            raise ValueError("Direction must be set before calling move.")

        # Update position based on direction
        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed

        # Add current position to the trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)    

    def change_direction(self, new_direction):
        # Prevent 180 degree turns
        opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }

        if new_direction is None or new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

    def check_wall_collision(self):
        # Check if out of bounds
        if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT:
            return True
        return False
    
    def check_self_collision(self):
        # Check for self collision
        if len(self.trail) > 2 and (self.x, self.y) in self.trail[:-1]:
            return True
        return False
    
    def get_position(self):
        # Return current position
        return [self.x, self.y]
            
class Player(Move):
    # Initialise Player class
    def __init__(self, x, y, speed= CELL_SIZE // 5, direction = None):
        super().__init__(x, y, speed, direction)

    def move(self):
        self.update_position()

    def draw(self, surface):
        pass

class UserPlayer(Player):
    def __init__(self, x, y, colour = BLUE, speed= CELL_SIZE // 5, direction="LEFT"):
        super().__init__(x, y, speed, direction)
        self.colour = colour

    def handle_input(self, keys):
        # Example of using arrow keys
        if keys[pygame.K_LEFT]:
            self.change_direction("LEFT")
        elif keys[pygame.K_RIGHT]:
            self.change_direction("RIGHT")
        elif keys[pygame.K_UP]:
            self.change_direction("UP")
        elif keys[pygame.K_DOWN]:
            self.change_direction("DOWN")

    def draw(self, surface):
        # Draw trail with fading + player's square
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / self.max_trail_length))
            trail_colour = (*self.colour, alpha)  # RGBA
            trail_rect = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
            trail_rect.fill(trail_colour)
            surface.blit(trail_rect, pos)

        pygame.draw.rect(surface, self.colour, (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

class ProgramPlayer(Player, TronAI):
    def __init__(self, x, y, grid_size, walls, opponent_pos, speed=5, direction="LEFT", colour = RED):
        super().__init__(x, y, speed, direction)
        self.ai = TronAI(grid_size, walls, (x, y), opponent_pos)
        self.colour = colour
    
    def update_ai(self, walls, opponent_pos):
        self.ai.walls = walls
        self.ai.opponent_pos = opponent_pos
        self.ai.player_pos = (self.x, self.y)
    
    def move(self):
        next_move = self.ai.find_best_move()
        if next_move:
            self.x, self.y = next_move
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def draw(self, surface):
        # Draw trail with fading + player's square
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / self.max_trail_length))
            trail_colour = (*self.colour, alpha)  # RGBA
            trail_rect = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
            trail_rect.fill(trail_colour)
            surface.blit(trail_rect, pos)

# class ProgramPlayer(Player):
#     def __init__(self, x, y, colour = RED, speed= CELL_SIZE // 5, direction= "RIGHT"):
#         super().__init__(x, y, speed, direction)
#         self.colour = tuple(colour)
#         self.turn_cooldown = 0



    # def get_safe_moves(self, grid, rows, cols):
    #     # Determine all valid moves for the Program Player in its current position

    #     # Current position in the grid
    #     grid_x = self.x // CELL_SIZE
    #     grid_y = self.y // CELL_SIZE

    #     # Possible directions and deltas
    #     directions = {
    #         "UP": (grid_x, grid_y - 1),
    #         "DOWN": (grid_x, grid_y + 1),
    #         "LEFT": (grid_x - 1, grid_y),
    #         "RIGHT": (grid_x + 1, grid_y)
    #     }

    #     # List to store safe moves
    #     safe_moves = []

    #     # Iterate through possible moves
    #     for direction, (new_x, new_y) in directions.items():
    #         # Check if new position is within bounds
    #         if 0 <= new_x < cols and 0 <= new_y < rows:
    #             # Check if the new position is not occupied
    #             if not grid[new_y][new_x]:
    #                 safe_moves.append(direction)

    #     # Debug
    #     print(f"AI safe moves from ({grid_x}, {grid_y}): {safe_moves}")

    #     return safe_moves

    # def decide_movement(self, grid, rows, cols):
        
    #     opposite_directions = {
    #         "UP": "DOWN",
    #         "DOWN": "UP",
    #         "LEFT": "RIGHT",
    #         "RIGHT": "LEFT"
    #     }
    #     safe_moves = self.get_safe_moves(grid, rows, cols)

    #     count = 0

    #     while count > 0 and count <= 3:
    #         chosen_move = random.choice(safe_moves)
    #         for i in range(3):
    #             self.update_position(chosen_move)
    #             count += 1
            
    #         count = 0

    # def collision_if_straight(self, grid):
    #     # Check if next position in current direction would cause collision with wall/self
    #     next_x, next_y = self.get_next_position(self.direction)
    #     grid_x, grid_y = next_x // CELL_SIZE, next_y // CELL_SIZE

    #     # Debugging
    #     print(f"AI moving {self.direction} to grid {grid_x}, {grid_y}")
       
    #     # Check if not within bounds
    #     if not (0 <= grid_x < COLS and 0 <= grid_y < ROWS):
    #         print("AI collision detected: Out of bounds")
    #         return True
        
    #     if grid[grid_y][grid_x]:
    #         print(f"AI collision detected: Cell ({grid_x}, {grid_y}) is occupied")
    #         return True
        
    #     return False
    
    # def get_next_position(self, direction):
    #     # If player moves one step in direction, which xy will they end up at?
    #     next_x, next_y = self.x, self.y
    #     if direction == "UP":
    #         next_y -= self.speed
    #     elif direction == "DOWN":
    #         next_y += self.speed
    #     elif direction == "LEFT":
    #         next_x -= self.speed
    #     elif direction == "RIGHT":
    #         next_x += self.speed
    #     return next_x, next_y




class Main():
    # Initialise Main
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PyTron")
        self.clock = pygame.time.Clock()
        
        self.running = True
        self.game_over = False
        self.font = pygame.font.Font(None, 74)

        # Create a grid where False = free, and True = occupied
        self.grid = [[False for _ in range(COLS)] for _ in range(ROWS)]

        self.grid_size = (COLS, ROWS)
        self.walls = set()  # Tracks occupied spaces
        
        # Two players created - user and program
        self.user = UserPlayer(x = WIDTH - 100, y = HEIGHT // 2, colour = BLUE, speed = CELL_SIZE // 5, direction = "LEFT")
        self.program = ProgramPlayer(100, HEIGHT // 2, self.grid_size, self.walls, self.user.get_position())

        # Ensure Program's position is not occupied
        self.grid[self.program.y // CELL_SIZE][self.program.x // CELL_SIZE] = False

        

    def handle_events(self):
        # Process game events frame by frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()

        self.user.handle_input(keys)
        # self.program.decide_movement() # Program decides movement on its own
    
    def update(self):
        # Update game state each frame
        self.user.update_position()
        user_grid_x = self.user.x // CELL_SIZE
        user_grid_y = self.user.y // CELL_SIZE
        # self.grid[user_grid_x][user_grid_y] = True # Mark user's new position as occupied

        # AI logic
        # safe_moves = self.program.get_safe_moves(self.grid, ROWS, COLS)
        # if safe_moves:
        #     self.program.change_direction(random.choice(safe_moves))
        
        # self.program.update_position() # Update AI movement
        # self.program.decide_movement(self.grid, ROWS, COLS)

        self.program.update_ai(self.walls, self.user.get_position())
        self.program.move()

        # Add trails to walls (occupied spaces)
        self.walls.update(self.user.trail)
        self.walls.update(self.program.trail)

        # Check for collisions
        # if self.user.check_wall_collision() or self.user.check_self_collision():
        #     self.game_over = True
        # if self.program.check_wall_collision() or self.program.check_self_collision():
        #     self.game_over = True

        # # Check if user hits AI trail or vice versa
        # if self.user.get_position() in self.program.trail:
        #     self.game_over = True
        # if self.program.get_position() in self.user.trail:
        #     self.game_over = True
            
        program_grid_x = self.program.x // CELL_SIZE
        program_grid_y = self.program.y // CELL_SIZE
        # self.grid[program_grid_x][program_grid_y] = True # Mark program's new position as occupied

        players = [self.user, self.program]
        
        # for player in players:
        #     if isinstance(player, ProgramPlayer):
        #         player.decide_movement(self.grid, ROWS, COLS)
        #     player.move()

        # Checks for collisions
        if self.user.check_wall_collision() or self.user.check_self_collision():
            # self.game_over = True
            pass
        if self.program.check_wall_collision() or self.program.check_self_collision():
            # self.game_over = True
            pass

        # Checks if user hits program's trail or vice versa
        if self.user.get_position() in self.program.trail:
            # self.game_over = True
            pass
        if self.program.get_position() in self.user.trail:
            # self.game_over = True
            pass


    def drawGrid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, LINES_COLOUR, rect, 1)
    
    def draw(self):
        self.screen.fill(BACKGROUND_COLOUR)
        self.drawGrid()
        if self.game_over:
            text = self.font.render("GAME OVER", True, (255, 255, 255))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, rect)
        else:
            self.user.draw(self.screen)
            self.program.draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        # Game loop
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()


            self.draw()

            self.clock.tick(FPS)
        pygame.quit()

   

if __name__ == "__main__":
    Main().run()
    
