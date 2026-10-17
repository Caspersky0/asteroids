import sys
import pygame
from logger import log_state, log_event
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_MIN_RADIUS
from constants import LARGE_ASTEROID_POINTS, MEDIUM_ASTEROID_POINTS, SMALL_ASTEROID_POINTS
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField 
from shot import Shot
from game_over import draw_game_over

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font("assets/fonts/PressStart2P-regular.ttf", 20)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    game_over = False
    restart_rect = None
    asteroid_field = AsteroidField()

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    
    clock = pygame.time.Clock()
    dt = 0.0
   
    while True:
        dt = clock.tick(60) / 1000
        
        if not game_over:
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if player.blink_timer <= 0 and asteroid.collides_with(player):
                        log_event("player_hit")
                        player.lives -= 1
                        if player.lives <= 0:
                            game_over = True
                        print(f"Lives remaining: {player.lives}")
                        center = pygame.Vector2(
                            SCREEN_WIDTH / 2,
                            SCREEN_HEIGHT / 2
                        )
                        player.position = center

                        for nearby_asteroid in asteroids:
                            distance = nearby_asteroid.position.distance_to(center)
                            if distance < player.radius + nearby_asteroid.radius + 50:
                                nearby_asteroid.kill()

                        player.blink_timer = 2.0
                    #print(f"Game over! Final score: {player.score}")
                    #sys.exit()

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        shot.kill()
                        if asteroid.radius == ASTEROID_MIN_RADIUS:
                            player.score += SMALL_ASTEROID_POINTS
                        elif asteroid.radius == ASTEROID_MIN_RADIUS * 2:
                            player.score += MEDIUM_ASTEROID_POINTS
                        else:
                            player.score += LARGE_ASTEROID_POINTS
                        asteroid.split()
                    

            log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if (
                game_over
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):
                if quit_rect is not None and quit_rect.collidepoint(event.pos):
                    sys.exit()
                if (
                    restart_rect is not None
                    and restart_rect.collidepoint(event.pos)
                ):
                    player.score = 0
                    player.lives = 3
                    player.position = pygame.Vector2(
                        SCREEN_WIDTH / 2,
                        SCREEN_HEIGHT / 2
                    )
                    for asteroid in asteroids:
                        asteroid.kill()
                    for shot in shots:
                        shot.kill()
                    game_over = False
        screen.fill("black")
        if not game_over:
            for obj in drawable:
                obj.draw(screen)
            score_surface = font.render(f"Score: {player.score}", True, "white")
            screen.blit(score_surface, (20, 20))
            lives_surface = font.render(f"Lives: {player.lives}", True, "white")
            screen.blit(
                lives_surface,
                ((SCREEN_WIDTH - lives_surface.get_width() - 20), 20)
            )
        else:
            restart_rect, quit_rect = draw_game_over(screen, font, player.score)
        pygame.display.flip()


 

if __name__ == "__main__":
    main()
