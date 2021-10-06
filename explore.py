#!/usr/bin/env python3

"""
Regroup all game functions
"""

from random import randint as rd



def index_1D(canvasdim, x, y):
    """
    Convert a 2D position to a 1D
    """
    width = canvasdim[1]
    return int(y*width+x)

def index_2D(canvasdim, n):
    """
    Convert a 1D position to 2D
    """
    width = canvasdim[1]
    x = n % width
    y = n // width
    return x, y


def neighbors(canvasdim, position):
    """
    Return neighboring coordinates of a given position (1D)
    """
    for height in [-1, 0, 1]:
        for width in [-1, 0, 1]:
            neighbor = position + width + height*canvasdim[1]
            if index_2D(canvasdim, position)[0] == index_2D(canvasdim, neighbor)[0]\
                    or index_2D(canvasdim, position)[1] == index_2D(canvasdim, neighbor)[1]:
                yield neighbor


def spawn_character(canvasdim, rooms_list, character):
    """
    Make player spawn somewhere on the floor map
    """
    random = rd(0, len(rooms_list)-1)
    spawning_room = rooms_list[random]
    x = spawning_room.x + spawning_room.width//2
    y = spawning_room.y + spawning_room.height//2
    character.position = index_1D(canvasdim, x, y)


def spawn(canvasdim, rooms_list, classobject):
    """
    Make a given object spawn somewhere on the floor map
    """
    random = rd(0, len(rooms_list)-1)
    spawning_room = rooms_list[random]
    x = spawning_room.x + rd(0, spawning_room.width-1)
    y = spawning_room.y + rd(0, spawning_room.height-1)
    classobject.position = index_1D(canvasdim, x, y)


def move_is_valid(classobject, character, rooms_coord, enemies_coord, corridors, change_position):
    """
    Return whether a move is valid
    """
    x, y = change_position
    position = classobject.position + x + y*classobject.canvasdim[1]
    if (position in rooms_coord or position in corridors)\
            and not (position in enemies_coord or position == character.position):
        return True
    return False

def move(classobject, character, rooms_coord, enemies_coord, corridors, key):
    """
    Code the movement of a given object
    """
    key = str(key)
    if key == 'z':  # go up
        x, y = (0, -1)
    elif key == 's':  # go down
        x, y = (0, 1)
    elif key == 'q':  # go left
        x, y = (-1, 0)
    elif key == 'd':  # go right
        x, y = (1, 0)
    if move_is_valid(classobject, character, rooms_coord, enemies_coord, corridors, (x, y)):
        classobject.position += x + y*classobject.canvasdim[1]


def attack_is_valid(character, enemies_list, blowdirection):
    """
    Return if an attack is valid
    """
    x, y = blowdirection
    if (x, y) == (None, None):
        return False, None, None
    coord = character.position + x + y*character.canvasdim[1]
    for i in enemies_list:
        if enemies_list[i].position == coord:
            return True, coord, i
    return False, None, None

def character_attack(character, enemies_list, key):
    """
    Code character attack in a given direction
    """
    (x, y) = (None, None)
    key = str(key)
    if key == 'KEY_UP':  # upwards blow
        x, y = (0, -1)
    elif key == 'KEY_DOWN':  # downwards blow
        x, y = (0, 1)
    elif key == 'KEY_LEFT':  # leftwards blow
        x, y = (-1, 0)
    elif key == 'KEY_RIGHT':  # rightwards blow
        x, y = (1, 0)
    valid, coord, i = attack_is_valid(character, enemies_list, (x, y))
    if valid:
        enemies_list[i].HP -= character.damage
        if enemies_list[i].HP <= 0:
            character.exp += 1 + enemies_list[i].rank*4
            return coord, i
        return None, None
    return None, None

def enemy_attack(character):
    """
    Code an enemy attack on the player
    """
    character.HP = max(0, character.HP-1)

