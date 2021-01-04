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
                dungeon_.get((k, i)).show()

    def objects(self, dungeon_):
        for position in dungeon_.coordinates.keys():
            dungeon_.get(position).show()

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

    def bottom_panel(self, dungeon_, coords):
        pygame.draw.rect(self.surf, PANEL_COLOR, (0, 550, WIDTH, PANEL_HEIGHT))
        en_ = dungeon_.get((coords[0] // TILE, (coords[1] - PANEL_HEIGHT) // TILE))
        if not en_ or not en_.entity:
            return
        en_ = en_.entity
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

    def fps(self, clock_):
        font = pygame.font.Font(None, 40)
        text = font.render(str(round(clock_.get_fps())), True, DAMAGE_COLOR)
        pygame.draw.rect(self.surf, PANEL_COLOR, (550, 13, 50, PANEL_HEIGHT - 13))
        self.surf.blit(text, (550, 13))
