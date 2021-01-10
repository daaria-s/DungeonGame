from objects import *
from entity import Player, Enemy
import config
from functions import *
import random
from PIL import Image
from interface import Panel, Button, Element


class UnknownMapSymbol(Exception):
    pass


class Dungeon(Element):
    """Класс подземелья"""

    def __init__(self):
        super().__init__()
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

        self.player = Player((1, 1), 5, 5, 1, 1, 5, 5)  # создаем игрока
        self.enemies = [  # создаем врагов
          Enemy((5, 2), 'blue', 2, 2, 1, 1, 3, 3),
          Enemy((3, 4), 'blue', 2, 2, 1, 1, 3, 3),
          Enemy((7, 1), 'blue', 2, 2, 1, 1, 3, 3),
        ]

        self.entities = [self.player, *self.enemies]

        self.objects = [  # создаем объекты
            Box((1, 4)),
            Chest((2, 4)),
        ]
        self.base = []  # список объектов "пустая клетка" и "стена"
        empty = Image.open('Sprites/ground/idle/00.png')  # открываем изображения
        wall = Image.open('Sprites/wall/idle/00.png')  # пустой клетки и стены
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

        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # возможные варианты движения врагов
        res = []  # список результатов взаимодействия
        # blocked_cells = []

        for enemy in self.enemies:  # проходим по всем врагам
            if not enemy.alive:  # если враг мертв, то пропускаем его
                continue

            diff = options[random.randint(0, len(options) - 1)]  # выбираем смещение случанйм образом
            # EDIT
            # This code doesn't work
            # player_pos = self.player.position
            # enemy_pos = enemy.position
            # if random.randint(0, 1):
            #     if enemy_pos[0] != player_pos[0]:
            #         diff = (-1, 0) if enemy_pos[0] > player_pos[0] else (1, 0)
            #     elif enemy_pos[1] != player_pos[1]:
            #         diff = (0, -1) if enemy_pos[1] > player_pos[1] else (0, 1)
            # else:
            #     if enemy_pos[1] != player_pos[1]:
            #         diff = (0, -1) if enemy_pos[1] > player_pos[1] else (0, 1)
            #     elif enemy_pos[0] != player_pos[0]:
            #         diff = (-1, 0) if enemy_pos[0] > player_pos[0] else (1, 0)
            # while (enemy_pos[0] + diff[0], enemy_pos[1] + diff[1]) in blocked_cells:
            #     diff = options[random.randint(0, len(options) - 1)]
            #
            # blocked_cells.append((enemy_pos[0] + diff[0], enemy_pos[1] + diff[1]))

            if enemy.animator.animation != 'idle':
                res.append(True)  # если враг уже совершает действие, то переходим к следущему врагу
                continue

            res.append(enemy.interaction(self, diff))  # добавляем результат взаимодействия с список

        if not any(res):  # если у всех врагов закончились очки действий
            config.TURN = 1  # передаем ход игроку
            for enemy in self.enemies:  # обновляем очки действий у врагов
                enemy.action_points[0] = enemy.action_points[1]

    def show(self, surf):
        """Отображение на поверхность"""
        if config.TURN == 2:  # если ход врагов
            self.enemies_move()  # то вызываем функцию их движения

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
        if config.TURN == 1:  # если ход игрока
            self.player_move(button)  # то вызываем функцию движения игрока
