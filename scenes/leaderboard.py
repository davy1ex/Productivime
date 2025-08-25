from core.scene_manager import Scene
from core.ui import Label, Button
from settings import WIDTH
from data.db import DBManager

class LeaderboardScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.widgets = []
        self.db = DBManager()

    def enter(self, **kwargs):
        cx = WIDTH//2
        rows = []
        try:
            rows = self.db.top5()
        except Exception:
            rows = []

        y = 200
        self.widgets = [
            Label("Топ‑5", (cx, 140), font_size=36, center=True),
        ]

        # rows: (name, score, delivered, time_spent, reason, created_at)
        rank = 1
        for r in rows:
            name, score, delivered, time_spent, reason, created_at = r
            line = f"{rank}) {name:>10} — {score} очк. | задач: {delivered} | {time_spent}s | {reason}"
            self.widgets.append(Label(line, (cx, y), center=True))
            y += 34
            rank += 1

        if not rows:
            self.widgets.append(Label("Нет записей", (cx, y), center=True))

        self.widgets.append(Button("В меню", (cx-110, y+60, 220, 52), lambda: self.manager.switch('menu')))
        self.widgets.append(Button("Сыграть ещё", (cx-110, y+120, 220, 52), lambda: self.manager.switch('play')))

    def handle_event(self, e):
        for w in self.widgets:
            if hasattr(w, "handle_event"):
                w.handle_event(e)

    def update(self, dt): pass

    def draw(self, surf):
        for w in self.widgets:
            w.draw(surf)
