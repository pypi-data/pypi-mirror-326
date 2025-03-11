import pygame as pg
from copy import deepcopy


class Color:
    """
    Store colors. Can add and get the colors. This class doesn't need to be instantiated.
    """

    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203),
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "grey": (128, 128, 128),
        "light_blue": (173, 216, 230),
        "dark_blue": (25, 25, 112),
        "light_green": (144, 238, 144),
        "dark_green": (0, 100, 0),
        "light_grey": (211, 211, 211),
        "dark_grey": (169, 169, 169),
        "brown": (139, 69, 19),
        "beige": (249, 228, 183),
        "gold": (255, 215, 0),
        "silver": (192, 192, 192),
        "magenta": (255, 0, 255),
    }

    @staticmethod
    def add_color(color_name, value_rgb):
        """
        :param color_name: name of the added color.
        :param value_rgb: RGB value of the added color.

        Add a new color into the dictionary.
        """
        Color.colors[str(color_name)] = value_rgb

    @staticmethod
    def get_color(color_requested):
        """
        :param color_requested: name of the requested color.
        :return: the RGB value of the requested color.
        """

        color_requested = color_requested.lower()

        for color_name, color_rgb in Color.colors.items():
            if color_name == color_requested:
                return color_rgb

        return None


class Text:
    """
    Create, change and display text.

    ATTRIBUTES:

        - I: _window: Surface object to draw and display the text in.
        - I: _text: text to display.

        - FONT:
            - I: _font_name: text font name.
            - I: _font_size: text font size.
            - I: _is_bold: is font bold.
            - I: _is_italic: is font italic.
            - O: _font: Font object representing the font features.
            
        - POSITION:
            - I: _pos: list of the vertical and horizontal position.
            - I: _alignment: is the text aligned, 0 by default:
                - 0: align at left.
                - 1: centre in the middle.
                - 2: align at right.

        - CHARACTERISTICS:
            - O: _size: text width and height depending on the font size.
            
        - APPEARANCE:
            - I: _color: text color in RGB.
        
        - SURFACE:
            - O: _surface: Surface object representing the text.

    METHODS:

        - SETTERS:
            - set_pos(): set a new text position with the centred setting.
            - set_text(): set a new text.
            - set_font(): set a new Font object.
            - set_alignment(): set a new alignment setting.
            - set_color(): set the color attribute.

        - GETTERS:
            - get_pos(): return the position.
            - get_size(): return the size.
            - get_text(): return the text displayed.
            - get_font(): return the text Font object.
            - get_surface(): return the Surface object representing the text.

        - render(): render the text into one Surface object.
        - draw(): draw the text on the _window depending on the x and y position.
    """

    def __init__(self, window, text, **kwargs):

        self._window = window  # Surface to display the text.
        self._text = text  # Text to display.

        # FONT:
        self._font_name = kwargs.get("font_name", "arial")  # Font name of the text.
        self._font_size = kwargs.get("font_size", 20)  # Font size of the text.

        self._is_bold = kwargs.get("is_bold", False)  # Is font bold.
        self._is_italic = kwargs.get("is_italic", False)  # Is font italic.

        # Font object representing the font features.
        self._font = pg.font.SysFont(self._font_name, self._font_size, self._is_bold, self._is_italic)

        # POSITION:
        self._pos = list(kwargs.get("pos", [0, 0]))  # Tuple with coordinates of text bottom left corner
        self._alignment = kwargs.get("alignment", 0)  # Is the text centred.

        # CHARACTERISTICS:
        self._size = [0, 0]  # Size is computed while rendering.

        # APPEARANCE:
        self._color = list(kwargs.get("color", [255, 255, 255]))  # Color of the text in RGB. White by default.

        # SURFACE
        self._surface = None  # Surface object containing the text, will be set in the render_text() method.
    
    def __str__(self):
        return self._text

    def set_pos(self, new_pos):
        self._pos = list(new_pos)

    def set_text(self, new_text):
        self._text = new_text

    def set_font(self, font_name="arial", font_size=20, is_bold=False, is_italic=False):
        """
        :param font_name: font name.
        :param font_size: font size.
        :param is_bold: is font bold.
        :param is_italic: is font italic.

        Set the Font object.
        """

        self._font = pg.font.SysFont(font_name, font_size, is_bold, is_italic)

    def set_alignment(self, new_alignment):
        self._alignment = new_alignment

    def set_color(self, new_color):
        self._color = list(new_color)

    def get_pos(self):
        return tuple(self._pos)

    def get_size(self):
        return tuple(self._size)
    
    def get_text(self):
        return self._text

    def get_font(self):
        return self._font

    def get_surface(self):
        return self._surface

    def render(self):
        """
        Create a Surface object gathering all lines of the text.
        """

        lines = self._text.split("\n")  # Split the string according to the line breaks.
        text_surfaces = [self._font.render(line, True, self._color, None) for line in lines]

        line_height = text_surfaces[0].get_height()  # Height of one line.

        self._size = [
            max([surface.get_width() for surface in text_surfaces]),
            sum([surface.get_height() for surface in text_surfaces])
        ]

        # Set the Surface object gathering all lines.
        # I don't really understand what SRCALPHA is but ChatGPT seems to know.
        self._surface = pg.Surface((self._size[0], self._size[1]), pg.SRCALPHA)

        y = 0  # y position in the Surface object.

        for surface in text_surfaces:  # Loop into the Surface object of each line.

            if self._alignment == 0:
                # Compute the x position to align the text at left.
                x = 0
            elif self._alignment == 1:
                # Compute the x position to centre the text in the middle.
                x = self._size[0] / 2 - surface.get_width() / 2
            elif self._alignment == 2:
                # Compute the x position to align the text at right.
                x = self._size[0] - surface.get_width()
            else:
                # Set default value.
                x = 0

            self._surface.blit(surface, (x, y))  # Draw the line into the Surface.

            y += line_height  # Shift back the y position.

        self._surface.set_alpha(255)  # Set a transparent background.

    def draw(self):
        """
        Position the Surface object gathering all lines and draw it on the _window.
        """

        self._window.blit(self._surface, tuple(self._pos))


