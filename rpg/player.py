## Player Def default health 100 to get started with
import random

direction_order = ['w', 'd', 's', 'a']

class Player():
    name = None
    health = 100
    pos_x = 0
    pos_y = 0
    direction = 'w'

    def __init__(self, name):
        self.name = name

    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def print_pos(self):
        print "%s is at (%d,%d)" % (self.name, self.pos_x, self.pos_y)

    def recieve_damage(self, damage):
        self.health -= damage

    def get_direction(self):
        return self.direction

    def change_direction(self):
        self.direction = random.choice(direction_order)
        return self.direction

