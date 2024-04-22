from image import load
from settings import *


class Hexagon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = 0
        self.image = load("Assets/hexagon.png", size=HEXAGON_SIZES)
        self.rect = self.image.get_rect(topleft=(self.x, self.y + HEXAGON_INDEX))

    def draw_hexagon(self, surface):
        surface.blit(self.image, self.rect)

    # Todo
    def shoot(self):
        # status = 0 nothing
        # status = 1 fire
        # status = 2 golden
        # status = 3 ice
        # status = 4 ground
        if self.status == 0:
            return
        elif self.status == 1:
            pass
        elif self.status == 2:
            pass
        elif self.status == 3:
            pass
        elif self.status == 4:
            pass
