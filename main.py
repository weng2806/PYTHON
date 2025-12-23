""" BUGS ***
 IN GAME OVER, the last block (located at the uppermost) overwrites the previous block below it  
pag sa dulo yung block, ayaw magrotate

try add on effects ***
    start menu, 
    hold piece tryy ---> hindi pa okay
    hold piece display
    sound effects (rotate, line clear, level up, game over)
"""
import pygame, sys
from game import Game
from colors import Colors

pygame.init()

# ------------------ WINDOW ------------------
WIDTH, HEIGHT = 500, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# ------------------ ASSETS ------------------
icon = pygame.image.load("Assets/tetrisLogoo.png")
pygame.display.set_icon(icon)

tetrisImage = pygame.image.load("Assets/tetrisLogoo.png")
tetrisImage = pygame.transform.scale(tetrisImage, (180, 100))

fullTetris = pygame.image.load("Assets/fullTetris.png")
fullTetris = pygame.transform.scale(fullTetris, (520, 620))

# ------------------ FONTS ------------------
title_font = pygame.font.Font(None, 30)
big_font = pygame.font.Font(None, 50)
menu_font = pygame.font.Font(None, 40)

# ------------------ UI ------------------
score_surface = title_font.render("Score", True, Colors.forText)
level_surface = title_font.render("Level", True, Colors.forText)
next_surface = title_font.render("Next", True, Colors.forText)
hold_surface = title_font.render("Hold", True, Colors.forText)
game_over_surface = title_font.render("GAME OVER", True, Colors.forText)

score_rect = pygame.Rect(395, 560, 100, 50)
level_rect = pygame.Rect(320, 560, 50, 50)
next_rect = pygame.Rect(320, 350, 170, 140)
hold_rect = pygame.Rect(320, 150, 170, 140)

# ------------------ GAME ------------------
game = Game()

# NES gravity table (milliseconds per cell)
NES_SPEED = [
    800, 710, 630, 550, 470, 380, 300, 220, 130, 100,
    90, 80, 70, 60, 50, 50, 50, 50, 50, 50
]

def get_gravity_delay():
    return NES_SPEED[min(game.level, len(NES_SPEED)-1)]

# ------------------ GRAVITY ------------------
gravity_timer = 0

# ------------------ INPUT COOLDOWNS ------------------
move_delay = 120
rotate_delay = 170
hard_drop_delay = 200

last_move_time = 0
last_rotate_time = 0
last_hard_drop_time = 0

# ------------------ START COUNTDOWN ------------------
COUNTDOWN_DURATION = 3000
start_time = None  # will be set after pressing Start

# ------------------ START MENU ------------------
def start_menu():
    start_button = pygame.Rect(50, 100, 180, 50)
    exit_button = pygame.Rect(270, 100, 180, 50)

    while True:
        screen.fill(Colors.bgColor)
        screen.blit(fullTetris, (-10,0))

        # Buttons
        pygame.draw.rect(screen, Colors.gridColor, start_button)
        pygame.draw.rect(screen, Colors.gridColor, exit_button)

        start_text = menu_font.render("Start Game", True, Colors.forText)
        exit_text = menu_font.render("Exit", True, Colors.forText)

        screen.blit(start_text, start_text.get_rect(center=start_button.center))
        screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "start"
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# ------------------ COUNTDOWN FUNCTION ------------------
def countdown_active():
    if start_time is None:
        return False
    return pygame.time.get_ticks() - start_time < COUNTDOWN_DURATION

# ------------------ DRAW HOLD PIECE CENTERED ------------------
def draw_hold_piece(screen, block, rect):
    if block is None:
        return
    # create a small surface for the hold piece
    hold_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    hold_surf.fill((0,0,0,0))
    # clone block for drawing
    temp_block = block.clone()
    # compute min/max of block cells
    positions = temp_block.get_cell_positions()
    min_col = min(c.column for c in positions)
    max_col = max(c.column for c in positions)
    min_row = min(c.row for c in positions)
    max_row = max(c.row for c in positions)
    block_width = (max_col - min_col +1) * temp_block.cell_size
    block_height = (max_row - min_row +1) * temp_block.cell_size
    # center offsets
    offset_x = (rect.width - block_width)//2 - min_col * temp_block.cell_size
    offset_y = (rect.height - block_height)//2 - min_row * temp_block.cell_size
    temp_block.draw(hold_surf, offset_x, offset_y)
    screen.blit(hold_surf, rect.topleft)

