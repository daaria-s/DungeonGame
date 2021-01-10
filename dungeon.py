from objects import *
from entity import Player, Enemy
from functions import *
import random
from PIL import Image
from interface import Panel, Button, Element


class UnknownMapSymbol(Exception):
    pass


class Room:
    def __init__(self, exit_, enemies, objects, num_of_room, enter=None):
        self.num = num_of_room
        if num_of_room == 1:
            self.first_room = True
        self.enter = enter
        self.exit_ = exit_

        self.enemies = enemies
        self.objects = objects

    def enter_from_exit(self):
        if self.exit_[0] == 9:
            return 0, self.exit_[1]
        return self.exit_[0], 0

    def structure(self):
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
        if self.enter:
            map[self.enter[0]][self.enter[1]] = self.num - 1

        map[self.exit_[0]][self.exit_[1]] = self.num + 1


        return map


class Dungeon(Element):

    def __init__(self, user_name=''):
        super().__init__()

        self.first = True
        self.rooms = {}
        self.enemies = []
        self.objects = []
        self.base = []
        self.entities = []

        self.player = Player((1, 1), 1, 1, 1, 1, 5, 3)
        self.current_room = 1
        self.turn = 1

        self.change_room(1)

    def new(self):
        self.first = True
        self.rooms = {}
        self.enemies = []
        self.objects = []
        self.base = []
        self.entities = []

        self.player = Player((1, 1), 1, 1, 1, 1, 5, 3)
        self.current_room = 1
        self.turn = 1

        self.change_room(1)

    def change_room(self, num):
        self.enemies = []
        self.objects = []
        self.base = []

        if num not in self.rooms.keys():
            self.generate_level(num)
        else:
            self.enemies = self.rooms[num].enemies
            self.objects = self.rooms[num].objects

        if self.first:
            self.player.position = (1, 1)
            self.first = False
        elif num > self.current_room:
            self.player.position = self.rooms[num].enter[1], \
                                   self.rooms[num].enter[0]
        else:
            self.player.position = self.rooms[num].exit_[1], \
                                   self.rooms[num].exit_[0]

        self.current_room = num
        self.entities = [self.player, *self.enemies]
        self.load_room(self.current_room)

    def load_room(self, num_of_room):
        level = self.rooms[num_of_room].structure()
        empty = Image.open('Sprites/ground/idle/00.png')
        wall = Image.open('Sprites/wall/idle/00.png')
        background = Image.new('RGB', (len(level[0]) * TILE, len(level) * TILE), (255, 255, 255))
        for i in range(len(level)):
            for k in range(len(level[i])):
                if level[i][k] == 'W':
                    self.base.append(Wall((k, i)))
                    background.paste(wall, (k * TILE, i * TILE))
                else:
                    self.base.append(Empty((k, i)))
                    background.paste(empty, (k * TILE, i * TILE))

        self.background = pygame.image.fromstring(background.tobytes(),
                                                  background.size,
                                                  background.mode)

        self.top_panel = Panel(self.player, True, 0)
        self.bottom_panel = Panel(self.enemies[0], False, 550)
        self.buttons = [
            Button('game/panel/exit', (550, 10), 'menu'),
            Button('game/panel/inventory', (450, 10), 'inventory'),
            Button('game/panel/save', (500, 10), 'save')
        ]

    def generate_level(self, num):
        closed_cells = [self.player.position]
        enter = None

        if num != 1:
            enter = self.rooms[num - 1].enter_from_exit()

        for i in range(random.randint(3, 5)):
            x, y = random.randint(2, 9), random.randint(2, 8)
            while (x, y) in closed_cells:
                x, y = random.randint(2, 9), random.randint(2, 8)
            self.enemies.append(
                Enemy((x, y), random.choice(['green', 'blue', 'purple']), 2, 2, 1, 1, 3, 2))
            closed_cells.append((x, y))

        for i in range(random.randint(6, 7)):
            x, y = random.randint(2, 8), random.randint(2, 7)
            while (x, y) in closed_cells:
                x, y = random.randint(2, 8), random.randint(2, 7)
            self.objects.append(Box((x, y)))
            closed_cells.append((x, y))

        exit_ = random.choice([(random.randint(2, 8), 11), (9, random.randint(2, 9))])

        self.rooms[num] = Room(exit_, self.enemies, self.objects, self.current_room,
                               enter=enter)

    def load_map(self, user_name):
        pass

    def save_map(self):
        print('save')

    def get(self, coords, diff=(0, 0)):
        for entity in [*self.entities, *self.objects, *self.base]:
            if entity.position == (coords[0] + diff[1], coords[1] + diff[0]):
                return entity

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

        self.player.interaction_teleport(self)

        if button not in buttons_keys.keys():
            return

        self.player.interaction(self, buttons_keys[button])

    def enemies_move(self):

        if self.player.animator.animation != 'idle':
            return

        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []
        blocked_cells = []

        for enemy in self.enemies:
            if not enemy.alive:
                continue

            diff = options[random.randint(0, len(options) - 1)]

            player_pos = self.player.position
            enemy_pos = enemy.position
            if random.randint(0, 1):
                if enemy_pos[0] != player_pos[0]:
                    diff = (0, -1) if enemy_pos[0] > player_pos[0] else (0, 1)
                elif enemy_pos[1] != player_pos[1]:
                    diff = (-1, 0) if enemy_pos[1] > player_pos[1] else (1, 0)
            else:
                if enemy_pos[1] != player_pos[1]:
                    diff = (-1, 0) if enemy_pos[1] > player_pos[1] else (1, 0)
                elif enemy_pos[0] != player_pos[0]:
                    diff = (0, -1) if enemy_pos[0] > player_pos[0] else (0, 1)

            while (
                    enemy_pos[0] + diff[0],
                    enemy_pos[1] + diff[1]) in blocked_cells or not isinstance(
                self.get(enemy_pos, diff), (Player, Empty)):
                diff = options[random.randint(0, len(options) - 1)]

            blocked_cells.append((enemy_pos[0] + diff[0], enemy_pos[1] + diff[1]))

            if enemy.animator.animation != 'idle':
                res.append(True)
                continue

            res.append(enemy.interaction(self, diff))

        if not any(res):
            self.turn = 1
            for enemy in self.enemies:
                enemy.action_points[0] = enemy.action_points[1]

    def show(self, surf):
        if self.turn == 2:
            self.enemies_move()

        surf.blit(self.background, apply((0, 0)))
        for entity in self.entities:
            entity.show(surf)
        for obj in self.objects:
            obj.show(surf)

        self.top_panel.show(surf)
        self.bottom_panel.show(surf)

        for button in self.buttons:
            button.show(surf)

    def button_down(self, mouse_pos):
        obj = self.get((mouse_pos[0] // TILE, (mouse_pos[1] - PANEL_HEIGHT) // TILE))
        if isinstance(obj, Enemy) and obj.alive:
            self.bottom_panel.change_target(obj)
        else:
            # EDIT
            # This doesn't work
            self.bottom_panel.change_target(None)

        for button in self.buttons:
            res = button.button_down(mouse_pos)
            if res:
                return res

    def key_down(self, button):
        if self.turn == 1:
            self.player_move(button)
