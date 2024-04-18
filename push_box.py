import pygame
from map_list import map_list

m = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 4, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
size = 16

# Load textures
background_texture = pygame.image.load('./texture/ground.jpg')
wall_texture = pygame.image.load('./texture/wall.jpg')
target_texture = pygame.image.load('./texture/target.jpg')
box_texture = pygame.image.load('./texture/box.jpg')
character_texture = pygame.image.load('./texture/pika_left.jpg')

# Define tile size
tile_size = 56
background_texture = pygame.transform.scale(background_texture, (tile_size, tile_size))
wall_texture = pygame.transform.scale(wall_texture, (tile_size, tile_size))
target_texture = pygame.transform.scale(target_texture, (tile_size, tile_size))
box_texture = pygame.transform.scale(box_texture, (tile_size, tile_size))
character_texture = pygame.transform.scale(character_texture, (tile_size, tile_size))

# Initialize pygame
pygame.init()

# Create the game window
window_width = size * tile_size
window_height = size * tile_size
window = pygame.display.set_mode((window_width, window_height))

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the map
    for row in range(size):
        for col in range(size):
            tile = m[row * size + col]
            x = col * tile_size
            y = row * tile_size

            if tile == 0:
                window.blit(background_texture, (x, y))
            elif tile == 1:
                window.blit(wall_texture, (x, y))
            elif tile == 2:
                window.blit(target_texture, (x, y))
            elif tile == 3:
                window.blit(box_texture, (x, y))
            elif tile == 4:
                window.blit(character_texture, (x, y))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()