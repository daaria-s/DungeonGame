import pygame
import config
from config import *
from animator import Animator
from functions import *
import random


class Entity:

    def __init__(self, position, name, path,
                 hit_points, max_hit_points,
                 min_damage, max_damage,
                 action_points, max_action_points):
        self.position = position  # позиция
        self.name = name  # имя

        self.action_points = [action_points, max_action_points]  # очки действий [текущие, максимальные]
        self.damage = [min_damage, max_damage]  # урон [минимальный, максимальный]
        self.hit_points = [hit_points, max_hit_points]  # здоровье [текущее, максимальное]

        self.alive = True  # живо ли существо
        self.animator = Animator('Sprites/' + path)  # аниматор

    def show(self, surf):
        """Отображение на поверхности"""
        image, shift = self.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))

    def get_direction(self, obj):
        """Получение текстового представления направления до соседнего объекта"""
        movement_keys = {
            (1, 0): 'left',
            (-1, 0): 'right',
            (0, 1): 'up',
            (0, -1): 'down'
        }
        return movement_keys[(self.position[0] - obj.position[0], self.position[1] - obj.position[1])]

    def interaction(self, dungeon_, movement):
        """Взаимодействие с другим объектом"""
        target = dungeon_.get(self.position, movement)  # получаем цель взаимодействия
        if not target or self.action_points[0] == 0:
            return False  # если цели нет или закончиличь очки действий ничего не делаем

        # словарь вида [имя объекта взаимодействия: [функция взаимодействия, аргументы для этой функции]]
        keys = {
            'enemy': [self.interaction_entity, [target]],
            'player': [self.interaction_entity, [target]],
            'empty': [self.interaction_empty, [target]],
            'wall': [lambda: False, []],
            'box': [self.interaction_box, [dungeon_, movement]],
            'chest': [self.interaction_chest, [target]],
            'teleport': [self.interaction_teleport, [target]]
        }
        if keys[target.name][0](*keys[target.name][1]):  # если взаимодействие прошло успешно
            self.action_points[0] -= 1  # уменьшаем количество очков действий
            if self.action_points[0] == 0 and dungeon_.turn == 1:  # если закончился ход игрока
                self.action_points[0] = self.action_points[1]  # то передаем ход врагам
                dungeon_.turn = 2
            return True  # возвращаем True для индикации успещности взаимодействия

    def interaction_entity(self, obj):
        """Взаимодействие с существами"""
        # EDIT
        if obj.hit_points[0] <= 0:  # если существо мертво, то просто перемещаемся в нужную точу
            self.animator.start('move_' + self.get_direction(obj))
            self.position = obj.position
        else:  # если существо живо, то атакуем его
            self.animator.start('attack_' + self.get_direction(obj))
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

    def get_hit(self, damage):
        """Получение урона"""
        # отнимаем случайное количество жизней в рамках урона
        self.hit_points[0] -= random.randint(damage[0], damage[1])
        if self.hit_points[0] <= 0:  # если жизней меньше 0
            self.die()  # то существо умирает

    def die(self):
        """Смерть существа"""
        self.alive = False
        self.animator.start('die')  # включаем анимацию смерти


class Player(Entity):
    """Класс игрока"""

    def __init__(self, position,
                 hit_points, max_hit_points,
                 min_damage, max_damage,
                 action_points, max_action_points):
        super().__init__(position, 'player', 'player',
                         hit_points, max_hit_points,
                         min_damage, max_damage,
                         action_points, max_action_points)
        # EDIT: fix
        self.inventory = ['red_key'] * 10  # у игрока есть инвентарь

    def interaction_box(self, dungeon_, movement):
        """Взаимодействие с коробкой"""
        # получаем клетку, в которую должна подвинуться коробка
        next_cell = dungeon_.get(self.position, (movement[0] * 2, movement[1] * 2))
        if next_cell and next_cell.name == 'empty':  # если клетка свободна
            box = dungeon_.get(self.position, movement)  # получаем коробку
            self.interaction_empty(box)  # двигаем игрока
            box.move((self.position[0] + movement[1], self.position[1] + movement[0]),
                     self.get_direction(next_cell))  # двигаем коробку
            return True

    def interaction_chest(self, obj):
        """Взаимодействие с сундуком"""
        self.animator.start('attack_' + self.get_direction(obj))  # включаем анимацию атаки
        res = obj.touch()  # вызываем функцию касания сундука
        if res == '__empty__':  # если сундук пуст
            self.interaction_empty(obj)  # то перемещаемся в эту клетку
            return True
        elif res:
            self.inventory.append(res)  # если в сундуке что-то есть, добавляем в свой инвентарь
            return True

    def interaction_teleport(self, obj):
        """Взаимодействие с телепортом"""
        if (self.position[1], self.position[0]) == obj.rooms[obj.current_room].exit_:
            obj.change_room(obj.current_room + 1)
        elif obj.current_room != 1 and (self.position[1], self.position[0]) == obj.rooms[obj.current_room].enter:
            obj.change_room(obj.current_room - 1)
        pass

    def die(self):
        super().die()
        config.LOSE_COUNTER = 56


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
