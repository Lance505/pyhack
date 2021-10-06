#!/usr/bin/env python3

"""
Regroup used class items
"""

from random import randint as rd
import math
from explore import index_1D, index_2D



class Staircase:
    """
    Staircase class used to access a higher floor
    """
    def __init__(self, canvasdim, x, y):
        self.position = index_1D(canvasdim, x, y)


class Item:
    """
    Item drops can be either scrolls or weapons
    """
    def __init__(self, canvasdim, x, y, itemtype):
        self.position = index_1D(canvasdim, x, y)
        self.type = itemtype


class Character:
    """
    Character class to manage your character
    """
    def __init__(self, canvasdim, x, y):
        self.canvasdim = canvasdim
        self.position = index_1D(self.canvasdim, x, y)
        self.level = 1
        self.maxHP = 20
        self.HP = 20
        self.exp = 0
        self.damage = 0
        self.armed = False
        self.kills = 0

    def levelup(self):
        self.level += 1
        self.maxHP += 2
        self.HP = self.maxHP
        self.exp = 0
        self.damage = round(self.damage+0.1, 1)

    def equip(self):
        self.damage = 1.1
        self.armed = True


class Enemy:
    """
    Enemy class used to annoy player
    """
    def __init__(self, canvasdim, x, y):
        self.canvasdim = canvasdim
        self.position = index_1D(canvasdim, x, y)
        rank = lambda x: not math.ceil(x/3)
        self.rank = rank(rd(0, 3))
        self.HP = 1 + self.rank*3


class Room:
    """
    Room class
    """
    def __init__(self, canvasdim, maxwidth, maxheight):
        self.canvasdim = canvasdim
        self.width = rd(canvasdim[1]//8, maxwidth)
        self.height = rd(canvasdim[0]//8, maxheight)
        self.x = rd(1, canvasdim[1] - self.width -1)
        self.y = rd(1, canvasdim[0] - self.height -1)
        x = self.x + self.width//2
        y = self.y + self.height//2
        self.entry = index_1D(self.canvasdim, x, y)


    def create_room(self):
        for i in range(self.y, self.y+self.height):
            for j in range(self.x, self.x+self.width):
                yield index_1D(self.canvasdim, j, i)

    def iter_room(self):
        for y in range(self.y, self.y+self.height+1):
            for x in range(self.x, self.x+self.width+1):
                yield index_1D(self.canvasdim, x, y)


class Corridor:
    """
    Corridor class to enable navigation between rooms
    """
    def __init__(self, canvasdim, start, end):
        self.canvasdim = canvasdim
        self.start = start
        self.end = end

    def create_corridor(self):
        xi, yi = index_2D(self.canvasdim, self.start)
        xf, yf = index_2D(self.canvasdim, self.end)
        yield index_1D(self.canvasdim, xi, yi)
        x, y = xi, yi
        sign = lambda x: (1, -1)[x < 0]
        while (x, y) != (xf, yf):
            random = rd(0, 1)
            if random and x != xf:
                x += sign(xf - x)
            elif y != yf:
                y += sign(yf - y)
            yield index_1D(self.canvasdim, x, y)


class Stage:
    """
    Stage class
    """
    def __init__(self, canvasdim):
        self.canvasdim = canvasdim
        self.height, self.width = canvasdim

    def iter_canvas(self, character, rooms_coord, staircase, enemies_coord, items_coord, corridors, radius, seen=dict()):
        x0, y0 = index_2D(self.canvasdim, character.position)
        for k in range(self.height*self.width):
            x = x0 - index_2D(self.canvasdim, k)[0]
            y = y0 - index_2D(self.canvasdim, k)[1]
            if k != 0 and k%self.width == 0:
                yield 'newline', None
            if k == character.position:
                yield '@', 1
            elif math.sqrt(x**2 + y**2) <= radius\
                    and 0 <= x0 - x <= self.width\
                    and 0 <= y0 - y <= self.height:
                if k in enemies_coord:
                    if enemies_coord[k] == 0:
                        yield 'm', 0
                    else:
                        yield 'M', 0
                elif k in items_coord:
                    yield '?', 0
                elif k == staircase.position:
                    yield '€', 0
                elif k in rooms_coord:
                    yield '.', 0
                elif k in corridors:
                    yield '#', 0
                else:
                    yield ' ', 0
            else:
                yield ' ', 0


class Quest:
    """
    Quest or achievement class
    """
    def __init__(self):
        self.state = 'IN PROGRESS'

    def complete(self):
        self.state = 'COMPLETED'

