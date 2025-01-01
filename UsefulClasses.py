import pygame

# This class can be used to make a call back function that runs at any time interval
# Perfect for game time, etc.  Just set the "timeBetweenCallbacks" to 1 for a 1 second timer!
from threading import Timer,Thread,Event
class perpetualTimer():

   def __init__(self,timeBetweenCallbacks,hFunction):
      self.timeBetweenCallbacks=timeBetweenCallbacks
      self.hFunction = hFunction
      self.thread = Timer(self.timeBetweenCallbacks,self.handle_function)
      self.running = True

   def Stop(self):
      self.running = False

   def handle_function(self):
      self.hFunction()
      #The timer carrys on each time because it makes a new one each time in the handling function.
      #Stop the timer just don't make the new timer!!!
      if(self.running == True):
        self.thread = Timer(self.timeBetweenCallbacks,self.handle_function)
        self.thread.daemon = True 
        self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

class spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
        
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

#Like the class above, but will only call the callback function one time before the thread dies.
class DelayedFunctionCall():

   def __init__(self,timeBetweenCallbacks,hFunction):
      self.timeBetweenCallbacks=timeBetweenCallbacks
      self.hFunction = hFunction
      self.thread = Timer(self.timeBetweenCallbacks,self.handle_function)

   def handle_function(self):
      self.hFunction()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

#Clickable image button class with callback function

class MyClickableImageButton:
    def __init__(self, x, y, newImage,newGreyImg,newParentSurface,theNewCallback):
        self.img=newImage
        self.greyImg = newGreyImg
        self.rect=self.img.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False
        self.parentSurface=newParentSurface
        self.theCallback = theNewCallback

    def DrawSelf(self):
        #The button will be grey until the mouse hovers over it!
        self.parentSurface.blit(self.greyImg, (self.rect.x, self.rect.y))
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked=True
                self.theCallback()
            if not pygame.mouse.get_pressed()[0]:
                self.clicked=False
                self.parentSurface.blit(self.img, (self.rect.x, self.rect.y))        