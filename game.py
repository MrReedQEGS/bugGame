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

import pygame, random
from pygame.locals import *
from UsefulClasses import spritesheet
##############################################################################
# VARIABLES
##############################################################################

APP_NAME = "Timon's Bug Catch"
COPYRIGHT_MESSAGE = "Mark Reed (c) 2024"
WINDOW_TEXT = APP_NAME + " - " + COPYRIGHT_MESSAGE

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

COL_WHITE = (255,255,255)

title = "BUG CATCH"

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#surface.set_colorkey((255, 255, 255))  #White background sprites should now be transparent background!
pygame.display.set_caption(WINDOW_TEXT)

backImageName = "./images/mainBackground.jpg"
bugTossbackImageName = "./images/bugTossBackground.jpg"
alphabetImageName = "./images/Letters.png"
menuThingImageName = "./images/menuThing.png"
pumbaIdleImageName = "./images/pumbaIdle2.png"
pumbaEatingImageName = "./images/pumbaEating.png"
pumbaRunningImageName = "./images/pumbaRunning.png"
lionKingTitleImageName = "./images/LionKingLogo.png"
bugsImageName = "./images/bugs.png"
timonImageName = "./images/timon.png"
 
#sounds
SOUND_ON = False

GAMING_LAPTOP = 1
RPI_400 = 2

runningOn = RPI_400

PUMBA_TIMER_DELAY = 18  #150 milliseconds works on gaming laptop - 18 for Rpi 400
PUMBA_TIMER_DELAY_2 = 12 # 12 milliseconds for both laptop and rpi400
PUMBA_IDLE_DELAY = 100  # 100 works on both laptop and rpi400
TIMON_RUNNING_DELAY = 20   #20 milliseconds on both laptop and rpi400

if(runningOn == GAMING_LAPTOP):
    PUMBA_TIMER_DELAY = 150  #150 milliseconds works on gaming laptop - 25 for Rpi 400
    SOUND_ON = True

if(SOUND_ON):
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
MENU_Y_POS_1 = 320
MENU_Y_POS_2 = MENU_Y_POS_1 + 1*MENU_SPACING
menuPos = 1
menuThingYVal = MENU_Y_POS_1
menuThingDirection = 1
MENU_MAX_AMPLITUDE = 6

DELAY1 = 45



pumba_X = 200
PUMBA_Y = 300
PUMBA_MAX_SPEED = 120
pumbaSpeed = 0
pumbaIdleFrame = 0
pumbaIdleAminationDirection = 1
PUMBASPEED_CHANGE = 10
PUMBA_IDLE = 1
PUMBA_EATING = 2
PUMBA_RUNNING = 3
pumbaState = PUMBA_IDLE
pumbaEatingFrame = 0
pumbaRunningFrame = 0
FACING_RIGHT = 1
FACING_LEFT = 2
pumbaDirection = FACING_RIGHT

timonSpeed = 10
timonRunningFrame = 0
timonDirection = FACING_RIGHT
timon_X = 50
TIMON_Y = 65

#my custom events used for timers, etc.
USEREVENT = 1
TIMONCALLBACK = USEREVENT
USEREVENT = USEREVENT + 1
PUMBACALLBACK = USEREVENT
USEREVENT = USEREVENT + 1
PUMBASTOPRUNNINGCALLBACK = USEREVENT
USEREVENT = USEREVENT + 1
STARTMENUWOBBLE = USEREVENT
USEREVENT = USEREVENT + 1
PUMBA_IDLE_CALLBACK = USEREVENT
USEREVENT = USEREVENT + 1

#fonts
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 25)

startTextSurface = my_font.render("Start Game", False, (255, 255, 255))
quitTextSurface = my_font.render("Quit", False, (255, 255, 255))

##############################################################################
# SUB PROGRAMS
##############################################################################

def Timer1Callback():
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

def TimonSwapDirection():
    global timonDirection,timonSpeed

    if(timonDirection == FACING_RIGHT):
        timonDirection = FACING_LEFT
    else:
        timonDirection = FACING_RIGHT
        
    timonSpeed = -timonSpeed

def TimonRunningCallback():

    global timon_X,timonRunningFrame
    timon_X = timon_X + timonSpeed

    if(timon_X >= 540 or timon_X <= -30):
        TimonSwapDirection()
    
    timonRunningFrame = timonRunningFrame + 1
    if(timonRunningFrame == 8):
        timonRunningFrame = 0

def PumbaIdleCallback():

    global pumbaIdleFrame,pumbaIdleAminationDirection,pumbaEatingFrame,pumbaState,pumbaRunningFrame
    global pumba_X,pumbaSpeed

    if(pumbaState == PUMBA_IDLE):

        #idle animation frame 0 is sitting down so i am not using it.
        #I am going frame 1,2,3,2,1 forever...
        
        if(pumbaIdleAminationDirection == 1):
            pumbaIdleFrame = pumbaIdleFrame + 1
            if(pumbaIdleFrame == 3):
                pumbaIdleAminationDirection = -1
        else:
            pumbaIdleFrame = pumbaIdleFrame - 1
            if(pumbaIdleFrame == 0):
                pumbaIdleAminationDirection = 1
        
    elif(pumbaState == PUMBA_EATING):
        #Should play the eating animation once!
        pumbaEatingFrame = pumbaEatingFrame + 1
        if(pumbaEatingFrame > 3):
            pumbaState = PUMBA_IDLE
            pumbaIdleAminationDirection = 1
            pumbaIdleFrame = 0

