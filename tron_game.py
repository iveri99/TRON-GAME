import pygame

# initialise PyGame
pygame.init()

# CONSTANTS
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PLAYER_SIZE = 10
MAX_TRAIL_LENGTH = 50
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) # Transparent surface created for trail
trail_alpha = 50
pygame.display.set_caption("TRON GAME")

game_over = False # 'Game over check' variable created with boolean value - originally falsy



# Variable created to identify that game is running
running = True
clock = pygame.time.Clock() # Used later for screen refresh rate
PLAYER_SIZE = 10
player_1_trail = []
player_2_trail = []
MAX_TRAIL_LENGTH = 50


class Move:
    def __init__(self, x, y, speed=5, direction = None):
        # Initialise Move class
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.previous_positions = []

        self.trail = [] # Keep track of position - prevent self collision
        self.max_trail_length = MAX_TRAIL_LENGTH # Limit length of trail


    def update_position(self):
        # Checking if self.direction has been given a value
        if self.direction is None:
            raise ValueError("Direction must be set before calling move.")
        
        # Save current position to trail
        self.previous_positions.append((self.x, self.y))

        # Update position based on direction
        if self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed

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

        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

    def check_collision(self):
        # Check if out of bounds
        if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT:
            return True
        elif (self.x, self.y) in self.previous_positions:
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
    def __init__(self):
        self.speed = CELL_SIZE // 5
        self.target_position = None

    def move(self):
        self.update_position()

    def draw(self, surface):
        pass

class UserPlayer(Player):
    def __init__(self, x, y, colour = BLUE, speed=5, direction="LEFT"):
        super().__init__(x, y, colour, speed, direction)

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
            trail_color = (self.colour, alpha)  # RGBA
            trail_rect = pygame.Surface((10, 10), pygame.SRCALPHA)
            trail_rect.fill(trail_color)
            surface.blit(trail_rect, pos)

class ProgramPlayer(Player):
    def __init__(self, x, y, colour = RED, speed=5, direction= "RIGHT"):
        super().__init__(x, y, colour, speed, direction)

class Main(UserPlayer, ProgramPlayer):
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
        self.user = UserPlayer(100, HEIGHT // 2, BLUE, speed=5, direction="LEFT")
        self.program = ProgramPlayer(WIDTH - 100, HEIGHT // 2, RED, speed=5, direction="RIGHT")

    def run(self):
        # Main game loop

        while self.running:
            self.handle_events()

            if not self.game_over:
                self.update()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

    def handle_events(self):
        # Process game events frame by frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    keys = pygame.key.get_pressed()

    user_input = UserPlayer.handle_input()

    # Add current position to trail
    player_1_trail.append(player_1['position'][:])
    player_2_trail.append(player_2['position'][:])

    if len(player_1_trail) > MAX_TRAIL_LENGTH:
        player_1_trail.pop(0) # Remove the oldest position
    
    if len(player_2_trail) > MAX_TRAIL_LENGTH:
        player_2_trail.pop(0) # Remove the oldest position

    screen.fill(BLACK)
    trail_surface.fill((0, 0, 0, 0))

    player_1_trail_colour = (*player_1['colour'], trail_alpha)
    player_2_trail_colour = (*player_2['colour'], trail_alpha)

    # # Draw player 1 trail
    # for pos in player_1_trail:
    #     pygame.draw.rect(screen, player_1_trail_colour, (pos[0], pos[1], PLAYER_SIZE, PLAYER_SIZE))
    
    # # Draw player 2 trail
    # for pos in player_2_trail:
    #     pygame.draw.rect(screen, player_2_trail_colour, (pos[0], pos[1], PLAYER_SIZE, PLAYER_SIZE))

    # Draw Player 1 trail with fading effect
    for i, pos in enumerate(player_1_trail):
        # Calculate alpha based on position in the trail list (older segments are more transparent)
        alpha = int(255 * (i / MAX_TRAIL_LENGTH))  # Older positions will have lower alpha
        trail_color = (*player_1['colour'], alpha)
        trail_rect = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        trail_rect.fill(trail_color)
        screen.blit(trail_rect, pos)
    
    # Draw Player 2 trail with fading effect
    for i, pos in enumerate(player_2_trail):
        alpha = int(255 * (i / MAX_TRAIL_LENGTH))
        trail_color = (*player_2['colour'], alpha)
        trail_rect = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        trail_rect.fill(trail_color)
        screen.blit(trail_rect, pos)

    if (player_1['position'][0] < 0 or 
        player_1['position'][0] >= WIDTH or
        player_1['position'][1] < 0 or 
        player_1['position'][1] >= HEIGHT):
        print("Player 1 hit the wall!")
        game_over = True



    screen.blit(trail_surface, (0, 0)) # Blit trail surface onto main screen

    # Drawing sprites for players, player 1 as blue square, player 2 as red square
    pygame.draw.rect(screen, player_1['colour'],
                (player_1['position'][0], player_1['position'][1], PLAYER_SIZE, PLAYER_SIZE))  
    pygame.draw.rect(screen, player_2['colour'], 
                 (player_2['position'][0], player_2['position'][1], PLAYER_SIZE, PLAYER_SIZE))
    
    pygame.display.flip() # Update display

    clock.tick(60) # Limit to 60 FPS

    
