import pygame
import random

# setting up our basics
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1240,680
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

# plain surface
surf = pygame.Surface((100,200))
x = 100

    


#importing an image
player_surf = pygame.image.load('images/player.png').convert_alpha()
star_surf = pygame.image.load('images/star.png').convert_alpha()
star_positions = [(random.randint(1,WINDOW_WIDTH),random.randint(1,WINDOW_HEIGHT)) for i in range(20)]

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # draw the game
    display_surface.fill('darkgray')
    for i in star_positions:
        display_surface.blit(star_surf,(i))   
    display_surface.blit(player_surf,(x,150))
    
    pygame.display.update()
pygame.quit()
