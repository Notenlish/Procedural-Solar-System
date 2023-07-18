import math
from typing import Tuple
import pygame


class AstralBody:
    def __init__(
        self,
        center: Tuple[int, int],
        radius: int,
        color: tuple[int, int, int],
        followed_body: "AstralBody",
        distance_to_followed_body: int,
        rotation: float,
        rotation_speed: float,
    ) -> None:
        self.center = center
        self.radius = radius
        self.color = color
        self.followed_body: AstralBody = followed_body
        self.distance_to_followed_body = distance_to_followed_body
        self.rotation = rotation  # in radians
        self.rotation_speed = rotation_speed  # in radians per second

    def update(self, dt):
        self.rotation += self.rotation_speed * dt

        x_pos = (
            self.followed_body.center[0]
            + self.distance_to_followed_body * math.cos(self.rotation)
        )

        y_pos = (
            self.followed_body.center[1]
            + self.distance_to_followed_body * math.sin(self.rotation)
        )
        self.center = x_pos, y_pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)
