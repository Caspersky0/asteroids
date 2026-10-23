
import pygame

from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH


class Shot(CircleShape):
    target_groups = ()

    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.homing = False
        self.heavy = False

    def draw(self, screen):
        radius = self.radius * 2 if self.heavy else self.radius

        pygame.draw.circle(
            screen,
            (255, 190, 70) if self.heavy else "white",
            (round(self.position.x), round(self.position.y)),
            radius,
            LINE_WIDTH,
        )

    def update(self, dt):
        if self.homing:
            targets = []

            for group in self.target_groups:
                targets.extend(group.sprites())

            if targets:
                target = min(
                    targets,
                    key=lambda obj: self.position.distance_to(obj.position),
                )

                direction = target.position - self.position

                if direction.length_squared() > 0:
                    direction = direction.normalize()
                    speed = self.velocity.length()
                    desired_velocity = direction * speed

                    self.velocity = self.velocity.lerp(
                        desired_velocity,
                        min(3 * dt, 1),
                    )

        self.position += self.velocity * dt
