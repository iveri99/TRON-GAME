import pygame
import random

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

class Move:
    def __init__(self, x, y, speed=5, direction = None):
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
    def __init__(self, x, y, speed=5, direction = None):
        super().__init__(x, y, speed, direction)

    def move(self):
        self.update_position()

    def draw(self, surface):
        pass

class UserPlayer(Player):
    def __init__(self, x, y, colour = BLUE, speed=5, direction="LEFT"):
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

class ProgramPlayer(Player):
    def __init__(self, x, y, colour = RED, speed=5, direction= "RIGHT"):
        super().__init__(x, y, speed, direction)
        self.colour = colour

    def get_safe_moves(self, grid, rows, cols):
        # Determine all valid moves for the Program Player in its current position

        # Current position in the grid
        grid_x = self.x // CELL_SIZE
        grid_y = self.y // CELL_SIZE

        rows = ROWS
        cols = COLS

        # Possible directions and deltas
        directions = {
            "UP": (grid_x, grid_y - 1),
            "DOWN": (grid_x, grid_y + 1),
            "LEFT": (grid_x - 1, grid_y),
            "RIGHT": (grid_x + 1, grid_y)
        }

        # List to store safe moves
        safe_moves = []

        # Iterate through possible moves
        for direction, (new_x, new_y) in directions.items():
            # Check if new position is within bounds
            if 0 <= new_x < cols and 0 <= new_y < rows:
                # Check if the new position is not occupied
                if not grid[new_y][new_x]:
                    safe_moves.append(direction)

        return safe_moves

    
    def decide_movement(self):
        # Basic AI logic, start with making random turns etc.
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        opposite = {"UP":"DOWN", "DOWN":"UP","LEFT":"RIGHT","RIGHT":"LEFT"}

        # 1) Randomly decide to turn
        if random.random() < 0.05: # 5% chance each frame
            possible_direction = [d for d in directions if d != opposite[self.direction]]
            new_direction = random.choice(possible_direction)
            self.change_direction(new_direction)

        # 2) Check if continuing straight will colide
        if self.collision_if_straight():
            # Pick a safe direction
            safe_directions = self.find_safe_directions()
            if safe_directions:
                self.change_direction(random.choice(safe_directions))
            else:
                # No safe directions? - Still need to pick one
                self.change_direction(random.choice(directions))

    def collision_if_straight(self):
        # Check if next position in current direction would cause collision with wall/self
        next_x, next_y = self.get_next_position(self.direction)
        # Check wall collision
        if next_x < 0 or next_x >= WIDTH or next_y < 0 or next_y >= HEIGHT:
            return True
        
        # Check self trail collision
        if (next_x, next_y) in self.trail:
            return True
        return False
    
    def find_safe_directions(self):
        # Returns list of directions that are safe for the next move (not an immediate collision)
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        safe = []

        for d in directions:
            next_x, next_y = self.get_next_position(d)
            # Check bounds
            if 0 <= next_x <= WIDTH and 0 <= next_y < HEIGHT:
                # Check self collision
                if (next_x, next_y) not in self.trail:
                    safe.append(d)
        return safe
    
    def get_next_position(self, direction):
        # If player moves one step in direction, which xy will they end up at?
        next_x, next_y = self.x, self.y
        if direction == "UP":
            next_y -= self.speed
        elif direction == "DOWN":
            next_y += self.speed
        elif direction == "LEFT":
            next_x -= self.speed
        elif direction == "RIGHT":
            next_x += self.speed
        return next_x, next_y

    
    def draw(self, surface):
        # Draw trail with fading + player's square
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / self.max_trail_length))
            trail_colour = (*self.colour, alpha)  # RGBA
            trail_rect = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
            trail_rect.fill(trail_colour)
            surface.blit(trail_rect, pos)


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

        # Two players created - user and program
        self.user = UserPlayer(x = WIDTH - 100, y = HEIGHT // 2, colour = BLUE, speed = 5, direction = "LEFT")
        self.program = ProgramPlayer(x = 100, y = HEIGHT // 2, colour = RED, speed = 5, direction = "RIGHT")

    def handle_events(self):
        # Process game events frame by frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()

        self.user.handle_input(keys)
        self.program.decide_movement() # Program decides movement on its own
    
    def update(self):
        self.user.update_position()
        self.program.update_position()

        # Checks for collisions
        if self.user.check_wall_collision() or self.user.check_self_collision():
            self.game_over = True
        if self.program.check_wall_collision() or self.program.check_self_collision():
            self.game_over = True

        # Checks if user hits program's trail or vice versa
        if self.user.get_position() in self.program.trail:
            self.game_over = True
        if self.program.get_position() in self.user.trail:
            self.game_over = True

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
    
