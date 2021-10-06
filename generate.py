#!/usr/bin/env python3

"""
Regroup generating functions
"""

import itertools
from random import randint as rd
from classes import Staircase, Item, Enemy, Room, Corridor, Stage, Quest
from explore import spawn_character, spawn



def generate_enemies(canvasdim, rooms_list, minnumber, maxnumber):
    """
    Generate all enemies for a given floor
    """
    number = rd(minnumber, maxnumber)
    enemies = {'coord': {}, 'list': {}}
    while len(enemies['list']) < number:
        enemy = Enemy(canvasdim, 0, 0)
        spawn(canvasdim, rooms_list, enemy)
        enemies['list'][len(enemies['list'])] = enemy
        enemies['coord'][enemy.position] = enemy.rank
    return enemies


def generate_rooms(canvasdim, minnumber, maxnumber):
    """
    Generate a set of rooms
    """
    maxwidth, maxheight = canvasdim[1]//3, canvasdim[0]//3
    number = rd(minnumber, maxnumber)
    rooms = {'coord': {}, 'list': {}}
    while len(rooms['list']) < number:
        room = Room(canvasdim, maxwidth, maxheight)
        rooms['list'][len(rooms['list'])] = room
        for k in room.create_room():
            if k not in rooms['coord']:
                rooms['coord'][k] = k
    return rooms


def generate_corridors(canvasdim, rooms_list):
    """
    Generate a set of corridors
    """
    corridors = {}
    for room1, room2 in itertools.combinations(rooms_list, 2):
        corridor = Corridor(canvasdim, rooms_list[room1].entry, rooms_list[room2].entry)
        for k in corridor.create_corridor():
            if k not in corridors:
                corridors[k] = k
    return corridors


def generate_quests():
    """
    Return initial achievement set
    """
    return {'weapon': Quest(), 'defeat1': Quest(), 'defeat5': Quest(), 'defeat10': Quest(), 'defeat20': Quest(), 'defeat50': Quest(), 'level5': Quest(), 'level10': Quest(), 'level15': Quest(), 'level20': Quest(), 'level25': Quest()}


def generate_stage(canvasdim, floor, character):
    """
    Generate a floor
    """
    items = {'coord': {}, 'list': {}}
    stage = Stage(canvasdim)
    rooms = generate_rooms(canvasdim, 3, 6)
    staircase = Staircase(canvasdim, 0, 0)
    hidden_staircase = Staircase(canvasdim, 0, 0)
    enemies = generate_enemies(canvasdim, rooms['list'], floor*5, floor*10)
    scroll = Item(canvasdim, 0, 0, 'scroll')
    corridors = generate_corridors(canvasdim, rooms['list'])
    spawn_character(canvasdim, rooms['list'], character)
    spawn(canvasdim, rooms['list'], staircase)
    spawn(canvasdim, rooms['list'], hidden_staircase)
    spawn(canvasdim, rooms['list'], scroll)
    items['list']['scroll'] = scroll
    items['coord'][scroll.position] = scroll.position
    if not character.armed:
        weapon = Item(canvasdim, 0, 0, 'weapon')
        spawn(canvasdim, rooms['list'], weapon)
        items['list']['weapon'] = weapon
        items['coord'][weapon.position] = weapon.position
    return stage, character, rooms, staircase, hidden_staircase, enemies, items, corridors

