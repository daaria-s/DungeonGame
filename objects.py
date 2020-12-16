class Object:

    def __init__(self, position):
        self.position = position


class Wall(Object):

    def __init__(self, position):
        super().__init__(position)


class Empty(Object):

    def __init__(self, position):
        super().__init__(position)


class Teleport(Object):

    def __init__(self, position, number):
        super().__init__(position)
        self.number = number


class Box(Object):

    def __init__(self, position):
        super().__init__(position)


class Chest(Object):

    def __init__(self, position):
        super().__init__(position)


