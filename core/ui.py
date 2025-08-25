import pygame as pg
from settings import FG_COLOR

class Label:
    def __init__(self, text, pos, color=FG_COLOR, font_size=28, center=False):
        self.text, self.pos, self.color = text, pos, color
        self.font = pg.font.SysFont(None, font_size)
        self.center = center
    def draw(self, surf):
        img = self.font.render(self.text, True, self.color)
        rect = img.get_rect()
        if self.center:
            rect.center = self.pos
        else:
            rect.topleft = self.pos
        surf.blit(img, rect)

class Button:
    def __init__(self, text, rect, on_click, font_size=28):
        self.text, self.rect = text, pg.Rect(rect)
        self.on_click = on_click
        self.font = pg.font.SysFont(None, font_size)
        self.hover = False
    def handle_event(self, e):
        if e.type == pg.MOUSEMOTION:
            self.hover = self.rect.collidepoint(e.pos)
        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1 and self.hover:
            self.on_click()
    def draw(self, surf):
        base = (55, 60, 80)
        hover = (75, 85, 120)
        color = hover if self.hover else base
        pg.draw.rect(surf, color, self.rect, border_radius=10)
        img = self.font.render(self.text, True, (245, 245, 255))
        surf.blit(img, img.get_rect(center=self.rect.center))
