import curses

# content - array of lines (list)
mylines = ["Line {0} ".format(id)*3 for id in range(1,14)]

import pprint
pprint.pprint(mylines)

def main(stdscr):
  hlines = begin_y = begin_x = 5 ; wcols = 10
  # calculate total content size
  padhlines = len(mylines)
  padwcols = 0
  for line in mylines:
    if len(line) > padwcols: padwcols = len(line)

  stdscr.addstr("padhlines "+str(padhlines)+" padwcols "+str(padwcols)+"; ")
  mypads = curses.newpad(padhlines, padwcols)

  stdscr.addstr(str(type(mypads)))

  mypads.scrollok(1)
  mypads.idlok(1)

  line_num = 0
  for line in mylines:

    mypads.addstr(line_num,1, line)
    line_num += 1

  stdscr.refresh()

  mypads.refresh(0,0, begin_y,begin_x, begin_y+hlines, begin_x+padwcols)

  keypressed = ""
  while keypressed != 'KEY_HOME':
    if keypressed == "KEY_DOWN":
      mypads.scroll(1)
    elif keypressed == "KEY_UP":
      mypads.scroll(-1)
    mypads.refresh(0, 0, begin_y, begin_x, begin_y + hlines, begin_x + padwcols)
    keypressed = stdscr.getkey()
    #mypads.refresh()

curses.wrapper(main)