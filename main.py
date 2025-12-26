"""
Author: Pamaran, Ruel Jr. P.
Date Started: November 13, 2025
Date Completed: December 25, 2025
Description: Main file to run the Tetris game.
"""

import pygame, sys
from game import Game
from colors import Colors

pygame.init()  

pygame.mixer.music.load("Sounds/starboy.ogg")
pygame.mixer.music.set_volume(0.3)

# ---- window setup --------------------------------------------------------------------------------------------
width, height = 500, 620  # window size
screen = pygame.display.set_mode((width, height))  # create main screen
pygame.display.set_caption("Monotris.")  # window title
clock = pygame.time.Clock()  # clock for fps timing



# --- assets ----------------------------------------------------------------------------------------
icon = pygame.image.load("Assets/tetrisLogoo.png")  # load icon
pygame.display.set_icon(icon)  # set window icon

tetrisImage = pygame.image.load("Assets/tetrisLogoo.png")  # main tetris image
tetrisImage = pygame.transform.scale(tetrisImage, (180, 100))  # resize it

fullTetris = pygame.image.load("Assets/fullTetris.png")  # background image
fullTetris = pygame.transform.scale(fullTetris, (520, 620))  # resize bg



# ---- fonts --------------------------------------------------------------------------------------------
bigFont = pygame.font.SysFont("gabriola", 50)  # big font for countdown numbers
menuFont = pygame.font.SysFont("gabriola", 40)  # menu font
mainFont = pygame.font.SysFont("gabriola", 30)  # main font
titleFont = pygame.font.SysFont(None, 30)  
pauseFont = pygame.font.SysFont("gabriola", 20)  # pause hint font


# ------user interface --------------------------------------------------------------------------------------
scoreSurface = mainFont.render("Score", True, Colors.white)  # score label
levelSurface = mainFont.render("Level", True, Colors.white)  # level label
nextSurface = mainFont.render("Next", True, Colors.white)  # next piece label
holdSurface = mainFont.render("Hold", True, Colors.white)  # hold label
pauseSurface = pauseFont.render("Press P for Pause", True, Colors.white)  # pause hint

scoreRect = pygame.Rect(395, 560, 100, 50)  # score box
levelRect = pygame.Rect(320, 560, 50, 50)  # level box
nextRect = pygame.Rect(320, 350, 170, 140)  # next piece box
holdRect = pygame.Rect(320, 150, 170, 140)  # hold box



# ------game class instance --------------------------------------------------------------------------------
game = Game()  # create game instance


# -----nes gravity speeds per level -----------------------------------------------------------------------
nesSpeed = [  # gravity per level (ms per drop)
    800, 710, 630, 550, 470, 380, 300, 220, 130, 100,
    90, 80, 70, 60, 50, 50, 50, 50, 50, 50
]

def getGravityDelay():  # returns delay based on current level
    return nesSpeed[min(game.level, len(nesSpeed)-1)]  # clamp to max



# ---- values for delay and movement ----------------------------------------------------------------
moveDelay = 120  # move repeat cooldown
rotateDelay = 100  # rotate repeat cooldown
hardDropDelay = 200  # hard drop cooldown

lastMoveTime = 0  # last move timestamp
lastRotateTime = 0  # last rotate timestamp
lastHardDropTime = 0  # last hard drop timestamp



# ------ timers --------------------------------------------------------------------------------------------
countdownDuration = 3000  # countdown time 3 sec
startTime = None  # when countdown started



# -----pause --------------------------------------------------------------------------------------------
paused = False  # start unpaused



