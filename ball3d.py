import pygame
from pygame._sdl2 import Renderer, Texture, Window
from copy import deepcopy

WIDTH = 600
HEIGHT = 600


def cubic_bezier(p0, p1, p2, p3, time):
    return (
        (1 - time) ** 3 * p0
        + 3 * (1 - time) ** 2 * time * p1
        + 3 * (1 - time) * time**2 * p2
        + time**3 * p3
    )


def cubic_bezier_circle(t, radius):
    K = 0.5522847498  # Constant for approximating a circle
    one_minus_t = 1 - t

    P0 = (radius, 0)
    P1 = (radius, radius * K)
    P2 = (radius * K, radius)
    P3 = (0, radius)

    # The cubic Bézier formula
    x = (
        one_minus_t**3 * P0[0]
        + 3 * one_minus_t**2 * t * P1[0]
        + 3 * one_minus_t * t**2 * P2[0]
        + t**3 * P3[0]
    )
    y = (
        one_minus_t**3 * P0[1]
        + 3 * one_minus_t**2 * t * P1[1]
        + 3 * one_minus_t * t**2 * P2[1]
        + t**3 * P3[1]
    )
    return x, y


class Point3D:
    def __init__(self, center: pygame.Vector2, x_index, y_index, width, height) -> None:
        self.center = center
        self.x_index = x_index
        self.y_index = y_index
        self.uv = [self.x_index / width, self.y_index / height]

    def __repr__(self) -> str:
        return f"<Point3D {self.center} indexes:[{self.x_index}, {self.y_index}] UV:{self.uv}>"


