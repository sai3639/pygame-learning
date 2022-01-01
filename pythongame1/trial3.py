import pygame, sys, os, random
clock = pygame.time.Clock()


from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initialize pygame
pygame.mixer.set_num_channels(64) # how many sounds can play at once

pygame.display.set_caption('My pygame window') # name of window

WINDOW_SIZE = (600,400)


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initialize the window

display = pygame.Surface((300,200)) # surface = image



grass_image = pygame.image.load('grass.png')
TILE_SIZE = grass_image.get_width()
dirt_image = pygame.image.load('dirt.png')
jump_sound = pygame.mixer.Sound('jump.wav')
grass_sounds = [pygame.mixer.Sound('grass_0.wav'),pygame.mixer.Sound('grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1) # play indefinitly

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
game_map = load_map('map')

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' +str(n)
        img_loc = path +'/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n +=1
    return animation_frame_data



def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0 # conditional
    return action_var, frame

#load_animation('player_animation/idle'.capitalize(7,7,40))
    

animation_database = {}
animation_database['run'] = load_animation('player_animations/run',[7,7])
animation_database['idle'] = load_animation('player_animations/idle',[7,7,40])

player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


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
#player_rect = pygame.Rect(50,50,player_image.get_width(),player_image.get_height())
player_rect = pygame.Rect(100,100,5,13)
#test_rect = pygame.Rect(100, 100, 100, 50)

true_scroll = [0,0]

while True: # game loop
    display.fill((146,244,255)) # fill surface with solid color each time the player moves - no overlay of player

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    true_scroll[0] += (player_rect.x - true_scroll[0]-152)/20 #focus on center of player
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0]*background_object[0],background_object[1][1] - scroll[1]*background_object[0],background_object[1][2], background_object[1][3])
        if background_object[0] ==0.5:
            pygame.draw.rect(display,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)


    
    # physics
    tile_rects = [] # keeping track of blocks not air for player collisions
    
    y = 0 # rendering position
    for row in game_map:
        x = 0 # rendering position
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x*TILE_SIZE-scroll[0], y*TILE_SIZE- scroll[1])) # pixel size
            if tile == '2':
                display.blit(grass_image, (x*TILE_SIZE- scroll[0], y*TILE_SIZE- scroll[1]))
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

    if player_movement[0] > 0:
       player_action, player_frame = change_action(player_action,player_frame,'run')
       player_flip = False
    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action,player_frame,'idle')
        
    if player_movement[0] < 0:
       player_action, player_frame = change_action(player_action,player_frame,'run')
       player_flip = True
    
    
    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']== True:
        player_y_momentum = 0
        air_timer =0
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
            
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    
    display.blit(pygame.transform.flip(player_img,player_flip,False), (player_rect.x - scroll[0], player_rect.y - scroll[1]))  # render the image on the window


    # loops through every even keyboard and mouse
    for event in pygame.event.get():
        if event.type == QUIT:  #'x' is clicked on the window
            pygame.quit()
            sys.exit() # exit the program


        if event.type == KEYDOWN: # key pushed down
            if event.key ==K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_e:
                pygame.mixer.mysic.play(-1)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
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
