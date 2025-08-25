from core.scene_manager import Scene
from core.ui import Label, Button
from settings import WIDTH

class LeaderboardScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.widgets = []
    def enter(self, **kwargs):
        cx = WIDTH//2
        self.widgets = [
            Label("Топ‑5 (заглушка)", (cx, 160), font_size=36, center=True),
            Label("1) --- 0000", (cx, 220), center=True),
            Label("2) --- 0000", (cx, 260), center=True),
            Label("3) --- 0000", (cx, 300), center=True),
            Label("4) --- 0000", (cx, 340), center=True),
            Label("5) --- 0000", (cx, 380), center=True),
            Button("В меню", (cx-110, 440, 220, 52), lambda: self.manager.switch('menu'))
        ]
    def handle_event(self, e):
        for w in self.widgets:
            if hasattr(w, "handle_event"):
                w.handle_event(e)
    def update(self, dt): pass
    def draw(self, surf):
        for w in self.widgets:
            w.draw(surf)
