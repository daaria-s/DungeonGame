from objects import *
from entity import Player, Enemy
from functions import *
import random
from PIL import Image
from interface import Panel, Button, Element
import sqlite3
import pygame


class Room:
    def __init__(self, exit_, enemies, objects, num_of_room, enter=(0, 0)):
        self.num = num_of_room
        self.enter = enter
        self.exit_ = exit_

        self.enemies = enemies
        self.objects = objects
        self.opened = -1

    def enter_from_exit(self):
        if self.exit_[0] == 9:
            return 0, self.exit_[1]
        return self.exit_[0], 0

    def structure(self):
        map_ = [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
                ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]
        if self.num != 1:
            map_[self.enter[0]][self.enter[1]] = self.num - 1

        map_[self.exit_[0]][self.exit_[1]] = self.num + 1

        self.opened += 1
        return map_


class Dungeon(Element):

    def __init__(self):
        super().__init__()

        self.unused_keys = []
        self.first = True
        self.rooms = {}
        self.enemies = []
        self.objects = []
        self.base = []
        self.entities = []
        self.buttons = []
        self.user_name = ''

        self.background, self.top_panel, self.bottom_panel = None, None, None

        self.player = Player((1, 1), 10, 10, 1, 1, 3, 3)
        self.current_room = 1
        self.turn = 1

        self.change_room(1)

    def new(self):
        self.unused_keys = []
        self.rooms = {}
        self.enemies = []
        self.objects = []
        self.base = []
        self.entities = []
        self.buttons = []
        self.user_name = ''
        self.first = True

        self.background, self.top_panel, self.bottom_panel = None, None, None

        self.player = Player((1, 1), 10, 10, 1, 1, 3, 3)
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
        background = Image.new('RGB',
                               (len(level[0]) * TILE, len(level) * TILE),
                               (255, 255, 255))
        # собираем из маленьких изображений пустых клетов и стен
        # одно большое изображение поля чтобы потом отображать только его
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

        self.top_panel = Panel(self.player, 0)  # создаем верхнюю
        self.bottom_panel = Panel(None, 550)  # и нижнюю панели
        self.buttons = [  # создаем кнопки
            Button('game/panel/exit', (550, 10), 'menu'),
            Button('game/panel/inventory', (450, 10), 'inventory'),
            Button('game/panel/save', (500, 10), 'save')
        ]

    def generate_level(self, num):
        closed_cells = [self.player.position]
        enter = (0, 0)

        if num != 1:
            enter = self.rooms[num - 1].enter_from_exit()

        num1, num2 = (2, 4) if num < 4 else (3, 5)
        for i in range(random.randint(num1, num2)):
            x_pos, y_pos = random.randint(2, 9), random.randint(2, 8)
            while (x_pos, y_pos) in closed_cells:
                x_pos, y_pos = random.randint(2, 9), random.randint(2, 8)
            self.enemies.append(
                Enemy((x_pos, y_pos),
                      random.choice(['green', 'blue', 'purple', 'red']), 2, 2,
                      1, 1, 2, 2))
            closed_cells.append((x_pos, y_pos))

        for i in range(random.randint(6, 7)):
            x_pos, y_pos = random.randint(2, 8), random.randint(2, 7)
            while (x_pos, y_pos) in closed_cells:
                x_pos, y_pos = random.randint(2, 8), random.randint(2, 7)
            self.objects.append(Box((x_pos, y_pos)))
            closed_cells.append((x_pos, y_pos))

        a, b = (0, 2)
        for i in range(random.randint(a, b)):
            x_pos, y_pos = random.randint(1, 9), random.randint(2, 8)
            while (x_pos, y_pos) in closed_cells:
                x_pos, y_pos = random.randint(1, 9), random.randint(2, 8)
            self.objects.append(Chest((x_pos, y_pos), 'potion'))
            closed_cells.append((x_pos, y_pos))
        exit_ = random.choice(
            [(random.randint(2, 8), 11), (9, random.randint(2, 9))])

        if not random.randint(0, 2) and len(self.unused_keys) < 6:
            door_color = random.choice(['red', 'blue'])

            x_pos, y_pos = random.randint(1, 9), random.randint(1, 8)
            while (x_pos, y_pos) in closed_cells:
                x_pos, y_pos = random.randint(2, 9), random.randint(2, 8)
            self.objects.append(Chest((x_pos, y_pos), 'key', door_color))
            self.unused_keys.append(door_color)

        if not random.randint(0, 2) and self.unused_keys:
            self.objects.append(
                Door((exit_[1], exit_[0]), self.unused_keys.pop(
                    random.randint(0, len(self.unused_keys) - 1))))

        self.rooms[num] = Room(exit_, self.enemies, self.objects,
                               self.current_room,
                               enter=enter)

    def load(self, user_name):
        con = sqlite3.connect('dungeonBase.db')
        cur = con.cursor()

        player = cur.execute(f"""SELECT room_num, 
                hit_points, max_hit_points, 
                action_points, max_action_points,
                damage, max_damage, posX, posY FROM users 
                WHERE user_name = '{user_name}'""").fetchone()

        self.player = Player((player[-2], player[-1]), *player[1:-2])
        self.current_room = player[0]

        rooms = cur.execute(f"""SELECT id, number, enter_posX, 
                    enter_posY, exit_posX, exit_posY FROM rooms
                    WHERE user = '{user_name}'""").fetchall()

        self.rooms = {}
        for room in rooms:
            enemies = cur.execute(f"""SELECT color, hit_points, 
                        max_hit_points,
                        action_points, max_action_points, 
                        damage, max_damage, posX, posY FROM entities
                        WHERE room_id = {room[0]}""").fetchall()

            list_of_enemies = []
            for i in enemies:
                list_of_enemies.append(Enemy((i[-2], i[-1]), *i[:-2]))
            self.rooms[room[1]] = Room(room[-2:], list_of_enemies, [], room[1],
                                       room[2:4])

        self.enemies = self.rooms[self.current_room].enemies
        self.entities = [self.player, *self.enemies]
        self.objects = []
        self.load_room(player[0])

    def add_room(self):
        pass

    def save(self, user_name):
        con = sqlite3.connect(DATABASE_NAME)
        cur = con.cursor()
        if (user_name,) in cur.execute("""SELECT user_name 
        FROM users""").fetchall():
            pass
        else:
            cur.execute(
                f"""INSERT INTO users(user_name, room_num, 
                hit_points, max_hit_points, 
                action_points, max_action_points,
                damage, max_damage, posX, posY)
                values('{user_name}', {self.current_room}, 
                {self.player.hit_points[0]}, {self.player.hit_points[1]}, 
                {self.player.action_points[0]}, {self.player.action_points[1]}, 
                {self.player.damage[0]},{self.player.damage[1]},
                {self.player.position[0]}, 
                {self.player.position[1]})""")
            con.commit()

            for obj in self.player.inventory:
                cur.execute(f"""INSERT INTO inventory(user, type, used)
                values({user_name}, {obj}, True)""")

            # print(self.unused_keys)
            for obj in self.unused_keys:
                cur.execute(f"""INSERT INTO inventory(user, type, used)
                values({user_name}, {obj}, False)""")
            for n, room in self.rooms.items():
                cur.execute(f"""INSERT INTO rooms(number, enter_posX, 
                    enter_posY, exit_posX, exit_posY, user) 
                    values({n}, {room.enter[0]}, {room.enter[1]}, 
                    {room.exit_[0]}, {room.exit_[1]}, '{user_name}')""")
                con.commit()
                id_ = cur.execute(f"""SELECT id FROM rooms 
                    WHERE user = '{user_name}' 
                    AND number = {n}""").fetchone()[0]
                for enemy in room.enemies:
                    if enemy.alive:
                        cur.execute(f"""INSERT INTO entities(hit_points, 
                        max_hit_points,
                        action_points, max_action_points, 
                        damage, max_damage, posX, posY, room_id, color)
                        values({enemy.hit_points[0]}, {enemy.hit_points[1]},
                        {enemy.action_points[0]}, {enemy.action_points[1]},
                        {enemy.damage[0]}, {enemy.damage[1]}, 
                        {enemy.position[0]}, {enemy.position[1]}, {id_}, 
                        '{enemy.color}')""")

                for obj in room.objects:
                    if obj.name == 'box':
                        cur.execute(f"""INSERT INTO objects(type, posX, posY, 
                        room_id) 
                        values(1, {obj.position[0]}, 
                        {obj.position[1]}, {id_})""")
                    elif obj.name == 'door':
                        if not obj.stage:
                            cur.execute(f"""INSERT INTO objects(type, posX, 
                            posY, room_id, color) values(3, {obj.position[0]}, 
                            {obj.position[1]}, {id_}, {obj.color})""")

                con.commit()

    def get(self, coordinates, diff=(0, 0)):
        """Возвращает объект по координатам"""
        for entity in [*self.entities, *self.objects, *self.base]:
            if entity.position == (coordinates[0] + diff[1],
                                   coordinates[1] + diff[0]):
                return entity

    def player_move(self, button):
        """Движение игрока"""

        # словарь вида {кнопка: (смещение на X и Y)}
        buttons_keys = {
            pygame.K_LEFT: (0, -1),
            pygame.K_RIGHT: (0, 1),
            pygame.K_UP: (-1, 0),
            pygame.K_DOWN: (1, 0)
        }

        if any([i.animator.animation not in ['idle', 'die'] for i in
                self.enemies]):
            # если враги еще совершают какие-то действия, то игрок стоит
            return
        if self.player.animator.animation != 'idle':
            # если игрок совершает какое-то действие, то
            # мы не начинаем новое действие
            return
        if button not in buttons_keys.keys():
            return  # если нажали на неизвестную кнопку

        # взаимодействуем с объектом
        self.player.interaction(self, buttons_keys[button])

    def enemies_move(self):
        """Движение врагов"""

        if self.player.animator.animation != 'idle':
            return
            # если игрок что-то делает, то враги не начинают новых действий

        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []
        blocked_cells = []

        for enemy in self.enemies:
            if not enemy.alive:
                # текущий враг метрв, то переходим к следущему врагу
                continue

            if enemy.animator.animation != 'idle':
                res.append(True)
                # если враг уже совершает действие,
                # то переходим к следущему врагу
                continue

            checking = []
            for i in options:
                checking.append(
                    self.get(enemy.position, i).name in ('player', 'empty'))
            if not any(checking):  # если врагу некуда идти
                res.append(False)
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

            # EDIT
            while (enemy_pos[0] + diff[0], enemy_pos[1] + diff[1]) in blocked_cells or not isinstance(self.get(enemy_pos, diff), (Player, Empty)):
                diff = options[random.randint(0, len(options) - 1)]

            blocked_cells.append(
                (enemy_pos[0] + diff[0], enemy_pos[1] + diff[1]))

            # добавляем результат взаимодействия с список
            res.append(enemy.interaction(self, diff))

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
        obj = self.get(
            (mouse_pos[0] // TILE, (mouse_pos[1] - PANEL_HEIGHT) // TILE))
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
        if button == pygame.K_0:
            USER_NAME = input()
            self.save(USER_NAME)
        if self.turn == 1:  # если ход игрока
            self.player_move(button)  # то вызываем функцию движения игрока
