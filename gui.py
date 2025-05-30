import pygame


class Button:
    def __init__(self, surface, font, text, x=None, y=None, padding=25, outline=2,
                 text_colour=(0, 0, 0), bg_colour=(255, 255, 255)):
        self.hovered = False
        self.surface = surface
        self.font = font

        self.text_colour = text_colour
        self.bg_colour = bg_colour
        self.padding = padding
        self.outline = outline

        self.text = self.font.render(text, 1, self.text_colour)
        if x is None:
            self.x = (self.surface.get_width() - self.text.get_width()) / 2
        else:
            self.x = x
        if y is None:
            self.y = (self.surface.get_height() - self.text.get_height()) / 2
        else:
            self.y = y
        self.width = self.text.get_width()
        self.height = self.text.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.hovered_text = self.font.render(text, 1, self.bg_colour)
        self.hovered_x = self.x - self.padding / 2
        self.hovered_y = self.y - self.padding / 2
        self.hovered_width = self.text.get_width() + self.padding
        self.hovered_height = self.text.get_height() + self.padding
        self.hovered_rect = pygame.Rect(self.hovered_x, self.hovered_y, self.hovered_width, self.hovered_height)

    def render(self):
        if self.hovered:
            pygame.draw.rect(self.surface, self.text_colour, self.hovered_rect)
            self.surface.blit(self.hovered_text,
                              (self.hovered_x + (self.hovered_width - self.hovered_text.get_width()) / 2,
                               self.hovered_y +
                               (self.hovered_height - self.hovered_text.get_height()) / 2))
        else:
            pygame.draw.rect(self.surface, self.text_colour, self.hovered_rect)
            pygame.draw.rect(self.surface, self.bg_colour, (
                self.hovered_x + self.outline, self.hovered_y + self.outline, self.hovered_width - self.outline * 2,
                self.hovered_height - self.outline * 2))
            self.surface.blit(self.text, (
                self.x + (self.width - self.text.get_width()) / 2, self.y + (self.height - self.text.get_height()) / 2))


def main_menu(win):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit()
                quit()

        font = pygame.font.SysFont("Roboto", 40)
        button_1 = Button(win, font, "Play Offline")
        win.fill((255, 255, 255))
        button_1.render()
        pygame.display.update()


pygame.init()
win = pygame.display.set_mode((500, 500))
main_menu(win)
