import config
from objects import GameObject
import random


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
            'teleport': [self.interaction_teleport, [target]],
            'door': [self.interaction_door, [target]]
        }
        if keys[target.name][0](
                *keys[target.name][1]):  # если взаимодействие прошло успешно
            self.action_points[0] -= 1  # уменьшаем количество очков действий
            if self.action_points[0] == 0 and\
                    dungeon_.turn == 1:  # если закончился ход игрока
                self.action_points[0] = self.action_points[
                    1]  # то передаем ход врагам
                dungeon_.turn = 2
            return True
            # возвращаем True для индикации успещности взаимодействия

    def interaction_entity(self, obj):
        """Взаимодействие с существами"""
        # EDIT
        if obj.hit_points[0] <= 0:
            # если существо мертво, то просто перемещаемся в нужную точу
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

    def interaction_door(self, obj):
        pass

    def get_hit(self, damage):
        """Получение урона"""
        # отнимаем случайное количество жизней в рамках урона
        self.hit_points[0] -= random.randint(damage[0], damage[1])
        if self.inventory:
            if 'green_potion' in self.inventory:
                self.hit_points[0] += 1
                self.inventory.remove('green_potion')
        if self.hit_points[0] <= 0:
            self.die()

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

    def new_inventory(self, object_):
        if object_ == 'green_potion' and self.hit_points[0] < self.hit_points[1]:
            self.hit_points[0] += 1
        elif object_ == 'red_potion':
            self.damage[0] += 1
            self.damage[1] += 1
        elif object_ == 'blue_potion':
            self.action_points[1] += 1
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
            print(box.position)
            box.move((self.position[0] + movement[1],
                      self.position[1] + movement[0]),
                     self.get_direction(next_cell))
            print(box.position)
            return True

    def interaction_chest(self, obj):
        self.animator.start('attack_' + self.get_direction(obj))
        res = obj.touch()
        if res == '__empty__':
            self.interaction_empty(obj)
            return True
        elif res:
            self.new_inventory(res)
            return True

    def interaction_door(self, obj):
        self.animator.start('attack_' + self.get_direction(obj))
        res = obj.touch(obj.color + '_key' in self.inventory)
        if obj.color + '_key' in self.inventory:
            self.inventory.remove(obj.color + '_key')
        if res == '__empty__':
            self.interaction_empty(obj)
        return True

    def interaction_teleport(self, obj):
        """Взаимодействие с телепортом"""
        if (self.position[1], self.position[0]) ==\
                obj.rooms[obj.current_room].exit_:
            obj.change_room(obj.current_room + 1)
        elif obj.current_room != 1 and \
                (self.position[1], self.position[0]) == \
                obj.rooms[obj.current_room].enter:
            obj.change_room(obj.current_room - 1)

    def die(self):
        super().die()
        config.LOSE = True


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
