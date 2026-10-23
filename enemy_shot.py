
import pygame

from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class EnemyShot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, 4)
        self.velocity = velocity
        self.lifetime = 4.0

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt

        if (
            self.lifetime <= 0
            or self.position.x < 0
            or self.position.x > SCREEN_WIDTH
            or self.position.y < 0
            or self.position.y > SCREEN_HEIGHT
        ):
            self.kill()

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 80, 100),
            (int(self.position.x), int(self.position.y)),
            self.radius,
        )
