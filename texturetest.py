import pygame
import random
from pygame._sdl2 import Renderer, Texture, Window
import pygame._sdl2 as _sdl2
import math

WIDTH = 600
HEIGHT = 600


class Point3D:
    def __init__(
        self, center: pygame.math.Vector2, x_index, y_index, width, height
    ) -> None:
        self.center = center
        self.x_index = x_index
        self.y_index = y_index
        self.uv = [self.x_index / width, self.y_index / height]

    def __repr__(self) -> str:
        return f"<Point3D {self.center} indexes:[{self.x_index}, {self.y_index}] UV:{self.uv}>"


class Map:
    def __init__(self, texture: Texture) -> None:
        self.width = 10
        self.height = 20
        self.step_amount = 25
        self.texture = texture
        self.setup_points()
        self.center = pygame.math.Vector2(WIDTH / 2 - 100, HEIGHT / 2 - 200)

    def setup_points(self):
        self._slices: list[list[Point3D]] = []
        for x in range(self.width):
            _slice = []
            for y in range(self.height):
                point = Point3D(
                    pygame.Vector2(x * self.step_amount, y * self.step_amount),
                    x_index=x,
                    y_index=y,
                    width=self.width,
                    height=self.height,
                )
                _slice.append(point)
            self._slices.append(_slice)

    def draw(self):
        for x in range(len(self._slices)):
            _slice = self._slices[x]  # right side
            _slice2 = self._get_item(
                _list=self._slices, i=x + 1, fallback_i=x
            )  # left side

            for y in range(len(_slice)):
                top_right = _slice[y]
                bottom_right = self._get_item(_list=_slice, i=y + 1, fallback_i=y)
                top_left = _slice2[y]
                bottom_left = self._get_item(_list=_slice2, i=y + 1, fallback_i=y)
                self.texture.draw_quad(
                    self.center + top_left.center,  # top left
                    self.center + top_right.center,  # top right
                    self.center + bottom_right.center,  # bottom right
                    self.center + bottom_left.center,  # bottom left
                    top_left.uv,  # top left
                    top_right.uv,  # top right
                    bottom_right.uv,  # bottom right
                    bottom_left.uv,  # bottom left
                )

    def _get_item(self, _list, i, fallback_i):
        try:
            elem = _list[i]
            return elem
        except IndexError:
            return _list[fallback_i]


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.window = Window.from_display_module()
        self.renderer = Renderer(self.window, accelerated=1, vsync=True)
        self.texture = Texture.from_surface(
            self.renderer, pygame.image.load("planet.png")
        )
        self.renderer.draw_color = (0, 0, 0, 255)
        self.running = True
        pygame.display.set_caption("Textured Map")
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.map = Map(texture=self.texture)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.renderer.clear()
        self.map.draw()
        self.renderer.present()


if __name__ == "__main__":
    game = Game()
    game.run()
