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

    def decide_movement(self):
        # Basic AI logic, start with making random turns etc.
        pass

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

    def draw(self):
        self.screen.fill(BLACK)
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

    # # Add current position to trail
    # player_1_trail.append(player_1['position'][:])
    # player_2_trail.append(player_2['position'][:])

    # if len(player_1_trail) > MAX_TRAIL_LENGTH:
    #     player_1_trail.pop(0) # Remove the oldest position
    
    # if len(player_2_trail) > MAX_TRAIL_LENGTH:
    #     player_2_trail.pop(0) # Remove the oldest position

    # screen.fill(BLACK)
    # trail_surface.fill((0, 0, 0, 0))

    # player_1_trail_colour = (*player_1['colour'], trail_alpha)
    # player_2_trail_colour = (*player_2['colour'], trail_alpha)

    # # Draw player 1 trail
    # for pos in player_1_trail:
    #     pygame.draw.rect(screen, player_1_trail_colour, (pos[0], pos[1], PLAYER_SIZE, PLAYER_SIZE))
    
    # # Draw player 2 trail
    # for pos in player_2_trail:
    #     pygame.draw.rect(screen, player_2_trail_colour, (pos[0], pos[1], PLAYER_SIZE, PLAYER_SIZE))

    # Draw Player 1 trail with fading effect
    # for i, pos in enumerate(player_1_trail):
    #     # Calculate alpha based on position in the trail list (older segments are more transparent)
    #     alpha = int(255 * (i / MAX_TRAIL_LENGTH))  # Older positions will have lower alpha
    #     trail_color = (*player_1['colour'], alpha)
    #     trail_rect = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
    #     trail_rect.fill(trail_color)
    #     screen.blit(trail_rect, pos)
    
    # # Draw Player 2 trail with fading effect
    # for i, pos in enumerate(player_2_trail):
    #     alpha = int(255 * (i / MAX_TRAIL_LENGTH))
    #     trail_color = (*player_2['colour'], alpha)
    #     trail_rect = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
    #     trail_rect.fill(trail_color)
    #     screen.blit(trail_rect, pos)

    # if (player_1['position'][0] < 0 or 
    #     player_1['position'][0] >= WIDTH or
    #     player_1['position'][1] < 0 or 
    #     player_1['position'][1] >= HEIGHT):
    #     print("Player 1 hit the wall!")
    #     game_over = True



    screen.blit(trail_surface, (0, 0)) # Blit trail surface onto main screen

    # # Drawing sprites for players, player 1 as blue square, player 2 as red square
    # pygame.draw.rect(screen, player_1['colour'],
    #             (player_1['position'][0], player_1['position'][1], PLAYER_SIZE, PLAYER_SIZE))  
    # pygame.draw.rect(screen, player_2['colour'], 
    #              (player_2['position'][0], player_2['position'][1], PLAYER_SIZE, PLAYER_SIZE))
    
    pygame.display.flip() # Update display

    clock.tick(60) # Limit to 60 FPS

    
