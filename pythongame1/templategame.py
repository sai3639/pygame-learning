
# set up game window 
import pygame, sys, os, random
clock = pygame.time.Clock()


from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initialize pygame
pygame.mixer.set_num_channels(64) # how many sounds can play at once

pygame.display.set_caption('Template game') # name of window

WINDOW_SIZE = (600,400)


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # initialize the window

display = pygame.Surface((300,200)) # surface = image


# set variables for images and sounds
grass_img =
dirt_img =
plant_img =
palnt_img.set_colorkey(

# load music to play indefinitly 

# infinite world or text file

# load animation

# collision tests

# move

# game loop
    # scroll/camera movement
    # parallax
    #tile rendering
    # velocity of player
    # jump
    # keyboard settings

# display game window/load program
