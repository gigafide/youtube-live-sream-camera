#IMPORT REQUIRED DEPENDENCIES
import pygame
import os
from time import sleep
import random

#SETUP ENVIRONMENT TO USE THE LCD SCREEN AND TOUCH
os.environ['SDL_FBDEV']= '/dev/fb1'
os.environ["SDL_MOUSEDEV"] = '/dev/input/touchscreen'
os.environ['SDL_MOUSEDRV'] = 'TSLIB'

#INITIALIZE PYGAME
pygame.init()

#SET A VARIABLE FOR THE LCD
lcd = pygame.display.set_mode((320,240))

#SET A VARIABLE FOR THE COLOR 'WHITE'
white = 255, 255, 255

#CREATE A FUNCTION TO GENERATE BUTTONS
def make_button(text, xpo, ypo, color):
        font=pygame.font.Font(None,24)
        label=font.render(str(text),1,(color))
        lcd.blit(label,(xpo,ypo))
        pygame.draw.rect(lcd, cream, (xpo-5,ypo-5,110,35),1)

#CREATE A FUNCTION TO GENERATE A RANDOM COLOR
def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

#FILL THE LCD BG WITH A COLOR
lcd.fill(random_color())

#DISABLE THE MOUSE VISIBILITY
pygame.mouse.set_visible(False)

#SETUP A WHILE LOOP TO DISPLAY THE GRAPHICS ON THE SCREEN
while 1:
        #GENERATE A BUTTON IN THE UPPER LEFT
        make_button("Menu item 1", 20, 20, white)
        
        #CREATE A FOR LOOP TO CHECK FOR EVENTS
        for event in pygame.event.get():
                #IF THE EVENT IS A "TOUCH" OR "MOUSE DOWN", THEN PERFORM AN ACTION
                if (event.type == pygame.MOUSEBUTTONDOWN):
                        #PRINT RESULTS TO THE TERMINAL SCREEN
                        print "screen pressed"
                        #CHANGE THE BG COLOR
                        lcd.fill(random_color())
                        #GET THE POSITION OF THE TOUCH
                        pos = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                        #PRINT THE POSITION
                        print pos
        #UPDATE THE DISPLAY
        pygame.display.update()
