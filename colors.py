class Colors:
    ghostColor = (255, 0, 0)
    bgColor = (28, 28, 28)
    forText = (255, 255, 255)
    black = (0, 0, 0)
    white = (255, 255, 255)
    gridColor = (46, 46, 46)

    lBlock = (160, 160, 160)
    jBlock = (192, 192, 192)
    iBlock = (107, 107, 107)
    oBlock = (129, 129, 129)
    sBlock = (151, 151, 151)
    tBlock = (173, 173, 173)
    zBlock = (195, 195, 195)

    @staticmethod
    def get_cell_colors():
        return {
            0: Colors.gridColor,
            1: Colors.lBlock,
            2: Colors.jBlock,
            3: Colors.iBlock,
            4: Colors.oBlock,
            5: Colors.sBlock,
            6: Colors.tBlock,
            7: Colors.zBlock
        }