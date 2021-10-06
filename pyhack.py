#!/usr/bin/env python3
"""
Main program
"""

import curses
import os
from random import randint as rd
from classes import Character
from generate import generate_stage, generate_quests
from explore import neighbors, move, character_attack, enemy_attack
from dessin import refresh_screen, pause, titlescreen, startscreen1, startscreen2, gameoverscreen, endscreen, openmenu

HEIGHT = 48
#WIDTH = 200
WIDTH = 150
DIRECTIONS = ['z', 's', 'q', 'd']
MAXFLOOR = rd(1, 4)*5 + rd(0, 5)



def main(win):
    """
    Runs game using curses module for graphics
    """
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    RADIUS = 15
    floor = 1
    canvasdim = (HEIGHT, WIDTH)
    character = Character(canvasdim, 0, 0)
    stage, character, rooms, staircase, hidden_staircase, enemies, items, corridors = generate_stage(canvasdim, floor, character)

    win.nodelay(True)
    key = ''
    trash = []
    hidden = False

    titlescreen(win)
    startscreen1(win)
    refresh_screen(win, stage, character, rooms['coord'], staircase, enemies, items['coord'], corridors, RADIUS, floor, trash)
    pause(win)
    startscreen2(win)

    refresh_screen(win, stage, character, rooms['coord'], staircase, enemies, items['coord'], corridors, RADIUS, floor, trash)

    quests = generate_quests()

    while floor <= MAXFLOOR:
        try:
            key = win.getkey()
            if (character.position == staircase.position or character.position == hidden_staircase.position) and key == os.linesep:
                if floor == MAXFLOOR:
                    hidden_staircase.position = -1

                if character.position == hidden_staircase.position:
                    hidden = True
                    RADIUS = 1000
                else:
                    if hidden:
                        floor = int(floor+0.5)
                        RADIUS = 10
                    else:
                        floor += 1
                    hidden = False
                stage, character, rooms, staircase, hidden_staircase, enemies, items, corridors = generate_stage(canvasdim, floor, character)
                if hidden:
                    enemies = {'list': {}, 'coord': {}}
                    hidden_staircase.position = -1
                    floor += 0.5
                refresh_screen(win, stage, character, rooms['coord'], staircase, enemies, items['coord'], corridors, RADIUS, floor, trash)
                trash = []

            if str(key) == 'e':
                forcexit = openmenu(win, character, quests)
                if forcexit:
                    return False, quests

            # CHARACTER ATTACK
            coord, i = character_attack(character, enemies['list'], key)
            if i is not None:
                trash.append(i)
                character.kills += 1
                if character.kills == 10:
                    quests['defeat1'].complete()
                if character.kills == 50:
                    quests['defeat5'].complete()
                if character.kills == 100:
                    quests['defeat10'].complete()
                if character.kills == 200:
                    quests['defeat20'].complete()
                if character.kills == 500:
                    quests['defeat50'].complete()

                del enemies['coord'][coord]
                enemies['coord'][-len(trash)] = enemies['list'][i].rank
                enemies['list'][i].position = -len(trash)
                refresh_screen(win, stage, character, rooms['coord'], staircase, enemies, items['coord'], corridors, RADIUS, floor, trash)
                if character.exp >= (character.level+4)*character.level:
                    win.addstr('\n\n   YOU LEVELED UP!')
                    character.levelup()
                    if character.level == 5:
                        quests['level5'].complete()
                    if character.level == 10:
                        quests['level10'].complete()
                    if character.level == 15:
                        quests['level15'].complete()
                    if character.level == 20:
                        quests['level20'].complete()
                    if character.level == 25:
                        quests['level25'].complete()

            # ENEMIES' TURN
            enemies['coord'] = {}
            for i in enemies['list']:
                enemy = enemies['list'][i]
                if character.position in neighbors(canvasdim, enemy.position):
                    enemy_attack(character)
                else:
                    direction = DIRECTIONS[rd(0, 3)]
                    move(enemy, character, rooms['coord'], enemies['coord'], corridors, direction)
                enemies['coord'][enemy.position] = enemy.rank
            refresh_screen(win, stage, character, rooms['coord'], staircase, enemies, items['coord'], corridors, RADIUS, floor, trash)

            if character.HP <= 0:
                win.addstr('\n\n   LOOKS LIKE MY HP HAS RUN OUT...')
                pause(win)
                gameoverscreen(win)
                return False, quests

            # CHARACTER MOVEMENT
            move(character, character, rooms['coord'], enemies['coord'], corridors, key)
            refresh_screen(win, stage, character, rooms['coord'], staircase, enemies, items['coord'], corridors, RADIUS, floor, trash)

            if character.position in items['coord']:
                if character.position == items['list']['scroll'].position:
                    win.addstr('\n\n   HEALED {} HP!'.format(character.maxHP//2))
                    character.HP = min(character.maxHP, character.HP + character.maxHP//2)
                    del items['coord'][character.position]
                else:
                    win.addstr('\n\n   EQUIPPED A WEAPON!')
                    character.equip()
                    quests['weapon'].complete()
                    del items['coord'][character.position]

            if character.position == staircase.position:
                win.addstr('\n\n   YOU HAVE REACHED A STAIRCASE! PRESS ENTER TO GO ON TO THE NEXT FLOOR')
            if character.position == hidden_staircase.position:
                win.addstr('\n\n   YOU HAVE FOUND A HIDDEN STAIRCASE! PRESS ENTER TO GO ON TO THE NEXT FLOOR')

        except:
            pass

    """
    Once max floor has been reached
    """
    RADIUS = 1000
    enemies = {'list': {}, 'coord': {}}
    rooms = {'coord': {}, 'list': {}}
    staircase.position = -1
    items = {'coord': {}, 'list': {}}
    corridors = {}
    refresh_screen(win, stage, character, rooms['coord'], staircase, enemies, items['coord'], corridors, RADIUS, floor, trash)
    win.addstr('\n\n   ...')
    pause(win)
    endscreen(win)
    return True, quests



"""
Display final info in terminal
"""
outcome, quests = curses.wrapper(main)
if not outcome:
    print('\n ----- GAME OVER! TRY AGAIN -----\n')
else:
    print('\n ----- CONGRATULATIONS! YOU HAVE SUCCESSFULLY COMPLETED THE GAME -----\n')

completed = 0
for quest in quests:
    if quests[quest].state == 'COMPLETED':
        completed += 1

print('YOU HAVE SUCCESSFULLY COMPLETED {} OUT OF {} QUESTS.\n\n'.format(completed, len(quests)))
