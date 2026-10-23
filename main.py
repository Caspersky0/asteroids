
import sys
import random
import pygame

from logger import log_state, log_event
from constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    ASTEROID_MIN_RADIUS,
    LARGE_ASTEROID_POINTS,
    MEDIUM_ASTEROID_POINTS,
    SMALL_ASTEROID_POINTS,
)
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from game_over import draw_game_over
from explosion import Explosion
from ufo import UFO
from enemy_shot import EnemyShot
from upgrade_menu import draw_upgrade_menu
from upgrades import get_random_upgrades


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font("assets/fonts/PressStart2P-regular.ttf", 20)

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    enemy_shots = pygame.sprite.Group()
    ufos = pygame.sprite.Group()

    # Configure sprite groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    UFO.containers = (updatable, drawable)
    EnemyShot.containers = (enemy_shots, updatable, drawable)

    # Homing shots can target asteroids and UFOs
    Shot.target_groups = (asteroids, ufos)

    # Create game objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    explosions = []
    game_over = False
    paused = False

    upgrade_choices = []
    upgrade_rects = []
    previous_level_up_pending = False

    restart_rect = None
    quit_rect = None

    ufo_spawn_timer = random.uniform(12, 20)

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000

        # Generate choices only when a new level-up begins.
        if player.level_up_pending and not upgrade_choices:
            upgrade_choices = get_random_upgrades()

        # Update gameplay only when not paused or choosing an upgrade.
        if not game_over and not paused and not player.level_up_pending:
            updatable.update(dt)

            # Spawn a UFO when none is active.
            if len(ufos) == 0:
                ufo_spawn_timer -= dt

                if ufo_spawn_timer <= 0:
                    ufos.add(UFO(player))
                    ufo_spawn_timer = random.uniform(20, 35)

            # Update and remove finished explosions.
            for explosion in explosions:
                explosion.update(dt)

            explosions = [
                explosion
                for explosion in explosions
                if explosion.particles
            ]

            # Player collides with asteroids.
            for asteroid in list(asteroids):
                if (
                    player.blink_timer <= 0
                    and asteroid.collides_with(player)
                ):
                    log_event("player_hit")
                    player.lives -= 1
                    print(f"Lives remaining: {player.lives}")

                    center = pygame.Vector2(
                        SCREEN_WIDTH / 2,
                        SCREEN_HEIGHT / 2,
                    )

                    player.position = center
                    player.velocity = pygame.Vector2(0, 0)

                    # Clear asteroids near the respawn point.
                    for nearby_asteroid in list(asteroids):
                        distance = nearby_asteroid.position.distance_to(center)

                        if distance < (
                            player.radius + nearby_asteroid.radius + 50
                        ):
                            nearby_asteroid.kill()

                    player.blink_timer = 2.0

                    if player.lives <= 0:
                        game_over = True

                    break

            # Player shots hit asteroids.
            for asteroid in list(asteroids):
                for shot in list(shots):
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        shot.kill()

                        explosions.append(
                            Explosion(
                                asteroid.position.x,
                                asteroid.position.y,
                            )
                        )

                        # Score and XP rewards.
                        if asteroid.radius == ASTEROID_MIN_RADIUS:
                            player.score += SMALL_ASTEROID_POINTS
                            player.add_xp(20)
                        elif asteroid.radius == ASTEROID_MIN_RADIUS * 2:
                            player.score += MEDIUM_ASTEROID_POINTS
                            player.add_xp(50)
                        else:
                            player.score += LARGE_ASTEROID_POINTS
                            player.add_xp(100)

                        asteroid.split()
                        break

            # Player shots hit UFOs.
            for ufo in list(ufos):
                for shot in list(shots):
                    if shot.collides_with(ufo):
                        shot.kill()
                        ufo.health -= 1

                        if ufo.health <= 0:
                            player.score += 500
                            player.add_xp(250)

                            explosions.append(
                                Explosion(
                                    ufo.position.x,
                                    ufo.position.y,
                                )
                            )

                            ufo.kill()

                        break

            # UFO shots hit the player.
            for enemy_shot in list(enemy_shots):
                if (
                    player.blink_timer <= 0
                    and enemy_shot.collides_with(player)
                ):
                    enemy_shot.kill()
                    log_event("player_hit")

                    player.lives -= 1
                    print(f"Lives remaining: {player.lives}")

                    player.position = pygame.Vector2(
                        SCREEN_WIDTH / 2,
                        SCREEN_HEIGHT / 2,
                    )
                    player.velocity = pygame.Vector2(0, 0)
                    player.blink_timer = 2.0

                    if player.lives <= 0:
                        game_over = True

                    break

            log_state()

        # Handle events. Keep the rectangles drawn during the previous frame
        # so they are still available when the user clicks.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Upgrade selection.
            if (
                player.level_up_pending
                and not game_over
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                for rect, key in upgrade_rects:
                    if rect.collidepoint(event.pos):
                        player.choose_upgrade(key)
                        upgrade_choices = []
                        break

            # Manual pause.
            if (
                event.type == pygame.KEYDOWN
                and not game_over
                and not player.level_up_pending
                and event.key == pygame.K_p
            ):
                paused = not paused

            # Game-over buttons.
            if (
                game_over
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                # Quit button.
                if (
                    quit_rect is not None
                    and quit_rect.collidepoint(event.pos)
                ):
                    sys.exit()

                # Restart button.
                if (
                    restart_rect is not None
                    and restart_rect.collidepoint(event.pos)
                ):
                    player.score = 0
                    player.xp = 0
                    player.next_level_xp = 3000
                    player.level = 0
                    player.level_up_pending = False

                    for key in player.upgrades:
                        player.upgrades[key] = 0

                    player.lives = 3
                    player.position = pygame.Vector2(
                        SCREEN_WIDTH / 2,
                        SCREEN_HEIGHT / 2,
                    )
                    player.velocity = pygame.Vector2(0, 0)
                    player.rotation = 0
                    player.cooldown_timer = 0
                    player.blink_timer = 0
                    player.blink_elapsed = 0
                    player.is_visible = True
                    player.thrusting = False

                    # Remove objects from the previous run.
                    for asteroid in list(asteroids):
                        asteroid.kill()

                    for shot in list(shots):
                        shot.kill()

                    for ufo in list(ufos):
                        ufo.kill()

                    for enemy_shot in list(enemy_shots):
                        enemy_shot.kill()

                    explosions.clear()
                    upgrade_choices = []
                    upgrade_rects = []
                    previous_level_up_pending = False
                    paused = False

                    # Reset UFO spawn countdown.
                    ufo_spawn_timer = random.uniform(12, 20)
                    game_over = False

        # Draw everything.
        screen.fill("black")

        if not game_over:
            for obj in drawable:
                obj.draw(screen)

            for explosion in explosions:
                explosion.draw(screen)

            # Score.
            score_surface = font.render(
                f"Score: {player.score}",
                True,
                "white",
            )
            screen.blit(score_surface, (20, 20))

            # XP.
            xp_surface = font.render(
                f"XP: {player.xp}/{player.next_level_xp}",
                True,
                (100, 220, 255),
            )
            screen.blit(xp_surface, (20, 55))

            # Lives.
            lives_surface = font.render(
                f"Lives: {player.lives}",
                True,
                "white",
            )
            screen.blit(
                lives_surface,
                (SCREEN_WIDTH - lives_surface.get_width() - 20, 20),
            )

        else:
            restart_rect, quit_rect = draw_game_over(
                screen,
                font,
                player.score,
            )

        # Pause overlay.
        if paused and not game_over and not player.level_up_pending:
            overlay = pygame.Surface(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                pygame.SRCALPHA,
            )
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))

            pause_font = pygame.font.Font(
                "assets/fonts/PressStart2P-regular.ttf",
                32,
            )
            pause_text = pause_font.render("PAUSED", True, "white")
            pause_rect = pause_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )
            screen.blit(pause_text, pause_rect)

        # Level-up overlay. Choices stay fixed until the menu closes.
        if player.level_up_pending and not game_over:
            upgrade_rects = draw_upgrade_menu(
                screen,
                font,
                upgrade_choices,
            )
        else:
            upgrade_rects = []

        # Remember the level-up state for the next frame.
        previous_level_up_pending = player.level_up_pending

        pygame.display.flip()


if __name__ == "__main__":
    main()
