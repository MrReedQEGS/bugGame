#An attempt at the megadrive lion king "Timon bug catch mini game"

# sprites for lion king
#
# https://www.spriters-resource.com/sega_genesis_32x/lionking/sheet/28938/
#
# music
#
# https://downloads.khinsider.com/game-soundtracks/album/lion-king-the-genesis
#
#  Sounds 
#  https://pixabay.com/sound-effects/search/clicks/
#
#  Music
#  https://pixabay.com/music/search/relaxing%20game%20music/
#
#  Sprite sheet
#  https://www.finalparsec.com/tools/sprite_sheet_maker
#
##############################################################################

import pygame
from pygame.locals import *

##############################################################################
# VARIABLES
##############################################################################

APP_NAME = "Timon's Bug Game"
COPYRIGHT_MESSAGE = "Mark Reed (c) 2024"
WINDOW_TEXT = APP_NAME + " - " + COPYRIGHT_MESSAGE

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#surface.set_colorkey((255, 255, 255))  #White background sprites should now be transparent background!
pygame.display.set_caption(WINDOW_TEXT)

backImageName = "./images/mainBackground.jpg"

#sounds
pygame.mixer.init()
#clickSound = pygame.mixer.Sound("./sounds/click.mp3")
pygame.mixer.music.load("./sounds/02 - This Land.mp3") 
pygame.mixer.music.play(-1,0.0)

running = True

##############################################################################
# SUB PROGRAMS
##############################################################################

def LoadImages():
    global backImage
    backImage = pygame.image.load(backImageName).convert()
    backImage = pygame.transform.scale(backImage, (600, 400))

def HandleInput(running):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
           
    return running
     
##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages()

#game loop
while running:
    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (0, 0))
    running = HandleInput(running)
    pygame.display.flip()

pygame.quit()