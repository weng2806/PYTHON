class Colors:
    bgColor = (55, 56, 59)
    forText = (232, 152, 118)
    black = (0, 0, 0)
    white = (255, 255, 255)
    gridColor = (252, 231, 227)
    iBlock = (247, 166, 227)
    oBlock = (180, 183, 240)
    tBlock = (240, 205, 96)
    lBlock = (173, 216, 230)
    jBlock = (247, 139, 184)
    sBlock = (186, 168, 214)
    zBlock = (158, 255, 210)

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