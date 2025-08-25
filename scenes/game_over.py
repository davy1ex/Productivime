from core.scene_manager import Scene
from core.ui import Label, Button
from settings import WIDTH, HEIGHT
from data.db import DBManager

class GameOverScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.widgets = []
        self.db = DBManager()
        self.saved = False  # prevent double insert

    def enter(self, **kwargs):
        reason = kwargs.get("reason", self.manager.state.get("reason", "finished"))
        name = self.manager.state.get("player_name", "---")
        score = int(self.manager.state.get("score", 0))
        delivered = int(self.manager.state.get("delivered", 0))
        target = int(self.manager.state.get("target", 0))
        time_spent = int(self.manager.state.get("time_spent", 0))

        # Save once per entry
        if not self.saved:
            try:
                self.db.insert_score(name, score, delivered, time_spent, reason)
            except Exception:
                # In production: log the error; here we ignore to not crash the UI
                pass
            self.saved = True

        cx, cy = WIDTH//2, HEIGHT//2
        title = "Победа!" if reason == "win" else "Игра окончена"
        details = f"Очки: {score} | Задач: {delivered}/{target} | Время: {time_spent}s | Причина: {reason}"

        self.widgets = [
            Label(title, (cx, 150), font_size=36, center=True),
            Label(details, (cx, 195), font_size=24, center=True),
            Button("Сыграть ещё", (cx-120, cy, 240, 52), lambda: self.manager.switch('play')),
            Button("Таблица лидеров", (cx-120, cy+70, 240, 52), lambda: self.manager.switch('leaderboard')),
            Button("В меню", (cx-120, cy+140, 240, 52), lambda: self.manager.switch('menu'))
        ]

    def exit(self):
        self.saved = False

    def handle_event(self, e):
        for w in self.widgets:
            if hasattr(w, "handle_event"):
                w.handle_event(e)

    def update(self, dt): pass

    def draw(self, surf):
        for w in self.widgets:
            w.draw(surf)