class Button:
    """
    Create, display and handle a button.

    ATTRIBUTES:

        - I: _window: Surface object to draw and display the text in.
        - I: _text: Text object representing the text to display.

        - POSITION:
            - I: _pos: button position.
            - I: _margins: button margins.

        - CHARACTERISTICS:
            - O: _size: button size according to the text size and the margins.
            
        - APPEARANCE:
            - I: _color: button color in RGB.
        
        - STATE:
            - O: _is_clicked: is the button clicked by any mouse button.
            - O: _mouse_buttons_pressed: list representing each mouse button,
                                         True if the button is pressed, False if not.

        - SURFACE:
            - O: _surface: Surface object containing the whole button.

    METHODS:

        - SETTERS:
            - set_text(): set the text.

            - set_pos(): set button positions.
            - set_margins(): set new margins.

            - set_color(): set the button color.
            
            - rest_is_clicked(): reset the button clicked state.

        - GETTERS:
            - get_text(): return the displayed text.
            
            - get_pos(): return the button position.
            - get_margins(): return the margins size.
            
            - get_size(): return the button size.
            
            - get_color(): return the color in RGB.
            
            - get_is_clicked(): return the button clicked state.
            - get_mouse_button_pressed(): return which mouse button is pressed.
            
            - get_surface(): return the Surface object representing the button

        - render(): set the attribute button_surface and button_rect.
        - draw(): draw the whole button into the Surface object given.

        - handle_event(): update the button state attributes.
    """

    def __init__(self, window, text, **kwargs):

        self._window = window  # Surface to display the text.
        self._text = text  # Text object representing the text in the button.

        # POSITION:
        self._pos = list(kwargs.get("pos", [0, 0]))  # Button position.
        self._margins = list(kwargs.get("margins", [3, 5]))  # Button margins.
        self._text.set_pos((
            self._pos[0] + self._margins[0],
            self._pos[1] + self._margins[1]
        ))

        # CHARACTERISTICS:
        self._size = [0, 0]  # Button size, computed in the render() method.

        # APPEARANCE:
        self._color = list(kwargs.get("color", [128, 128, 128]))  # Color of the background in RGB.
        
        # STATE:
        self._is_clicked = False
        self._mouse_buttons_pressed = [False, False, False]

        # SURFACE:
        self._surface = None  # Surface object containing all the button, will be set in the render() method.
    
    def __str__(self):
        return self._is_clicked

    def set_text(self, new_text):
        self._text = new_text

    def set_pos(self, new_pos):
        self._pos = list(new_pos)
        self._text.set_pos((
            self._pos[0] + self._margins[0],
            self._pos[1] + self._margins[1]
        ))

    def set_margins(self, new_margins):
        self._margins = list(new_margins)
        self._text.set_pos((
            self._pos[0] + self._margins[0],
            self._pos[1] + self._margins[1]
        ))

    def set_color(self, new_color):
        self._color = list(new_color)
        
    def reset_is_clicked(self):
        self._is_clicked = False

    def get_text(self):
        return self._text
    
    def get_pos(self):
        return tuple(self._color)
    
    def get_margins(self):
        return tuple(self._margins)
    
    def get_size(self):
        return tuple(self._size)
    
    def get_color(self):
        return tuple(self._color)
    
    def get_is_clicked(self):
        return self._is_clicked
    
    def get_mouse_button_pressed(self):
        return tuple(self._mouse_buttons_pressed)
    
    def get_surface(self):
        return self._surface

    def render(self):
        """
        Create a Surface object containing the button.
        """

        self._text.render()  # Create a Surface object of the text.

        self._size = [
            self._text.get_size()[0] + self._margins[0],
            self._text.get_size()[1] + self._margins[1]
        ]
        self._surface = pg.Surface(tuple(self._size))  # Set the Surface object.
        self._surface.fill(tuple(self._color))  # Fill the Surface with the button color.

        self._surface.blit(self._text.get_surface(), self._text.get_pos())  # Draw the text into the Surface.

    def draw(self):
        """
        Draw the button into the window.
        """

        self._window.blit(self._surface, tuple(self._pos))

    def handle_event(self, event):
        """
        :param event: PyGame event.
        
        Update the button state attributes depending on if the button is clicked.
        """
        
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_position = pg.mouse.get_pos()
            
            if self._pos[0] < mouse_position[0] < self._pos[0] + self._size[0] and \
                    self._pos[1] < mouse_position[1] < self._pos[1] + self._size[1]:
                self._is_clicked = True
                self._mouse_buttons_pressed = [button_state for button_state in pg.mouse.get_pressed()]
                
            else:
                self._is_clicked = False
                self._mouse_buttons_pressed = [False for _ in range(3)]


