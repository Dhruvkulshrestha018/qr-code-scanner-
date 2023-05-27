import pygame as pg


class TextBox:

    def __init__(self, display_surface: pg.Surface,
                 x: int, y: int, width: int, height: int,
                 border_thickness: int = 1,
                 text_font: str = "consolas", text_size: int = 27):
        # Keep values of width & height parameters as even numbers

        self.DISPLAY_SURFACE = display_surface
        self.RECT = pg.Rect(x, y, width, height)
        self.FONT = pg.font.SysFont(text_font, text_size)
        self.thickness = self.ORIGINAL_THICKNESS = border_thickness
        self.hover = self.typing = self.action = False
        self.text = ""
        self.display_cursor = self.FONT.render("|", True, pg.colordict.THECOLORS["black"])
        self.SHIFT_CHARACTERS = {"`": "~",
                                 "1": "!",
                                 "2": "@",
                                 "3": "#",
                                 "4": "$",
                                 "5": "%",
                                 "6": "^",
                                 "7": "&",
                                 "8": "*",
                                 "9": "(",
                                 "0": ")",
                                 "-": "_",
                                 "=": "+",
                                 "[": "{",
                                 "]": "}",
                                 "\\": "|",
                                 ";": ":",
                                 "'": "\"",
                                 ",": "<",
                                 ".": ">",
                                 "/": "?",
                                 }

    def mouse_input(self):

        mouse_pos = pg.mouse.get_pos()
        if mouse_pos[0] in range(self.RECT.left, self.RECT.right) \
                and mouse_pos[1] in range(self.RECT.top, self.RECT.bottom):
            self.hover = True
        else:
            self.hover = False

        if self.hover and pg.mouse.get_pressed()[0]:
            self.typing = True

        if not self.hover and self.typing and pg.mouse.get_pressed()[0]:
            self.typing = False
            if self.text:
                self.action = True
            else:
                self.action = False

    def keyboard_input(self, event: pg.event.Event):

        if self.action:
            self.action = False

        keys = pg.key.get_pressed()
        if self.typing:
            key_string = pg.key.name(event.key)
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pg.K_DELETE:
                self.text = ""
            elif event.key == pg.K_RETURN and self.text:
                self.typing = False
                self.action = True
            elif len(key_string) == 1 and len(self.text) < 45:
                if key_string.isalpha():
                    if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                        self.text += key_string.upper()
                    else:
                        self.text += key_string
                elif key_string in self.SHIFT_CHARACTERS:
                    if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                        self.text += self.SHIFT_CHARACTERS[key_string]
                    else:
                        self.text += key_string

    def display(self):

        if self.typing:
            self.thickness = self.ORIGINAL_THICKNESS * 3
        elif self.hover:
            if self.thickness < self.ORIGINAL_THICKNESS * 3:
                self.thickness += 0.4
        else:
            self.thickness = self.ORIGINAL_THICKNESS

        border_rect = pg.Rect(self.RECT.x, self.RECT.y,
                              self.RECT.width + int(2 * self.thickness),
                              self.RECT.height + int(2 * self.thickness))
        border_rect.center = self.RECT.center
        pg.draw.rect(self.DISPLAY_SURFACE, pg.colordict.THECOLORS["black"], border_rect)
        pg.draw.rect(self.DISPLAY_SURFACE, pg.colordict.THECOLORS["white"], self.RECT)

        text_to_display = self.FONT.render(self.text, True, pg.colordict.THECOLORS["black"])
        text_x = self.RECT.x + 10
        text_y = self.RECT.y + ((self.RECT.height - text_to_display.get_height()) // 2)
        self.DISPLAY_SURFACE.blit(text_to_display, (text_x, text_y))

        if self.typing:
            cursor_x = text_x + text_to_display.get_width() - 5
            self.DISPLAY_SURFACE.blit(self.display_cursor,
                                      (cursor_x, text_y))
