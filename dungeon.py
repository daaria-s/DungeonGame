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
        # EDIT
        # remake generate level function
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
        self.enemies = [
          Enemy((5, 2)),
          Enemy((3, 4)),
          Enemy((7, 1))
        ]
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

    def generate_level(self, enter_x, enter_y, exit_x, exit_y, prev_room=None, next_room=None):
        if not prev_room:
            prev_room = 0
            next_room = 2
        if not next_room:
            next_room = prev_room + 1

        map = [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
               ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
               ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
               ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
               ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
               ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
               ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
               ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
               ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
               ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]

        if enter_x in (0, 9):
            map[abs(enter_x - 1)][enter_y] = 'P'
        else:
            map[enter_x][abs(enter_y - 1)] = 'P'

        map[enter_x][enter_y] = str(prev_room)

        map[exit_x][exit_y] = str(next_room)

        for i in range(random.randint(3, 4)):
            x, y = 0, 0
            while map[x][y] != '.':
                x, y = random.randint(1, 8), random.randint(1, 9)
            map[x][y] = 'E'

        return map

    def load_map(self, user_name):
        pass

    def save_map(self):
        pass

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
        blocked_cells = []

        for enemy in self.enemies:
            if not enemy.alive:
                continue
                
            player_pos = self.player.position
            enemy_pos = enemy.position
            if random.randint(0, 1):
                if enemy_pos[0] != player_pos[0]:
                    diff = (-1, 0) if enemy_pos[0] > player_pos[0] else (1, 0)
                elif enemy_pos[1] != player_pos[1]:
                    diff = (0, -1) if enemy_pos[1] > player_pos[1] else (0, 1)
            else:
                if enemy_pos[1] != player_pos[1]:
                    diff = (0, -1) if enemy_pos[1] > player_pos[1] else (0, 1)
                elif enemy_pos[0] != player_pos[0]:
                    diff = (-1, 0) if enemy_pos[0] > player_pos[0] else (1, 0)

            while (enemy_pos[0] + diff[0], enemy_pos[1] + diff[1]) in blocked_cells:
                diff = options[random.randint(0, len(options) - 1)]
            blocked_cells.append((enemy_pos[0] + diff[0], enemy_pos[1] + diff[1]))

            if enemy.animator.animation != 'idle':
                res.append(True)
                continue

            res.append(enemy.interaction(self.get(enemy.position, diff)))

        if not any(res):
            config.TURN = 1
            for enemy in self.enemies:
                enemy.action_points = enemy.max_action_points
