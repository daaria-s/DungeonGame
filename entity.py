import pygame
import config
from config import *
from animator import Animator
from functions import *


class Entity:

    def __init__(self, position, name, max_action_points, damage, max_hit_points):
        self.position = position
        self.name = name

        self.action_points = max_action_points
        self.max_action_points = max_action_points
        self.damage = damage
        self.max_hit_points = max_hit_points
        self.hit_points = max_hit_points

        self.alive = True
        self.animator = Animator('Sprites/' + name)

    def show(self):
        return self.animator.next_(), apply((self.position[0] * TILE, self.position[1] * TILE))

    def get_direction(self, obj):
        movement_keys = {
            (1, 0): 'left',
            (-1, 0): 'right',
            (0, 1): 'up',
            (0, -1): 'down'
        }
        return movement_keys[(self.position[0] - obj.position[0], self.position[1] - obj.position[1])]

    def interaction(self, obj):
        if obj.entity:
            target = obj.entity
        elif obj.base:
            target = obj.base
        if self.action_points == 0:
            return False
        if target.name == 'enemy' or target.name == 'player':
            self.interaction_entity(target)
        else:
            exec('self.interaction_' + target.name + '(target)')
        return True

    def interaction_entity(self, obj):
        self.action_points -= 1
        if self.action_points == 0 and config.TURN == 1:
            self.action_points = self.max_action_points
            config.TURN = 2
        self.animator.start('attack_' + self.get_direction(obj))
        obj.hit_points -= 1
        if obj.hit_points == 0:
            obj.die()

    def interaction_empty(self, obj):
        self.action_points -= 1
        if self.action_points == 0 and config.TURN == 1:
            self.action_points = self.max_action_points
            config.TURN = 2
        self.animator.start('move_' + self.get_direction(obj))
        self.position = obj.position

    def interaction_wall(self, obj):
        return False

    def interaction_box(self, obj):
        pass

    def interaction_chest(self, obj):
        pass

    def die(self):
        self.alive = False
        self.animator.start('die')


class Player(Entity):

    def __init__(self, position, max_action_points=3, damage=1, max_hit_points=5):
        super().__init__(position, 'player', max_action_points, damage, max_hit_points)

    def interaction_teleport(self, obj):
        pass

    def die(self):
        super().die()
        config.LOSE = True


class Enemy(Entity):

    def __init__(self, position, max_action_points=2, damage=1, max_hit_points=2):
        super().__init__(position, 'enemy', max_action_points, damage, max_hit_points)
