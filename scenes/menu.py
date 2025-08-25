import pygame as pg
from core.scene_manager import Scene
from core.ui import Label, Button
from settings import WIDTH, HEIGHT

class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.widgets = []
    def enter(self, **kwargs):
        cx, cy = WIDTH // 2, HEIGHT // 2
        self.widgets = [
            Label("Kanban Carrier", (cx, 160), font_size=44, center=True),
            Button("Начать", (cx - 110, cy, 220, 52),
                   lambda: self.manager.switch('input_name')),
            Button("Выход", (cx - 110, cy + 70, 220, 52),
                   lambda: pg.event.post(pg.event.Event(pg.QUIT)))
        ]
    def handle_event(self, e):
        for w in self.widgets:
            if hasattr(w, "handle_event"):
                w.handle_event(e)
    def update(self, dt): pass
    def draw(self, surf):
        for w in self.widgets:
            w.draw(surf)
