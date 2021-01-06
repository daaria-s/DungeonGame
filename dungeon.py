from objects import Wall, Empty
from entity import Player, Enemy
import pygame
import config
from config import *
import random
from PIL import Image


class UnknownMapSymbol(Exception):
    pass


class Dungeon:

    def __init__(self):
        level = [['W', 'W', 'W', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]

        self.player = Player((1, 1))
        self.enemies = [Enemy((5, 2)),
                        Enemy((3, 4)),
                        Enemy((7, 1))]
        self.entities = [self.player, *self.enemies]

        self.objects = []
        empty = Image.open('Sprites/ground/idle/00.png')
        wall = Image.open('Sprites/wall/idle/00.png')
        background = Image.new('RGB', (len(level[0]) * TILE, len(level) * TILE), (255, 255, 255))
        for i in range(len(level)):
            for k in range(len(level[i])):
                if level[i][k] == '.':
                    self.objects.append(Empty((k, i)))
                    background.paste(empty, (k * TILE, i * TILE))
                elif level[i][k] == 'W':
                    self.objects.append(Wall((k, i)))
                    background.paste(wall, (k * TILE, i * TILE))
        self.background = pygame.image.fromstring(background.tobytes(),
                                                  background.size,
                                                  background.mode)

    def get(self, coords, diff=(0, 0)):
        for entity in self.entities:
            if entity.position == (coords[0] + diff[1], coords[1] + diff[0]):
                return entity
        for obj in self.objects:
            if obj.position == (coords[0] + diff[1], coords[1] + diff[0]):
                return obj

    def player_move(self, button):

        if any([i.animator.animation not in ['idle', 'die'] for i in self.enemies]):
            return

        buttons_keys = {
            pygame.K_LEFT: (0, -1),
            pygame.K_RIGHT: (0, 1),
            pygame.K_UP: (-1, 0),
            pygame.K_DOWN: (1, 0)
        }

        if self.player.animator.animation != 'idle':
            return
        if button not in buttons_keys.keys():
            return

        self.player.interaction(self.get(self.player.position, buttons_keys[button]))

    def enemies_move(self):

        if self.player.animator.animation != 'idle':
            return

        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []

        for enemy in self.enemies:
            if not enemy.alive:
                continue

            diff = options[random.randint(0, len(options) - 1)]

            if enemy.animator.animation != 'idle':
                res.append(True)
                continue

            res.append(enemy.interaction(self.get(enemy.position, diff)))

        if not any(res):
            config.TURN = 1
            for enemy in self.enemies:
                enemy.action_points = enemy.max_action_points
