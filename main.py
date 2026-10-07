import pygame
from logger import log_state
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    
    clock = pygame.time.Clock()
    dt = 0.0

    #updatable = pygame.sprite.Group()
    #drawable = pygame.sprite.Group()
    
    while True:
        dt = clock.tick(60) / 1000
        
        player.update(dt)

        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        player.draw(screen)
        pygame.display.flip()


 

if __name__ == "__main__":
    main()
