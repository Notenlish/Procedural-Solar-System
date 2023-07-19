import math
import pygame
import random

WIDTH = 600
HEIGHT = 600


# ok so the problem is that when you use rotate, it rotates around the origin.
# But I want it to rotate around the center of the ball.
# So I need to figure out how to rotate around a point.
# I think I need to translate the points to the origin, rotate, then translate back.
# I think I can do this by subtracting the center from the point, then adding it back.
# Here's the code:
# node = pygame.math.Vector2(100, 0).rotate(i)
# node = node - self.center
# node = node.rotate(i)
# node = node + self.center
# But it doesn't work. I think it's because the rotation is relative to the origin.
# So I need to rotate it relative to the center.
# I think I can do this by subtracting the center from the point, then adding it back.
# Here's the code:
# node = pygame.math.Vector2(100, 0).rotate(i)
# node = node - self.center
# node = node.rotate(i)
# node = node + self.center
# But it doesn't work. I think it's because the rotation is relative to the origin.

# bro copilot is thinking on its own lmao :moyai: 


class Point3D:
    def __init__(self, center, color) -> None:
        self.center: pygame.math.Vector2 = center
        self.color = color


class Ball3D:
    def __init__(self, slice_count: int = 10) -> None:
        self.center = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.points: list[Point3D] = []
        self.slice_count = slice_count
        self.setup_points2()

    def OLDsetup_points(self):
        for slice_index in range(0, self.slice_count // 2):
            print(slice_index)
            start_diff = slice_index * 10
            end_diff = (slice_index + 1) * 10
            outer_slice: list[pygame.math.Vector2] = []
            inner_slice: list[pygame.math.Vector2] = []
            for i in range(-90, 90, 5):
                outer_node = pygame.math.Vector2(100, 0).rotate(i)

                multiplier = math.sin(math.radians(i))
                inner_node = pygame.math.Vector2(
                    (100 - start_diff)
                    + ((math.sin(math.radians(i)) * start_diff) * multiplier),
                    0,
                ).rotate(i)

                multiplier = math.sin(math.radians(i))
                inner_node = pygame.math.Vector2(
                    (100 - end_diff)
                    + ((math.sin(math.radians(i)) * end_diff) * multiplier),
                    0,
                ).rotate(i)

                outer_slice.append(outer_node)
                inner_slice.append(inner_node)
            self.points.extend(outer_slice)
            self.points.extend(inner_slice)

    def setup_points2(self):
        self.points = []
        for slice_index in range(self.slice_count):
            dist = 100 - slice_index * 10
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            for p in range(-90, 90, 10):
                node = pygame.math.Vector2(dist, 0).rotate(p)
                self.points.append(Point3D(node, color))

    def draw(self, screen):
        for point in self.points:
            pygame.draw.circle(screen, point.color, self.center + point.center, 1)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        pygame.display.set_caption("3D Ball")
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.ball = Ball3D()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self.events()
            self.update()
            self.draw()
            pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.ball.draw(self.screen)


if __name__ == "__main__":
    game = Game()
    game.run()
