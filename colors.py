"""
Author: Pamaran, Ruel Jr. P.
Date Completed: 11/13/2025
Date Completed: 12/26/2025
Description: Color definitions for Tetris blocks and UI elements.
""" 

class Colors:                                   # class that stores all colors
    ghostColor = (255, 0, 0)                   # color for ghost piece
    bgColor = (28, 28, 28)                     # background color
    black = (0, 0, 0)                          # black color
    white = (255, 255, 255)                    # white color
    gridColor = (46, 46, 46)                   # color of the grid lines

    lBlock = (160, 160, 160)                   # color for l block
    jBlock = (192, 192, 192)                   # color for j block
    iBlock = (107, 107, 107)                   # color for i block
    oBlock = (129, 129, 129)                   # color for o block
    sBlock = (151, 151, 151)                   # color for s block
    tBlock = (173, 173, 173)                   # color for t block
    zBlock = (195, 195, 195)                   # color for z block

    @staticmethod                              # method that doesnt need an object
    def getCellColors():                       # returns all block colors
        return {                               # dictionary of block colors
            0: Colors.gridColor,               # empty grid cell color
            1: Colors.lBlock,                  # l block color
            2: Colors.jBlock,                  # j block color
            3: Colors.iBlock,                  # i block color
            4: Colors.oBlock,                  # o block color
            5: Colors.sBlock,                  # s block color
            6: Colors.tBlock,                  # t block color
            7: Colors.zBlock                   # z block color
        }
