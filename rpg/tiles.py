from random import randint


class MapTile:
    is_visited = False
    x = None
    y = None

    def __str__(self):
        return "%s at (%d,%d)" % (self.__class__.__name__, self.x, self.y)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_visited(self):
        self.is_visited = True

    def get_repr(self):
        if self.is_visited:
            return "x"
        else:
            return "_"


class BombTile(MapTile):
    def get_damage(self):
        return randint(20, 40)

    def get_repr(self):
        if self.is_visited:
            return "B"
        else:
            return "_"


class WallTile(MapTile):
    def get_repr(self):
        if self.is_visited:
            return "W"
        else:
            return "_"


class ExitTile(MapTile):
    pass
