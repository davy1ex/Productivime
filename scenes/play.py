import pygame as pg
from core.scene_manager import Scene
from core.ui import Label

class PlayScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.hud = None
        self.timer = 0.0
    def enter(self, **kwargs):
        name = self.manager.state.get("player_name", "")
        self.hud = Label(f"Игрок: {name} | Очки: 0 | [Плейсхолдер HUD]", (20, 20))
        self.timer = 0.0
    def handle_event(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            self.manager.switch('game_over', reason="quit")
    def update(self, dt):
        self.timer += dt
    def draw(self, surf):
        self.hud.draw(surf)
