import random
import curses
from time import sleep

stdscr = curses.initscr()
curses.noecho()
stdscr.keypad(1)
curses.cbreak()
curses.curs_set(0)

MAP_HEIGHT = 20
MAP_WIDTH = 50


stdscr.addstr(5,5,"Catch all the goblins!")
stdscr.addstr(10,5,"Use number pad to move, 'x' to quit.")
stdscr.addstr(15,5,"Melee combat only, just bump into things!")
stdscr.addstr(20,5,"Press any key to start.")
stdscr.refresh()

anykey = stdscr.getch()
stdscr.clear()
stdscr.refresh()


gmap = []

for i in range (MAP_HEIGHT):
    gmap.append([])
    for j in range (MAP_WIDTH):
        gmap[i].append(None)


class Being:
    def __init__ (self, ypos, xpos, char, init_hp, init_strength, init_intel):
        self.y = ypos
        self.x = xpos
        self.glyph = char
        self.hp = init_hp
        self.strength = init_strength
        self.intel = init_intel
        self.dead = False
        self.move(0,0)
    def move (self,ymod,xmod):
        if self.glyph == '@':
            stdscr.addstr(3,51,"         ")
            stdscr.addstr(3,51,"HP {0}".format(str(self.hp)))
        if self.hp < 1 and self.dead == False:
            self.dead = True
            self.glyph = ' '
            stdscr.addch(self.y,self.x,self.glyph)
            stdscr.refresh()
        newy = self.y + ymod
        newx = self.x + xmod
        if  self.dead == False and newy >= 0 and \
         newy < MAP_HEIGHT and newx >= 0 \
         and newx < MAP_WIDTH:
            if gmap[newy][newx] == None or gmap[newy][newx].glyph == ' ':
                gmap[self.y][self.x] = None
                stdscr.addch(self.y,self.x,' ')
                self.y = self.y + ymod
                self.x = self.x + xmod
                gmap[self.y][self.x] = self
                stdscr.addch(self.y,self.x,self.glyph)
                stdscr.refresh()
            elif gmap[newy][newx].glyph != '#' and \
                    self.glyph != gmap[newy][newx].glyph:
                gmap[newy][newx].hp -= random.randrange(self.strength)

player = Being(0,0,'@',10,10,10)

goblins = []


for q in range (20):
    randpos = random.randrange(5) + 10
    newgoblin = Being (randpos,q,'g',5,5,5)
    goblins.append(newgoblin)

escape = 0
while escape == 0:
    if player.hp < 1:
        print "Game Over"
        escape == 1
    inpt = stdscr.getch()
    if inpt == ord('8'):
        player.move (-1, 0)
    elif inpt == ord('7'):
        player.move (-1,-1)
    elif inpt == ord('4'):
        player.move (0, -1)
    elif inpt == ord('1'):
        player.move(1, -1)
    elif inpt == ord('2'):
        player.move (1, 0)
    elif inpt == ord('6'):
        player.move (0, 1)
    elif inpt == ord('3'):
        player.move (1,1)
    elif inpt == ord('9'):
        player.move(-1,1)
    elif inpt == ord('5'):
        player.move(0,0)
    elif inpt == ord('x'):
        escape = 1
    winnertest = 1
    for v in range (len(goblins)):
        goblins[v].move (random.randrange(2)-1,random.randrange(2)-1)
        if goblins[v].dead == False:
            winnertest -= 1
    if winnertest == 1:
        print "YOU WON"

curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()
