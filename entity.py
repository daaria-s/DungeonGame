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
        self.position = position
        self.name = name

        self.action_points = [max_action_points, max_action_points]
        self.damage = [min_damage, max_damage]
        self.hit_points = [hit_points, max_hit_points]

        self.alive = True
        self.animator = Animator('Sprites/' + path)

    def show(self, surf):
        image, shift = self.animator.next_()
        surf.blit(image, apply((self.position[0] * TILE + shift[0],
                                self.position[1] * TILE + shift[1])))

    def get_direction(self, obj):
        movement_keys = {
            (1, 0): 'left',
            (-1, 0): 'right',
            (0, 1): 'up',
            (0, -1): 'down'
        }
        return movement_keys[(self.position[0] - obj.position[0], self.position[1] - obj.position[1])]

    def interaction(self, dungeon_, movement):
        target = dungeon_.get(self.position, movement)
        if not target or self.action_points[0] == 0:
            return False

        keys = {
            'enemy': [self.interaction_entity, [target]],
            'player': [self.interaction_entity, [target]],
            'empty': [self.interaction_empty, [target]],
            'wall': [lambda: False, []],
            'box': [self.interaction_box, [dungeon_, movement]],
            'chest': [self.interaction_chest, [target]],
            'teleport': [self.interaction_teleport, [target]]
        }
        if keys[target.name][0](*keys[target.name][1]):
            self.action_points[0] -= 1
            if self.action_points[0] == 0 and dungeon_.turn == 1:
                self.action_points[0] = self.action_points[1]
                dungeon_.turn = 2
            return True

    def interaction_entity(self, obj):
        if obj.hit_points[0] <= 0:
            self.animator.start('move_' + self.get_direction(obj))
            self.position = obj.position
        else:
            self.animator.start('attack_' + self.get_direction(obj))
            obj.get_hit(self.damage)
        return True

    def interaction_empty(self, obj):
        self.animator.start('move_' + self.get_direction(obj))
        self.position = obj.position
        return True

    def interaction_box(self, dungeon_, movement):
        pass

    def interaction_chest(self, obj):
        pass

    def interaction_teleport(self, obj):
        pass

    def get_hit(self, damage):
        self.hit_points[0] -= random.randint(damage[0], damage[1])
        if self.hit_points[0] <= 0:
            self.die()

    def die(self):
        self.alive = False
        self.animator.start('die')


class Player(Entity):

    def __init__(self, position,
                 hit_points, max_hit_points,
                 min_damage, max_damage,
                 action_points, max_action_points):
        super().__init__(position, 'player', 'player',
                         hit_points, max_hit_points,
                         min_damage, max_damage,
                         action_points, max_action_points)
        self.inventory = ['red_key'] * 10  # EDIT: fix

    def interaction_box(self, dungeon_, movement):
        next_cell = dungeon_.get(self.position, (movement[0] * 2, movement[1] * 2))
        if next_cell and next_cell.name == 'empty':
            box = dungeon_.get(self.position, movement)
            self.interaction_empty(box)
            box.move((self.position[0] + movement[1], self.position[1] + movement[0]),
                     self.get_direction(next_cell))
            return True

    def interaction_chest(self, obj):
        self.animator.start('attack_' + self.get_direction(obj))
        res = obj.touch()
        if res == '__empty__':
            self.interaction_empty(obj)
            return True
        elif res:
            self.inventory.append(res)
            return True

    def interaction_teleport(self, obj):
        if (self.position[1], self.position[0]) == obj.rooms[obj.current_room].exit_:
            obj.change_room(obj.current_room + 1)
        elif obj.current_room != 1 and (self.position[1], self.position[0]) == obj.rooms[obj.current_room].enter:
            obj.change_room(obj.current_room - 1)

    def die(self):
        super().die()
        config.LOSE = True


class Enemy(Entity):

    def __init__(self, position, color,
                 hit_points, max_hit_points,
                 min_damage, max_damage,
                 action_points, max_action_points):
        super().__init__(position, 'enemy', 'enemies/' + color,
                         hit_points, max_hit_points,
                         min_damage, max_damage,
                         action_points, max_action_points)
        self.color = color
