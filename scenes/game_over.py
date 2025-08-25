from core.scene_manager import Scene
from core.ui import Label, Button
from settings import WIDTH, HEIGHT

class GameOverScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.widgets = []
    def enter(self, **kwargs):
        reason = kwargs.get("reason", "finished")
        cx, cy = WIDTH//2, HEIGHT//2
        self.widgets = [
            Label(f"Игра окончена ({reason})", (cx, 180), font_size=36, center=True),
            Button("Сыграть ещё", (cx-120, cy, 240, 52), lambda: self.manager.switch('play')),
            Button("Таблица лидеров", (cx-120, cy+70, 240, 52), lambda: self.manager.switch('leaderboard')),
            Button("В меню", (cx-120, cy+140, 240, 52), lambda: self.manager.switch('menu'))
        ]
    def handle_event(self, e):
        for w in self.widgets:
            if hasattr(w, "handle_event"):
                w.handle_event(e)
    def update(self, dt): pass
    def draw(self, surf):
        for w in self.widgets:
            w.draw(surf)
