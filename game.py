#An attempt at the megadrive lion king "Timon bug catch mini game"

#  sprites for lion king
#  https://www.spriters-resource.com/sega_genesis_32x/lionking/sheet/28938/
#
#  music for lion king
#  https://downloads.khinsider.com/game-soundtracks/album/lion-king-the-genesis
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
#  Font
#  https://fontmeme.com/lion-king-font/#google_vignette
#
##############################################################################

import pygame
from pygame.locals import *
from UsefulClasses import spritesheet,perpetualTimer
##############################################################################
# VARIABLES
##############################################################################

APP_NAME = "Timon's Bug Game"
COPYRIGHT_MESSAGE = "Mark Reed (c) 2024"
WINDOW_TEXT = APP_NAME + " - " + COPYRIGHT_MESSAGE

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

COL_WHITE = (255,255,255)

title = "BUG TOSS"

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#surface.set_colorkey((255, 255, 255))  #White background sprites should now be transparent background!
pygame.display.set_caption(WINDOW_TEXT)

backImageName = "./images/mainBackground.jpg"
bugTossbackImageName = "./images/bugTossBackground.jpg"
alphabetImageName = "./images/Letters.png"
menuThingImageName = "./images/menuThing.png"

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

MENU_SPACING = 35
MENU_Y_POS_1 = 300
MENU_Y_POS_2 = MENU_Y_POS_1 + 1*MENU_SPACING
menuPos = 1
menuThingYVal = MENU_Y_POS_1
menuThingDirection = 1
MENU_MAX_AMPLITUDE = 6

DELAY1 = 0.05
myTimer1 = None

#fonts
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 25)

startTextSurface = my_font.render("Start Game", False, (255, 255, 255))
quitTextSurface = my_font.render("Quit", False, (255, 255, 255))

##############################################################################
# SUB PROGRAMS
##############################################################################

def TurnOffTimers():
        
    global myTimer1
    if(myTimer1!=None):
        myTimer1.Stop()
        myTimer1 = None

def Timer1Callback():
    #called every 0.1 seconds
    #wobble the menu thing up and down  :)
    global menuThingDirection,menuThingYVal
    startingPos = MENU_Y_POS_1
    if(menuPos == 2):
        startingPos = MENU_Y_POS_2

    if(menuThingDirection == 1):
        menuThingYVal = menuThingYVal + 4
        if(menuThingYVal >= startingPos + MENU_MAX_AMPLITUDE):
            menuThingDirection = -1
    else:
        menuThingYVal = menuThingYVal - 4
        if(menuThingYVal <= startingPos - MENU_MAX_AMPLITUDE):
            menuThingDirection = 1


def LoadImages():
    global backImage,theImage,bugTossBackImage,alphabet
    global menuThingImage

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
    
    menuThingImage = pygame.image.load(menuThingImageName).convert()
    menuThingImage = pygame.transform.scale(menuThingImage, (30, 30))  #change size first before doing alpha things
    menuThingImage.set_colorkey((0,0,0))
    menuThingImage.convert_alpha()
    

def HandleInput(running):

    global theImage,gameState,menuPos,menuThingYVal

    if(gameState == MAIN_MENU):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_RETURN and menuPos == 1:
                        gameState = TOSSING_BUGS
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("./sounds/15 - Bonus Stage 2.mp3")
                        pygame.mixer.music.play(-1,0.0) 
                
                if event.key == pygame.K_RETURN and menuPos == 2 or event.key == pygame.K_ESCAPE:
                    #Time to quit!
                    return False
                
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            
                    if(menuPos == 1):
                        menuPos = 2
                        menuThingYVal = MENU_Y_POS_2
                    else:
                        menuPos = 1
                        menuThingYVal = MENU_Y_POS_1
                        
    elif(gameState == TOSSING_BUGS):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    print("right pressed")
                if event.key == pygame.K_LEFT:
                    print("left pressed")
                if event.key == pygame.K_ESCAPE:
                        gameState = MAIN_MENU
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("./sounds/02 - This Land.mp3") 
                        pygame.mixer.music.play(-1,0.0)
                
           
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
            surface.blit(alphabet[posInArray], (140 + i*spacing, 200))
        i = i + 1   

    #draw the menu things
    surface.blit(menuThingImage, (220,menuThingYVal))
    surface.blit(startTextSurface, (260,MENU_Y_POS_1))
    surface.blit(quitTextSurface, (260,MENU_Y_POS_2))

def DrawGame():
    surface.blit(bugTossBackImage, (0, 0))

##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages()

if(myTimer1 == None):
    myTimer1 = perpetualTimer(DELAY1,Timer1Callback)
    myTimer1.start()

#game loop
while running:
    # Using blit to copy the background grid onto the blank screen
    
    if(gameState == MAIN_MENU):
        DrawMainMenu()
    elif(gameState == TOSSING_BUGS):
        DrawGame()

    running = HandleInput(running)
    pygame.display.flip()

TurnOffTimers()

pygame.quit()