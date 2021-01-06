import pygame
import config
from config import *
from functions import *
from entity import Entity


class Drawing:

    def __init__(self, surf):
        self.surf = surf

        self.player_image = pygame.transform.scale(load_image('Sprites/panel/damage.png'), PANEL_IMAGE_SIZE)
        self.health_image = pygame.transform.scale(load_image('Sprites/panel/health.png'), PANEL_IMAGE_SIZE)
        self.damage_image = pygame.transform.scale(load_image('Sprites/panel/damage.png'), PANEL_IMAGE_SIZE)
        self.action_points_image = pygame.transform.scale(load_image('Sprites/panel/action_points.png'), PANEL_IMAGE_SIZE)
        self.inventory_image = pygame.transform.scale(load_image('Sprites/panel/inventory.png'), PANEL_IMAGE_SIZE)
        self.save_image = pygame.transform.scale(load_image('Sprites/panel/save.png'), PANEL_IMAGE_SIZE)
        self.exit_image = pygame.transform.scale(load_image('Sprites/panel/exit.png'), PANEL_IMAGE_SIZE)
        self.inventory_background_image = load_image('Sprites/game/inventory.png')
        self.key_images = {
            'key': pygame.transform.scale(load_image('Sprites/keys/blue/die/00.png'), INVENTORY_IMAGE_SIZE)
        }

    def dungeon(self, dungeon_):
        for obj in dungeon_.all_objects:
            self.surf.blit(*obj.show())

    def entities(self, dungeon_):
        for entity in dungeon_.entities:
            self.surf.blit(*entity.show())

    def entities(self, dungeon_):
        self.surf.blit(dungeon_.background, apply((0, 0)))
        for entity in dungeon_.entities:
            self.surf.blit(*entity.show())

    def top_panel(self, dungeon_):
        player_ = dungeon_.player
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
        self.surf.blit(self.inventory_image, (450, 10))
        self.surf.blit(self.save_image, (500, 10))
        self.surf.blit(self.exit_image, (550, 10))

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
