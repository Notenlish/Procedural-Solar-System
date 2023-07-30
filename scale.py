import pygame as pg

screen = pg.display.set_mode((1,1))

textures = [
    "saturn.jpg"
    #"sun.jpg",
    #"uranus.jpg",
    #"venus.jpg",
    #"neptune.jpg",
    #"moon.jpg",
    #"mars.jpg",
    #"jupiter.jpg",
    #"earth.jpg",
    #"bg.jpg",
]

DIVIDER = 2

for t in textures:
    image = pg.image.load(t)
    # scale the image down while keeping the aspect ratio
    image = pg.transform.scale(image, (int(image.get_width() / DIVIDER), int(image.get_height() / DIVIDER)))
    pg.image.save(image, t)

