import pygame

#initialise PyGame
pygame.init()

#Setting up display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TRON GAME")

#Define colours
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

#Variable created to identify that game is running
running = True
clock = pygame.time.Clock() #used later for screen refresh rate

#Dictionary for player 1 with position, colour, direction and speed keys
player_1 = {
    'position': [100, HEIGHT // 2],
    'colour': BLUE,
    'direction': 'RIGHT',
    'speed': 5
}

#Same done for player 2
player_2 = {
    'position': [WIDTH - 100, HEIGHT // 2],
    'colour': RED,
    'direction': 'LEFT',
    'speed': 5
}

#Loop to keep game running until event quit from pygame
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Handling player 1 movement (arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_1['direction'] == 'RIGHT':
        player_1['position'][0] += player_1['speed']
    elif keys[pygame.K_RIGHT] and player_1['direction'] == 'RIGHT':
        player_1['position'][0] -= player_1['speed']
    elif keys[pygame.K_UP] and player_1['direction'] == 'UP':
        player_1['position'][1] -= player_1['speed']
    elif keys[pygame.K_DOWN] and player_1['direction'] == 'DOWN':
        player_1['position'][1] += player_1['speed']
    
    #Move player 2
    if keys[pygame.K_LEFT] and player_2['direction'] == 'RIGHT':
        player_2['position'][0] += player_2['speed']
    elif keys[pygame.K_RIGHT] and player_2['direction'] == 'RIGHT':
        player_2['position'][0] -= player_2['speed']
    elif keys[pygame.K_UP] and player_2['direction'] == 'UP':
        player_2['position'][1] -= player_2['speed']
    elif keys[pygame.K_DOWN] and player_2['direction'] == 'DOWN':
        player_2['position'][1] += player_2['speed']


screen.fill(BLACK)

pygame.display.flip()

clock.tick(60)

#Dictionary for player 1 with position, colour, direction and speed keys
player_1 = {
    'position': [100, HEIGHT // 2],
    'colour': BLUE,
    'direction': 'RIGHT',
    'speed': 5
}

#Same done for player 2
player_2 = {
    'position': [WIDTH - 100, HEIGHT // 2],
    'colour': RED,
    'direction': 'LEFT',
    'speed': 5
}

