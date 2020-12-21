from objects import Teleport, Wall, Empty
from entity import Player, Enemy
import pygame
import config
import random


class UnknownMapSymbol(Exception):
    pass


class Cell:

    def __init__(self):
        self.base = None
        self.decor = []
        self.entity = None

    def show_base(self, surf):
        surf.blit(*self.base.show())

    def show_decor(self, surf):
        for i in self.decor:
            surf.blit(*i.show())

    def show_entity(self, surf):
        if self.entity:
            surf.blit(*self.entity.show())


class Dungeon:

    def __init__(self):
        # сделать случайную генерацию карты
        # и вынести это в отдельный метод
        level = [['W', 'W', 'W', '2', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
                 ['W', 'P', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', 'E', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', 'E', '.', '.', 'W'],
                 ['W', '.', '.', '.', 'E', '.', '.', '.', '.', '.', '.', '3'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]

        self.map_ = [[Cell() for _ in range(len(level[i]))] for i in range(len(level))]

        self.entities_position = []

        for i in range(len(level)):
            for k in range(len(level[i])):
                if level[i][k] == 'W':
                    self.map_[i][k].base = Wall((k, i))
                else:
                    self.map_[i][k].base = Empty((k, i))

                if level[i][k] == 'E':
                    self.map_[i][k].entity = Enemy((k, i))
                    self.entities_position.append((k, i))
                elif level[i][k] == 'P':
                    self.map_[i][k].entity = Player((k, i))
                    self.entities_position.append((k, i))
                elif level[i][k].isdigit():
                    self.map_[i][k].decor.append(Teleport((k, i), self.map_[i][k]))

                if not self.map_[i][k]:
                    print(level[i][k])
                    raise UnknownMapSymbol
        self.entities_direction = [(0, 0) for i in self.entities_position]

    def get(self, coords, diff=(0, 0)):
        if 0 <= coords[1] + diff[1] < len(self.map_):
            if 0 <= coords[0] + diff[0] < len(self.map_[0]):
                return self.map_[coords[1] + diff[1]][coords[0] + diff[0]]
        return False

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
