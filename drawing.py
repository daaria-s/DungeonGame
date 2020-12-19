import pygame
from config import *


class Drawing:

    def __init__(self, surf):
        self.surf = surf

    def dungeon(self, dungeon_):
        for i in range(len(dungeon_.map_)):
            for k in range(len(dungeon_.map_[i])):
                dungeon_.get((k, i)).show_base(self.surf)
                dungeon_.get((k, i)).show_decor(self.surf)
                dungeon_.get((k, i)).show_entity(self.surf)

    def entities(self, dungeon_):
        coordinates = []
        for i in range(len(dungeon_.entities_position)):
            x1, y1 = dungeon_.entities_position[i]
            pygame.draw.rect(self.surf, BLACK, (x1 * TILE, y1 * TILE, TILE, TILE))
            coordinates.append((x1, y1))

        for coords in set(coordinates):
            dungeon_.get(coords).show_base(self.surf)
        for coords in set(coordinates):
            dungeon_.get(coords).show_decor(self.surf)
        for coords in set(coordinates):
            dungeon_.get(coords).show_entity(self.surf)