def PumbaTimerCallback():

    global pumbaIdleFrame,pumbaIdleAminationDirection,pumbaEatingFrame,pumbaState,pumbaRunningFrame
    global pumba_X,pumbaSpeed

        
    if(pumbaState == PUMBA_RUNNING):
        #Should play the eating animation once!
        pumbaRunningFrame = pumbaRunningFrame + 1
        if(pumbaRunningFrame >= 10):
            pumbaRunningFrame = 0

    #move pumba - sometimes the speed is zero and he will not move
    pumba_X = pumba_X + pumbaSpeed
    #print(pumba_X,pumbaSpeed)

    if(pumba_X > SCREEN_WIDTH - 90):
        pumba_X = SCREEN_WIDTH - 90
    if(pumba_X < -25):
        pumba_X = -25


def PumbaTimerStopRunningCallback():
    #Used to stop the running pumba.  He should skid to a stop...pretty quickly.

    global pumbaSpeed

    if(pumbaState != PUMBA_RUNNING):

        #Slow pumba down
        if(pumbaSpeed < 0):
            pumbaSpeed = pumbaSpeed + PUMBASPEED_CHANGE
        
        if(pumbaSpeed > 0):
           # print("here")
            pumbaSpeed = pumbaSpeed - PUMBASPEED_CHANGE
            #pumbaSpeed = round(pumbaSpeed,0)
    
        if(pumbaSpeed < PUMBASPEED_CHANGE and pumbaSpeed > - PUMBASPEED_CHANGE):
            pumbaSpeed = 0

def LoadImages():
    global backImage,theImage,bugTossBackImage,alphabet
    global menuThingImage,pumbaIdle,pumbaEating,lionKingTitleImage,pumbaRunningLeft,pumbaRunningRight,bugs
    global timonRight,timonLeft,smallBugs

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

    pumbaIdleSS = spritesheet(pumbaIdleImageName)
    pumbaIdle = []
    for i in range(4):
            image = pumbaIdleSS.image_at((i*45,0,45,50),colorkey=COL_WHITE)
            image = pygame.transform.scale(image, (90, 100))
            pumbaIdle.append(image)

    pumbaEatingSS = spritesheet(pumbaEatingImageName)
    pumbaEating = []
    for i in range(4):
            image = pumbaEatingSS.image_at((i*45,0,45,50),colorkey=COL_WHITE)
            image = pygame.transform.scale(image, (90, 100))
            pumbaEating.append(image)

    pumbaRunningSS = spritesheet(pumbaRunningImageName)
    pumbaRunningRight = []
    pumbaRunningLeft = []
    for i in range(13):
            image = pumbaRunningSS.image_at((i*75,0,75,50),colorkey=(255,0,255))
            image = pygame.transform.scale(image, (150, 100))
            pumbaRunningRight.append(image)
            image = pygame.transform.flip(image, True, False)
            pumbaRunningLeft.append(image)

    
    menuThingImage = pygame.image.load(menuThingImageName).convert()
    menuThingImage = pygame.transform.scale(menuThingImage, (30, 30))  #change size first before doing alpha things
    menuThingImage.set_colorkey((0,0,0))
    menuThingImage.convert_alpha()

    lionKingTitleImage = pygame.image.load(lionKingTitleImageName).convert()
    lionKingTitleImage = pygame.transform.scale(lionKingTitleImage, (400, 100))  #change size first before doing alpha things
    lionKingTitleImage.set_colorkey((0,163,127))
    lionKingTitleImage.convert_alpha()

    #load the bugs from the bugs spritesheet
    bugsSS = spritesheet(bugsImageName)
    bugs = []
    smallBugs = []

    for i in range(5):
        for j in range(3):
            image = bugsSS.image_at((i*21,j*24,21,24),colorkey=(255,255,255))
            smallBugImage = pygame.transform.scale(image, (28, 32)) 
            smallBugs.append(smallBugImage)
            image = pygame.transform.scale(image, (42, 48))
            bugs.append(image)

     #load the timon spritesheet
    timonSS = spritesheet(timonImageName)
    timonRight = []
    timonLeft = []
    
    for i in range(8):
        image = timonSS.image_at((i*60,0,60,38),colorkey=(255,255,255))
        image = pygame.transform.scale(image, (120, 76))
        timonRight.append(image)
        image = pygame.transform.flip(image, True, False)
        timonLeft.append(image)       
    
