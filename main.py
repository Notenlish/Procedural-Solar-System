import pygame

from system_manager import SystemManager
from astral_body import AstralBody

WIDTH = 600
HEIGHT = 600


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.line_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self.fade_effect = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.fade_effect_alpha = 1
        self.fade_effect.fill((0, 0, 0, self.fade_effect_alpha))

        self.running = True
        pygame.display.set_caption("Orbit")
        self.system_manager = SystemManager()
        self.setup()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.speedup = False
        self.disable_fade = False

    def setup(self):
        sun = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=20,
            color=(242, 192, 68),
            followed_body=None,
            distance_to_followed_body=0,
            rotation=0,
            rotation_speed=0,
            name="Sun",
        )
        sun.update = lambda dt: None  # system center doesn't move
        self.system_manager.add_astral_body(sun)

        earth = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=5,
            color=(102, 20, 255),
            followed_body=sun,
            distance_to_followed_body=20,
            rotation=0,
            rotation_speed=0.5,
            name="Earth",
        )
        self.system_manager.add_astral_body(earth)

        moon = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=2,
            color=(73, 73, 73),
            followed_body=earth,
            distance_to_followed_body=10,
            rotation=0,
            rotation_speed=1,
            name="Moon",
        )
        self.system_manager.add_astral_body(moon)

        mars = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=3,
            color=(180, 144, 130),
            followed_body=sun,
            distance_to_followed_body=70,
            rotation=0,
            rotation_speed=0.3,
            name="Mars",
        )
        self.system_manager.add_astral_body(mars)

        phobos = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=1,
            color=(152, 71, 62),
            followed_body=mars,
            distance_to_followed_body=9,
            rotation=0,
            rotation_speed=1,
            name="Phobos",
        )
        self.system_manager.add_astral_body(phobos)

        deimos = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=1,
            color=(163, 124, 64),
            followed_body=mars,
            distance_to_followed_body=16,
            rotation=0,
            rotation_speed=0.5,
            name="Deimos",
        )
        self.system_manager.add_astral_body(deimos)

        jupiter = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=10,
            color="orange",
            followed_body=sun,
            distance_to_followed_body=120,
            rotation=0,
            rotation_speed=0.1,
            name="Jupiter",
        )

        self.system_manager.add_astral_body(jupiter)

        europa = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=2,
            color=(38, 42, 16),
            followed_body=jupiter,
            distance_to_followed_body=10,
            rotation=0,
            rotation_speed=1.47,
            name="Europa",
        )

        self.system_manager.add_astral_body(europa)

        ganymede = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=2,
            color=(84, 68, 43),
            followed_body=jupiter,
            distance_to_followed_body=20,
            rotation=0,
            rotation_speed=0.45,
            name="Ganymede",
        )

        self.system_manager.add_astral_body(ganymede)

        callisto = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=2,
            color=(255, 93, 115),
            followed_body=jupiter,
            distance_to_followed_body=30,
            rotation=0,
            rotation_speed=0.21,
            name="Callisto",
        )

        self.system_manager.add_astral_body(callisto)

        saturn = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=8,
            color=(247, 157, 132),
            followed_body=sun,
            distance_to_followed_body=150,
            rotation=0,
            rotation_speed=0.13,
            name="Saturn",
        )

        self.system_manager.add_astral_body(saturn)

        uranus = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=6,
            color=(0, 52, 89),
            followed_body=sun,
            distance_to_followed_body=200,
            rotation=0,
            rotation_speed=0.1,
            name="Uranus",
        )

        self.system_manager.add_astral_body(uranus)

        neptune = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=6,
            color=(0, 167, 225),
            followed_body=sun,
            distance_to_followed_body=250,
            rotation=0,
            rotation_speed=0.09,
            name="Neptune",
        )

        self.system_manager.add_astral_body(neptune)

        pluto = AstralBody(
            center=(WIDTH / 2, HEIGHT / 2),
            radius=2,
            color=(227, 220, 194),
            followed_body=sun,
            distance_to_followed_body=300,
            rotation=0,
            rotation_speed=0.07,
            name="Pluto",
        )

        self.system_manager.add_astral_body(pluto)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.system_manager.toggle_names()
                if event.key == pygame.K_e:
                    self.speedup = True
                if event.key == pygame.K_d:
                    self.disable_fade = not self.disable_fade
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    self.speedup = False

    def update(self):
        if self.speedup:
            self.dt = 16 / 1000  # 60 fps
            for _ in range(10):
                self.system_manager.update(self.dt, pygame.mouse.get_pos())
                self.draw()  # needed to update the fade effect
        else:
            self.system_manager.update(self.dt, pygame.mouse.get_pos())

    def draw(self):
        self.screen.fill("black")

        self.system_manager.draw(self.screen, self.line_screen)

        if not self.disable_fade:
            # Blit the fade_effect onto the line_screen
            self.line_screen.blit(self.fade_effect, (0, 0))


if __name__ == "__main__":
    game = Game()
    game.run()