# -----menu function --------------------------------------------------------------------------------------
def startMenu():  # menu function
    startButton = pygame.Rect(50, 100, 180, 50)  # start button rect
    exitButton = pygame.Rect(270, 100, 180, 50)  # exit button rect

    while True:
        screen.fill(Colors.bgColor)  # clear screen
        screen.blit(fullTetris, (-10,0))  # draw bg

        pygame.draw.rect(screen, Colors.gridColor, startButton, 0, 10)  # start box
        pygame.draw.rect(screen, Colors.gridColor, exitButton, 0, 10)  # exit box

       

        startText = menuFont.render("Start Game", True, Colors.white)  # start text
        exitText = menuFont.render("Exit", True, Colors.white)  # exit text

        startRect = startText.get_rect(center = startButton.center)
        startRect.y -= -15  #  vertical adjust
        startRect.x += 0  # horizontal adjust
        screen.blit(startText, startRect)

        exitRect = exitText.get_rect(center = exitButton.center)
        exitRect.y -= -15  #  vertical adjust
        exitRect.x += 0  # horizontal adjust
        screen.blit(exitText, exitRect)

        pygame.display.update()  # update display

        for event in pygame.event.get():  # event loop
            if event.type == pygame.QUIT:  # quit
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # click events
                if startButton.collidepoint(event.pos):  # start clicked
                    return "start"
                if exitButton.collidepoint(event.pos):  # exit clicked
                    pygame.quit()
                    sys.exit()



# --------cooldown check function -----------------------------------------------------------------------
def countdownActive():  # returns True if countdown active
    if startTime is None:  # if not started
        return False
    
    return pygame.time.get_ticks() - startTime < countdownDuration  # compare time



# ----------hold piece centered drawing function ---------------------------------------------------------------
def drawHoldPiece(screen, block, rect):  # draw hold piece in box
    if block is None:  # skip if empty
        return
    
    holdSurf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)  # transparent surf
    holdSurf.fill((0,0,0,0))  # clear surf
    
    tempBlock = block.clone()  # clone block
    positions = tempBlock.getCellPositions()  # get block tiles

    minCol = min(tile.column for tile in positions)  # leftmost col
    maxCol = max(tile.column for tile in positions)  # rightmost col

    minRow = min(tile.row for tile in positions)  # top row
    maxRow = max(tile.row for tile in positions)  # bottom row
    
    blockWidth = (maxCol - minCol + 1) * tempBlock.cellSize  # width in pixels
    blockHeight = (maxRow - minRow + 1) * tempBlock.cellSize  # height in pixels
    
    offsetX = (rect.width - blockWidth) // 2 - minCol * tempBlock.cellSize  # center x
    offsetY = (rect.height - blockHeight) // 2 - minRow * tempBlock.cellSize   # center y
    tempBlock.draw(holdSurf, offsetX, offsetY)  # draw on temp surface
    screen.blit(holdSurf, rect.topleft)  # draw to main screen



# ----------next piece centered drawing function ---------------------------------------------------------------
def drawNextPiece(screen, block, rect):  # draw the next piece inside the box
    if block is None:  # if there's no block, do nothing
        return
    surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)  # create a transparent surface for drawing
    surf.fill((0,0,0,0))  # fill surface with transparent pixels

    tempBlock = block.clone()  # clone the block so dont modify original
    positions = tempBlock.getCellPositions()  # get all cell positions of the block

    minCol = min(tile.column for tile in positions)  # find leftmost column
    maxCol = max(tile.column for tile in positions)  # find rightmost column

    minRow = min(tile.row for tile in positions)  # find topmost row
    maxRow = max(tile.row for tile in positions)  # find bottommost row
    
    blockWidth = (maxCol - minCol + 1) * tempBlock.cellSize  # calculate block width in pixels
    blockHeight = (maxRow - minRow + 1) * tempBlock.cellSize  # calculate block height in pixels
    
    offsetX = (rect.width - blockWidth) // 2 - minCol * tempBlock.cellSize  # center block horizontally
    offsetY = (rect.height - blockHeight) // 2 - minRow * tempBlock.cellSize  # center block vertically
    tempBlock.draw(surf, offsetX, offsetY)  # draw block onto temporary surface
    screen.blit(surf, rect.topleft)  # blit temporary surface onto main screen at rect position


