from rpg.exceptions import PlayerDiedException, GameWinException
from rpg.map import Map
from rpg.player import Player

if __name__ == "__main__":
    print "Welcome to the Game"
    name = raw_input("Please enter your name ?\n")
    player = Player(name)
    board = Map(player)
    print "Initializing Player"
    board.print_map()
    move_type = raw_input("Enter your move:\na for left, w for top, d for right, s for bottom, q for quit\n")

    while move_type != 'q':
        try:
            board.move_player(move_type)
            board.print_map()
            move_type = raw_input("Enter your move:\n")
        except PlayerDiedException:
            print "You Died! Game Over!"
            break
        except GameWinException:
            print "Found the exit! Your Won!!!"
            break
