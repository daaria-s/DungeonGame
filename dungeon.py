class Dungeon:

    def __init__(self):
        pass

    def get(self, coords, diff=(0, 0)):
        return self.map_[coords[1] + diff[1]][coords[0] + diff[0]]

    def player_move(self, button):
        pass

    def enemies_move(self):
        pass
