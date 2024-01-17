import CursesWidgets
import CursesLayouts
import curses
import abc
import CursesLogger

class Display(abc.ABC):
    _layout: CursesLayouts.Layout

    def __init__(self, scrn: curses.window, log_level=0):
        self.logger = CursesLogger.Logger(log_level)
        self.active_widget = None
        self.new_handle = None
        self.value = -1
        self.widgets = []
        self.scrn = scrn
        self.value = -1
        self.screen = []

    @property
    def layout(self):
        """The layout of the base screen"""
        return self._layout

    @layout.setter
    def layout(self, value: CursesLayouts.Layout): #todo change to make class here
        scrn_size = self.scrn.getmaxyx()
        self._layout = value
        self._layout.win = self.scrn.derwin(0,0)
        self._layout.win.resize(scrn_size[0], scrn_size[1])
        self._layout.logger = self.logger

    def draw_scrn(self):
        self.logger.log("Drawing Layout " + str(self._layout), "Cursor Position: " + str(self.scrn.getyx()))
        self._layout.draw()
        self.logger.log("Drawing screen", "Cursor Position: " + str(self.scrn.getyx()))
        self.scrn.refresh()


    def clear_layout(self): #may cause memory leak
        self._layout.clear_widgets()
        self.scrn.clear()

    def handle_input(self, keypress=None):
        self.logger.log("Handling Input", "Cursor Position: " + str(self.scrn.getyx()))
        if keypress is None:
            keypress = self.scrn.getch()
        if keypress == 9:
            self._layout.change_active()
        else:
            self._layout.input(keypress)

    def wait_for_enter(self):
        keypress = self.scrn.getch()
        if str(curses.keyname(keypress)) == "b'^J'":
            return False
        else:
            self.handle_input(keypress)
            return True
