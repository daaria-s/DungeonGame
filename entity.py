import config
from objects import GameObject
import random
from config import *


class Entity(GameObject):

    def __init__(self, position, name, path,
                 hit_points, max_hit_points,
                 min_damage, max_damage,
                 action_points, max_action_points):
        super().__init__(path, position, name)

        self.action_points = [action_points, max_action_points]
        self.damage = [min_damage, max_damage]
        self.hit_points = [hit_points, max_hit_points]

        self.alive = True
        self.inventory = []

    def get_direction(self, obj):
        """Получение представления направления до соседнего объекта"""
        movement_keys = {
            (1, 0): 'left',
            (-1, 0): 'right',
            (0, 1): 'up',
            (0, -1): 'down'
        }
        return movement_keys[
            (self.position[0] - obj.position[0],
             self.position[1] - obj.position[1])]

    def interaction(self, dungeon_, movement):
        """Взаимодействие с другим объектом"""
        target = dungeon_.get(self.position,
                              movement)  # получаем цель взаимодействия
        if not target or self.action_points[0] == 0:
            return False
            # если цели нет или закончились очки действий ничего не делаем

        # словарь вида [имя объекта взаимодействия:
        # [функция взаимодействия, аргументы для этой функции]]
        keys = {
            'enemy': [self.interaction_entity, [target]],
            'player': [self.interaction_entity, [target]],
            'empty': [self.interaction_empty, [target]],
            'wall': [lambda: False, []],
            'box': [self.interaction_box, [dungeon_, movement]],
            'chest': [self.interaction_chest, [target]],
            'door': [self.interaction_door, [target]]
        }
        if keys[target.name][0](
                *keys[target.name][1]):  # если взаимодействие прошло успешно
            self.action_points[0] -= 1  # уменьшаем количество очков действий
            # если закончился ход игрока
            if self.action_points[0] == 0 and dungeon_.turn == 1:
                self.action_points[0] = self.action_points[1]
                dungeon_.turn = 2  # то передаем ход врагам
            # возвращаем True для индикации успещности взаимодействия
            return True

    def interaction_entity(self, obj):
        """Взаимодействие с существами"""
        # EDIT
        if obj.hit_points[0] <= 0:
            # если существо мертво, то просто перемещаемся в нужную точу
            self.animator.start('move_' + self.get_direction(obj))
            self.position = obj.position
        else:  # если существо живо, то атакуем его
            self.animator.start('attack_' + self.get_direction(obj))
            music.play_sound('hit')
            obj.get_hit(self.damage)
        return True

    def interaction_empty(self, obj):
        """Взаимодействие с пустой клеткой"""
        self.animator.start('move_' + self.get_direction(obj))
        self.position = obj.position
        return True

    def interaction_box(self, dungeon_, movement):
        """Взаимодействие с коробкой"""
        pass

    def interaction_chest(self, obj):
        """Взаимодействие с сундуком"""
        pass

    def interaction_teleport(self, obj):
        """Взаимодействие с телепортом"""
        pass

    def interaction_door(self, obj):
        pass

    def get_hit(self, damage):
        """Получение урона"""
        # отнимаем случайное количество жизней в рамках урона
        self.hit_points[0] -= random.randint(damage[0], damage[1])
        if self.inventory:
            while 'green_potion' in self.inventory and self.hit_points[0] < \
                    self.hit_points[1]:
                self.hit_points[0] += 1
                self.inventory.remove('green_potion')
        if self.hit_points[0] <= 0:
            self.die()

    def die(self):
        """Смерть существа"""
        self.alive = False
        self.name = 'empty'
        self.animator.start('die')  # включаем анимацию смерти


class Player(Entity):
    """Класс игрока"""

    def __init__(self, position,
                 hit_points, max_hit_points,
                 min_damage, max_damage,
                 action_points, max_action_points, experience, max_experience):
        super().__init__(position, 'player', 'player',
                         hit_points, max_hit_points,
                         min_damage, max_damage,
                         action_points, max_action_points)
        self.experience = [experience, max_experience]

    def new_inventory(self, object_):
        if object_ == 'green_potion' and \
                self.hit_points[0] < self.hit_points[1]:
            self.hit_points[0] += 1
        elif object_ == 'red_potion':
            self.damage[0] += 1
            self.damage[1] += 1
            # максимум 3 урона
            if self.damage[0] == 4:
                self.damage[0] = 3
                self.damage[1] = 3
        elif object_ == 'blue_potion':
            self.action_points[1] += 1
            # максимум 9 очков действий
            if self.action_points[1] == 10:
                self.action_points[1] = 9
        elif len(self.inventory) < 20:
            self.inventory.append(object_)

    def interaction_box(self, dungeon_, movement):
        """Взаимодействие с коробкой"""
        # получаем клетку, в которую должна подвинуться коробка
        next_cell = dungeon_.get(self.position,
                                 (movement[0] * 2, movement[1] * 2))
        if next_cell and next_cell.name == 'empty':  # если клетка свободна
            box = dungeon_.get(self.position, movement)  # получаем коробку
            self.interaction_empty(box)  # двигаем игрока
            box.move((self.position[0] + movement[1],
                      self.position[1] + movement[0]),
                     self.get_direction(next_cell))
            return True

    def interaction_chest(self, obj):
        """Взаимодействие с сундуком"""
        self.animator.start('attack_' + self.get_direction(obj))
        res = obj.touch()
        if res == '__empty__':
            self.interaction_empty(obj)
        else:
            music.play_sound('hit')
            if res:
                self.new_inventory(res)
        return True

    def interaction_door(self, obj):
        """Взаимодействие с дверью"""
        self.animator.start('attack_' + self.get_direction(obj))
        res = obj.touch(obj.color + '_key' in self.inventory)
        if obj.color + '_key' in self.inventory:  # если есть подходящий ключ
            self.inventory.remove(obj.color + '_key')
            music.play_sound('hit')
        if res == '__empty__':
            self.interaction_empty(obj)
        return True

    def interaction_teleport(self, dungeon_):
        """Взаимодействие с телепортом"""
        # если игрок находится на входе или выходе

        if (self.position[1], self.position[0]) == \
                dungeon_.rooms[dungeon_.current_room].exit_:
            dungeon_.change_room(dungeon_.current_room + 1)
        elif dungeon_.current_room != 1 and \
                (self.position[1], self.position[0]) == \
                dungeon_.rooms[dungeon_.current_room].enter:
            dungeon_.change_room(dungeon_.current_room - 1)

    def die(self):
        super().die()
        config.NEXT_WINDOW = 'lose'


class Enemy(Entity):
    """Класс врага"""

    def __init__(self, position, color,
                 hit_points, max_hit_points,
                 min_damage, max_damage,
                 action_points, max_action_points):
        super().__init__(position, 'enemy', 'enemies/' + color,
                         hit_points, max_hit_points,
                         min_damage, max_damage,
                         action_points, max_action_points)
        self.color = color  # цвет врага
