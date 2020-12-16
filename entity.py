class Entity:

    def __init__(self, position):
        self.position = position

    def show(self):
        pass

    def interaction(self):
        pass

    def die(self):
        pass


class Player(Entity):
    pass


class Enemy(Entity):
    pass
