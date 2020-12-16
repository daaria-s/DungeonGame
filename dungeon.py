from objects import Teleport, Wall, Empty
from entity import Player, Enemy


class UnknownMapSymbol(Exception):
    pass


class Cell:

    def __init__(self):
        self.base = None
        self.decor = []
        self.entity = None

    def show_base(self):
        pass

    def show_decor(self):
        pass

    def show_entity(self):
        pass


class Dungeon:

    def __init__(self):
        # сделать случаную генерацию карты
        # и вынести это в отдельный метод
        level = [['W', 'W', 'W', '2', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
                 ['W', 'P', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', 'E', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', 'E', '.', '.', 'W'],
                 ['W', '.', '.', '.', 'E', '.', '.', '.', '.', '.', '.', '3'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W'],
                 ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]

        self.map_ = [[Cell() for k in range(len(level[i]))] for i in range(len(level))]

        self.entities_position = []

        for i in range(len(level)):
            for k in range(len(level[i])):
                if level[i][k] == 'W':
                    self.map_[i][k].base = Wall((k, i))
                else:
                    self.map_[i][k].base = Empty((k, i))

                if level[i][k] == 'E':
                    self.map_[i][k].entity = Enemy((k, i))
                    self.entities_position.append((k, i))
                elif level[i][k] == 'P':
                    self.map_[i][k].entity = Player((k, i))
                    self.entities_position.append((k, i))
                elif level[i][k].isdigit():
                    self.map_[i][k].decor.append(Teleport((k, i), self.map_[i][k]))

                if not self.map_[i][k]:
                    print(level[i][k])
                    raise UnknownMapSymbol

    def player_move(self, button):
        pass

    def enemies_move(self):
        pass
