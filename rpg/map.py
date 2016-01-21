from rpg.exceptions import PlayerDiedException, GameWinException
from rpg.tiles import BombTile, MapTile, WallTile, ExitTile


## Map Class
## Size is flexible
## TODO : Random allocation of bombs, exit pos and wall pos


class Map():
    grid_size = 12
    player = None
    bomb_pos = [(0, 3), (3, 8), (8, 3)]
    exit_pos = [(9, 9)]
    wall_tile = [(1, 7), (2, 7), (5, 10), (6, 10), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)]
    visited_junctions = []
    visited_nodes = []

    board_grid = {}
    is_won = False

    def __init__(self, player):
        print "Initializing Map, Find your way out...."
        self.player = player
        for x in xrange(self.grid_size):
            for y in xrange(self.grid_size):
                self.board_grid[(x, y)] = MapTile()

        print "Setting up bombs......"
        for pos in self.bomb_pos:
            self.board_grid[pos] = BombTile()

        print "Setting up Walls...."
        for pos in self.wall_tile:
            self.board_grid[pos] = WallTile()

        print "Setting up Exit Gate...."
        for pos in self.exit_pos:
            self.board_grid[pos] = ExitTile()

        self.get_tile(0, 0).is_visited = True

    def get_tile(self, x, y):
        return self.board_grid[(x, y)]

    def print_map(self):
        # print self.visited_junctions
        # print self.visited_nodes

        for y in xrange(self.grid_size - 1, -1, -1):
            for x in xrange(self.grid_size):
                if x == self.player.pos_x and y == self.player.pos_y:
                    print "Y",
                else:
                    print self.board_grid[(x, y)].get_repr(),
            print

    def get_move(self):
        player_pos_x = self.player.pos_x
        player_pos_y = self.player.pos_y

        direction = self.player.get_direction()

        if direction == "a":
            player_pos_x -= 1
        elif direction == "w":
            player_pos_y += 1
        elif direction == "d":
            player_pos_x += 1
        elif direction == "s":
            player_pos_y -= 1

        if player_pos_x < 0 or player_pos_y < 0 or player_pos_x >= self.grid_size or player_pos_y >= self.grid_size:
            # self.visited_junctions.append((self.player.pos_x,self.player.pos_y))
            self.player.change_direction()
            return self.get_move()

        tile = self.get_tile(player_pos_x, player_pos_y)

        if tile.is_visited > 0:
            self.visited_junctions.append((self.player.pos_x,self.player.pos_y))
            self.player.change_direction()
            return self.get_move()

        if tile.is_visited == 0:
            return direction

    def get_next_move(self):
        return self.get_move()

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
        elif tile_type == "ExitTile":
            raise GameWinException
        self.player.pos_y = player_pos_y
        self.player.pos_x = player_pos_x
        self.visited_nodes.append((self.player.pos_x,self.player.pos_y))
        print self.player.print_pos()
