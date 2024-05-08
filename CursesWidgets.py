import abc
import curses
import curses.textpad
import CursesLogger


class DisplayWidget(abc.ABC):
    """Abstract base class for displaying widgets."""

    win: curses.window
    logger: CursesLogger.Logger

    _accept_input = False

    @property
    def accept_input(self):
        """Property to control if the widget handles input"""
        return self._accept_input

    def add_win(self, win: curses.window):
        """Adds a new window. Should only be used by the owning widget.
        :param win: The window to add.
        :type win: curses.window
        """
        self.logger.log("Widget Gaining Window", str(win))
        self.win = win

    def draw(self):
        """Draws the widget and any widgets the widget owns."""
        self.logger.log("Widget Drawing", str(self))
        self.draw_self()

    @abc.abstractmethod
    def draw_self(self):
        """Draws the widget and only itself."""
        pass

    def resize(self, y: int, x: int):
        """Allows the widget to resize to a new size.
        :param x: x dimension
        :param y: y dimension"""
        self.logger.log("Reszing ", str([y, x]))
        self.win.erase()
        self.win.resize(y, x)


class InputWidget(DisplayWidget):
    """Abstract base class for widgets that can handle input."""

    _accept_input = True

    @property
    def accept_input(self):
        """Property to control if the widget handles input"""
        return self._accept_input

    @accept_input.setter
    def accept_input(self, value):
        self._accept_input = value

    @abc.abstractmethod
    def handle_input(self, keypress):
        """Abstract function to handle keypress.
        :type keypress: str
        :param keypress: Keypress to handle"""
        return True


class ContentWidget(DisplayWidget):
    """Abstract widget that holds a content value"""

    @abc.abstractmethod
    def __init__(self, value):
        self.value = value


class TitleWidget(ContentWidget):
    """A widget that is meant to be a title"""

    def __init__(self, title: str):
        super().__init__(title)

    def draw_self(self):
        self.logger.log("Drawing Title To Screen")
        self.win.addstr(self.value)


class LabelWidget(TitleWidget):
    """A simple widget to put a piece of text on the screen"""

    def __init__(self, text: str):
        super().__init__(text)
        self.value_changed = True

    def draw_self(self, logger=None):  ##todo: allow for position of the lable
        self.logger.log("Label Widget is drawing", str(self))
        if self.win is not None:
            if self.value_changed:
                self.logger.log("Label Widget is refreshing")
                self.win.addstr(0, 0, self.value)
                self.value_changed = False
                self.win.refresh()

    def change_value(self, value):
        """Changes the displayed text."""
        self.logger.log("Label value changed")
        self.value = str(value)
        self.value_changed = True
        self.draw_self()

    def resize(self, y: int, x: int):
        self.value_changed = True
        super().draw_self()


class ListView(InputWidget):
    """Display a list of things and allows for scrolling"""

    def __init__(self, values: list):
        super().__init__()
        self.line_pos = 0
        self.cursor = 0
        self.values = values

    def draw_self(self, logger=None):
        self.logger.log("ListView is drawing")
        self.win.clear()

        if self.win.getmaxyx()[0] > len(self.values):  #todo move to add_win
            lines = len(self.values)
        else:
            lines = self.win.getmaxyx()[0]

        if self.line_pos < 0:
            self.line_pos = 0
        elif self.line_pos + lines > len(self.values):
            self.logger.log("Moving List to fit")
            self.line_pos = len(self.values) - lines

        for index in range(lines):
            if index < len(self.values):
                self.win.addstr(index, 1, self.values[index + self.line_pos])
        self.win.refresh()

    def handle_input(self, keypressed):
        self.logger.log("Handdling keypress")
        keypressed = str(curses.keyname(keypressed))  # is a byte object
        if keypressed == "b'KEY_DOWN'":
            self.line_pos += 1

        elif keypressed == "b'KEY_UP'":
            self.line_pos -= 1

        elif keypressed == "b'^J'":
            return True


