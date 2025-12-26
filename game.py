"""
Author: Pamaran, Ruel Jr. P.
Date Completed: 11/13/2025
Date Completed: 12/26/2025
Description: Core game logic for Tetris.
""" 

import random, pygame
from grid import Grid
from colors import Colors
from blocks import *


class Game:                                              # main game class
    def __init__(self):                                
        self.speed = 1.0                                 # base falling speed
        self.totalLines = 0                              # total cleared lines
        self.level = 0                                   # current level

        self.grid = Grid()                               # create game grid
        self.blocks = [                                 # bag of blocks
            iBlock(), jBlock(), lBlock(),
            oBlock(), sBlock(), tBlock(), zBlock()
        ]

        self.currentBlock = self.spawnBlock(self.getRandomBlock())  # active block
        self.nextBlock = self.getRandomBlock()            # next block preview

        self.gameOver = False                             # game over flag
        self.score = 0                                   # player score

        self.gameOverSound = pygame.mixer.Sound("Sounds/gameOver.ogg")  # load game over sound
        self.rotateSound = pygame.mixer.Sound("Sounds/rotate.ogg")  # rotate sound
        self.clearSound = pygame.mixer.Sound("Sounds/clear.ogg")    # line clear sound
        self.countdown = pygame.mixer.Sound("Sounds/countdown.ogg")   # countdown sound

        
        self.musicPlaying = False                         # music state flag
        self.holdBlock = None                             # held block
        self.canHold = True                               # hold availability

        self.lockDelay = 120                              # delay before locking
        self.lockTimer = 0                                # lock timer counter

    def spawnBlock(self, block):                          # spawns a block
        block.rowOffset = 0                               # reset vertical offset

        if block.blockId == 4:                            # if o-block
            block.columnOffset = 4                        # center block

        else: 
            block.columnOffset = 3                        # center block

        return block                                      # return the block
                        
    def updateScore(self, linesCleared, moveDownPoints):  # update scoring
        pointsTable = {1: 40, 2: 100, 3: 300, 4: 1200}    # score values
        self.score += pointsTable.get(linesCleared, 0) * (self.level + 1)  # add score
        self.score += moveDownPoints                      # add drop points

    def updateLevel(self):                                # update level
        self.level = self.totalLines // 10                # every 10 lines = level up

    def getRandomBlock(self):                             # bag randomizer
        if len(self.blocks) == 0:                         # if bag is empty
            self.blocks = [                               # refill bag
                iBlock(), jBlock(), lBlock(),
                oBlock(), sBlock(), tBlock(), zBlock()
            ]
        block = random.choice(self.blocks)                # pick random block
        self.blocks.remove(block)                         # remove from bag
        return block                                      # return block

    def moveLeft(self):                                   # move block left
        self.currentBlock.move(0, -1)                     # move left
        if not self.blockInside() or not self.blockFits():# check collision
            self.currentBlock.move(0, 1)                  # undo move

    def moveRight(self):                                  # move block right
        self.currentBlock.move(0, 1)                      # move right
        if not self.blockInside() or not self.blockFits():# check collision
            self.currentBlock.move(0, -1)                 # undo move

    def moveDown(self):                                   # soft drop
        self.currentBlock.move(1, 0)                      # move down
        if not self.blockInside() or not self.blockFits():# if collision
            self.currentBlock.move(-1, 0)                 # move back up
            now = pygame.time.get_ticks()                 # get current time
            if self.lockTimer == 0:                       # start lock timer
                self.lockTimer = now
            if now - self.lockTimer >= self.lockDelay:    # lock delay reached
                self.lockTimer = 0                        # reset timer
                self.lockBlock()                          # lock the block
                return False                              # stop falling
            return True                                   # still falling
        else:
            self.lockTimer = 0                            # reset timer
            return True                                   # valid move

    def lockBlock(self):                                  # lock block into grid
        tiles = self.currentBlock.getCellPositions()      # get block cells

        for tile in tiles:                                # check game over
            if not self.grid.isInside(tile.row, tile.column) or \
               not self.grid.isEmpty(tile.row, tile.column):
                self.gameOver = True                      # trigger game over
                return 0

        for tile in tiles:                                # write to grid
            self.grid.grid[tile.row][tile.column] = self.currentBlock.blockId

        rowsCleared = self.grid.clearFullRows()           # clear rows
        if rowsCleared > 0:                               # if rows cleared
            self.clearSound.play()                        # play sound
            self.totalLines += rowsCleared                # add to total
            self.updateScore(rowsCleared, 0)              # update score
            self.updateLevel()                            # update level

        self.currentBlock = self.spawnBlock(self.nextBlock)  # spawn next
        self.nextBlock = self.getRandomBlock()             # get new next
        self.canHold = True                                # re-enable hold
        return rowsCleared                                 # return cleared rows

    def rotate(self):                                     # rotate block
        self.currentBlock.rotate()                        # rotate
        kicks = [(0, 0), (0, -1), (0, 1), (0, -2), (0, 2)] # wall kicks
        for rowKick, colKick in kicks:                    # try kicks
            self.currentBlock.move(rowKick, colKick)      # apply kick
            if self.blockInside() and self.blockFits():   # if valid
                self.rotateSound.play()                   # play sound
                return
            self.currentBlock.move(-rowKick, -colKick)    # undo kick
        self.currentBlock.undoRotation()                  # revert rotation

    def blockFits(self):                                  # collision check
        for tile in self.currentBlock.getCellPositions(): # check each tile
            if not self.grid.isEmpty(tile.row, tile.column):
                return False
        return True

    def blockInside(self):                                # bounds check
        for tile in self.currentBlock.getCellPositions(): # check each tile
            if not self.grid.isInside(tile.row, tile.column):
                return False
        return True

    def hardDrop(self):                                   # instant drop
        movePoints = 0                                   # drop points
        while True:
            self.currentBlock.move(1, 0)                  # move down
            if not self.blockInside() or not self.blockFits():
                self.currentBlock.move(-1, 0)             # move back
                rows = self.lockBlock()                   # lock block
                return rows, movePoints
            movePoints += 1                               # add drop points

    def getGhostPiece(self):                               # ghost block logic
        ghost = self.currentBlock.clone()                 # copy block
        while ghost.validMove(1, 0, self.grid):           # move until hit
            ghost.rowOffset += 1
        return ghost

    def drawGhost(self, screen, ghost, offsetX, offsetY): # draw ghost piece
        baseColor = ghost.colors[ghost.blockId]           # ghost color
        alphaSurface = pygame.Surface(                    # transparent surface
            (ghost.cellSize, ghost.cellSize), pygame.SRCALPHA
        )
        alphaSurface.fill((*baseColor, 100))              # set transparency
        for cell in ghost.getCellPositions():             # draw each cell
            rect = pygame.Rect(
                offsetX + cell.column * ghost.cellSize,
                offsetY + cell.row * ghost.cellSize,
                ghost.cellSize - 1,
                ghost.cellSize - 1
            )
            screen.blit(alphaSurface, rect.topleft)       # draw ghost
            pygame.draw.rect(screen, baseColor, rect, 2) # outline

    def draw(self, screen):                                # draw everything
        self.grid.draw(screen)                            # draw grid
        if not self.gameOver:                             # if still playing
            ghost = self.getGhostPiece()                  # get ghost
            self.drawGhost(screen, ghost, 11, 11)         # draw ghost
            self.currentBlock.draw(screen, 11, 11)        # draw block

    def hold(self):                                       # hold block
        if not self.canHold:                              # cant hold again
            return
        if self.holdBlock is None:                        # if empty hold
            self.holdBlock = self.currentBlock            # store block
            self.currentBlock = self.spawnBlock(self.getRandomBlock()) # new block
        else:
            self.holdBlock, self.currentBlock = self.currentBlock, self.holdBlock # swap blocks
            self.currentBlock = self.spawnBlock(self.currentBlock) # respawn
        self.canHold = False                              # disable hold

    def reset(self):                                      # reset game
        self.grid.reset()                                 # clear grid
        self.blocks = [                                   # reset bag
            iBlock(), jBlock(), lBlock(),
            oBlock(), sBlock(), tBlock(), zBlock()
        ]
        self.currentBlock = self.spawnBlock(self.getRandomBlock())
        self.nextBlock = self.getRandomBlock()
        self.score = 0                                   # reset score
        self.totalLines = 0                               # reset lines
        self.level = 0        
        self.lockTimer = 0                                # reset timer

        self.gameOver = False                             # reset state
        self.holdBlock = None                             # clear hold
        self.canHold = True                               # enable hold
