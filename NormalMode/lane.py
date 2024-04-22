from hexagon import Hexagon
from image import load
from settings import LANE_SIZES


class Lane:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load("Assets/floor1.png",size = LANE_SIZES)
        self.rec = self.image.get_rect(topleft=(self.x, self.y))

    def draw_lane(self, surface: object) -> object:
        hexagon = Hexagon(self.x + 30, self.y)
        surface.blit(self.image, self.rec)
        hexagon.draw_hexagon(surface)
