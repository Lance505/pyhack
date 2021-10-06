#!/usr/bin/env python3

"""
Draw stage
"""

import os
import curses


def pause(win):
    """
    Pause screen
    """
    win.nodelay(True)
    key = ''
    while True:
        try:
            key = win.getkey()
            if key == os.linesep:
                return
        except:
            pass


def titlescreen(win):
    """
    First screen after launching
    """
    win.clear()
    win.addstr('\n\n\n')
    win.addstr('\n\n\n---------------------------------------------------------------------------------------')
    win.addstr('\n---------------------------------------------------------------------------------------')
    win.addstr('\n\n\n                    ####.    .     .   .    .     ..        ...   .    .')
    win.addstr('\n                    .    .   .     .   .    .    .  .     ..      .   .')
    win.addstr('\n                    .    .    .   .    #####.   .    .   .        ###.')
    win.addstr('\n                    . ..       ###     .    .   #####.   .        .  .')
    win.addstr('\n                    .           .      .    .   .    .    ..      .   .')
    win.addstr('\n                    .           .      .    .   .    .      ###   .    .')
    win.addstr('\n\n\n---------------------------------------------------------------------------------------')
    win.addstr('\n---------------------------------------------------------------------------------------')
    win.addstr('\n\n\n\n\n                                  PRESS ENTER TO START GAME')
    pause(win)


def startscreen1(win):
    """
    First text display
    """
    win.clear()
    win.addstr('\n ...')
    pause(win)
    win.addstr('\n\n WHERE AM I?')
    pause(win)
    win.addstr('\n\n WHAT IS THIS PLACE?')
    pause(win)

def startscreen2(win):
    """
    Second text display + controls list
    """
    win.clear()
    win.addstr('\n ...')
    win.addstr('\n\n WHERE AM I?')
    win.addstr('\n\n WHAT IS THIS PLACE?')
    win.addstr('\n\n ...')
    pause(win)
    win.addstr('\n\n OKAY...')
    pause(win)
    win.addstr('\n\n THIS LOOKS KINDA DANGEROUS.')
    pause(win)
    win.addstr('\n\n IF I GO IN FAR ENOUGH...')
    pause(win)
    win.addstr("\n\n MAYBE I'LL BE ABLE TO GET OUT...")
    pause(win)
    win.addstr('\n\n WELL THEN.')
    pause(win)
    win.addstr("\n\n LET'S DO THIS!")
    pause(win)
    win.addstr('\n\n RIGHT.')
    pause(win)
    win.addstr('\n\n I MIGHT NEED A WEAPON FIRST...')
    pause(win)
    reviewcontrols(win)
    pause(win)


def reviewcontrols(win):
    """
    Display controls list
    """
    win.addstr('\n\n\n---------------------------------------------------------------------------------------')
    win.addstr('\n\n  CONTROLS:')
    win.addstr("\n\n\n   MOVE AROUND USING YOUR KEYBOARD'S ZQSD KEYS.")
    win.addstr('\n\n   PROGRESS THROUGH THE DIFFERENT FLOORS USING STAIRCASES MARKED AS € ON YOUR FLOOR MAP.')
    win.addstr('\n\n   ITEM DROPS WILL BE SIGNALLED WITH A ? SYMBOL.')
    win.addstr('\n\n   MONSTERS WILL BE SIGNALLED AS EITHER AN m OR M SYMBOL ACCORDING TO RANK.')
    win.addstr("\n\n   YOU CAN ATTACK ADJACENT POSITIONS USING YOUR KEYBOARD'S ARROW KEYS.")
    win.addstr('\n\n   OPEN MENU WITH E.')
    win.addstr('\n\n---------------------------------------------------------------------------------------')


def gameoverscreen(win):
    """
    Display in the event of a game over
    """
    win.clear()
    win.addstr('\n ...')
    pause(win)
    win.addstr('\n\n IS THIS...')
    pause(win)
    win.addstr(' THE END?')
    pause(win)
    win.addstr('\n\n I GUESS...')
    pause(win)
    win.addstr(' I TRIED MY BEST...')
    pause(win)
    win.addstr('\n\n MAYBE...')
    pause(win)
    win.addstr('\n\n IF I TRY AGAIN...')
    pause(win)
    win.addstr('\n\n ...')
    pause(win)
    win.addstr('\n\n ...')
    pause(win)


