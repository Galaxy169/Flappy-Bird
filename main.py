import random  # For generating random numbers
import sys  # for using sys.exit to exit the game
import pygame  # Importing pygame library
from pygame.locals import *  # Basic pygame imports

# Global Variables for the game

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  # Initilize the display
img = pygame.image.load('resources/sprites/icon.png') # Load our logo image
pygame.display.set_icon(img) # Set out logo image as the icon of the game
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'resources/sprites/bird.png'
BACKGROUND = 'resources/sprites/bg.jpeg'
PIPE = 'resources/sprites/pipe.png'


def welcomeScreen():
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2
    messagex = int(SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    # Drawing Rectangle for playbutton
    playbutton = pygame.Rect(108,222,68,65)

    while True:
        for event in pygame.event.get():  # Get game event like user input

            # If user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user pressed space or up key, start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pos()[0] > playbutton[0] and pygame.mouse.get_pos()[0] < playbutton[0] + playbutton[2]:
                if pygame.mouse.get_pos()[1] > playbutton[1] and pygame.mouse.get_pos()[1] < playbutton[1] + playbutton[3]:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if playbutton.collidepoint(pygame.mouse.get_pos()):  # checking if mouse is collided with the play button

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # checking if mouse has been clicked
                    mainGame()
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                #Adding INTRO Music
                pygame.mixer.music.load('resources/AUDIO/INTROMUSIC.mp3')
                pygame.mixer.music.play()
                pygame.display.update()
                FPSCLOCK.tick(FPS)



def mainGame():

    #ADDING THE BACKGROUND MUSIC
    pygame.mixer.music.stop()
    pygame.mixer.music.load('resources/AUDIO/BGMUSIC.mp3')
    pygame.mixer.music.play()
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # My list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200+(SCREENWIDTH/2), 'y': newPipe2[0]['y']},

    ]

    # My lists of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},

    ]

    # Velocity
    pipeVelX = -4

    playerVelY = -9 # Player velocity for falling
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    # Changing bird velocity when pressing keys (flapping)
    playerFlapAccv = -8
    playerFlapped = False # It turns true when the bird if flapping

    # Game Loop
    while True:
        for event in pygame.event.get():
            # Quit game if Arrow down or Esc key is pressed
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE or event.type == KEYDOWN and event.key == K_q):
                pygame.quit() #Quit Pygamr
                sys.exit() #Quit from sys
            # Flap bird using Space and Arrow Up keys
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP or event.type == pygame.MOUSEBUTTONUP):
                if playery > 0:  # if player y is greater than 0 (bird is in the screen)
                    playerVelY = playerFlapAccv  # assign Vel y to player Accelartion
                    playerFlapped = True  # switch boolean to true as player flapped
                    GAME_SOUNDS['wing'].play()  # Player wing sound
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        # player is crashed
        if crashTest:
            return

        # Check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2 #get width of playerx
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2 # Pipes middle position
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score +=1
                print(f"Your score is {score}") # Print score to the screen
                GAME_SOUNDS['point'].play() # Play the sound

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight) # Prevent player from going below the ground

        # Moves pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # If the pipe is out of the screen then remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

            # lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery<0:
        GAME_SOUNDS['hit'].play()
        pygame.mixer.music.stop()
        gameOver()

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            pygame.mixer.music.stop()
            gameOver()

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            pygame.mixer.music.stop()
            gameOver()

    return False

def getRandomPipe():

    # Generate positions of two pipes(One bottom straight and one top rotated) for blitting on the screen
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # Upper Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe


def gameOver():
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['OVER'] = pygame.image.load('resources/SPRITES/gameover.png').convert_alpha()
    GAME_SPRITES['RETRY'] = pygame.image.load('resources/SPRITES/retry.png').convert_alpha()
    GAME_SPRITES['HOME'] = pygame.image.load('resources/SPRITES/Home.png').convert_alpha()
    SCREEN.blit(GAME_SPRITES['background'], (0, 0))
    SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
    SCREEN.blit(GAME_SPRITES['OVER'], (0, 0))
    SCREEN.blit(GAME_SPRITES['RETRY'], (30, 220))
    SCREEN.blit(GAME_SPRITES['HOME'], (30, 280))

    pygame.display.update()

    while True:
        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:
                mainGame()

            ### RETRY BUTTON
            if pygame.mouse.get_pos()[0] > 30 and pygame.mouse.get_pos()[0] < 30 + GAME_SPRITES['RETRY'].get_width():
                if pygame.mouse.get_pos()[1] > 220 and pygame.mouse.get_pos()[1] < 220 + GAME_SPRITES['RETRY'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mainGame()

            ### HOME BUTTON
            if pygame.mouse.get_pos()[0] > 30 and pygame.mouse.get_pos()[0] < 30 + GAME_SPRITES['HOME'].get_width():
                if pygame.mouse.get_pos()[1] > 280 and pygame.mouse.get_pos()[1] < 280 + GAME_SPRITES['HOME'].get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        welcomeScreen()
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

# Main point from the game will start
if __name__ == '__main__':

    pygame.init()  # Initialize all pygames modules
    FPSCLOCK = pygame.time.Clock()  # Lock the FPS
    pygame.display.set_caption('Flappy Bird By Aadil Ansari')  # Main Window Name

    # Load Numbers from 0-9
    GAME_SPRITES['numbers'] = (
        pygame.image.load('resources/SPRITES/0.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/1.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/2.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/3.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/4.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/5.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/6.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/7.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/8.png').convert_alpha(),
        pygame.image.load('resources/SPRITES/9.png').convert_alpha(),

    )

    # Load Welcome screen image
    GAME_SPRITES['message'] = pygame.image.load('resources/SPRITES/message.png').convert_alpha()

    # Load the base (ground)
    GAME_SPRITES['base'] = pygame.image.load('resources/SPRITES/base.png').convert_alpha()

    # Load the pipe
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),  # Rotate to 180, Used global var
        pygame.image.load(PIPE).convert_alpha()  # Nomal Pipe, Used global var
    )

    # Game Sound
    GAME_SOUNDS['die'] = pygame.mixer.Sound('resources/AUDIO/die.wav')  # Player Dead
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('resources/AUDIO/hit.wav')  # Player hit (collision) sound
    GAME_SOUNDS['INTROMUSIC'] = pygame.mixer.Sound('resources/AUDIO/INTROMUSIC.mp3')  # Intro
    GAME_SOUNDS['point'] = pygame.mixer.Sound('resources/AUDIO/point.wav')  # Scored a point sound
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('resources/AUDIO/swoosh.wav')  # swoosh Soinr
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('resources/AUDIO/wing.wav')  # Wings sound

    # Load the Background from global var
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()

    # Load the Player (Bird) From global var
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()  # Shows welcome screen to the user until he presses a button
        mainGame()  # This is the main game function
