import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

# Initialize the screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fading Effect Demo")
clock = pygame.time.Clock()

# Create the line_screen
line_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Initialize the fading black surface
fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
fade_alpha = 25  # Starting alpha value (fully opaque)


ballx = WIDTH / 2
bally = HEIGHT / 2

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fading logic
    # fade_alpha += 5  # You can adjust this value to control the fading speed
    if fade_alpha >= 255:
        fade_alpha = 0
        fade_surface.fill((0, 0, 0, 255))

    print(fade_alpha)
    fade_surface.fill((0, 0, 0, fade_alpha))

    # Draw a line
    pygame.draw.line(line_screen, (255, 0, 0), (0, 0), (WIDTH, HEIGHT))
    pygame.draw.circle(
        line_screen,
        (255, 255, 255),
        (ballx, bally),
        10,
    )

    ballx += random.randint(-10, 10) / 2
    bally += random.randint(-10, 10) / 2

    # Blit the fade_surface onto the line_screen
    line_screen.blit(
        fade_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2
    )  # BLENDADD

    # Blit the line_screen onto the screen
    screen.blit(line_screen, (0, 0))

    # Update the display
    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
sys.exit()
