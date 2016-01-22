import random

from rpg.exceptions import PlayerDiedException, GameWinException
from rpg.tiles import BombTile, MapTile, WallTile, ExitTile

## Map Class
## Size is flexible
## TODO : Random allocation of bombs, exit pos and wall pos

direction_order = ['w', 'd', 's', 'a']


class Map():
    grid_size = 12
    player = None
    exit_pos = [(9, 9)]
    visit_stack = []
    num_bombs = 5
    num_walls = 20
    board_grid = {}
    is_won = False

    def gen_pos(self):
        return (random.randint(0, self.grid_size), random.randint(0, self.grid_size))

    def __init__(self, player):
        print "Initializing Map, Find your way out...."
        self.player = player
        for x in xrange(self.grid_size):
            for y in xrange(self.grid_size):
                self.board_grid[(x, y)] = MapTile()

        print "Setting up bombs......"
        for _ in xrange(self.num_bombs):
            pos = self.gen_pos()
            self.board_grid[pos] = BombTile()

        print "Setting up Walls...."
        for _ in xrange(self.num_walls):
            pos = self.gen_pos()
            self.board_grid[pos] = WallTile()

        print "Setting up Exit Gate...."
        for pos in self.exit_pos:
            self.board_grid[pos] = ExitTile()

        self.get_tile(0, 0).is_visited = True

    def get_tile(self, x, y):
        return self.board_grid[(x, y)]

    def print_map(self):
        for y in xrange(self.grid_size - 1, -1, -1):
            for x in xrange(self.grid_size):
                if x == self.player.pos_x and y == self.player.pos_y:
                    print "Y",
                else:
                    print self.board_grid[(x, y)].get_repr(),
            print

    def is_valid_move(self, pos_x, pos_y):
        if pos_x < 0 or pos_y < 0 or pos_x >= self.grid_size or pos_y >= self.grid_size:
            return False

        tile = self.get_tile(pos_x, pos_y)
        if tile.is_visited:
            return False
        return True

    def get_move(self):
        for direction in direction_order:
            player_pos_x = self.player.pos_x
            player_pos_y = self.player.pos_y
            if direction == "a":
                player_pos_x -= 1
            elif direction == "w":
                player_pos_y += 1
            elif direction == "d":
                player_pos_x += 1
            elif direction == "s":
                player_pos_y -= 1
            if self.is_valid_move(player_pos_x, player_pos_y):
                return player_pos_x,player_pos_y
        new_pos = self.visit_stack.pop()
        return new_pos[0],new_pos[1]

    def move_player(self, pos_x,pos_y):
        tile = self.get_tile(pos_x, pos_y)
        tile_type = tile.__class__.__name__

        if not tile.is_visited:
            self.visit_stack.append((pos_x, pos_y))

        tile.set_visited()

        if tile_type == "WallTile":
            print "Found Wall, Cannot Move Player"
            return
        elif tile_type == "BombTile":
            damage = tile.get_damage()
            print "Found Bomb, Recieved Damage %d" % damage
            self.player.recieve_damage(damage)
            if self.player.health <= 0:
                raise PlayerDiedException
            print "Player Health now : %d" % self.player.health
            return
        elif tile_type == "ExitTile":
            raise GameWinException
        self.player.pos_x = pos_x
        self.player.pos_y = pos_y
        # print self.player.print_pos()