class Ball3D:
    def __init__(
        self,
        radius: int,
        texture: Texture,
        center=pygame.math.Vector2(WIDTH / 2, HEIGHT / 2),
        debug=False,
    ) -> None:
        self.center = center
        self.texture = texture
        self.radius = radius
        self.num_points = 4  # half height
        # num of slices per half a circle
        self.num_slices = 6  # half width
        self.FULL_UV = 1
        self.HALF_UV = 0.5
        self.ROTATE_DIRECTION = -1
        self.setup_points()
        self.debug = debug

    def setup_points(self):
        self.quarters: list[list[list[Point3D]]] = []
        self.stuff = [  # arguments for cubic bezier func used to "correct" the vertical segment positions.
            0.700,
            0.760,
            0.880,
            0.960,
        ]
        self._create_slices()

    def _create_slices(self):
        """num_points means number of points in each quarter of the circle."""
        # create the top right slice
        _slices: list[list[Point3D]] = []
        for u in range(self.num_slices + 1):  # iterate over each vertical line segment
            radius = (self.num_slices - u) / self.num_slices * self.radius
            _slice = []
            for i in range(self.num_points + 1):
                t = i / self.num_points
                x, y = cubic_bezier_circle(t, radius)
                ratio = abs(t / (0.5))
                # center ratio will be 0, top will be -1, bottom will be 1
                ratio -= 1
                _, testy = cubic_bezier_circle(t, self.radius)
                y_diff = testy - y
                ratio = cubic_bezier(
                    self.stuff[0], self.stuff[1], self.stuff[2], self.stuff[3], ratio
                )
                y += ratio * y_diff

                point = Point3D(  # top right
                    pygame.Vector2(x, -y),
                    x_index=u,
                    y_index=i,
                    width=self.num_slices * 2,
                    height=self.num_points * 2,
                )
                point.uv[0] = self.FULL_UV - point.uv[0]
                point.uv[1] = self.HALF_UV - point.uv[1]
                _slice.append(point)
            _slices.append(_slice)
        self.quarters.append(_slices)

        copy = deepcopy(_slices)
        for _slice in copy:  # top left
            for point in _slice:
                point.center.x *= -1
                point.x_index += self.num_slices
                point.uv[0] = self.FULL_UV - point.uv[0]
        self.quarters.append(copy)

        copy_2 = deepcopy(_slices)
        for _slice in copy_2:  # bottom right
            for point in _slice:
                point.center.y *= -1
                point.y_index += self.num_points
                point.uv[1] = self.FULL_UV - point.uv[1]
        self.quarters.append(copy_2)

        copy_3 = deepcopy(_slices)
        for _slice in copy_3:  # bottom left
            for point in _slice:
                point.center.y *= -1
                point.center.x *= -1
                point.y_index += self.num_points
                point.x_index += self.num_slices
                point.uv[1] = self.FULL_UV - point.uv[1]
                point.uv[0] = self.FULL_UV - point.uv[0]
        self.quarters.append(copy_3)

    def draw(self, dt):
        for _slices in self.quarters:
            for x in range(len(_slices)):
                _slice = _slices[x]  # right side
                _slice2 = self._get_item(
                    _list=_slices, i=x + 1, fallback_i=x
                )  # left side

                for y in range(len(_slice)):
                    top_right = _slice[y]
                    bottom_right = self._get_item(
                        _list=_slice, i=y + 1, fallback_i=y
                    )  # fallback index
                    top_left = _slice2[y]
                    bottom_left = self._get_item(_list=_slice2, i=y + 1, fallback_i=y)

                    top_right.uv[0] += self.ROTATE_DIRECTION * dt * 0.07
                    top_right.uv[0] %= 1

                    uv_diff = abs(top_left.uv[0] - top_right.uv[0])
                    # şundan dolayı oluyor:
                    # 0.9 du 1 oldu sonra bir anda 0 oldu ama diğer kısımlar hala 0.9 kaldı
                    # aradaki fark oldu sana 0.9 sonra niye garip uvler var

                    # the problem is that you cant specify the uv thing to go from outside of the texture: 0.1 to 0.9 from outside
                    # it always uses the inside, which becomes a problem when trying to do texture wrapping/scrolling
                    # idk if this is something that can even be fixed

                    val = 0.2
                    mult = 0.1
                    if uv_diff >= (1 - val):  # Try and fix that weird visual bug
                        if top_right.uv[0] <= 0 + val:
                            add_thing = 1
                        if top_right.uv[0] >= 1 - val:
                            add_thing = -1
                        else:
                            add_thing = 0
                        add = val * mult * add_thing

                        if bottom_right.uv[0] <= 0 + val:
                            add_thing2 = 1
                        if bottom_right.uv[0] >= 1 - val:
                            add_thing2 = -1
                        else:
                            add_thing2 = 0
                        add2 = val * mult * add_thing2

                        uv_args = [
                            (
                                top_right.uv[0],  # originally top left
                                top_right.uv[1],
                            ),
                            (
                                top_right.uv[0] + add,
                                top_right.uv[1],
                            ),
                            (
                                bottom_right.uv[0],  # originally bottom left
                                bottom_right.uv[1],
                            ),
                            (
                                bottom_right.uv[0] + add2,
                                bottom_right.uv[1],
                            ),
                        ]

                        self.texture.draw_quad(
                            self.center + top_left.center,
                            self.center + top_right.center,
                            self.center + bottom_right.center,
                            self.center + bottom_left.center,
                            *uv_args,
                        )
                    else:
                        self.texture.draw_quad(
                            self.center + top_left.center,
                            self.center + top_right.center,
                            self.center + bottom_right.center,
                            self.center + bottom_left.center,
                            (top_left.uv[0], top_left.uv[1]),
                            (top_right.uv[0], top_right.uv[1]),
                            (bottom_right.uv[0], bottom_right.uv[1]),
                            (bottom_left.uv[0], bottom_left.uv[1]),
                        )
            if self.debug:
                self.draw_lines_quarter(_slices)

    def draw_lines_quarter(self, _slices: list[list[Point3D]]):
        for x in range(len(_slices)):
            _slice = _slices[x]  # right side
            _slice2 = self._get_item(_list=_slices, i=x + 1, fallback_i=x)  # left side

            for y in range(len(_slice)):
                top_right = _slice[y]
                bottom_right = self._get_item(_list=_slice, i=y + 1, fallback_i=y)
                # top_left = _slice2[y]
                # bottom_left = self._get_item(_list=_slice2, i=y + 1, fallback_i=y)
                val = int(top_right.uv[0] * 255)
                self.texture.renderer.draw_color = (val, 255, 0, 255)
                self.texture.renderer.draw_line(
                    self.center + top_right.center,
                    self.center + bottom_right.center,
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
        self.renderer = Renderer(self.window, accelerated=1)
        self.texture = Texture.from_surface(
            self.renderer, pygame.image.load("planet.png")
        )
        self.renderer.draw_color = (0, 0, 0, 255)
        self.running = True
        pygame.display.set_caption("3D Ball")
        self.time = 0
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.ball = Ball3D(radius=200, texture=self.texture, debug=True)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60)
            self.time += self.dt
            self.dt /= 1000

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()
        self.ball.draw(self.dt)
        self.renderer.present()


if __name__ == "__main__":
    game = Game()
    game.run()
