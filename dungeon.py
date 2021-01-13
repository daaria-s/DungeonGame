from objects import *
from entity import Player, Enemy
from config import *
import config
import random
from PIL import Image
from interface import Button, Panel, Element
import sqlite3
import pygame


class Room:
    """класс комнаты подземелья"""

    def __init__(self, exit_, enemies, objects, num_of_room, enter=(0, 0)):
        self.num = num_of_room
        self.enter = tuple(enter)
        self.exit_ = tuple(exit_)  # вход и выход из данной комнаты

        self.enemies = enemies
        self.objects = objects

    def enter_from_exit(self):  # трансформирует выход во вход для след двери
        if self.exit_[0] == 9:
            return 0, self.exit_[1]
        return self.exit_[0], 0

    def structure(self):  # возвращает карту в виде списка
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
        if self.num != 1:  # если не первая комната, то есть существует вход
            map_[self.enter[0]][self.enter[1]] = self.num - 1

        map_[self.exit_[0]][self.exit_[1]] = self.num + 1
        return map_


class Dungeon(Element):
    """класс подземелья"""

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
        self.con = sqlite3.connect(DATABASE)

        self.background, self.top_panel, self.bottom_panel = None, None, None

        self.player = Player((1, 1), 5, 5, 1, 1, 3, 3, 0, 255)
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

        self.player = Player((1, 1), 5, 5, 1, 1, 3, 3, 0, 255)
        self.current_room = 1
        self.turn = 1

        self.change_room(1)

    def change_room(self, num):  # смена комнаты, в которой находится игрок
        self.enemies = []
        self.objects = []
        self.base = []

        if num not in self.rooms.keys():
            # если следующей комнаты не существует
            self.generate_level(num)
        else:
            self.enemies = self.rooms[num].enemies
            self.objects = self.rooms[num].objects

        if self.first:
            # если запустили первый раз
            self.player.position = (1, 1)
            self.first = False
        elif num > self.current_room:  # смотрим, откуда пришел игрок
            self.player.position = self.rooms[num].enter[1], \
                                   self.rooms[num].enter[0]
        else:
            self.player.position = self.rooms[num].exit_[1], \
                                   self.rooms[num].exit_[0]

        self.current_room = num
        self.entities = [self.player, *self.enemies]
        self.load_room(self.current_room)

    def load_room(self, num_of_room):  # загрузка комнаты на экран
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
            Button('game/panel/save', (500, 10), 'save'),
        ]

    def generate_enemies(self, room):
        patterns = [
            ['blue', 2, 2, 1, 1, 2, 2],
            ['green', 3, 3, 1, 2, 2, 2],
            ['red', 3, 3, 2, 2, 2, 2],
            ['purple', 4, 4, 2, 3, 3, 3],
        ]
        if room == 1:
            a = random.randint(2, 4)
            enemy_number = [a, 4 - a, 0, 0]
        elif 2 <= room <= 5:
            a = random.randint(3, 4)
            enemy_number = [4 - a, a, 0, 0]
        elif 6 <= room <= 9:
            a = random.randint(2, 3)
            enemy_number = [1, a, 3 - a, 0]
        elif 10 <= room <= 14:
            a = random.randint(3, 5)
            enemy_number = [0, 5 - a, a, 0]
        elif 15 <= room <= 20:
            a = random.randint(3, 4)
            enemy_number = [0, 4 - a, a, 1]
        elif room > 20:
            a = random.randint(4, 5)
            enemy_number = [0, 0, 6 - a, a]

        return [patterns[i] for i in range(len(patterns)) for _ in
                range(enemy_number[i])]

    def generate_level(self, num):  # генерация уровня игры (карты)
        closed_cells = [self.player.position]
        enter = (0, 0)

        if num != 1:
            enter = self.rooms[num - 1].enter_from_exit()

        enemies_options = self.generate_enemies(num)
        for i in range(len(enemies_options)):  # генерация врагов
            x, y = random.randint(2, 9), random.randint(2, 8)
            while (x, y) in closed_cells:
                x, y = random.randint(2, 9), random.randint(2, 8)
            self.enemies.append(Enemy((x, y), *enemies_options[i]))
            closed_cells.append((x, y))

        for i in range(random.randint(6, 7)):  # генерация коробок
            x, y = random.randint(2, 8), random.randint(2, 7)
            while (x, y) in closed_cells:
                x, y = random.randint(2, 8), random.randint(2, 7)
            self.objects.append(Box((x, y)))
            closed_cells.append((x, y))

        a, b = (0, 2)
        for i in range(random.randint(a, b)):  # генерация зельев для здоровья
            x, y = random.randint(1, 9), random.randint(2, 8)
            while (x, y) in closed_cells:
                x, y = random.randint(1, 9), random.randint(2, 8)
            self.objects.append(Chest((x, y), 'potion', 'green'))
            closed_cells.append((x, y))
        exit_ = random.choice(
            [(random.randint(2, 8), 11), (9, random.randint(2, 9))])

        if num > 6:  # генерация зельев для повышения силы или количества ходов
            x, y = random.randint(1, 9), random.randint(2, 8)
            while (x, y) in closed_cells:
                x, y = random.randint(1, 9), random.randint(2, 8)
            self.objects.append(
                Chest((x, y), 'potion', random.choice(['red', 'blue'])))
            closed_cells.append((x, y))

        if not random.randint(0, 2) and len(self.unused_keys) < 6:
            # генерация двери, если неиспользованных ключей меньше 6
            door_color = random.choice(['red', 'blue', 'green'])

            x, y = random.randint(1, 9), random.randint(1, 8)
            while (x, y) in closed_cells:
                x, y = random.randint(2, 9), random.randint(2, 8)
            self.objects.append(Chest((x, y), 'key', door_color))
            self.unused_keys.append(door_color)

        if not random.randint(0, 2) and self.unused_keys:
            # добавится ли дверь в текущую комнату
            self.objects.append(
                Door((exit_[1], exit_[0]), self.unused_keys.pop(
                    random.randint(0, len(self.unused_keys) - 1))))

        self.rooms[num] = Room(exit_, self.enemies, self.objects,
                               num, enter)

    def load(self, user_name):  # загрузка игры с базы
        cur = self.con.cursor()
        self.user_name = user_name

        player = cur.execute(f"""SELECT room_num, 
            hit_points, max_hit_points, 
            damage, max_damage, 
            action_points, max_action_points,
            posX, posY, experience, max_experience FROM users 
            WHERE user_name = '{user_name}'""").fetchone()
        # все харастеристикик игрока

        self.unused_keys = list(map(lambda i: i[0], cur.execute(f"""SELECT type
            FROM inventory 
            WHERE user = '{user_name}' AND used = 'False'""")))

        self.player = Player((player[-4], player[-3]), *player[1:-4],
                             *player[-2:])  # игрок

        self.player.inventory = list(map(lambda i: i[0], cur.execute(f"""SELECT
            type FROM inventory 
            WHERE user = '{user_name}' AND used = 'True'""")))
        self.current_room = player[0]

        rooms = cur.execute(f"""SELECT id, number, enter_posX, 
                    enter_posY, exit_posX, exit_posY FROM rooms
                    WHERE user = '{user_name}'""").fetchall()

        self.rooms = {}
        for room_id, number, *positions in rooms:  # все комнаты подземелья
            enemies = cur.execute(f"""SELECT color, hit_points, 
                        max_hit_points,
                        action_points, max_action_points, 
                        damage, max_damage, posX, posY FROM entities
                        WHERE room_id = {room_id}""").fetchall()

            list_of_enemies = []
            list_of_objects = []
            # все враги на карте
            for color, hit, m_hit, act, m_act, dam, m_dam, x, y in enemies:
                list_of_enemies.append(
                    Enemy((x, y), color, hit, m_hit, dam, m_dam, act, m_act))

            objects = cur.execute(f"""SELECT type, posX, posY, inside, color 
                FROM objects
                WHERE room_id = {room_id}""").fetchall()

            for type_, x, y, inside, color in objects:  # все объекты на карте
                if type_ == 1:  # коробки
                    list_of_objects.append(Box((x, y)))
                elif type_ == 2:  # сундуки
                    list_of_objects.append(
                        Chest((x, y), *reversed(inside.split('_'))))
                else:  # двери
                    list_of_objects.append(Door((x, y), color))

            self.rooms[number] = Room(positions[-2:], list_of_enemies,
                                      list_of_objects,
                                      number,
                                      positions[:2])

        self.enemies = self.rooms[self.current_room].enemies
        self.entities = [self.player, *self.enemies]
        self.objects = self.rooms[self.current_room].objects
        self.load_room(player[0])

    def save_room(self, n):  # сохранение 1 комнаты в базе
        cur = self.con.cursor()
        room_id = cur.execute(f"""SELECT id FROM rooms 
            WHERE number = {n} and user = '{self.user_name}'""").fetchone()[0]
        room = self.rooms[n]
        for enemy in room.enemies:
            if enemy.alive:
                cur.execute(f"""INSERT INTO entities(hit_points, 
                max_hit_points,
                action_points, max_action_points, 
                damage, max_damage, posX, posY, room_id, color)
                values({enemy.hit_points[0]}, {enemy.hit_points[1]},
                {enemy.action_points[0]}, {enemy.action_points[1]},
                {enemy.damage[0]}, {enemy.damage[1]}, 
                {enemy.position[0]}, {enemy.position[1]}, {room_id}, 
                '{enemy.color}')""")

        for obj in room.objects:  # объекты комнаты
            if obj.name == 'box':
                cur.execute(f"""INSERT INTO objects(type, posX, posY, 
                room_id) 
                values(1, {obj.position[0]}, 
                {obj.position[1]}, {room_id})""")
            elif not obj.stage:  # если объект активен
                if obj.name == 'chest':
                    cur.execute(f"""INSERT INTO objects(type, posX, 
                        posY, room_id, inside) values(2, {obj.position[0]}, 
                        {obj.position[1]}, {room_id}, '{obj.inside.name}')""")
                elif obj.name == 'door':
                    cur.execute(f"""INSERT INTO objects(type, posX, 
                        posY, room_id, color) values(3, {obj.position[0]}, 
                        {obj.position[1]}, {room_id}, '{obj.color}')""")
            self.con.commit()

    def update_base(self):
        # обновление базы (если имя пользователя уже вводилось)
        cur = self.con.cursor()
        cur.execute(
            f"""UPDATE users
                    SET room_num = {self.current_room},
                    hit_points = {self.player.hit_points[0]}, 
                    max_hit_points = {self.player.hit_points[1]}, 
                    action_points = {self.player.action_points[0]}, 
                    max_action_points = {self.player.action_points[1]},
                    damage = {self.player.damage[0]}, 
                    max_damage = {self.player.damage[1]}, 
                    posX = {self.player.position[0]}, 
                    posY = {self.player.position[1]}, 
                    experience = '{self.player.experience[0]}', 
                    max_experience = '{self.player.experience[1]}'
                    WHERE user_name = '{self.user_name}'""")
        self.con.commit()

        cur.execute("""DELETE FROM inventory 
        WHERE user = '{self.user_name}'""")  # удаление старого инвентаря

        for obj in self.player.inventory:
            cur.execute(f"""INSERT INTO inventory(user, type, used)
            values('{self.user_name}', '{obj}', 'True')""")

        for obj in self.unused_keys:
            cur.execute(f"""INSERT INTO inventory(user, type, used)
            values('{self.user_name}', '{obj}', 'False')""")

        self.con.commit()

        for n, room in self.rooms.items():
            # если в комнату заходили, то есть могли изменяться
            # положения врагов, объектов и тд
            room_id = cur.execute(f"""SELECT id FROM rooms 
                    WHERE number = {n} 
                    and user = '{self.user_name}'""").fetchone()[0]

            cur.execute(f"""DELETE FROM entities 
                    WHERE room_id = {room_id}""")

            self.con.commit()

            cur.execute(f"""DELETE FROM objects 
                    WHERE room_id = {room_id}""")

            self.con.commit()
            self.save_room(n)

    def save(self, user_name):  # функция сохранения базы
        cur = self.con.cursor()
        self.user_name = user_name if not self.user_name else self.user_name
        cur.execute(
            f"""INSERT INTO users(user_name, room_num, 
            hit_points, max_hit_points, 
            action_points, max_action_points,
            damage, max_damage, posX, posY, experience, max_experience)
            values('{self.user_name}', {self.current_room}, 
            {self.player.hit_points[0]}, {self.player.hit_points[1]}, 
            {self.player.action_points[0]}, {self.player.action_points[1]}, 
            {self.player.damage[0]},{self.player.damage[1]},
            {self.player.position[0]}, 
            {self.player.position[1]},
            '{self.player.experience[0]}', '{self.player.experience[1]}')""")
        # добавление нового пользователя со всеми характеристиками
        self.con.commit()

        for obj in self.player.inventory:  # добавление инвентаря игрока
            cur.execute(f"""INSERT INTO inventory(user, type, used)
            values('{self.user_name}', '{obj}', 'True')""")

        for obj in self.unused_keys:  # добавляются неиспользованные ключи
            cur.execute(f"""INSERT INTO inventory(user, type, used)
            values('{self.user_name}', '{obj}', 'False')""")

        for n, room in self.rooms.items():
            cur.execute(f"""INSERT INTO rooms(number, enter_posX, 
            enter_posY, exit_posX, exit_posY, user) 
            values({n}, {room.enter[0]}, {room.enter[1]}, 
            {room.exit_[0]}, {room.exit_[1]}, '{self.user_name}')""")
            self.con.commit()
            self.save_room(n)  # добавление каждой комнаты в базу

    def get(self, coordinates, diff=(0, 0)):
        """Возвращает объект по координатам"""
        for obj in [*self.entities, *self.objects, *self.base]:
            if obj.position == (coordinates[0] + diff[1],
                                coordinates[1] + diff[0]):
                if getattr(obj, 'alive', True):
                    return obj

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

        # проверяем на нахождение в телепорте
        self.player.interaction_teleport(self)
        # взаимодействуем с объектом
        obj = self.get(self.player.position, buttons_keys[button])
        obj_name = obj.name
        self.player.interaction(self, buttons_keys[button])
        if obj_name == 'enemy' and not obj.alive:
            self.player.experience[0] += 1
            if self.player.experience[0] > self.player.experience[1]:
                config.NEXT_WINDOW = 'win'

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

            player_pos = self.player.position
            enemy_pos = enemy.position
            if random.randint(0, 1):  # генерация ходов врага
                # враг пытается приблизиться к игроку
                if enemy_pos[0] != player_pos[0]:
                    diff = (0, -1) if enemy_pos[0] > player_pos[0] else (0, 1)
                elif enemy_pos[1] != player_pos[1]:
                    diff = (-1, 0) if enemy_pos[1] > player_pos[1] else (1, 0)
            else:
                if enemy_pos[1] != player_pos[1]:
                    diff = (-1, 0) if enemy_pos[1] > player_pos[1] else (1, 0)
                elif enemy_pos[0] != player_pos[0]:
                    diff = (0, -1) if enemy_pos[0] > player_pos[0] else (0, 1)

            while (enemy_pos[0] + diff[0],
                   enemy_pos[1] + diff[1]) in blocked_cells or \
                    self.get(enemy_pos, diff).name not in ('empty', 'player'):
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
        for obj in self.objects:  # отображаем объекты
            obj.show(surf)

        self.top_panel.show(surf)  # отображаем верхнюю
        self.bottom_panel.show(surf)  # и нижнюю панели

        for elem in self.buttons:  # отображаем кнопки
            elem.show(surf)

    def button_down(self, mouse_pos):
        """Нажатие мыши"""
        # получаем объект, на который нажали
        obj = self.get(
            (mouse_pos[0] // TILE, (mouse_pos[1] - PANEL_HEIGHT) // TILE))
        if isinstance(obj, Enemy) and obj.alive:  # если нажали на врага
            self.bottom_panel.change_target(obj)  # меняем цель нижней панели
        else:
            self.bottom_panel.change_target(None)

        for elem in self.buttons:  # проверяем нажатие на кнопки
            elem.button_down(mouse_pos)

    def key_down(self, key):
        """Нажатие на клавиатуру"""
        for elem in self.buttons:
            elem.key_down(key)
        if self.turn == 1:  # если ход игрока
            self.player_move(key)  # то вызываем функцию движения игрока