def HandleInput(running):

    global theImage,gameState,menuPos,menuThingYVal,pumbaSpeed,pumbaEatingFrame,pumbaState
    global pumbaIdleFrame,pumbaDirection,pumbaRunningFrame,pumbaIdleAminationDirection,bugAboutToDrop

    if(gameState == MAIN_MENU):

        if(pygame.event.get(STARTMENUWOBBLE)):
            Timer1Callback()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_RETURN and menuPos == 1:

                        gameState = TOSSING_BUGS
                        if(SOUND_ON):
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

        keys = pygame.key.get_pressed()  # Checking pressed keys
        if keys[pygame.K_RIGHT]:
            pumbaDirection = FACING_RIGHT
            pumbaState = PUMBA_RUNNING
            if(pumbaSpeed < PUMBA_MAX_SPEED):
                pumbaSpeed = pumbaSpeed + 0.2

        if keys[pygame.K_LEFT]:
            pumbaDirection = FACING_LEFT
            pumbaState = PUMBA_RUNNING
            if(pumbaSpeed > -PUMBA_MAX_SPEED):
                pumbaSpeed = pumbaSpeed - 0.2

        if pygame.event.get(TIMONCALLBACK): # check event queue contains PLAYSOUNDEVENT 
            TimonRunningCallback()
        elif pygame.event.get(PUMBACALLBACK): # check event queue contains PLAYSOUNDEVENT 
            PumbaTimerCallback()
        elif pygame.event.get(PUMBASTOPRUNNINGCALLBACK): # check event queue contains PLAYSOUNDEVENT 
            PumbaTimerStopRunningCallback()
        elif (pygame.event.get(PUMBA_IDLE_CALLBACK)):
            PumbaIdleCallback()
    
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
           
                if event.key == pygame.K_ESCAPE:
                        gameState = MAIN_MENU
                        if(SOUND_ON):
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("./sounds/02 - This Land.mp3") 
                            pygame.mixer.music.play(-1,0.0)
                if( event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                    #reset running animation
                    pumbaRunningFrame = 0

                if(event.key == pygame.K_SPACE):
                    pumbaState = PUMBA_EATING
                    pumbaEatingFrame = 0
                    bugAboutToDrop = GetRandomBug()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    pumbaState = PUMBA_IDLE
                    pumbaEatingFrame = 0
                    pumbaRunningFrame = 0
                    pumbaIdleAminationDirection = 1
                    pumbaIdleFrame = 0
       
                
    return running

def DrawMainMenu():
    surface.blit(backImage, (0, 0))

    surface.blit(lionKingTitleImage, (110, 20))

    #pygame.draw.rect(surface, COL_WHITE, pygame.Rect(145, 115, 340, 58))
    #Write the bug toss title using the font that I loaded into alphabet
    spacing = 40
    i = 0
    for letter in title:
        asciiVal = ord(letter)
        posInArray = asciiVal-65
        if(asciiVal != 32): 
            surface.blit(alphabet[posInArray], (115 + i*spacing, 200))
        i = i + 1   

    #draw the menu and selection icon thingy
    surface.blit(menuThingImage, (220,menuThingYVal))
    surface.blit(startTextSurface, (260,MENU_Y_POS_1))
    surface.blit(quitTextSurface, (260,MENU_Y_POS_2))

    #draw the bugs around the title
    for i in range(11):
        surface.blit(bugs[i], (80 + i*40,150))
        surface.blit(bugs[i], (80 + i*40,250))

def DrawGame():
    surface.blit(bugTossBackImage, (0, 0))

    #Draw pumba in whatever state he is in!
    if(pumbaState == PUMBA_IDLE):
        surface.blit(pumbaIdle[pumbaIdleFrame], (pumba_X, PUMBA_Y))
    elif(pumbaState == PUMBA_EATING):
        surface.blit(pumbaEating[pumbaEatingFrame], (pumba_X, PUMBA_Y))
    elif(pumbaState == PUMBA_RUNNING):
        if(pumbaDirection == FACING_LEFT):
            surface.blit(pumbaRunningLeft[pumbaRunningFrame], (pumba_X, PUMBA_Y))
        else:
            surface.blit(pumbaRunningRight[pumbaRunningFrame], (pumba_X, PUMBA_Y))

    if(timonDirection == FACING_RIGHT):
        surface.blit(timonRight[timonRunningFrame], (timon_X, TIMON_Y))
    else:
        surface.blit(timonLeft[timonRunningFrame], (timon_X, TIMON_Y))
    
    #draw a random bug on timon
    if(timonDirection == FACING_RIGHT):
        surface.blit(bugAboutToDrop, (timon_X + 85, TIMON_Y-10))
    else:
        surface.blit(bugAboutToDrop, (timon_X, TIMON_Y-10))

def GetRandomBug():
    someBugImage = random.choice(smallBugs)
    return someBugImage
    
##############################################################################
# MAIN
##############################################################################
pygame.init()

pygame.time.set_timer(TIMONCALLBACK, TIMON_RUNNING_DELAY)
pygame.time.set_timer(PUMBACALLBACK, PUMBA_TIMER_DELAY)
pygame.time.set_timer(PUMBASTOPRUNNINGCALLBACK, PUMBA_TIMER_DELAY_2)
pygame.time.set_timer(STARTMENUWOBBLE, DELAY1)
pygame.time.set_timer(PUMBA_IDLE_CALLBACK, PUMBA_IDLE_DELAY)

LoadImages()

bugAboutToDrop = GetRandomBug()

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