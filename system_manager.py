from astral_body import AstralBody


class SystemManager:
    def __init__(self) -> None:
        self.astral_bodies: list[AstralBody] = []
    
    def update(self, dt, mouse_pos):
        for body in self.astral_bodies:
            body.update(dt)
            body.check_mouse_collision(mouse_pos)
    
    def draw(self, screen, line_screen):
        # Blit the line_screen onto the screen
        screen.blit(line_screen, (0, 0))
        for body in self.astral_bodies:
            body.draw(screen, line_screen)
    
    def add_astral_body(self, body: AstralBody):
        self.astral_bodies.append(body)
