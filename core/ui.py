import pygame as pg
from settings import FG_COLOR

class HUD:
    def __init__(self):
        self.font = pg.font.SysFont(None, 24)
        self.timer = 0.0
        self.score = 0
        self.hint = "arrows/WASD — moving | Esc — exit"

    def set_score(self, score):
        self.score = score

    def update_timer(self, t):
        self.timer = t

    def draw(self, surf):
        tsec = int(self.timer)
        parts = [
            f"Время: {tsec}s",
            f"Очки: {self.score}",
            self.hint
        ]
        x, y = 16, 8
        for p in parts:
            img = self.font.render(p, True, FG_COLOR)
            surf.blit(img, (x, y))
            x += img.get_width() + 24

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
