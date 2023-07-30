import math
from typing import Tuple
import pygame
from pygame._sdl2 import Renderer, Texture


from ball3d import Ball3D


class AstralBody:
    def __init__(
        self,
        renderer: Renderer,
        center: Tuple[int, int] = (0, 0),
        radius: int = 0,
        color: tuple[int, int, int] = (0, 0, 0),
        followed_body: "AstralBody" = None,
        distance_to_followed_body: int = 0,
        rotation: float = 0,
        rotation_speed: float = 0,
        name: str = "",
        texture_path: str = "planet.png",
    ) -> None:
        self.center = pygame.math.Vector2(center[0], center[1])
        self.radius = radius
        if type(color) == tuple:
            self.color = color
        else:
            self.color = pygame.color.THECOLORS[color]
        self.followed_body: AstralBody = followed_body
        self.distance_to_followed_body = distance_to_followed_body
        self.rotation = rotation  # in radians
        self.rotation_speed = rotation_speed  # in radians per seconds
        self.name = name
        self.old_center = self.center.copy()
        self.hovered = False
        self.renderer = renderer
        self.texture = Texture.from_surface(
            self.renderer, pygame.image.load(texture_path)
        )
        self.ball = Ball3D(self.radius, self.texture, center=self.center)

    def update(self, dt):
        self.rotation += self.rotation_speed * dt  # increase rotation
        self.rotation %= 2 * math.pi  # keep rotation between 0 and 2pi radians

        orbit = pygame.math.Vector2(math.cos(self.rotation), math.sin(self.rotation))
        orbit *= (
            self.distance_to_followed_body + self.followed_body.radius + self.radius
        )  # scale orbit to distance_to_followed_body

        self.old_center = self.center.copy()  # save old center

        # update center
        self.center.x = self.followed_body.center.x + orbit.x
        self.center.y = self.followed_body.center.y + orbit.y

    def check_mouse_collision(self, mouse_pos):
        if (
            self.center.x - self.radius <= mouse_pos[0] <= self.center.x + self.radius
            and self.center.y - self.radius
            <= mouse_pos[1]
            <= self.center.y + self.radius
        ):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self, dt):
        self.ball.draw(dt)

    def draw2(self, screen, line_screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)

        pygame.draw.line(
            surface=line_screen,
            color=(self.color[0]*0.9, self.color[1]*0.9, self.color[2]*0.9),
            start_pos=self.old_center,
            end_pos=self.center,
            width=max(2, int(self.radius**0.9))
        )

        if self.hovered:
            pygame.draw.circle(
                screen,
                (
                    min(255, self.color[0] ** 1.05),
                    min(255, self.color[1] ** 1.05),
                    min(255, self.color[2] ** 1.05),
                ),
                self.center,
                self.radius + 2,
                2,
            )
