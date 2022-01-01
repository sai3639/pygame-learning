import pygame, sys

clock = pygame.time.Clock()


from pygame.locals import *
pygame.init() # initialize pygame

pygame.display.set_caption('My pygame window') # name of window

WINDOW_SIZE = (400,400)


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initialize the window



player_image = pygame.image.load('fox.png') # load player image

grass_image = pygame.image.load('grass.png')
dirt_image = pygame.image.load('dirt.png')


# 0 - air 2 - grass 1 - dirt
game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]



moving_right = False
moving_left = False

player_location = [50,50]
player_y_momentum = 0


player_rect = pygame.Rect(player_location[0],player_location[1],player_image.get_width(),player_image.get_height())

test_rect = pygame.Rect(100, 100, 100, 50)

while True: # game loop
    screen.fill((146,244,255)) # fill surface with solid color each time the player moves - no overlay of player
    
    screen.blit(player_image, player_location)  # render the image on the window


    # tests to see if image goes off screen
    if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
        player_y_momentum = -player_y_momentum  # bounce back up to top
    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum #simulates gravity, always falling
        

    
    if moving_right == True:
        player_location[0] += 4  # '[0]' bc wanting to change x value
    if moving_left == True:
        player_location[0] -= 4

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]
    
    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen, (255,0,0), test_rect)
    else:
        pygame.draw.rect(screen,(0,0,0), test_rect)

    # loops through every even keyboard and mouse
    for event in pygame.event.get():
        if event.type == QUIT:  #'x' is clicked on the window
            pygame.quit()
            sys.exit() # exit the program


        if event.type == KEYDOWN: # key pushed down
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:  # key comes up 
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False



    pygame.display.update()  #updates the display
    clock.tick(60) # keep window running at 60 fps (frame rate)
