import pygame
import random
from logger import log_state, log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.shape = self.generate_shape()

    def generate_shape(self):
        points = []
        point_count = 10

        for i in range(point_count):
            angle = i * 360 / point_count

            random_radius = self.radius * random.uniform(0.8, 1.2)

            point = pygame.Vector2(0, 1).rotate(angle)
            point *= random_radius

            points.append(point)
        return points

    def draw(self, screen: pygame.Surface) -> None:
        points = [
            self.position + point
            for point in self.shape
        ]

        pygame.draw.polygon(
            screen,
            "white",
            points,
            2,
        )

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()     #destroys the asteroid
        if self.radius <= ASTEROID_MIN_RADIUS:
            return      #This destroys the small asteroid and keeps it without splitting
        else:
            log_event("asteroid_split")     #here goes splitting
            angle = random.uniform(20, 50)  #randoming and assigning angles
            new_velocity_first_asteroid = self.velocity.rotate(angle)
            new_velocity_second_asteroid = self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS  #making new radius (to asteroids to become for size smaller)
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = new_velocity_first_asteroid * 1.2      #assigning the new speed
            asteroid2.velocity = new_velocity_second_asteroid * 1.2




