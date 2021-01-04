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
            (2, 3): Enemy((2, 3))
        }

    def get(self, coords, diff=(0, 0)):
        return self.coordinates.get([coords[1] + diff[1]][coords[0] + diff[0]])

    def player_move(self, button):

        if any([self.get(i).entity.animation.name not in ['IDLE', 'DIE'] for i in self.entities_position[1:] if self.get(i).entity]):
            return

        buttons_keys = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1)
        }

        player = self.get(self.entities_position[0]).entity

        if player.animation.name != 'IDLE':
            return
        if button not in buttons_keys.keys():
            return

        target = self.get(self.entities_position[0], buttons_keys[button])

        if not target:
            return

        player.interaction(target)
        self.get(self.entities_position[0]).entity = None
        self.entities_position[0] = player.position
        self.entities_direction[0] = (-buttons_keys[button][0], -buttons_keys[button][1])
        self.get(player.position).entity = player

    def enemies_move(self):

        if self.get(self.entities_position[0]).entity.animation.name != 'IDLE':
            return

        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []

        for i in range(1, len(self.entities_position)):
            if self.get(self.entities_position[i]).entity and not self.get(self.entities_position[i]).entity.alive:
                self.get(self.entities_position[i]).entity = None
                continue
            if not self.get(self.entities_position[i]).entity:
                continue
            if self.get(self.entities_position[i]).entity.name != 'enemy':
                continue

            diff = options[random.randint(0, len(options) - 1)]
            enemy = self.get(self.entities_position[i]).entity

            if enemy.animation.name != 'IDLE':
                res.append(True)
                continue

            target = self.get(self.entities_position[i], diff)

            if not target:
                return

            res.append(enemy.interaction(target))
            self.get(self.entities_position[i]).entity = None
            self.entities_position[i] = enemy.position
            self.entities_direction[i] = (-diff[0], -diff[1])
            self.get(self.entities_position[i]).entity = enemy

        if not any(res):
            config.TURN = 1
            for i in range(1, len(self.entities_position)):
                if self.get(self.entities_position[i]).entity:
                    enemy = self.get(self.entities_position[i]).entity
                    enemy.action_points = enemy.max_action_points
