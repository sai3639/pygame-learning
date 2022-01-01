import pygame, sys

clock = pygame.time.Clock()


from pygame.locals import *
pygame.init() # initialize pygame

pygame.display.set_caption('My pygame window') # name of window

WINDOW_SIZE = (600,400)


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initialize the window

display = pygame.Surface((300,200)) # surface = image

player_image = pygame.image.load('player.png').convert() # load player image
player_image.set_colorkey((255,255,255))  # set color to transparent

grass_image = pygame.image.load('grass.png')
TILE_SIZE = grass_image.get_width()
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



def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles): # movement (x,y)
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            #player moves right and collides with tile
            rect.right = tile.left # player on left tile on right
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False


player_y_momentum = 0
air_timer =0


player_rect = pygame.Rect(50,50,player_image.get_width(),player_image.get_height())

test_rect = pygame.Rect(100, 100, 100, 50)

while True: # game loop
    display.fill((146,244,255)) # fill surface with solid color each time the player moves - no overlay of player

    # physics
    tile_rects = [] # keeping track of blocks not air for player collisions
    
    y = 0 # rendering position
    for row in game_map:
        x = 0 # rendering position
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x*TILE_SIZE, y*TILE_SIZE)) # pixel size
            if tile == '2':
                display.blit(grass_image, (x*TILE_SIZE, y*TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1 # moving across list by one
        y += 1 # move down to next row
        
        

    
    


    # velocity of the player
    player_movement = [0,0]
    if moving_right:
        player_movement[0] +=2
    if moving_left:
        player_movement[0] -=2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3: # player cant fall faster than 3 pixels per sec
        player_y_momentum = 3
   
    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer =0
    else:
        air_timer += 1
    
    display.blit(player_image, (player_rect.x, player_rect.y))  # render the image on the window


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
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum =-5
        if event.type == KEYUP:  # key comes up 
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
                


    surf = (pygame.transform.scale(display,WINDOW_SIZE)) # scale changes size of surface (what you want to change, what you want it to chhange to)
    screen.blit(surf,(0,0)) # perfectly aligned 
    pygame.display.update()  #updates the display
    clock.tick(60) # keep window running at 60 fps (frame rate)