# ----------game start ----------------------------------------------------------------------------------------
menuChoice = startMenu()                 # show the start menu and wait for player choice
if menuChoice == "start":                # only continue if player pressed start
    startTime = pygame.time.get_ticks()  # mark time for countdown start

    # hard reset audio (bulletproof)
    pygame.mixer.music.stop()            # make 100% sure bg music is not playing
    game.gameOverSound.stop()            # stop game over sound just in case

    game.reset()                         # fully reset game state (grid, blocks, score)
    gravityTimer = 0                     # reset gravity timer so block doesn't fall instantly

    gameOverSoundPlayed = False          # allow game over sound to play again
    countdownSFXPlayed = False           # allow countdown sound to play again
    countdownOver = False                # mark that countdown has not finished yet
    paused = False                       # game starts unpaused


# ----- loop --------------------------------------------------------------------------------------------
while True:
    mS = clock.tick(60)                  # lock game to 60 FPS and get elapsed ms
    gravityTimer += mS                   # add elapsed time to gravity timer
    now = pygame.time.get_ticks()        # current time for delays
    keys = pygame.key.get_pressed()      # get held keys for long press
    countdown = countdownActive()        # check if countdown is still running

    # ----- event handling --------------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # window close button
            pygame.quit()                # shut down pygame
            sys.exit()                   # exit the program completely

        if event.type == pygame.KEYDOWN: # check for key presses

            # ----pause toggle ------------------------------------------------------------------------------------
            if event.key == pygame.K_p and not countdown:   # press P to pause (not during countdown)
                paused = not paused                          # toggle pause state
                pygame.mixer.music.set_volume(0 if paused else 0.3)  # mute music when paused

            # ----kapag nirestart after game over ----------------------------------------------------------------
            if game.gameOver and not countdown:  # any key restarts after game over
                pygame.mixer.music.stop()        # stop background music
                game.gameOverSound.stop()        # stop game over sound

                game.reset()                     # reset the game
                gravityTimer = 0                 # reset gravity timer
                startTime = pygame.time.get_ticks()  # restart countdown timer

                gameOverSoundPlayed = False      # allow game over sound again
                countdownSFXPlayed = False       # allow countdown sound again
                countdownOver = False            # countdown not finished yet
                paused = False                   # unpause on restart
                continue                         # skip rest of this event

            if countdown or paused:               # block controls during countdown or pause
                continue

            # -------keyboard controls ----------------------------------------------------------------
            if event.key in (pygame.K_LEFT, pygame.K_a):   # move left
                game.moveLeft()
                lastMoveTime = now                          # save time for long press delay

            elif event.key in (pygame.K_RIGHT, pygame.K_d): # move right
                game.moveRight()
                lastMoveTime = now

            elif event.key in (pygame.K_DOWN, pygame.K_s):  # soft drop
                game.moveDown()
                game.updateScore(0, 1)                      # reward soft drop
                lastMoveTime = now

            elif event.key in (pygame.K_UP, pygame.K_w):    # rotate
                if now - lastRotateTime > rotateDelay:      # prevent fast rotation spam
                    game.rotate()
                    lastRotateTime = now

            elif event.key == pygame.K_SPACE:               # hard drop
                if now - lastHardDropTime > hardDropDelay:  # prevent spam
                    rows, points = game.hardDrop()
                    game.updateScore(0, points)             # add hard drop score
                    gravityTimer = 0                         # reset gravity
                    lastHardDropTime = now

            elif event.key in (pygame.K_LSHIFT, pygame.K_c): # hold piece
                game.hold()

    # ---- long press movement -----------------------------------------------------------------------------
    if not countdown and not game.gameOver and not paused:  # allow movement only when active
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and now - lastMoveTime > moveDelay:
            game.moveLeft()
            lastMoveTime = now

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and now - lastMoveTime > moveDelay:
            game.moveRight()
            lastMoveTime = now

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and now - lastMoveTime > moveDelay:
            game.moveDown()
            game.updateScore(0, 1)
            lastMoveTime = now

    # -----falling block gravity -----------------------------------------------------------------------------
    if not countdown and not game.gameOver and not paused and gravityTimer >= getGravityDelay():
        gravityTimer = 0                 # reset gravity timer
        game.moveDown()                  # auto drop block


    # ------- background music restart after countdown ------------------------------------------------
    if not countdown and not countdownOver and not game.gameOver:
        pygame.mixer.music.play(-1)      # loop background music forever
        countdownOver = True             # make sure this only happens once

    # ------drawing assets -----------------------------------------------------------------------------
    screen.fill(Colors.bgColor)          # clear screen
    scoreValue = titleFont.render(str(game.score), True, Colors.white)  # render score
    levelValue = titleFont.render(str(game.level), True, Colors.white)  # render level

    screen.blit(tetrisImage, (317, 10))  # draw logo
    screen.blit(scoreSurface, (415, 535))# score label
    screen.blit(levelSurface, (320, 535))# level label
    screen.blit(nextSurface, (385, 320)) # next box label
    screen.blit(holdSurface, (385, 120)) # hold box label
    screen.blit(pauseSurface, (350, 500))# pause hint

    pygame.draw.rect(screen, Colors.gridColor, scoreRect, 0, 10) # score box
    pygame.draw.rect(screen, Colors.gridColor, levelRect, 0, 10) # level box
    pygame.draw.rect(screen, Colors.gridColor, nextRect, 0, 10)  # next box
    pygame.draw.rect(screen, Colors.gridColor, holdRect, 0, 10)  # hold box

    screen.blit(scoreValue, scoreValue.get_rect(center=scoreRect.center)) # draw score
    screen.blit(levelValue, levelValue.get_rect(center=levelRect.center)) # draw level

    game.grid.draw(screen)               # draw the grid

    if not game.gameOver:
        ghost = game.getGhostPiece()     # get ghost piece position
        game.drawGhost(screen, ghost, 11, 11)  # draw ghost piece
        game.currentBlock.draw(screen, 11, 11) # draw current block

    drawHoldPiece(screen, game.holdBlock, holdRect) # draw hold piece
    drawNextPiece(screen, game.nextBlock, nextRect) # draw next piece

    # ------kapag game over ---------------------------------------------------------------------------------
    if game.gameOver:
        pygame.mixer.music.stop()        # stop bg music immediately

        dimSurface = pygame.Surface((width, height), pygame.SRCALPHA) # dim overlay
        dimSurface.fill((0, 0, 0, 150))
        screen.blit(dimSurface, (0, 0))

        font = pygame.font.SysFont("gabriola", 50)
        text = font.render("GAME OVER", True, Colors.white)
        screen.blit(text, text.get_rect(center=(250, 310)))

        font = pygame.font.SysFont("gabriola", 30)
        text = font.render("Press any key to restart.", True, Colors.white)
        screen.blit(text, text.get_rect(center=(250, 360)))

        if not gameOverSoundPlayed:
            game.gameOverSound.play()     # play game over sound once
            gameOverSoundPlayed = True


    # ------pause overlay ---------------------------------------------------------------------------------
    if paused and not countdown and not game.gameOver:
        dimSurface = pygame.Surface((width, height), pygame.SRCALPHA) # darken screen
        dimSurface.fill((0, 0, 0, 160))
        screen.blit(dimSurface, (0, 0))

        pauseTitleFont = pygame.font.SysFont("gabriola", 52, bold=True)
        pauseSubFont = pygame.font.SysFont("gabriola", 28)

        titleText = pauseTitleFont.render("PAUSED", True, Colors.white)
        hintText = pauseSubFont.render("Press P to resume", True, Colors.white)

        screen.blit(titleText, titleText.get_rect(center=(250, 300)))
        screen.blit(hintText, hintText.get_rect(center=(250, 340)))


    # --------countdown overlay ---------------------------------------------------------------------------------   
    if countdown:
        pygame.mixer.music.stop()         # force stop bg music during countdown
        countdownOver = False             # allow music to restart after countdown

        dimSurface = pygame.Surface((width, height), pygame.SRCALPHA) # dim screen
        dimSurface.fill((0, 0, 0, 150))
        screen.blit(dimSurface, (0, 0))

        remaining = 3 - ((pygame.time.get_ticks() - startTime) // 1000) # seconds left

        if not countdownSFXPlayed:
            game.countdown.play()         # play countdown sound once
            countdownSFXPlayed = True

        if remaining > 0:
            number = bigFont.render(str(remaining), True, Colors.white)
            screen.blit(number, number.get_rect(center=(250, 310)))

    pygame.display.update()               # finally update the screen
