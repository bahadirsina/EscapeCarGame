import pygame, random, sys
from pygame.locals import *

"""
 * @file : escapeCar
 * @description : Don't hit the oncoming vehicles and increase your score.
 * @assignment : Final project
 * @date :  25.05.2022 - 12.00 PM
 * @author Bahadır Sina TERZİOĞLU, Mustafa DEVECİ 
"""
WINDOWWIDTH = 500
WINDOWHEIGHT = 800
TEXTCOLOR = (255, 195, 0)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
CARSIZE = 50
ADDNEWCARRATE = 40 # new vehicle spawn rate
PLAYERSENSITIVITY = 6

def finishGame():
    pygame.quit()
    sys.exit()

def startGame():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: # This part ends the game when we press the close button of the window with the mouse.
                finishGame()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # This code allows the keyboard to close the game with the esc key.
                    finishGame()
                return

def playerHasHitCars(player_rect, cars):
    for b in cars:
        if player_rect.colliderect(b['rect']): #Required function for crash(.colliderect)
            return True
    return False

def drawText(text, font, surface, x, y): # Function required to write on the screen
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

pygame.init()
mainClock = pygame.time.Clock() # Time object defined for FPS value.
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # Initializes the window for viewing.
pygame.display.set_caption('ESCAPE CAR')
pygame.mouse.set_visible(False) # Thanks to this function, the mouse does not appear on the screen.
font = pygame.font.SysFont(None, 48)
background = pygame.image.load('Road.png')
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')
playerImage = pygame.image.load('MiniFrog.png')
player_rect = playerImage.get_rect() #Each Surface object basically occupies a rectangular area, although not in appearance.
# The get_rect() method returns a Rect object that specifies the location and size of the Surface object on the screen.
carImage = pygame.image.load('newCar1.png')
carImage2 = pygame.image.load('newCar2.png')
carImage3 = pygame.image.load('newCar3.png')
drawText('ESCAPE CAR', font, windowSurface, (WINDOWWIDTH / 3 - 30), (WINDOWHEIGHT / 3 + 10))
drawText('Press any key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 90, (WINDOWHEIGHT / 3) + 50)
pygame.display.update() # Updates the changes within the screen.
startGame()
topScore = 0
while True:
    cars = []
    score = 0
    player_rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50) # Sets the player's starting place.
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCars = slowDownCars = False
    carAddCounter = 0
    pygame.mixer.music.play(-1, 0.0) # Makes the background music start playing.
    while True: # The game loop is started and this loop runs continuously.
        if reverseCars and score >= 0: # With the Reversecars feature, the score starts to decrease.
            score -= 1
        elif slowDownCars and score >= 0: # With the SlowDownCars feature, the score remains constant.
            score = score
        else:
            score += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                finishGame()
            if event.type == KEYDOWN: # As long as we keep the keys pressed, the following events will work.
                if event.key == ord('z'):
                    reverseCars = True
                if event.key == ord('x'):
                    slowDownCars = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:  # As soon as we take our hands off the keys, the following events will run.
                if event.key == ord('z'):
                    reverseCars = False
                if event.key == ord('x'):
                    slowDownCars = False
                if event.key == K_ESCAPE: # It provides fast exit while playing games with ESC.
                    finishGame()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
        if not reverseCars and not slowDownCars:
            carAddCounter += 1
        if carAddCounter == ADDNEWCARRATE:
            carAddCounter = 0
            carType = random.randint(0, 2)
            # The vehicles are added to the screen.
            surface = pygame.transform.scale(carImage, (70, 120))
            if carType == 1:
                surface = pygame.transform.scale(carImage2, (70, 120))
            if carType == 2:
                surface = pygame.transform.scale(carImage3, (70, 120))
            speed = 0
            # Vehicle speed and spawn speed have been increased according to the score.
            if 0 <= score <= 400:
                speed = 3
                ADDNEWCARRATE = 40
            elif 400 < score <= 1000:
                speed = 5
                ADDNEWCARRATE = 30
            elif 1000 < score <= 2000:
                speed = 7
                ADDNEWCARRATE = 20
            else:
                speed = 10
                ADDNEWCARRATE = 15
            newCar = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-50), 0 - CARSIZE, 70, 120),
                        'speed': speed,
                        'surface': surface
                        }
            cars.append(newCar)
            # The code that allows the player to be moved.
        if moveLeft and player_rect.left > 0:
            player_rect.move_ip(-1 * PLAYERSENSITIVITY, 0)
        if moveRight and player_rect.right < WINDOWWIDTH:
            player_rect.move_ip(PLAYERSENSITIVITY, 0)
        if moveUp and player_rect.top > 0:
            player_rect.move_ip(0, -1 * PLAYERSENSITIVITY)
        if moveDown and player_rect.bottom < WINDOWHEIGHT:
            player_rect.move_ip(0, PLAYERSENSITIVITY)
        # Required code for vehicles to move downwards.
        for b in cars:
            if not reverseCars and not slowDownCars:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCars:
                b['rect'].move_ip(0, -5)  # It was possible to go backwards at 5 speeds.
            elif slowDownCars:
                b['rect'].move_ip(0, 1)   # Vehicles are slowed down by bringing 1 speed.
        for b in cars[:]:
            if b['rect'].top > WINDOWHEIGHT:  # Vehicles are deleted when they go out of the window.
                cars.remove(b)
        windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(background,(0,0))
        if score >= 0:
            drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        else:
            drawText('Score: 0', font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        windowSurface.blit(playerImage, player_rect) # Adds the player to the screen.
        for b in cars:
            windowSurface.blit(b['surface'], b['rect']) # Add cars to the screen.
        pygame.display.update()
        if playerHasHitCars(player_rect, cars): # The new Topscore value is obtained by comparing the score with the topscore when the player hits the car.
            if score > topScore:
                topScore = score
            break
        mainClock.tick(FPS) # The program runs as much as the FPS value per second. This makes the game fluid.
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3 - 20), (WINDOWHEIGHT / 3 + 10))
    drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 110, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    startGame()
    gameOverSound.stop()


