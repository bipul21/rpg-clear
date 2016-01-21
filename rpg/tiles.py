from random import randint

## Different types of tiles to lay out

class MapTile:
    is_visited = 0

    def set_visited(self):
        self.is_visited += 1

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
