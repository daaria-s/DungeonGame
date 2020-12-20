import pygame
import config
from config import *
import animations


class Entity:

    def __init__(self, position, name, max_action_points, damage, max_hit_points):
        self.image = pygame.image.load('Sprites/' + name + '.png')
        self.position = position
        self.name = name

        self.action_points = max_action_points
        self.max_action_points = max_action_points
        self.damage = damage
        self.max_hit_points = max_hit_points
        self.hit_points = max_hit_points

        self.alive = True
        self.animation = animations.new('IDLE')

    def show(self):
        adj = (0, 0)
        try:
            adj = next(self.animation)
        except StopIteration:
            self.animation = animations.new('IDLE')

        animated_position = (self.position[0] * TILE + (TILE - self.image.get_width()) // 2 - adj[0],
                             self.position[1] * TILE + (TILE - self.image.get_height()) // 2 - adj[1])
        return self.image, animated_position

    def get_direction(self, obj):
        movement_keys = {
            (1, 0): 'LEFT',
            (-1, 0): 'RIGHT',
            (0, 1): 'UP',
            (0, -1): 'DOWN'
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
        self.animation = animations.new(self.get_direction(obj) + '_ATTACK')
        obj.hit_points -= 1
        if obj.hit_points == 0:
            obj.die()

    def interaction_empty(self, obj):
        self.action_points -= 1
        if self.action_points == 0 and config.TURN == 1:
            self.action_points = self.max_action_points
            config.TURN = 2
        self.animation = animations.new(self.get_direction(obj) + '_MOVE')
        self.position = obj.position

    def interaction_wall(self, obj):
        return False

    def interaction_box(self, obj):
        pass

    def interaction_chest(self, obj):
        pass

    def die(self):
        self.alive = False
        self.animation = animations.new('DIE')


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