def endscreen(win):
    """
    Display if game is successfully completed
    """
    win.clear()
    win.addstr('\n DID I MAKE IT?')
    pause(win)
    win.addstr('\n\n ...')
    pause(win)
    win.addstr('\n\n SEEMS LIKE IT...')
    pause(win)
    win.addstr('\n\n WELL...')
    pause(win)
    win.addstr('\n\n I GUESS I SHOULD GO BACK NOW.')
    pause(win)
    win.addstr('\n\n FAREWELL, ADVENTURER!')
    pause(win)


def draw_stage(win, stage, character, rooms_coord, staircase, enemies, items_coord, corridors, radius, floor, trash):
    """
    Display floor
    """
    for itemtype, colorscheme in stage.iter_canvas(character, rooms_coord, staircase, enemies['coord'], items_coord, corridors, radius):
        if itemtype == 'newline':
            win.addstr('\n')
            continue
        win.addstr(itemtype, curses.color_pair(colorscheme))
    win.addstr('\n')
    win.addstr('   FLOOR {}'.format(floor))
    win.addstr('   |   ENEMIES ON THIS FLOOR: {}    |'.format(len(enemies['list'])-len(trash)))
    win.addstr('|    CHARACTER LEVEL {}'.format(character.level))
    win.addstr('   |   HP: {}/{}'.format(character.HP, character.maxHP))
    if character.armed:
        win.addstr('   |   WEAPON EQUIPPED')


def refresh_screen(win, stage, character, rooms_coord, staircase, enemies, items_coord, corridors, radius, floor, trash):
    """
    Refresh floor display
    """
    win.clear()
    draw_stage(win, stage, character, rooms_coord, staircase, enemies, items_coord, corridors, radius, floor, trash)



def checkcharacterinfo(win, character):
    """
    Display character info
    """
    win.addstr('\n\n\n---------------------------------------------------------------------------------------')
    win.addstr('\n\n  CHARACTER INFO:')
    win.addstr('\n\n\n   LEVEL: {}'.format(character.level))
    win.addstr('\n\n   HP: {}/{}'.format(character.HP, character.maxHP))
    win.addstr('\n\n   EXP: {}/{}'.format(character.exp, (character.level+4)*character.level))
    win.addstr('\n\n   DAMAGE DEALT: {}'.format(character.damage))
    win.addstr('\n\n\n---------------------------------------------------------------------------------------')

def openjournal(win, quests):
    """
    Display achievements list with current completion status
    """
    win.addstr('\n\n\n---------------------------------------------------------------------------------------')
    win.addstr('\n\n  JOURNAL:')
    win.addstr('\n\n\n   FIND A WEAPON [{}]'.format(quests['weapon'].state))
    win.addstr('\n\n   DEFEAT 10 MONSTERS [{}]'.format(quests['defeat1'].state))
    win.addstr('\n\n   DEFEAT 50 MONSTERS [{}]'.format(quests['defeat5'].state))
    win.addstr('\n\n   DEFEAT 100 MONSTERS [{}]'.format(quests['defeat10'].state))
    win.addstr('\n\n   DEFEAT 200 MONSTERS [{}]'.format(quests['defeat20'].state))
    win.addstr('\n\n   DEFEAT 500 MONSTERS [{}]'.format(quests['defeat50'].state))
    win.addstr('\n\n   REACH LEVEL 5 [{}]'.format(quests['level5'].state))
    win.addstr('\n\n   REACH LEVEL 10 [{}]'.format(quests['level10'].state))
    win.addstr('\n\n   REACH LEVEL 15 [{}]'.format(quests['level15'].state))
    win.addstr('\n\n   REACH LEVEL 20 [{}]'.format(quests['level20'].state))
    win.addstr('\n\n   REACH LEVEL 25 [{}]'.format(quests['level25'].state))
    win.addstr('\n\n\n---------------------------------------------------------------------------------------')

