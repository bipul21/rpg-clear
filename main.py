from rpg.exceptions import PlayerDiedException, GameWinException, NoPathException
from rpg.map import Map
from rpg.player import Player

if __name__ == "__main__":
    print "Welcome to the Game"
    name = raw_input("Please enter your name ?\n")
    player = Player(name)
    board = Map(player)
    print "Initializing Player"
    board.print_map()
    # move_type = raw_input("Enter your move:\na for left, w for top, d for right, s for bottom, q for quit\n")

    while True:
        try:
            pos_x, pos_y = board.get_move()
            board.move_player(pos_x,pos_y)
            board.print_map()
            raw_input("=========== Press Any Key For Next Move ===========")
        except PlayerDiedException:
            print "You Died! Game Over!"
            break
        except GameWinException:
            print "Found the exit! Your Won!!!"
            break
        except NoPathException:
            print "Cannot find any path blocked"
            break

