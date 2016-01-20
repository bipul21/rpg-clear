from rpg.exceptions import PlayerDiedException, GameWinException
from rpg.tiles import BombTile, MapTile, WallTile, ExitTile


class Map():
    grid_size = 12
    player = None
    bomb_pos = [(0, 3), (3, 8), (8, 3)]
    exit_pos = [(9, 9)]
    wall_tile = [(1, 7), (2, 7), (5, 10), (6, 10), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)]

    board_grid = {}
    is_won = False

    def __init__(self, player):
        print "Initializing Map, Find your way out...."
        self.player = player
        for x in xrange(self.grid_size):
            for y in xrange(self.grid_size):
                self.board_grid[(x, y)] = MapTile(x, y)

        print "Setting up bombs......"
        for pos in self.bomb_pos:
            self.board_grid[pos] = BombTile(pos[0], pos[1])

        print "Setting up Walls...."
        for pos in self.wall_tile:
            self.board_grid[pos] = WallTile(pos[0], pos[1])

        print "Setting up Exit Gate...."
        for pos in self.exit_pos:
            self.board_grid[pos] = ExitTile(pos[0], pos[1])

    def get_tile(self, x, y):
        return self.board_grid[(x, y)]

    def print_map(self):
        for y in xrange(self.grid_size - 1, -1, -1):
            for x in xrange(self.grid_size):
                print self.board_grid[(x, y)].get_repr(),
            print

    def move_player(self, move_type):
        player_pos_x = self.player.pos_x
        player_pos_y = self.player.pos_y
        if move_type == "a":
            player_pos_x -= 1
        elif move_type == "w":
            player_pos_y += 1
        elif move_type == "d":
            player_pos_x += 1
        elif move_type == "s":
            player_pos_y -= 1
        if player_pos_x < 0 or player_pos_y < 0 or player_pos_x >= 12 or player_pos_y >= 12:
            print "Cannot Move"
            return

        tile = self.get_tile(player_pos_x, player_pos_y)

        tile_type = tile.__class__.__name__
        tile.is_visited = True
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
        elif tile_type == "ExitTile":
            raise GameWinException
        self.player.pos_y = player_pos_y
        self.player.pos_x = player_pos_x
        print self.player.print_pos()