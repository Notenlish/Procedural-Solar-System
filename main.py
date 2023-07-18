import pygame

from system_manager import SystemManager
from astral_body import AstralBody

WIDTH = 500
HEIGHT = 500


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.system_manager = SystemManager()
        self.setup()
        self.clock = pygame.time.Clock()
        self.dt = 0

    def setup(self):
        system_center = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=20,
            color=(255, 255, 255),
            followed_body=None,
            distance_to_followed_body=0,
            rotation=0,
            rotation_speed=0,
        )
        system_center.update = lambda dt: None  # system center doesn't move
        self.system_manager.add_astral_body(system_center)

        earth = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=5,
            color=(102, 20, 255),
            followed_body=system_center,
            distance_to_followed_body=100,
            rotation=0,
            rotation_speed=0.5,
        )
        self.system_manager.add_astral_body(earth)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000
            pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.system_manager.update(self.dt)

    def draw(self):
        self.screen.fill("black")
        self.system_manager.draw(self.screen)


if __name__ == "__main__":
    game = Game()
    game.run()
