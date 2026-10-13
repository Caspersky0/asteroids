import pygame
import random
from logger import log_state, log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
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




