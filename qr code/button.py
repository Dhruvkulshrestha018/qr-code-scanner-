import pygame as pg


class Button:

    def __init__(self, display_surface: pg.Surface, caption: str,
                 x: int, y: int, width: int, height: int,
                 border_thickness: int = 2,
                 text_font: str = "consolas", text_size: int = 27):
        # Keep values of width & height parameters as even numbers

        self.DISPLAY_SURFACE = display_surface
        self.CAPTION = caption
        self.RECT = pg.Rect(x, y, width, height)
        self.thickness = self.ORIGINAL_THICKNESS = border_thickness
        self.FONT = pg.font.SysFont(text_font, text_size)
        self.hover = self.action = False

    def mouse_input(self):

        if self.action:
            self.action = False

        mouse_pos = pg.mouse.get_pos()
        if mouse_pos[0] in range(self.RECT.left, self.RECT.right) \
                and mouse_pos[1] in range(self.RECT.top, self.RECT.bottom):
            self.hover = True
        else:
            self.hover = False

        if self.hover and pg.mouse.get_pressed()[0]:
            self.action = True

    def display(self):

        if self.hover:
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
        caption = self.FONT.render(self.CAPTION, True, pg.colordict.THECOLORS["black"])
        caption_x = self.RECT.centerx - (caption.get_width() // 2)
        caption_y = self.RECT.centery - (caption.get_height() // 2)
        self.DISPLAY_SURFACE.blit(caption, (caption_x, caption_y))
