
import pygame
import random

from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_ACCELERATION,
    PLAYER_DRAG,
    PLAYER_MAX_SPEED,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)

        self.rotation = 0
        self.cooldown_timer = 0
        self.score = 0
        self.xp = 0
        self.next_level_xp = 500
        self.level = 0
        self.upgrades = {
            "rapid_fire": 0,
            "double_shot": 0,
            "homing": 0,
            "heavy_rounds": 0,
        }
        self.level_up_pending = False
        self.blink_timer = 0
        self.blink_interval = 0.1
        self.blink_elapsed = 0
        self.is_visible = True
        self.lives = 3
        self.thrusting = False

    def add_xp(self, amount):
        self.xp += amount

        if self.xp >= self.next_level_xp:
            self.level_up_pending = True

    def choose_upgrade(self, upgrade):
        self.upgrades[upgrade] += 1
        self.level += 1
        self.next_level_xp += 3000
        self.level_up_pending = self.xp >= self.next_level_xp

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = (
            pygame.Vector2(0, 1)
            .rotate(self.rotation + 90)
            * self.radius / 1.5
        )

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def wrap_position(self):
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
            self.blink_timer = 0.8
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
            self.blink_timer = 0.8

        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
            self.blink_timer = 0.8
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
            self.blink_timer = 0.8

    def draw(self, screen):
        self.draw_engine(screen)

        if not self.is_visible:
            return

        pygame.draw.polygon(
            screen,
            "white",
            self.triangle(),
            LINE_WIDTH,
        )

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.cooldown_timer -= dt
        keys = pygame.key.get_pressed()
        self.thrusting = keys[pygame.K_w]

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.velocity -= forward * PLAYER_ACCELERATION * dt
        if keys[pygame.K_SPACE]:
            self.shoot()

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.velocity *= max(0, 1 - PLAYER_DRAG * dt)

        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

        self.position += self.velocity * dt
        self.wrap_position()

        if self.blink_timer > 0:
            self.blink_timer -= dt
            self.blink_elapsed += dt

            if self.blink_elapsed >= self.blink_interval:
                self.is_visible = not self.is_visible
                self.blink_elapsed = 0
        else:
            self.is_visible = True

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def shoot(self):
        if self.cooldown_timer > 0:
            return

        cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        if self.upgrades["rapid_fire"]:
            cooldown *= 0.7 ** self.upgrades["rapid_fire"]

        if self.upgrades["double_shot"]:
            cooldown *= 1.25 ** self.upgrades["double_shot"]

        self.cooldown_timer = cooldown

        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        if self.upgrades["double_shot"]:
            right = pygame.Vector2(0, 1).rotate(self.rotation + 90)
            offset = self.radius * 0.5

            shot1 = Shot(
                self.position.x - right.x * offset,
                self.position.y - right.y * offset,
            )
            shot2 = Shot(
                self.position.x + right.x * offset,
                self.position.y + right.y * offset,
            )

            shot1.velocity = forward * PLAYER_SHOOT_SPEED
            shot2.velocity = forward * PLAYER_SHOOT_SPEED
            shot1.homing = self.upgrades["homing"] > 0
            shot2.homing = self.upgrades["homing"] > 0
            shot1.heavy = self.upgrades["heavy_rounds"] > 0
            shot2.heavy = self.upgrades["heavy_rounds"] > 0
        else:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = forward * PLAYER_SHOOT_SPEED
            shot.homing = self.upgrades["homing"] > 0
            shot.heavy = self.upgrades["heavy_rounds"] > 0

    def draw_engine(self, screen):
        if not self.thrusting:
            return

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90)

        flame_length = random.uniform(
            self.radius * 0.8,
            self.radius * 1.5,
        )

        base_left = (
            self.position
            - forward * self.radius
            - right * self.radius / 2
        )
        base_right = (
            self.position
            - forward * self.radius
            + right * self.radius / 2
        )
        flame_tip = self.position - forward * (
            self.radius + flame_length
        )

        pygame.draw.polygon(
            screen,
            (255, 100, 20),
            [base_left, base_right, flame_tip],
        )
