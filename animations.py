from config import *


class Iterator:

    def __init__(self, values, n=None):
        if len(values) == 0:
            raise IndexError
        self.values = values
        self.counter = 0
        self.limit = n

    def __next__(self):
        if not self.limit or self.counter < self.limit:
            self.counter += 1
            return self.values[(self.counter - 1) % len(self.values)]
        else:
            raise StopIteration

    def reset(self):
        self.counter = 0


class Animation:

    def __init__(self, name, iterator):
        self.name = name
        self.iterator = iterator

    def __next__(self):
        return next(self.iterator)

    def reset(self):
        self.iterator.reset()


class UnknownAnimation(Exception):
    pass


def new(animation_name):
    if animation_name == 'IDLE':
        return Animation('IDLE', Iterator([(0, -1), (0, -1), (0, -2), (0, -2), (0, -3), (0, -3),
                                           (0, -2), (0, -2), (0, -1), (0, -1), (0, 0), (0, 0),
                                           (0, 1), (0, 1), (0, 2), (0, 2), (0, 3), (0, 3),
                                           (0, 2), (0, 2), (0, 1), (0, 1), (0, 0), (0, 0)]))
    elif animation_name == 'RIGHT_MOVE':
        return Animation('RIGHT_MOVE', Iterator([(i, 0) for i in range(TILE, 0, -4)], TILE // 4),)
    elif animation_name == 'LEFT_MOVE':
        return Animation('LEFT_MOVE', Iterator([(-i, 0) for i in range(TILE, 0, -4)], TILE // 4))
    elif animation_name == 'UP_MOVE':
        return Animation('UP_MOVE', Iterator([(0, -i) for i in range(TILE, 0, -4)], TILE // 4))
    elif animation_name == 'DOWN_MOVE':
        return Animation('DOWN_MOVE', Iterator([(0, i) for i in range(TILE, 0, -4)], TILE // 4))

    elif animation_name == 'RIGHT_ATTACK':
        return Animation('RIGHT_ATTACK', (Iterator([(abs(TILE - i) - TILE, 0) for i in range(0, 2 * TILE, 4)], TILE // 2)))
    elif animation_name == 'LEFT_ATTACK':
        return Animation('LEFT_ATTACK', Iterator([(TILE - abs(TILE - i), 0) for i in range(0, 2 * TILE, 4)], TILE // 2))
    elif animation_name == 'UP_ATTACK':
        return Animation('UP_ATTACK', Iterator([(0, TILE - abs(TILE - i)) for i in range(0, 2 * TILE, 4)], TILE // 2))
    elif animation_name == 'DOWN_ATTACK':
        return Animation('DOWN_ATTACK', Iterator([(0, abs(TILE - i) - TILE) for i in range(0, 2 * TILE, 4)], TILE // 2))

    elif animation_name == 'DIE':
        return Animation('DIE', Iterator([(0, 0)]))
    raise UnknownAnimation(animation_name)
