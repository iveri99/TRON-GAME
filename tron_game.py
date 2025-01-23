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
USER_INITAL_DIRECTION = "LEFT"
PROGRAM_INITIAL_DIRECTION = "RIGHT"

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
    def __init__(self, x, y, speed=5):
        # Initialise Move class
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = None
        self.previous_positions = []

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
    
    def get_position(self):
        # Return current position
        return [self.x, self.y]
            
class Player(Move):
    def __init__(self):
        self.speed = CELL_SIZE // 5
        self.target_position = None

    def move(self):
        self.update_position()

    

# Dictionary for player 1 with position, colour, direction and speed keys
player_1 = {
    'position': [100, HEIGHT // 2],
    'colour': BLUE,
    'direction': 'RIGHT',
    'speed': 5
}

# Same done for player 2
player_2 = {
    'position': [WIDTH - 100, HEIGHT // 2],
    'colour': RED,
    'direction': 'LEFT',
    'speed': 5
}

# Main code loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # If game over, show message and skip movement/logic
    if game_over:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 255, 255))
        
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        continue  # Skip the rest of the loop if game over

    # Handling player 1 movement (arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_1['direction'] != 'RIGHT': # prevents reversing
        player_1['direction'] = 'LEFT'
    elif keys[pygame.K_RIGHT] and player_1['direction'] != 'LEFT':
        player_1['direction'] = 'RIGHT'
    elif keys[pygame.K_UP] and player_1['direction'] != 'DOWN':
        player_1['direction'] = 'UP'
    elif keys[pygame.K_DOWN] and player_1['direction'] != 'UP':
        player_1['direction'] = 'DOWN'
    
    # Handling player 2 movement (wasd keys)
    if keys[pygame.K_a] and player_2['direction'] != 'RIGHT':
        player_2['direction'] = 'LEFT'
    elif keys[pygame.K_d] and player_2['direction'] != 'LEFT':
        player_2['direction'] = 'RIGHT'
    elif keys[pygame.K_w] and player_2['direction'] != 'DOWN':
        player_2['direction'] = 'UP'
    elif keys[pygame.K_s] and player_2['direction'] != 'UP':
        player_2['direction'] = 'DOWN'

    # Move Player 1
    if player_1['direction'] == 'RIGHT':
        player_1['position'][0] += player_1['speed']
    elif player_1['direction'] == 'LEFT':
        player_1['position'][0] -= player_1['speed']
    elif player_1['direction'] == 'UP':
        player_1['position'][1] -= player_1['speed']
    elif player_1['direction'] == 'DOWN':
        player_1['position'][1] += player_1['speed']

    # Move Player 2
    if player_2['direction'] == 'RIGHT':
        player_2['position'][0] += player_2['speed']
    elif player_2['direction'] == 'LEFT':
        player_2['position'][0] -= player_2['speed']
    elif player_2['direction'] == 'UP':
        player_2['position'][1] -= player_2['speed']
    elif player_2['direction'] == 'DOWN':
        player_2['position'][1] += player_2['speed']

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

    
