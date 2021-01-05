from objects import Teleport, Wall, Empty
from entity import Player, Enemy
import pygame
import config
import random


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

        self.map_ = [[Wall((k, i)) if level[i][k] == 'W' else Empty((k, i)) for k in range(len(level[i]))] for i in range(len(level))]

        self.coordinates = {
            (1, 1): Player((1, 1)),
            (5, 2): Enemy((5, 2)),
            (2, 3): Enemy((2, 3)),
            (3, 0): Teleport((3, 0), 2)
        }
        self.player = [obj for obj in self.coordinates.values() if obj.name == 'player'][0]
        self.enemies = [obj for obj in self.coordinates.values() if obj.name == 'enemy']

    def get(self, coords, diff=(0, 0)):
        return self.coordinates.get([coords[1] + diff[1]][coords[0] + diff[0]])

    def player_move(self, button):

        if any([i.animation.name not in ['IDLE', 'DIE'] for i in self.enemies]):
            return

        buttons_keys = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1)
        }

        if self.player.animation.name != 'IDLE':
            return
        if button not in buttons_keys.keys():
            return

        self.coordinates[self.player.position] = None
        self.player.interaction(self.get(self.player.position, buttons_keys[button]))
        self.coordinates[self.player.position] = self.player

    def enemies_move(self):

        if self.player.animation.name != 'IDLE':
            return

        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []

        for enemy in self.enemies:
            diff = options[random.randint(0, len(options) - 1)]

            if enemy.animation.name != 'IDLE':
                res.append(True)
                continue

            target = self.get(enemy.position, diff)
            self.coordinates[enemy.position] = None
            res.append(enemy.interaction(target))
            self.coordinates[enemy.position] = enemy

        if not any(res):
            config.TURN = 1
            for enemy in self.enemies:
                enemy.action_points = enemy.max_action_points
