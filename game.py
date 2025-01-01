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
# Font
#
# https://fontmeme.com/lion-king-font/#google_vignette
#
##############################################################################

import pygame
from pygame.locals import *
from UsefulClasses import spritesheet
##############################################################################
# VARIABLES
##############################################################################

APP_NAME = "Timon's Bug Game"
COPYRIGHT_MESSAGE = "Mark Reed (c) 2024"
WINDOW_TEXT = APP_NAME + " - " + COPYRIGHT_MESSAGE

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

COL_WHITE = (255,255,255)

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#surface.set_colorkey((255, 255, 255))  #White background sprites should now be transparent background!
pygame.display.set_caption(WINDOW_TEXT)

backImageName = "./images/mainBackground.jpg"
bugTossbackImageName = "./images/bugTossBackground.jpg"
alphabetImageName = "./images/Letters.png"

#sounds
pygame.mixer.init()
#clickSound = pygame.mixer.Sound("./sounds/click.mp3")
pygame.mixer.music.load("./sounds/02 - This Land.mp3") 
pygame.mixer.music.play(-1,0.0)

running = True
MAIN_MENU = 1
TOSSING_BUGS = 2
GAME_OVER = 3

gameState = MAIN_MENU

##############################################################################
# SUB PROGRAMS
##############################################################################

def LoadImages():
    global backImage,theImage,bugTossBackImage,alphabetImage,alphabet
    backImage = pygame.image.load(backImageName).convert()
    backImage = pygame.transform.scale(backImage, (600, 400))
    bugTossBackImage = pygame.image.load(bugTossbackImageName).convert()
    bugTossBackImage = pygame.transform.scale(bugTossBackImage, (600, 400))
    theImage = backImage

    alphabetSS = spritesheet(alphabetImageName)

    alphabet = []
    for j in range(4):
        for i in range(7):
            image = alphabetSS.image_at((4+i*120,4+j*100, 110, 85),colorkey=COL_WHITE)
            image = pygame.transform.scale(image, (55, 45))
            alphabet.append(image)

def HandleInput(running):

    global theImage,gameState

    if(gameState == MAIN_MENU):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE:
                        gameState = TOSSING_BUGS
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("./sounds/15 - Bonus Stage 2.mp3")
                        pygame.mixer.music.play(-1,0.0) 
                        
    elif(gameState == TOSSING_BUGS):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    print("right pressed")
                if event.key == pygame.K_LEFT:
                    print("left pressed")
                
           
    return running

def DrawMainMenu():
    surface.blit(backImage, (0, 0))
    #pygame.draw.rect(surface, COL_WHITE, pygame.Rect(145, 115, 340, 58))
    spacing = 40
    i = 0
    for letter in title:
        asciiVal = ord(letter)
        posInArray = asciiVal-65
        if(asciiVal != 32): 
            surface.blit(alphabet[posInArray], (140 + i*spacing, 213))
        i = i + 1   

def DrawGame():
    surface.blit(bugTossBackImage, (0, 0))

##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages()

title = "BUG TOSS"

#game loop
while running:
    # Using blit to copy the background grid onto the blank screen
    

    if(gameState == MAIN_MENU):
        DrawMainMenu()
    elif(gameState == TOSSING_BUGS):
        DrawGame()

    running = HandleInput(running)
    pygame.display.flip()

pygame.quit()