class TextInput:
    """
    Create, display and handle text input.
    
    ATTRIBUTES:
        - I: _window: Surface object to draw and display the input zone in.
        
        - TEXT:
            - I: _displayed_text: Text object representing the displayed text.
            - I: _default_text: text displayed by default if the input box is empty.
            - O: _text_input: text input by the user.
            
        - POSITIONS:
            - I: _pos: input zone position.
            - I: _margins: input box margins.
            
        - CHARACTERISTICS:
            - I: _size: input box size.
        
        - APPEARANCE:
            - I: _box_color: input box color.
            
        - STATE:
            - O: _is_active: is the user meddling with the input zone.
            - O: _is_completed: has the user typed 'Enter'.
            
        - SURFACE:
            - O: Surface object containing the box and the text.
        
    METHODS:
        - SETTERS:
            - set_displayed_text(): set a new Text object.
            - set_default_text(): set a new default text.
            
            - set_pos(): set a new position.
            - set_margins(): set new margins.
            - set_size(): set a new size.
            
            - set_box_color(): set a new box color in RGB.
            
        - GETTERS:
            - get_displayed_text(): return the Text object displayed.
            - get_default_text(): return the default text.
            - get_text_input(): return the text input.
            
            - get_pos(): return the position.
            - get_margins(): return the margins size.
            - get_size(): return the box size.
            
            - get_box_color(): return the box color.
            
            - get_surface(): return the Surface object representing the whole box.
        
        - is_active(): return the active state.
        - is_completed(): return the completed state.
        
    """
    
    def __init__(self, window, **kwargs):
        
        self._window = window
        
        # TEXT:
        self._displayed_text = kwargs.get("displayed_text", Text(self._window, ""))
        self._default_text = kwargs.get("default_text", "Type here...")
        self._text_input = ""
        
        # POSITIONS:
        self._pos = list(kwargs.get("pos", [0, 0]))
        self._margins = list(kwargs.get("margins", [3, 5]))
        self._displayed_text.set_pos((self._margins[0], self._margins[1]))
        
        # CHARACTERISTICS:
        self._size = list(kwargs.get("size", [50, 15]))
        
        # APPEARANCE:
        self._box_color = list(kwargs.get("box_color", [128, 128, 128]))
        
        # STATE:
        self._is_active = False
        self._is_completed = False
        
        # SURFACE:
        self._surface = None
    
    def __str__(self):
        return self._text_input
        
    def set_displayed_text(self, new_displayed_text):
        self._displayed_text = new_displayed_text
    
    def set_default_text(self, new_default_text):
        self._default_text = str(new_default_text)
    
    def set_pos(self, new_pos):
        self._pos = list(new_pos)
    
    def set_margins(self, new_margins):
        self._margins = list(new_margins)
        self._displayed_text.set_pos((self._margins[0], self._margins[1]))
    
    def set_size(self, new_size):
        self._size = list(new_size)
        
    def set_box_color(self, new_box_color):
        self._box_color = list(new_box_color)
        
    def get_displayed_text(self):
        return self._displayed_text
    
    def get_default_text(self):
        return self._default_text
    
    def get_text_input(self):
        return self._text_input
    
    def get_pos(self):
        return tuple(self._pos)
    
    def get_margins(self):
        return tuple(self._margins)
    
    def get_size(self):
        return tuple(self._size)
    
    def get_box_color(self):
        return tuple(self._box_color)
    
    def get_surface(self):
        return self._surface
        
    def render(self):
        """
        Render the input zone.
        """
        
        self._displayed_text.render()  # Render the displayed text.
        
        self._surface = pg.Surface(tuple(self._size))  # Set the Surface object depending on the box size.
        
        self._surface.fill(self._box_color)  # Fill the Surface with the color.
        
        self._surface.blit(self._displayed_text.get_surface(), self._displayed_text.get_pos())  # Add the text.
    
    def draw(self):
        """
        Draw the input zone into the window.
        """

        self._window.blit(self._surface, self._pos)
    
    def handle_event(self, event):
        """
        :param event: PyGame event.

        Update text input according to the event.
        """
        
        # If the text input is completed, events are no longer handled.
        if self._is_completed:
            return
        
        self._is_active = False  # Reset the attribute.
        if event.type == pg.MOUSEBUTTONDOWN:   # If one mouse button is pressed.
            mouse_position = pg.mouse.get_pos()
            if self._pos[0] < mouse_position[0] < self._pos[0] + self._size[0] and \
                    self._pos[1] < mouse_position[1] < self._pos[1] + self._size[1]:  # If it's in the right zone.
                if pg.mouse.get_pressed()[0]:  # If it's the left mouse button.
                    self._is_active = True  # The input zone is active.
        
        if event.type == pg.KEYDOWN:
            # if self._is_active:  # If the input zone is active.
                if event.key == pg.K_RETURN:  # Key 'Enter' pressed.
                    self._is_completed = True
                elif event.key == pg.K_BACKSPACE:  # Key 'Backspace' pressed.
                    self._text_input = self._text_input[:-1]
                else:  # Normal key pressed
                    self._text_input = f"{self._text_input}{event.unicode}"

        if self._text_input == "":
            self._displayed_text.set_text(self._default_text)
        else:
            self._displayed_text.set_text(self._text_input)
    
    def is_active(self):
        return self._is_active
    
    def is_completed(self):
        return self._is_completed


