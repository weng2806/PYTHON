""" BUGS ***
 IN GAME OVER, the last block overwrites the previous block below it  
 the block is not speeding as level increases, my level is based on total lines cleared 
 
270, 390
 new updates/ bugs ***
    OPTIONAL ---> SCORE FOR SOFT DROP -> fixed (1 point per cell)
    level display not increasing properly based on lines cleared 
    pag sa dulo yung block, ayaw magrotate
    IN GAME OVER, the last block overwrites the previous block below it  
    in game over, add a restart prompt  

try add on effects ***
    ghost piece para makita kung saan lalapag yung block ---> okay na
    hold piece tryy ---> hindi pa okay

"""


import pygame, sys
from game import Game
from colors import Colors

pygame.init() 

#icon
newIcon = pygame.image.load('Assets/tetrisLogoo.png', )
pygame.display.set_icon(newIcon)

#image
tetrisImage = pygame.image.load("Assets/tetrisLogoo.png")
tetrisImage = pygame.transform.scale(tetrisImage, (180, 100))

#fonts
title_font = pygame.font.Font(None, 30) 
big_font = pygame.font.Font(None, 50) 

score_surface = title_font.render("Score", True, Colors.forText)
hold_surface = title_font.render("Hold", True, Colors.forText)
next_surface = title_font.render("Next", True, Colors.forText)
level_surface = title_font.render("Level", True, Colors.forText)  

game_over_surface = title_font.render("GAME OVER", True, Colors.forText)

score_rect = pygame.Rect(395, 560, 100, 50)
level_rect = pygame.Rect(320, 560, 50, 50)

next_rect = pygame.Rect(320, 350, 170, 140)
hold_rect = pygame.Rect(320, 150, 170, 140)



screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("tetris.")

clock = pygame.time.Clock()
game = Game()

# nes based speed table, recommended ng google (milliseconds)
NES_SPEED = [
    800, 710, 630, 550, 470, 380, 300, 220, 130, 100,
    90, 80, 70, 60, 50, 50, 50, 50, 50, 50
]

# track totals for display/speed sync in main loop
total_lines_cleared = 0
level = 0

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, NES_SPEED[level])

def update_fall_speed():
        # Update speed based on current level.
    speed = NES_SPEED[min(level, len(NES_SPEED)-1)]
    pygame.time.set_timer(GAME_UPDATE, speed)

def get_ghost_piece(block, grid):
    ghost = block.clone()

    while ghost.valid_move(1, 0, grid):
        ghost.move(1, 0)

    return ghost

# ---- COOLDOWNS ----
move_delay = 120
rotate_delay = 170
hard_drop_delay = 200

last_move_time = 0
last_rotate_time = 0
last_hard_drop_time = 0

# ---- 3 SECOND START COUNTDOWN ----
start_time = pygame.time.get_ticks()
COUNTDOWN_DURATION = 3000  # 3 seconds

def countdown_active():
    now = pygame.time.get_ticks()
    return (now - start_time) < COUNTDOWN_DURATION


def draw_countdown_overlay():
    """Draw the countdown number over the current game state."""
    now = pygame.time.get_ticks()
    remaining = 3 - ((now - start_time) // 1000)
    if remaining > 0:
        screen.fill(Colors.bgColor)

        score_value_surface = title_font.render(str(game.score), True, Colors.forText)
        level_value_surface = title_font.render(str(level), True, Colors.forText)

        screen.blit(hold_surface, (385, 120))
        screen.blit(next_surface, (385, 320))

        screen.blit(tetrisImage, (317, 10))
        screen.blit(score_surface, (415, 535))
        screen.blit(level_surface, (320, 535))

        pygame.draw.rect(screen, Colors.gridColor, score_rect, 0, 10)
        pygame.draw.rect(screen, Colors.gridColor, next_rect, 0, 10)
        pygame.draw.rect(screen, Colors.gridColor, hold_rect, 0, 10)
        pygame.draw.rect(screen, Colors.gridColor, level_rect, 0, 10)

        screen.blit(score_value_surface, score_value_surface.get_rect(center=score_rect.center))
        screen.blit(level_value_surface, level_value_surface.get_rect(center=level_rect.center))

        game.draw(screen)

        number = big_font.render(str(remaining), True, Colors.forText)
        rect = number.get_rect(center=(160, 310))
        screen.blit(number, rect)

        pygame.display.update()
        return True
    return False


while True:
    # ------------------ COUNTDOWN ------------------
    if countdown_active():
        draw_countdown_overlay()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)
        continue

    # ------------------ NORMAL GAME LOGIC ------------------
    keys = pygame.key.get_pressed()
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------- SINGLE TAP INPUT ----------
        if event.type == pygame.KEYDOWN:

            if game.game_over:
                game.game_over = False
                game.reset()
                total_lines_cleared = 0
                level = 0
                update_fall_speed()
                start_time = pygame.time.get_ticks()
                continue

            if not game.game_over:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.move_left()
                    last_move_time = now
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.move_right()
                    last_move_time = now
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    moved = game.move_down()
                    # soft drop gives 1 point per cell moved; only award if it actually moved
                    # move_down returns True both when moved and while in lock-delay; this is fine for soft-drop scoring
                    game.update_score(0, 1)
                    last_move_time = now

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if now - last_rotate_time > rotate_delay:
                        game.rotate()
                        last_rotate_time = now

                if event.key == pygame.K_SPACE:
                    # hard drop, lock agad
                    if now - last_hard_drop_time > hard_drop_delay:
                        rows, points = game.hard_drop()
                        # score the points and (rows) nasa lock_block under ng update_score for cleared lines
                        # ang atake, hard drop, points is 1 point per cell dropped
                        game.update_score(0, points)
                        last_hard_drop_time = now

        # AUTO FALL
        if event.type == GAME_UPDATE and not game.game_over:
            before_score = game.score
            before_total_lines = game.total_lines

            moved = game.move_down()

            # if move_down returned False -> the piece actually locked this tick
            if not moved:
                # game.total_lines has been updated inside lock_block()
                if game.total_lines != before_total_lines:
                    total_lines_cleared = game.total_lines
                    level = game.level
                    update_fall_speed()
                else:
                    # still update level fallback
                    level = game.level

    # ---------- LONG PRESS INPUT ----------
    if not game.game_over:
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
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and now - last_rotate_time > rotate_delay:
            game.rotate()
            last_rotate_time = now

    # ---------- DRAWING ----------
    score_value_surface = title_font.render(str(game.score), True, Colors.forText)
    level_value_surface = title_font.render(str(level), True, Colors.forText)

    screen.fill(Colors.bgColor)
    screen.blit(tetrisImage, (317, 10))
    screen.blit(score_surface, (415, 535))
    screen.blit(next_surface, (385, 320))
    screen.blit(hold_surface, (385, 120))
    screen.blit(level_surface, (320, 535))


    if game.game_over:
        screen.blit(game_over_surface, (323, 430))
        
    pygame.draw.rect(screen, Colors.gridColor, score_rect, 0, 10)
    pygame.draw.rect(screen, Colors.gridColor, next_rect, 0, 10)
    pygame.draw.rect(screen, Colors.gridColor, hold_rect, 0, 10)
    pygame.draw.rect(screen, Colors.gridColor, level_rect, 0, 10)

    screen.blit(score_value_surface, score_value_surface.get_rect(center=score_rect.center))
    screen.blit(level_value_surface, level_value_surface.get_rect(center=level_rect.center))

    if not game.game_over:
        ghost = game.get_ghost_piece()
        game.draw_ghost(screen, ghost, 11, 11)
        
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)