# ------------------ MAIN LOOP ------------------
menu_choice = start_menu()
if menu_choice == "start":
    start_time = pygame.time.get_ticks()  # begin countdown

while True:
    dt = clock.tick(60)
    gravity_timer += dt
    now = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    countdown = countdown_active()

    # ---------- EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ONLY ALLOW INPUT IF NOT COUNTDOWN
        if event.type == pygame.KEYDOWN and not countdown:

            if game.game_over:
                game.reset()
                gravity_timer = 0
                start_time = pygame.time.get_ticks()
                continue

            if event.key in (pygame.K_LEFT, pygame.K_a):
                game.move_left()
                last_move_time = now
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                game.move_right()
                last_move_time = now
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                game.move_down()
                game.update_score(0, 1)
                last_move_time = now
            elif event.key in (pygame.K_UP, pygame.K_w):
                if now - last_rotate_time > rotate_delay:
                    game.rotate()
                    last_rotate_time = now
            elif event.key == pygame.K_SPACE:
                if now - last_hard_drop_time > hard_drop_delay:
                    rows, points = game.hard_drop()
                    game.update_score(0, points)
                    gravity_timer = 0
                    last_hard_drop_time = now
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_c:
                game.hold()

    # ---------- LONG PRESS ----------
    if not countdown and not game.game_over:
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and now - last_move_time > move_delay:
            game.move_left()
            last_move_time = now
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and now - last_move_time > move_delay:
            game.move_right()
            last_move_time = now
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and now - last_move_time > move_delay:
            game.move_down()
            game.update_score(0, 1)
            last_move_time = now

    # ---------- GRAVITY ----------
    if not countdown and not game.game_over and gravity_timer >= get_gravity_delay():
        gravity_timer = 0
        game.move_down()

    # ---------- DRAW UI ----------
    screen.fill(Colors.bgColor)

    # Score & Level
    score_value = title_font.render(str(game.score), True, Colors.forText)
    level_value = title_font.render(str(game.level), True, Colors.forText)

    screen.blit(tetrisImage, (317, 10))
    screen.blit(score_surface, (415, 535))
    screen.blit(level_surface, (320, 535))
    screen.blit(next_surface, (385, 320))
    screen.blit(hold_surface, (385, 120))

    pygame.draw.rect(screen, Colors.gridColor, score_rect, 0, 10)
    pygame.draw.rect(screen, Colors.gridColor, level_rect, 0, 10)
    pygame.draw.rect(screen, Colors.gridColor, next_rect, 0, 10)
    pygame.draw.rect(screen, Colors.gridColor, hold_rect, 0, 10)

    screen.blit(score_value, score_value.get_rect(center=score_rect.center))
    screen.blit(level_value, level_value.get_rect(center=level_rect.center))

    # Game over text
    if game.game_over:
        screen.blit(game_over_surface, (323, 430))

    # ---------- DRAW GAME ----------
    game.draw(screen)

    # ---------- DRAW HOLD PIECE ----------
    draw_hold_piece(screen, game.hold_block, hold_rect)

    # ---------- COUNTDOWN DIM OVERLAY ----------
    if countdown:
        dim_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim_surface.fill((0, 0, 0, 150))  # black with 150 alpha
        screen.blit(dim_surface, (0, 0))

        remaining = 3 - ((pygame.time.get_ticks() - start_time) // 1000)
        if remaining > 0:
            number = big_font.render(str(remaining), True, Colors.forText)
            screen.blit(number, number.get_rect(center=(160, 310)))

    pygame.display.update()
