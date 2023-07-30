import pygame
from pygame._sdl2 import Renderer, Texture, Window


from system_manager import SystemManager
from astral_body import AstralBody

WIDTH = 700
HEIGHT = 700


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.window = Window.from_display_module()
        self.renderer = Renderer(self.window, vsync=True)
        # self.line_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # self.fade_effect = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # self.fade_effect_alpha = 1
        # self.fade_effect.fill((0, 0, 0, self.fade_effect_alpha))

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
            renderer=self.renderer,
            center=(WIDTH / 2, HEIGHT / 2),
            radius=30,
            color=(242, 192, 68),
            followed_body=None,
            distance_to_followed_body=0,
            rotation=0,
            rotation_speed=0,
            name="Sun",
            texture_path="sun.jpg"
        )
        sun.update = lambda dt: None  # system center doesn't move
        self.system_manager.add_astral_body(sun)

        earth = AstralBody(
            renderer=self.renderer,
            center=(WIDTH / 2, HEIGHT / 2),
            radius=18,
            color=(102, 20, 255),
            followed_body=sun,
            distance_to_followed_body=40,
            rotation=0,
            rotation_speed=0.5,
            name="Earth",
            texture_path="earth.jpg"
        )
        self.system_manager.add_astral_body(earth)

        moon = AstralBody(
            renderer=self.renderer,
            center=(WIDTH / 2, HEIGHT / 2),
            radius=7,
            color=(73, 73, 73),
            followed_body=earth,
            distance_to_followed_body=10,
            rotation=0,
            rotation_speed=1,
            name="Moon",
            texture_path="moon.jpg"
        )
        self.system_manager.add_astral_body(moon)

        mars = AstralBody(
            renderer=self.renderer,
            center=(WIDTH / 2, HEIGHT / 2),
            radius=15,
            color=(180, 144, 130),
            followed_body=sun,
            distance_to_followed_body=70,
            rotation=0,
            rotation_speed=0.3,
            name="Mars",
            texture_path="mars.jpg"
        )
        self.system_manager.add_astral_body(mars)

        jupiter = AstralBody(
            renderer=self.renderer,
            center=(WIDTH / 2, HEIGHT / 2),
            radius=30,
            color="orange",
            followed_body=sun,
            distance_to_followed_body=120,
            rotation=0,
            rotation_speed=0.1,
            name="Jupiter",
            texture_path="jupiter.jpg"
        )

        self.system_manager.add_astral_body(jupiter)

        saturn = AstralBody(
            renderer=self.renderer,
            center=(WIDTH / 2, HEIGHT / 2),
            radius=32,
            color=(247, 157, 132),
            followed_body=sun,
            distance_to_followed_body=150,
            rotation=0,
            rotation_speed=0.13,
            name="Saturn",
            texture_path="saturn.jpg"
        )

        self.system_manager.add_astral_body(saturn)

        uranus = AstralBody(
            renderer=self.renderer,
            center=(WIDTH / 2, HEIGHT / 2),
            radius=17,
            color=(0, 52, 89),
            followed_body=sun,
            distance_to_followed_body=200,
            rotation=0,
            rotation_speed=0.1,
            name="Uranus",
            texture_path="uranus.jpg"
        )

        self.system_manager.add_astral_body(uranus)

        neptune = AstralBody(
            renderer=self.renderer,
            center=(WIDTH / 2, HEIGHT / 2),
            radius=26,
            color=(0, 167, 225),
            followed_body=sun,
            distance_to_followed_body=250,
            rotation=0,
            rotation_speed=0.09,
            name="Neptune",
            texture_path="neptune.jpg"
        )

        self.system_manager.add_astral_body(neptune)

        pluto = AstralBody(
            renderer=self.renderer,
            center=(WIDTH / 2, HEIGHT / 2),
            radius=14,
            color=(227, 220, 194),
            followed_body=sun,
            distance_to_followed_body=320,
            rotation=0,
            rotation_speed=0.07,
            name="Pluto",
            texture_path="pluto.jpg"
        )

        self.system_manager.add_astral_body(pluto)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            pygame.display.set_caption(f"FPS:{self.clock.get_fps()}")
            self.dt = self.clock.tick(60) / 1000
            # pygame.display.update() not used in _sdl2

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
            for _ in range(15):
                self.system_manager.update(self.dt, pygame.mouse.get_pos())
                self.draw()  # needed to update the fade effect
        else:
            self.system_manager.update(self.dt, pygame.mouse.get_pos())

    def draw(self):
        self.renderer.draw_color = (0,0,0,255)
        self.renderer.clear()
        self.system_manager.draw(self.dt)
        self.renderer.present()

    def draw2(self):
        self.screen.fill("black")

        self.system_manager.draw(self.screen, self.line_screen)

        if not self.disable_fade:
            # Blit the fade_effect onto the line_screen
            self.line_screen.blit(self.fade_effect, (0, 0))


if __name__ == "__main__":
    game = Game()
    game.run()
