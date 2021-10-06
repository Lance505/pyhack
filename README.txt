---------------------------------------------------------------------------
                		PYHACK
---------------------------------------------------------------------------


I. Brief description

This is a simplified reproduction of the popular nethack game.
It is a single-player roguelike game featuring text-based graphics.
This version was entirely made using the python language.



II. How to start the program

Make sure all following modules have been placed in the same directory:
    classes.py
    generate.py
    explore.py
    dessin.py
    pyhack.py

To launch the game, start by opening a terminal window and maximizing it (else the game won't display).
Then, type in the following command line: $ python3 pyhack.py



III. How to play

You will encounter a small variety of symbols as you play:
    @		is your character
    .		is an accessible position inside a room
    #		is an accessible position inside a corridor
    €		is a staircase used to access the next floor (each floor map also has a randomly assigned hidden staircase permitting access to a secret floor)
    m or M	is a monster which will deal 1 damage if it reaches a position adjacent to yours (number increases with floor height)
    ?		is a magic scroll which will restore half of your current max HP (only 1 per floor, consumed after use)

Do note that your field of vision is limited, and only symbols within it will be displayed.
Use your zqsd keys to move around in the dungeon and arrow keys to attack in a given direction.
You will not be able to deal damage unless you have a weapon equipped.
Access Menu anytime while playing using your keyboard's E key.
The game ends once you have reached the top floor or your HP has run out.
You may also exit through the menu.



IV. Others

Game made using the python editor vim and curses module for graphic interface.
