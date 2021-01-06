import pygame
import config
from config import *
from functions import *
from entity import Entity


# EDIT
# delete this class
class Drawing:

    def __init__(self, surf):
        self.surf = surf

    def dungeon(self, dungeon_):
        self.surf.blit(dungeon_.background, apply((0, 0)))
        for entity in dungeon_.entities:
            self.surf.blit(*entity.show())

    def bottom_panel(self, dungeon_, coords):
        pygame.draw.rect(self.surf, PANEL_COLOR, (0, 550, WIDTH, PANEL_HEIGHT))
        en_ = dungeon_.get((coords[0] // TILE, (coords[1] - PANEL_HEIGHT) // TILE))
        if not en_ or not isinstance(en_, Entity):
            return
        font = pygame.font.Font(None, 40)
        self.surf.blit(self.player_image, (10, 560))
        self.surf.blit(self.health_image, (50, 560))
        text = font.render(str(en_.hit_points) + '/' + str(en_.max_hit_points), True, HP_COLOR)
        self.surf.blit(text, (90, 563))
        self.surf.blit(self.damage_image, (170, 560))
        text = font.render(str(en_.damage), True, DAMAGE_COLOR)
        self.surf.blit(text, (210, 563))
        self.surf.blit(self.action_points_image, (250, 560))
        text = font.render(str(en_.action_points) + '/' + str(en_.max_action_points),
                           True, ACTION_POINTS_COLOR)
        self.surf.blit(text, (290, 563))

    def inventory(self, dungeon_):
        player_ = dungeon_.player
        row, col = 0, 0
        for obj in player_.inventory:
            self.inventory_background_image.blit(self.key_images[obj],
                                                 (INVENTORY_INDENT + 3 + col * (INVENTORY_INDENT + INVENTORY_IMAGE_SIZE[0]),
                                                  INVENTORY_INDENT + 3 + row * (INVENTORY_INDENT + INVENTORY_IMAGE_SIZE[1])))
            col += 1
            if col == 5:
                col = 0
                row += 1
        self.surf.blit(self.inventory_background_image, (100, 100))
