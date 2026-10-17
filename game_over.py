
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


def draw_game_over(screen, font, score):
    screen.fill("black")

    game_over_surface = font.render("GAME OVER", True, "white")
    screen.blit(
        game_over_surface,
        (
            (SCREEN_WIDTH - game_over_surface.get_width()) / 2,
            SCREEN_HEIGHT / 2 - 30,
        ),
    )

    final_score_surface = font.render(
        f"Final Score: {score}", True, "white"
    )
    screen.blit(
        final_score_surface,
        (
            (SCREEN_WIDTH - final_score_surface.get_width()) / 2,
            SCREEN_HEIGHT / 2 + 20,
        ),
    )
    # Restart buttons
    restart_text = font.render("RESTART", True, "white")
    restart_rect = restart_text.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 90)
    )
    if restart_rect.collidepoint(pygame.mouse.get_pos()):
        restart_text = font.render("RESTART", True, "lightgray")

    screen.blit(restart_text, restart_rect)

    quit_text = font.render("QUIT", True, "white")
    quit_rect = quit_text.get_rect(
        center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120)
    )
    if quit_rect.collidepoint(pygame.mouse.get_pos()):
        quit_text = font.render("QUIT", True, "lightgray")
    
    screen.blit(quit_text, quit_rect)
    return restart_rect, quit_rect