def openmenu(win, character, quests):
    """
    Display menu
    """
    win.clear()
    win.addstr('\n\n  --------------- MENU ---------------')
    win.addstr('\n\n\n\n  > CHECK CHARACTER INFO')
    win.addstr('\n\n   OPEN JOURNAL')
    win.addstr('\n\n   REVIEW CONTROLS')
    win.addstr('\n\n   RESUME GAME')
    win.addstr('\n\n   EXIT GAME\n\n')
    win.nodelay(True)
    key = ''
    cursor = 0
    while True:
        try:
            key = win.getkey()
            if str(key) == 'z':
                cursor = (cursor-1) % 5
            elif str(key) == 's':
                cursor = (cursor+1) % 5

            if cursor == 0:
                win.clear()
                win.addstr('\n\n  --------------- MENU ---------------')
                win.addstr('\n\n\n\n  > CHECK CHARACTER INFO')
                win.addstr('\n\n   OPEN JOURNAL')
                win.addstr('\n\n   REVIEW CONTROLS')
                win.addstr('\n\n   RESUME GAME')
                win.addstr('\n\n   EXIT GAME\n\n')
                if key == os.linesep:
                    checkcharacterinfo(win, character)

            elif cursor == 1:
                win.clear()
                win.addstr('\n\n  --------------- MENU ---------------')
                win.addstr('\n\n\n\n   CHECK CHARACTER INFO')
                win.addstr('\n\n  > OPEN JOURNAL')
                win.addstr('\n\n   REVIEW CONTROLS')
                win.addstr('\n\n   RESUME GAME')
                win.addstr('\n\n   EXIT GAME\n\n')
                if key == os.linesep:
                    openjournal(win, quests)

            elif cursor == 2:
                win.clear()
                win.addstr('\n\n  --------------- MENU ---------------')
                win.addstr('\n\n\n\n   CHECK CHARACTER INFO')
                win.addstr('\n\n   OPEN JOURNAL')
                win.addstr('\n\n  > REVIEW CONTROLS')
                win.addstr('\n\n   RESUME GAME')
                win.addstr('\n\n   EXIT GAME\n\n')
                if key == os.linesep:
                    reviewcontrols(win)

            elif cursor == 3:
                win.clear()
                win.addstr('\n\n  --------------- MENU ---------------')
                win.addstr('\n\n\n\n   CHECK CHARACTER INFO')
                win.addstr('\n\n   OPEN JOURNAL')
                win.addstr('\n\n   REVIEW CONTROLS')
                win.addstr('\n\n  > RESUME GAME')
                win.addstr('\n\n   EXIT GAME\n\n')
                if key == os.linesep:
                    return

            elif cursor == 4:
                win.clear()
                win.addstr('\n\n  --------------- MENU ---------------')
                win.addstr('\n\n\n\n   CHECK CHARACTER INFO')
                win.addstr('\n\n   OPEN JOURNAL')
                win.addstr('\n\n   REVIEW CONTROLS')
                win.addstr('\n\n   RESUME GAME')
                win.addstr('\n\n  > EXIT GAME\n\n')
                if key == os.linesep:
                    win.addstr('\n\n\n---------------------------------------------------------------------------------------')
                    win.addstr('\n\n  ARE YOU SURE?')
                    win.addstr('\n\n  > STAY')
                    win.addstr('\n\n   QUIT ANYWAYS\n\n')
                    cursor2 = False
                    while True:
                        """
                        Ask for confirmation
                        """
                        try:
                            key = win.getkey()
                            if str(key) == 'z' or str(key) == 's':
                                cursor2 = not cursor2

                            if cursor2 == 0:
                                win.clear()
                                win.addstr('\n\n  --------------- MENU ---------------')
                                win.addstr('\n\n\n\n   CHECK CHARACTER INFO')
                                win.addstr('\n\n   OPEN JOURNAL')
                                win.addstr('\n\n   REVIEW CONTROLS')
                                win.addstr('\n\n   RESUME GAME')
                                win.addstr('\n\n  > EXIT GAME\n\n')
                                win.addstr('\n\n\n---------------------------------------------------------------------------------------')
                                win.addstr('\n\n  ARE YOU SURE?')
                                win.addstr('\n\n  > STAY')
                                win.addstr('\n\n   QUIT ANYWAYS\n\n')
                                if key == os.linesep:
                                    win.clear()
                                    win.addstr('\n\n  --------------- MENU ---------------')
                                    win.addstr('\n\n\n\n   CHECK CHARACTER INFO')
                                    win.addstr('\n\n   OPEN JOURNAL')
                                    win.addstr('\n\n   REVIEW CONTROLS')
                                    win.addstr('\n\n   RESUME GAME')
                                    win.addstr('\n\n  > EXIT GAME\n\n')
                                    break

                            elif cursor2 == 1:
                                win.clear()
                                win.addstr('\n\n  --------------- MENU ---------------')
                                win.addstr('\n\n\n\n   CHECK CHARACTER INFO')
                                win.addstr('\n\n   OPEN JOURNAL')
                                win.addstr('\n\n   REVIEW CONTROLS')
                                win.addstr('\n\n   RESUME GAME')
                                win.addstr('\n\n  > EXIT GAME\n\n')
                                win.addstr('\n\n\n---------------------------------------------------------------------------------------')
                                win.addstr('\n\n  ARE YOU SURE?')
                                win.addstr('\n\n   STAY')
                                win.addstr('\n\n  > QUIT ANYWAYS\n\n')
                                if key == os.linesep:
                                    return True
                        except:
                            pass

        except:
            pass

