
import math
import random
import pygame

from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from enemy_shot import EnemyShot


class UFO(CircleShape):
    def __init__(self, player):
        radius = 20

        start_x = random.choice([-radius, SCREEN_WIDTH + radius])
        start_y = random.randint(50, SCREEN_HEIGHT - 50)

        super().__init__(start_x, start_y, radius)

        self.player = player
        self.health = 5
        self.max_health = 5

        direction = 1 if start_x < 0 else -1
        self.velocity = pygame.Vector2(
            direction * 90,
            random.uniform(-20, 20),
        )

        self.shoot_timer = 1.5
        self.shoot_cooldown = 1.5

    def update(self, dt):
        self.position += self.velocity * dt

        if random.random() < 0.01:
            self.velocity.y = random.uniform(-35, 35)

        self.shoot_timer -= dt

        if self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_cooldown
            self.shoot()

        # Remove the UFO after it leaves the arena.
        if (
            self.position.x < -self.radius - 10
            or self.position.x > SCREEN_WIDTH + self.radius + 10
        ):
            self.kill()



    def shoot(self):
        # Pick a random angle between 0 and 360 degrees
        angle = random.uniform(0, 360)

        # Convert that angle into a direction
        direction = pygame.Vector2(0, 1).rotate(angle)

        # Set the projectile speed
        velocity = direction * 220

        # Create the projectile
        EnemyShot(self.position.x, self.position.y, velocity)


    def draw(self, screen):
        x = round(self.position.x)
        y = round(self.position.y)

        # Saucer body
        pygame.draw.ellipse(
            screen,
            (170, 190, 210),
            (x - 20, y - 7, 40, 16),
            2,
        )

        # Dome
        pygame.draw.arc(
            screen,
            (80, 220, 255),
            (x - 11, y - 16, 22, 20),
            0,
            math.pi,
            2,
        )

        # Glowing lights
        for offset in (-12, 0, 12):
            pygame.draw.circle(
                screen,
                (100, 255, 180),
                (x + offset, y + 5),
                2,
            )

        # Health bar
        bar_width = 44
        bar_height = 5
        bar_x = x - bar_width // 2
        bar_y = y - 25

        pygame.draw.rect(
            screen,
            (90, 30, 30),
            (bar_x, bar_y, bar_width, bar_height),
        )

        health_width = int(
            bar_width * max(0, self.health) / self.max_health
        )

        pygame.draw.rect(
            screen,
            (80, 255, 100),
            (bar_x, bar_y, health_width, bar_height),
        )
