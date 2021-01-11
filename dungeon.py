from objects import *
from entity import Player, Enemy
import config
from functions import *
import random
from PIL import Image
from interface import Panel, Button, Element


class UnknownMapSymbol(Exception):
    pass


class Room:
    def __init__(self, exit_, enemies, objects, num_of_room, enter=None):
        self.num = num_of_room
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
    """Класс подземелья"""

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
        # собираем из маленьких изображений пустых клетов и стен
        # одно большое изображение поля чтобы потом отображать только его
        for i in range(len(level)):
            for k in range(len(level[i])):
                if level[i][k] == '.':
                    self.base.append(Empty((k, i)))
                    background.paste(empty, (k * TILE, i * TILE))
                elif level[i][k] == 'W':
                    self.base.append(Wall((k, i)))
                    background.paste(wall, (k * TILE, i * TILE))
        self.background = pygame.image.fromstring(background.tobytes(),
                                                  background.size,
                                                  background.mode)

        self.top_panel = Panel(self.player, True, 0)  # создаем верхнюю
        self.bottom_panel = Panel(self.enemies[0], False, 550)  # и нижнюю панели
        self.buttons = [  # создаем кнопки
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
                Enemy((x, y), random.choice(['green', 'blue', 'purple']), 2, 2, 1, 1, 2, 2))
            closed_cells.append((x, y))

        for i in range(random.randint(6, 7)):
            x, y = random.randint(2, 8), random.randint(2, 7)
            while (x, y) in closed_cells:
                x, y = random.randint(2, 8), random.randint(2, 7)
            self.objects.append(Box((x, y)))
            closed_cells.append((x, y))

        for i in range(random.randint(0, 2)):
            x, y = random.randint(1, 9), random.randint(2, 8)
            while (x, y) in closed_cells:
                x, y = random.randint(1, 9), random.randint(2, 8)
            self.objects.append(Chest((x, y), 'potion'))
            closed_cells.append((x, y))
        exit_ = random.choice([(random.randint(2, 8), 11), (9, random.randint(2, 9))])

        self.rooms[num] = Room(exit_, self.enemies, self.objects, self.current_room,
                               enter=enter)

    def load_map(self, user_name):
        pass

    def save_map(self):
        print('save')

    def get(self, coords, diff=(0, 0)):
        """Возвращает объект по координатам"""
        for entity in [*self.entities, *self.objects, *self.base]:
            if entity.position == (coords[0] + diff[1], coords[1] + diff[0]):
                return entity

    def player_move(self, button):
        """Движение игрока"""

        if any([i.animator.animation not in ['idle', 'die'] for i in self.enemies]):
            return  # если враги еще соверщают какие-то действия, то игрок стоит

        # словарь вида {кнопка: (смещение на X и Y)}
        buttons_keys = {
            pygame.K_LEFT: (0, -1),
            pygame.K_RIGHT: (0, 1),
            pygame.K_UP: (-1, 0),
            pygame.K_DOWN: (1, 0)
        }

        if self.player.animator.animation != 'idle':
            return  # если игрок не покоится, то он не может начать новое действие
        if button not in buttons_keys.keys():
            return  # если нажали на неизвестную кнопку

        self.player.interaction(self, buttons_keys[button])  # взаимодействуем с объектом

    def enemies_move(self):
        """Движение врагов"""

        if self.player.animator.animation != 'idle':
            return  # если игрок что-то делает, то враги не начинают новых действий

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
                res.append(True)  # если враг уже совершает действие, то переходим к следущему врагу
                continue

            res.append(enemy.interaction(self, diff))  # добавляем результат взаимодействия с список

        if not any(res):  # если у всех врагов закончились очки действий
            self.turn = 1  # передаем ход игроку
            for enemy in self.enemies:  # обновляем очки действий у врагов
                enemy.action_points[0] = enemy.action_points[1]

    def show(self, surf):
        """Отображение на поверхность"""
        if self.turn == 2:
            self.enemies_move()

        surf.blit(self.background, apply((0, 0)))  # отображаем поле
        for entity in self.entities:  # отображаем существ
            entity.show(surf)
        for obj in self.objects:  # отображает объекты
            obj.show(surf)

        self.top_panel.show(surf)  # отображаем верхнюю
        self.bottom_panel.show(surf)  # и нижнюю панели

        for button in self.buttons:  # отображаем кнопки
            button.show(surf)

    def button_down(self, mouse_pos):
        """Нажатие мыши"""
        # получаем объект, на который нажали
        obj = self.get((mouse_pos[0] // TILE, (mouse_pos[1] - PANEL_HEIGHT) // TILE))
        if isinstance(obj, Enemy) and obj.alive:  # если нажали на врага
            self.bottom_panel.change_target(obj)  # меняем цель нижней панели
        else:
            # EDIT
            # This doesn't work
            self.bottom_panel.change_target(None)

        for button in self.buttons:  # проверяем нажатие на кнопки
            res = button.button_down(mouse_pos)
            if res:
                return res

    def key_down(self, button):
        """Нажатие на клавиатуру"""
        if self.turn == 1:  # если ход игрока
            self.player_move(button)  # то вызываем функцию движения игрока

