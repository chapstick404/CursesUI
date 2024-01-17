import CursesDisplay
import CursesWidgets
import CursesLayouts
import curses


def main(stdscr):
    curses.start_color()
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)
    display = CursesDisplay.Display(stdscr, log_level=2)
    mylines = ["Line {0} ".format(id) * 3 for id in range(14)]
    myMultiLines = [['test0', 'test0b', 'test0c'], ['test1', 'test1b', 'test1c'], ['test2', 'test2b']]
    label = CursesWidgets.LabelWidget("test1")
    label2 = CursesWidgets.LabelWidget("test2")
    label3 = CursesWidgets.LabelWidget("test3")
    label4 = CursesWidgets.LabelWidget("test1")
    label5 = CursesWidgets.LabelWidget("test2")

    textinput = CursesWidgets.TextBox()
    # layout = CursesLayouts.HorizonalLayout()
    vertlayout1 = CursesLayouts.VerticalLayout()
    display.layout = vertlayout1
    # layout.add_widget(vertlayout1)
    vertlayout1.add_widget(label)
    vertlayout1.add_widget(label2)
    vertlayout1.add_widget(label3)
    #layout.add_widget(textinput)


    display.draw_scrn()
    #layout.add_widget(CursesWidgets.ListView(mylines))
    #layout.add_widget(textinput)

    while display.wait_for_enter():
        display.draw_scrn()


    selcetion = display.get_value_of_widget(0)
    display.clear_widgets()
    display.add_widget(CursesWidgets.TitleWidget(str(selcetion)))
    display.draw_scrn()
    while True:
        display.widget_input()

def smalltests(stdscr: curses.window):
    colorlist = (("red", curses.COLOR_RED),
                      ("green", curses.COLOR_GREEN),
                      ("yellow", curses.COLOR_YELLOW),
                      ("blue", curses.COLOR_BLUE),
                      ("cyan", curses.COLOR_CYAN),
                      ("magenta", curses.COLOR_MAGENTA),
                      ("black", curses.COLOR_BLACK),
                      ("white", curses.COLOR_WHITE))
    colors = {}
    colorpairs = 0
    for name, i in colorlist:
        colorpairs += 1
        curses.init_pair(colorpairs, curses.COLOR_WHITE, i)
        colors[name] = curses.color_pair(i)
    stdscr.bkgd(' ', colors["green"])

    testwin1 = stdscr.derwin(stdscr.getmaxyx()[0], 4, 0,0) #todo use this in actual code
    testwin1.bkgd(' ', colors["red"])
    # testwin1.refresh()
    stdscr.refresh()

    testwin1.mvderwin(0,5)
    testwin1.erase()
    testwin1.addstr(4, 0, "bl")
    #stdscr.touchwin()
    testwin1.refresh()
    while True:
        stdscr.refresh()
def test(stdscr):
    curses.start_color()
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)

    stdscr.bkgd(' ', curses.color_pair(7))
    stdscr.addstr(str(curses.color_pair(5)))
    while True:
        keypress = stdscr.getch()
        stdscr.addstr(str(curses.keyname(keypress)))


curses.wrapper(main)
