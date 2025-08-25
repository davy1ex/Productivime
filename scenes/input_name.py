import pygame as pg
from core.scene_manager import Scene
from core.ui import Label, Button
from settings import WIDTH

class InputNameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.name = ""
        self.font = None
        self.btn_menu = None
        self.hint = None
    def enter(self, **kwargs):
        self.font = pg.font.SysFont(None, 36)
        self.name = ""
        self.hint = Label("Введите ник и нажмите Enter", (WIDTH//2, 200), center=True)
        self.btn_menu = Button("В меню", (WIDTH//2-110, 420, 220, 52),
                               lambda: self.manager.switch('menu'))
    def handle_event(self, e):
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_RETURN and self.name.strip():
                self.manager.state["player_name"] = self.name.strip()
                self.manager.switch('play')
            elif e.key == pg.K_BACKSPACE:
                self.name = self.name[:-1]
            else:
                if e.unicode and e.unicode.isprintable():
                    self.name += e.unicode
        self.btn_menu.handle_event(e)
    def update(self, dt): pass
    def draw(self, surf):
        self.hint.draw(surf)
        box = pg.Rect(220, 260, 460, 56)
        pg.draw.rect(surf, (50, 55, 70), box, border_radius=10)
        txt = self.font.render(self.name or "_", True, (230,230,240))
        surf.blit(txt, (box.x+14, box.y+14))
        self.btn_menu.draw(surf)
