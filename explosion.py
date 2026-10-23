import random
import pygame

class Explosion:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.particles = []

        particle_count = random.randint(4, 8)

        for particle in range(particle_count):
            angle = random.uniform(0, 360)
            direction = pygame.Vector2(1, 0).rotate(angle)
            speed = random.uniform(60, 120)
            velocity = direction * speed
        
            particle = {
                "position": self.position.copy(),
                "velocity": velocity,
                "lifetime": random.uniform(0.15, 0.25),
            }
            self.particles.append(particle)
    
    def update(self, dt):
        for particle in self.particles:
            particle["position"] += particle["velocity"] * dt
            particle["lifetime"] -= dt
        self.particles = [
            particle
            for particle in self.particles
            if particle["lifetime"] > 0
        ]
    
    def draw(self, screen):
        for particle in self.particles:
            position = particle["position"]
            velocity = particle["velocity"]

            end_position = position - velocity.normalize() * 7

            pygame.draw.line(
                screen,
                (255, 255, 255),
                position,
                end_position,
                1,
            )