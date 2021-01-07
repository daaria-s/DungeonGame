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

    def interaction(self, target):
        if not target or self.action_points[0] == 0:
            return False
        if target.name == 'enemy' or target.name == 'player':
            self.interaction_entity(target)
        else:
            exec('self.interaction_' + target.name + '(target)')
        return True

    def interaction_entity(self, obj):
        self.action_points[0] -= 1
        if self.action_points[0] == 0 and config.TURN == 1:
            self.action_points[0] = self.action_points[1]
            config.TURN = 2
        if obj.hit_points[0] <= 0:
            self.animator.start('move_' + self.get_direction(obj))
            self.position = obj.position
        else:
            self.animator.start('attack_' + self.get_direction(obj))
            obj.get_hit(self.damage)

    def interaction_empty(self, obj):
        self.action_points[0] -= 1
        if self.action_points[0] == 0 and config.TURN == 1:
            self.action_points[0] = self.action_points[1]
            config.TURN = 2
        self.animator.start('move_' + self.get_direction(obj))
        self.position = obj.position

    def interaction_wall(self, obj):
        return False

    def interaction_box(self, obj):
        pass

    def interaction_chest(self, obj):
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
        self.inventory = ['key'] * 10  # fix

    def interaction_teleport(self, obj):
        pass

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