class Grid:
    """
    Create, display and handle a grid.
    
    ATTRIBUTES:
        
        - I: _window: Surface object to draw and display the grid in.
            
        - POSITION:
            - I: _pos: grid position on the window.
            
        - GRID:
            - I: _grid_length: number of cells in each row and column.
            - I: _grid_size: grid size.
            
        - CELLS:
            - O: _cells_default_size: cells default size depending on the grid size.
            - I: _cells_default_color: cells default color in RGB.
            
            - O: _cells_attr: Dictionary of a two-dimensional table containing its attributes:
                - "color": cell color in RGB.
                - "size": cell size.
                - "surface": cell Surface object.

        - SURFACE:
            - O: _surface: grid Surface object.
        
    METHODS:
        
        - SETTERS:
            - set_pos(): set the grid position.
            
            - set_cell_size(): set the size of one cell.
            - set_cell_color(): set the color of one cell.
            
            - set_default_size(): set the cells size with the previous default size with the new default size.
            - set_default_color(): set the cells color with the previous default color with the new default color.
            
            - reset_cells_size(): reset all the cells size.
            - reset_cells_color(): reset all the cells color.
            
            - set_grid_length(): resize the grid.
        
        - GETTERS:
            - get_pos(): return the grid position.
            
            - get_grid_length(): return the grid length.
            - get_grid_size(): return the grid size.
            
            - get_cells_default_size(): return the cells default size.
            - get_cells_default_color(): return the cells default color.
            
            - get_surface(): return the grid Surface object.
        
        - render(): render the grid depending on its attributes.
        - draw(): draw the grid into the window.
        
    """

    def __init__(self, window, **kwargs):

        self._window = window
        
        # POSITION:
        self._pos = list(kwargs.get("pos", [0, 0]))
        
        # GRID:
        self._grid_length = list(kwargs.get("grid_length", [3, 3]))
        self._grid_size = list(kwargs.get("grid_size", [500, 500]))
        
        # CELLS:
        self._cells_default_size = [self._grid_size[0] // self._grid_length[0], self._grid_size[1] // self._grid_length[1]]
        self._cells_default_color = list(kwargs.get("default_color", (255, 255, 255)))
        self._cell_attr = {
            "size": self._cells_default_size,
            "color": self._cells_default_color
        }
        
        self._cells_attr = [[deepcopy(self._cell_attr)
                             for _ in range(self._grid_length[0])] for _ in range(self._grid_length[1])]

        # SURFACE:
        self._surface = pg.Surface(tuple(self._grid_size))  # Set the principle Surface dimensions.
    
    def set_pos(self, new_pos):
        self._pos = new_pos
    
    def set_grid_length(self, new_grid_length):
        """
        :param new_grid_length: new number of cells in each row and column.
        
        Resize the grid.
        """

        prev_grid_length = self._grid_length
        self._grid_length = new_grid_length

        # Update the grid size.
        self._grid_size = [self._grid_length[0] * self._cells_default_size[0],
                           self._grid_length[1] * self._cells_default_size[1]]
        # Update the Surface object.
        self._surface = pg.Surface(tuple(self._grid_size))
        
        # If the previous abscissa is bigger than the new.
        if prev_grid_length[0] > self._grid_length[0]:
            for row in self._cells_attr:
                del row[self._grid_length[0]: -1]
        
        # If the previous ordinate is bigger than the new.
        if prev_grid_length[1] > self._grid_length[1]:
            del self._cells_attr[self._grid_length[1]: -1]
        
        # If the previous abscissa is smaller than the new.
        if prev_grid_length[0] < self._grid_length[0]:
            for row in self._cells_attr:
                for _ in range(self._grid_length[0] - prev_grid_length[0]):
                    row.append({"color": self._cells_default_color, "size": self._cells_default_size})
        
        # If the previous ordinate is smaller than the new.
        if prev_grid_length[1] < self._grid_length[1]:
            row = [{"color": self._cells_default_color, "size": self._cells_default_size}
                   for _ in range(self._grid_length[0])]
            for _ in range(self._grid_length[1] - prev_grid_length[1]):
                self._cells_attr.append(row)
        
    def set_cell_size(self, pos, size):
        """
        :param pos: cell position in the grid.
        :param size: cell size.

        Change cell size.
        """
        
        self._cells_attr[pos[1]][pos[0]]["size"] = list(size)
        
    def set_cell_color(self, pos, color):
        """
        :param pos: cell position in the grid.
        :param color: cell color.
        
        Change cell color.
        """
        
        self._cells_attr[pos[1]][pos[0]]["color"] = list(color)
    
    def reset_cells_size(self, new_size):
        """
        :param new_size: new cells size.
        
        Reset all the cells size.
        """
        
        self._cells_default_size = list(new_size)
        
        for row in self._cells_attr:
            for cell in row:
                cell["size"] = self._cells_default_size
                
    def reset_cells_color(self, new_color):
        """
        :param new_color: new cells color.
        
        Reset all the cells color.
        """
        
        self._cells_default_color = list(new_color)
        
        for row in self._cells_attr:
            for cell in row:
                cell["color"] = self._cells_default_color
                
    def set_cells_default_size(self, new_size):
        """
        :param new_size: new cells default size.
        
        Set the cells size with the previous default size with the new default size.
        """
        
        prev_size = self._cells_default_size
        self._cells_default_color = list(new_size)
        
        for row in self._cells_attr:
            for cell in row:
                if cell["size"] == prev_size:
                    cell["size"] = self._cells_default_size
        
    def set_cells_default_color(self, new_color):
        """
        :param new_color: new cells default color in RGB.
        
        Set the cells color with the previous default color with the new default color.
        """
        
        prev_color = self._cells_default_color
        self._cells_default_color = list(new_color)
        
        for row in self._cells_attr:
            for cell in row:
                if cell["color"] == prev_color:
                    cell["color"] = self._cells_default_color
        
    def get_pos(self):
        return self._pos
    
    def get_grid_length(self):
        return self._grid_length
    
    def get_grid_size(self):
        return self._grid_size
    
    def get_attr(self, pos, key):
        return self._cells_attr[pos[1]][pos[0]][str(key)]
    
    def get_cells_default_size(self):
        return self._cells_default_size
    
    def get_cells_default_color(self):
        return self._cells_default_color
    
    def get_surface(self):
        return self._surface
        
    def render(self):
        """
        Render the grid.
        """

        def render_cells():
            """
            Render each cell independently. Store the Surface objects in the
            """

            for y, row in enumerate(self._cells_attr):
                for x, cell in enumerate(row):
                    
                    self._cells_attr[y][x]["surface"] = pg.Surface(tuple(cell["size"]))
                    self._cells_attr[y][x]["surface"].fill(tuple(self._cells_attr[y][x]["color"]))
                    
        render_cells()
        
        self._surface = pg.Surface(tuple(self._grid_size))
        
        pos = [0, [0 for _ in range(self._grid_length[1])]]
        
        for y, row in enumerate(self._cells_attr):
            for x, cell in enumerate(row):
                self._surface.blit(cell["surface"], (pos[0], pos[1][x]))
                
                pos[0] += cell["size"][0]  # Update cell x position according to its size.
                pos[1][x] += cell["size"][1]
            
            pos[0] = 0
            
    def draw(self):
        """
        Draw the grid into the window.
        """

        self._window.blit(self._surface, tuple(self._pos))


class DropdownMenu:
    """
    Create and handle a drop-down menu.

    ATTRIBUTES:

        - I: _window: Surface object to draw and display the menu in.
        - I: _text: Text object representing the selected option.

        - POSITION:
            - I: _pos: menu position.
            - I: _margins: menu margins.

        - CHARACTERISTICS:
            - I: _size: menu size.

        - APPEARANCE:
            - I: _color: menu color.

        - STATE:
            - O: _is_open: is the menu open.
            - O: _options: list of options in the menu.
            - O: _selected_option: index of the selected option.

        - SURFACE:
            - O: _surface: Surface object representing the menu.

    METHODS:

        - SETTERS:
            - set_options(): set the options in the menu.
            - set_selected_option(): set the selected option.

            - set_pos(): set menu position.
            - set_margins(): set menu margins.
            - set_size(): set menu size.

            - set_color(): set the menu color.

        - GETTERS:
            - get_text(): return the selected option.

            - get_pos(): return the menu position.
            - get_margins(): return the menu margins.
            - get_size(): return the menu size.

            - get_color(): return the menu color.

            - get_is_open(): return the menu open state.
            - get_options(): return the options in the menu.
            - get_selected_option(): return the index of the selected option.

            - get_surface(): return the Surface object representing the menu.

        - render(): create the Surface object representing the menu.
        - draw(): draw the menu onto the window.
        - handle_event(): update the menu state based on user input.
    """

    def __init__(self, window, options, **kwargs):
        self._window = window
        self._options = options

        # POSITION:
        self._pos = list(kwargs.get("pos", [0, 0]))
        self._margins = list(kwargs.get("margins", [3, 5]))
        self._options.set_pos((
            self._pos[0] + self._margins[0],
            self._pos[1] + self._margins[1]
        ))

        # CHARACTERISTICS:
        self._size = list(kwargs.get("size", [100, 20]))

        # APPEARANCE:
        self._color = list(kwargs.get("color", [128, 128, 128]))

        # STATE:
        self._is_open = False
        self._options = []
        self._selected_option = -1

        # SURFACE:
        self._surface = None

    def set_options(self, options):
        self._options = options

    def set_selected_option(self, index):
        if 0 <= index < len(self._options):
            self._selected_option = index
            self._text.set_text(self._options[self._selected_option])

    def set_pos(self, pos):
        self._pos = list(pos)
        self._text.set_pos((
            self._pos[0] + self._margins[0],
            self._pos[1] + self._margins[1]
        ))

    def set_margins(self, margins):
        self._margins = list(margins)
        self._text.set_pos((
            self._pos[0] + self._margins[0],
            self._pos[1] + self._margins[1]
        ))

    def set_size(self, size):
        self._size = list(size)

    def set_color(self, color):
        self._color = list(color)

    def get_text(self):
        return self._text.get_text()

    def get_pos(self):
        return tuple(self._pos)

    def get_margins(self):
        return tuple(self._margins)

    def get_size(self):
        return tuple(self._size)

    def get_color(self):
        return tuple(self._color)

    def get_is_open(self):
        return self._is_open

    def get_options(self):
        return self._options

    def get_selected_option(self):
        return self._selected_option

    def get_surface(self):
        return self._surface

    def render(self):
        self._surface = pg.Surface(self._size)
        self._surface.fill(self._color)

    def draw(self):
        if self._surface is not None:
            self._window.blit(self._surface, self._pos)
            self._text.draw()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self._is_open:
                    if self._surface.get_rect(
                            topleft=self._pos).collidepoint(
                                event.pos):
                        self._is_open = False
                    else:
                        self._is_open = False
                        option_index = (
                            event.pos[1] - self._pos[1]
                        ) // self._size[1]
                        if 0 <= option_index < len(self._options):
                            self.set_selected_option(option_index)
                else:
                    if self._surface.get_rect(
                            topleft=self._pos).collidepoint(
                                event.pos):
                        self._is_open = True

    def update(self):
        if self._is_open:
            self.render()
