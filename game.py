import random, pygame
from grid import Grid
from colors import Colors
from blocks import *



class Game:
    def __init__(self):
        self.speed = 1.0                  # fall speed multiplier (not used directly)
        self.total_lines = 0              # total lines cleared (unified)
        self.level = 0                    # NES-style level
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")

        pygame.mixer.music.load("Sounds/starboy.ogg")
        pygame.mixer.music.play(10) # loop 10 times
        
        # lock delay: small grace period before a colliding piece locks (ms)
        self.lock_delay = 120
        self.lock_timer = 0

      

    # --------------------------------------------------------
    # NES SCORING TABLE
    # 1 line = 40 × (level + 1)
    # 2 lines = 100 × (level + 1)
    # 3 lines = 300 × (level + 1)
    # 4 lines = 1200 × (level + 1)
    # --------------------------------------------------------

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 40 * (self.level + 1)
        elif lines_cleared == 2:
            self.score += 100 * (self.level + 1)
        elif lines_cleared == 3:
            self.score += 300 * (self.level + 1)
        elif lines_cleared == 4:
            self.score += 1200 * (self.level + 1)

        # soft drop / hard drop points
        self.score += move_down_points

    def update_level(self):
        # Increase level every 10 total lines tulad sa NES.
        self.level = self.total_lines // 10

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        """
        called sa auto-fall or soft-drop.
        
           returns: True  -> piece is still active (moved or in lock delay)
           returns: False -> piece was locked (and spawn/clear happened)
        
            difference: if locking happens, lock_block() is executed and it updates
            self.total_lines and self.level.
        """
        self.current_block.move(1, 0)

        if not self.block_inside() or not self.block_fits():
            # collision: move back up
            self.current_block.move(-1, 0)

            now = pygame.time.get_ticks()
            if self.lock_timer == 0:
                self.lock_timer = now

            # wait lock_delay ms before actually locking (allows rotation/kicking)
            if now - self.lock_timer >= self.lock_delay:
                self.lock_timer = 0
                self.lock_block()
                return False      # locked
            # still in lock delay window; treat as "active" (not locked yet)
            return True
        else:
            # successful move down — reset lock timer
            self.lock_timer = 0
            return True

    def lock_block(self):
        # nilolock yung piece sa grid, clears rows, spawns next piece. nirereturn yung number of cleared rows.
        
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id

        # clear rows first (count how many)
        rows_cleared = self.grid.clear_full_rows()

        if rows_cleared > 0:
            self.clear_sound.play()
            # update totals & score
            self.total_lines += rows_cleared
            self.update_score(rows_cleared, 0)
            self.update_level()

        # check game over with the current locked grid (if next block doesn't fit in spawn pos)
        # spawn next piece only if game is not over
        self.current_block = self.next_block
        self.next_block = self.get_random_block()

        if not self.block_fits():
            self.game_over = True

        return rows_cleared

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()

        self.score = 0
        self.total_lines = 0
        self.level = 0
        self.game_over = False
        self.lock_timer = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)

    # --- Draw Ghost FIRST ---
        ghost = self.get_ghost_piece()
        self.draw_ghost(screen, ghost, 11, 11)

    # --- Then draw actual falling piece ---
        self.current_block.draw(screen, 11, 11)

    # Next piece preview
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 400)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 390)
        else:
            self.next_block.draw(screen, 270, 390)

    def hard_drop(self):
        """
        agad maglolock (bypass lock delay).
        return tuple: (rows_cleared, move_down_points)
        move_down_points is number of soft/hard-drop points earned during the hard drop.
        """
        move_points = 0
        while True:
            self.current_block.move(1, 0)
            if not self.block_inside() or not self.block_fits():
                # step back and lock immediately
                self.current_block.move(-1, 0)
                rows = self.lock_block()
                return rows, move_points
            # piece moved down one cell
            move_points += 1 # isa lang bakit sugapa ah eme

    def draw_ghost(self, screen, ghost, offset_x, offset_y):
        # Use the same exact color as the real block
        base_color = ghost.colors[ghost.id]

    # Create a transparent surface for ghost cells
        alpha_surface = pygame.Surface((ghost.cell_size, ghost.cell_size), pygame.SRCALPHA)
        alpha_surface.fill((*base_color, 100))  # 100 = opacity (0–255)

        for cell in ghost.get_cell_positions():
            rect = pygame.Rect(
                offset_x + cell.column * ghost.cell_size,
                offset_y + cell.row * ghost.cell_size,
                ghost.cell_size - 1,
                ghost.cell_size - 1
            )

        # Draw filled transparent block
            screen.blit(alpha_surface, rect.topleft)

        # Optional: draw faint outline using same color
            pygame.draw.rect(screen, base_color, rect, 2)

    def get_ghost_piece(self):
        ghost = self.current_block.clone()

    # Move down until next step would collide
        while ghost.valid_move(1, 0, self.grid):
            ghost.row_offset += 1

        return ghost