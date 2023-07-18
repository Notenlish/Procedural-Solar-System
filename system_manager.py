from astral_body import AstralBody


class SystemManager:
    def __init__(self) -> None:
        self.astral_bodies: list[AstralBody] = []
    
    def update(self, dt):
        for body in self.astral_bodies:
            body.update(dt)
    
    def draw(self, screen):
        for body in self.astral_bodies:
            body.draw(screen)
    
    def add_astral_body(self, body: AstralBody):
        self.astral_bodies.append(body)
