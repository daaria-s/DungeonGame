import pygame
import config
from config import *


class Drawing:

    def __init__(self, surf):
        self.surf = surf

        self.player_image = pygame.transform.scale(pygame.image.load('Sprites/wall.png'), PANEL_IMAGE_SIZE)
        self.health_image = pygame.transform.scale(pygame.image.load('Sprites/wall.png'), PANEL_IMAGE_SIZE)
        self.damage_image = pygame.transform.scale(pygame.image.load('Sprites/wall.png'), PANEL_IMAGE_SIZE)
        self.action_points_image = pygame.transform.scale(pygame.image.load('Sprites/wall.png'), PANEL_IMAGE_SIZE)

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
            x2, y2 = x1 + dungeon_.entities_direction[i][0], y1 + dungeon_.entities_direction[i][1]

            pygame.draw.rect(self.surf, BLACK, (*config.apply((x1 * TILE, y1 * TILE)), TILE, TILE))
            pygame.draw.rect(self.surf, BLACK, (*config.apply((x2 * TILE, y2 * TILE)), TILE, TILE))

            coordinates.append((x1, y1))
            coordinates.append((x2, y2))

        for coords in set(coordinates):
            dungeon_.get(coords).show_base(self.surf)
        for coords in set(coordinates):
            dungeon_.get(coords).show_decor(self.surf)
        for coords in set(coordinates):
            dungeon_.get(coords).show_entity(self.surf)

    def top_panel(self, dungeon_):
        player_ = dungeon_.get(dungeon_.entities_position[0]).entity
        font = pygame.font.Font(None, 40)
        pygame.draw.rect(self.surf, PANEL_COLOR, (0, 0, WIDTH, PANEL_HEIGHT))
        self.surf.blit(self.player_image, (10, 10))
        self.surf.blit(self.health_image, (50, 10))
        text = font.render(str(player_.hit_points) + '/' + str(player_.max_hit_points), True, HP_COLOR)
        self.surf.blit(text, (90, 13))
        self.surf.blit(self.damage_image, (170, 10))
        text = font.render(str(player_.damage), True, DAMAGE_COLOR)
        self.surf.blit(text, (210, 13))
        self.surf.blit(self.action_points_image, (250, 10))
        text = font.render(str(player_.action_points) + '/' + str(player_.max_action_points),
                           True, ACTION_POINTS_COLOR)
        self.surf.blit(text, (290, 13))
