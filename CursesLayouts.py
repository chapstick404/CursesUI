import curses
import curses.textpad


import CursesLogger
import CursesWidgets
import abc


class Layout(CursesWidgets.DisplayWidget):
    widgets: list[CursesWidgets.DisplayWidget]
    win: curses.window
    logger: CursesLogger.Logger

    def __init__(self, log_level: int = 0):
        super().__init__()
        self.log_level = log_level
        self.active_widget = None
        self.new_handle = None
        self.value = -1
        self.widgets = []
        self.value = -1
        self.screen = []
        self.allow_input = True
        self.colorlist = (("red", curses.COLOR_RED),
                          ("green", curses.COLOR_GREEN),
                          ("yellow", curses.COLOR_YELLOW),
                          ("blue", curses.COLOR_BLUE),
                          ("cyan", curses.COLOR_CYAN),
                          ("magenta", curses.COLOR_MAGENTA),
                          ("black", curses.COLOR_BLACK),
                          ("white", curses.COLOR_WHITE))
        self.colors = {}
        colorpairs = 0
        for name, i in self.colorlist:
            colorpairs += 1
            curses.init_pair(colorpairs, curses.COLOR_WHITE, i)
            self.colors[name] = curses.color_pair(i)

    @abc.abstractmethod
    def add_widget_to_layout(self, widget: CursesWidgets.DisplayWidget):
        pass

    def get_widget(self, pos):
        return self.widgets[pos]

    def clear_widgets(self):
        for item in self.widgets:
            del item
        self.widgets = []
        self.win.clear()

    def add_widget(self, widget: CursesWidgets.DisplayWidget,
                   color_pair=None):
        self.widgets.append(widget)
        widget.logger = self.logger
        self.active_widget = 0
        self.add_widget_to_layout(widget)
        return widget

    def draw_self(self):
        self.draw()

    def draw(self, logger=None):
        for widget in self.widgets:
            self.logger.log("Drawing Widget", str(widget.win.getbkgd()))
            self.new_handle = widget.draw()
        self.win.refresh()

    def change_active(self):
        self.active_widget += 1
        if self.active_widget > len(self.widgets) - 1:
            self.active_widget = 0
        if self.widgets[self.active_widget].accept_input:
            self.move_to_active()
        else:
            self.active_widget -= 1

    def move_to_active(self):
        self.win.move(self.widgets[self.active_widget].win.getbegyx()[0],
                      self.widgets[self.active_widget].win.getbegyx()[1])
        self.win.cursyncup()

    # def update_to_active(self):  # todo remove
    #     if hasattr(self.widgets[self.active_widget], "value"):
    #         if self.widgets[self.active_widget].text != -1:
    #             self.value = self.widgets[self.active_widget].text

    def input(self, keypress):
        if keypress == 9:
            self.change_active()
        else:
            self.widget_input(keypress)

    def widget_input(self, keypress):  # todo send input for any widget
        if self.widgets[self.active_widget].accept_input:  # check to see if the widget can accept input
            # noinspection PyUnresolvedReferences
            self.widgets[self.active_widget].handle_input(keypress)
        else:
            return

    def save_screen(self):
        self.screen.append(self.widgets)
        return len(self.screen) - 1

    def load_screen(self, pos):
        self.widgets = self.screen[pos]
        self.win.clear()
        self.draw()


class HorizonalLayout(Layout):

    def add_widget_to_layout(self, widget: CursesWidgets.DisplayWidget):
        num_widgets = len(self.widgets)
        widget_win_size = [self.win.getmaxyx()[0], int(self.win.getmaxyx()[1] / num_widgets)]
        for index in range(num_widgets):
            # creates a basic horizontal layout
            self.logger.log("Making window", str((0, int(self.win.getmaxyx()[1] / num_widgets) * (num_widgets - 1))))
            new_win = self.win.derwin(0, widget_win_size[1] * index)
            self.widgets[index].add_win(new_win)
            self.widgets[index].resize(self.win.getmaxyx()[0], int(self.win.getmaxyx()[1] / num_widgets))
            self.widgets[index].win.bkgd(' ', list(self.colors.values())[index])
            self.active_widget = index


class VerticalLayout(Layout):
    def add_widget_to_layout(self, widget: CursesWidgets.DisplayWidget):
        num_widgets = len(self.widgets)
        widget_win_size = [int(self.win.getmaxyx()[0] / num_widgets), self.win.getmaxyx()[1]]
        for index in range(num_widgets):
            self.logger.log("Making window", str((widget_win_size[0], widget_win_size[1] * (num_widgets - 1))))
            new_win = self.win.derwin(widget_win_size[0] * index, 0)
            self.widgets[index].add_win(new_win)
            self.widgets[index].resize(widget_win_size[0], widget_win_size[1])
            self.widgets[index].win.bkgd(' ', list(self.colors.values())[index])
            self.active_widget = index
