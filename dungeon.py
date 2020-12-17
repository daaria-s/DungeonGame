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

    def show_base(self):
        pass

    def show_decor(self):
        pass

    def show_entity(self):
        pass


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

    def get(self, coords, diff=(0, 0)):
        return self.map_[coords[1] + diff[1]][coords[0] + diff[0]]

    def player_move(self, button):

        buttons_keys = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1)
        }

        if button not in buttons_keys.keys():
            return

        player = self.get(self.entities_position[0]).entity
        target = self.get(self.entities_position[0], buttons_keys[button])

        player.interaction(target)
        self.get(self.entities_position[0]).entity = None
        self.entities_position[0] = player.position
        self.get(player.position).entity = player

    def enemies_move(self):

        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []

        for i in range(1, len(self.entities_position)):
            if not self.get(self.entities_position[i]).entity:
                continue
            diff = options[random.randint(0, len(options) - 1)]

            enemy = self.get(self.entities_position[i]).entity
            target = self.get(self.entities_position[i], diff)

            res.append(enemy.interaction(target))
            self.get(self.entities_position[i]).entity = None
            self.entities_position[i] = enemy.position
            self.get(self.entities_position[i]).entity = enemy

        if not any(res):
            config.TURN = 1
            for i in range(1, len(self.entities_position)):
                if self.get(self.entities_position[i]).entity:
                    enemy = self.get(self.entities_position[i]).entity
                    enemy.action_points = enemy.max_action_points
