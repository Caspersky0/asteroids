import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0
        self.score = 0
        self.blink_timer = 0
        self.blink_interval = 0.1
        self.blink_elapsed = 0
        self.is_visible = True
        self.lives = 3
    
        # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        if not self.is_visible:
            return
        pygame.draw.polygon(
            screen,
            "white",
            self.triangle(),
            LINE_WIDTH
        )
    def rotate(self, dt) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        self.cooldown_timer -= dt
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        if self.blink_timer > 0:
            self.blink_timer -= dt
            self.blink_elapsed += dt
            if self.blink_elapsed >= self.blink_interval:
                self.is_visible = not self.is_visible
                self.blink_elapsed = 0
        else:
            self.is_visible = True
            


    def move(self, dt):
        foward = pygame.Vector2(0, 1).rotate(self.rotation)
        foward *= PLAYER_SPEED * dt
        self.position += foward

    def shoot(self):
        if self.cooldown_timer > 0:
            return

        self.cooldown_timer= PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity *= PLAYER_SHOOT_SPEED