class MultiColumnList(ListView):
    """Displays a list with multiple columns"""

    def __init__(self, values: list):
        super().__init__(values)
        self.lists = []

    def add_win(self, win: curses.window):
        self.win = win
        columns = len(self.values[0])
        spacing = int(self.win.getmaxyx()[1] / columns) - 1
        self.lists = []
        for row in self.values:
            complete_row = ''
            for item in row:
                item = str(item)
                if len(item) > spacing:
                    complete_row += item[:spacing]
                elif len(item) < spacing:
                    spaces = " " * (spacing - len(item))
                    complete_row += item + spaces
                else:
                    complete_row = item
            self.lists.append(complete_row)
        self.values = self.lists


class ListMenu(ListView):
    """A menu that is a list of options"""

    def __init__(self, values: list):
        super().__init__(values)
        self.value = None
        self.list_pos = 0
        self.cursor = 1

    def draw_self(self, logger=None):
        self.logger.log("MultiColumnList is drawing")
        self.win.clear()
        if self.win.getmaxyx()[0] > len(
                self.values):  # makes sure the list wont wrap around if the screen is bigger then the values
            lines = len(self.values)
        else:
            lines = self.win.getmaxyx()[0]

        self.logger.log("Moving Selection")
        if self.cursor > lines:
            self.list_pos += 1
            self.cursor = lines
        elif self.cursor < 1:
            self.list_pos -= 1
            if self.list_pos < 0:
                self.list_pos = 0
            self.cursor = 1

        if self.list_pos + lines > len(self.values):
            self.list_pos = len(self.values) - lines
        for index in range(0, lines):
            if index + 1 == self.cursor:
                self.win.addstr(index, 1, self.values[index + self.list_pos], curses.A_STANDOUT)
            else:
                self.win.addstr(index, 1, self.values[index + self.list_pos])
        self.win.refresh()

    def handle_input(self, keypressed):
        self.logger.log("Handdling keypress")
        keypressed = str(curses.keyname(keypressed))
        if keypressed == "b'KEY_DOWN'":

            self.cursor += 1

        elif keypressed == "b'KEY_UP'":
            self.cursor -= 1

        elif keypressed == "b'^J'":
            self.value = self.cursor + self.list_pos - 1


class TextBox(InputWidget):
    def __init__(self):
        super().__init__()
        self.value = None
        self.text_box = None
        self.editwin = None

    def add_win(self, win: curses.window):
        self.win = win
        self.win.box()
        self.editwin = self.win.derwin(self.win.getmaxyx()[0] - 2, self.win.getmaxyx()[1] - 2, 1, 1)
        self.text_box = curses.textpad.Textbox(self.editwin)
        self.editwin.cursyncup()
        self.editwin.refresh()

    def draw_self(self):  # todo change size
        self.editwin.refresh()

    def handle_input(self, keypress):
        self.logger.log("Textbox handling keypress")
        if self.text_box.do_command(keypress) == 0:
            self.value = self.text_box.gather()
        self.editwin.cursyncup()
        self.editwin.refresh()

    def resize(self, y: int, x: int):
        self.logger.log("Textbox resizing windows")
        self.win.clear()
        self.win.resize(y, x)
        self.win.box()
        self.editwin.resize(y - 2, x - 2)


class TextInput(TextBox):
    # todo add user help text option
    def add_win(self, win: curses.window):
        self.win = win
        y, x = self.win.getmaxyx()
        self.win.resize(3, x)
        self.editwin = self.win.derwin(1, 1)
        self.text_box = curses.textpad.Textbox(self.editwin)
        self.editwin.refresh()

    def handle_input(self, keypress):
        self.logger.log("TextInput handling keypress")
        if str(curses.keyname(keypress)) == "b'^J'":
            self.value = self.text_box.gather()
        if self.text_box.do_command(keypress) == 0:
            self.value = self.text_box.gather()
        self.editwin.refresh()

    def resize(self, y: int, x: int):
        self.logger.log("TextInput resizing window")
        self.win.clear()
        self.win.resize(3, x)
        self.win.box()
        self.editwin.resize(1, x - 3)
        self.win.refresh()
