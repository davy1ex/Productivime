import pygame as pg
from core.scene_manager import Scene
from core.ui import HUD
from game.board import Board
from game.player import Player

class PlayScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.hud = None
        self.board = None
        self.player = None
        self.elapsed = 0.0

    def enter(self, **kwargs):
        self.hud = HUD()
        self.board = Board()
        # start the player near the ToDo zone
        todo_rect = self.board.rects["todo"]
        start_pos = (todo_rect.centerx - 18, todo_rect.centery - 18)
        self.player = Player(self.board, start_pos)
        self.elapsed = 0.0
        # reset points at scene start
        self.manager.state["score"] = 0

    def handle_event(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            self.manager.switch('game_over', reason="quit")

    def update(self, dt):
        self.elapsed += dt
        keys = pg.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(dt)
        # here update hud
        self.hud.set_score(self.manager.state.get("score", 0))
        self.hud.update_timer(self.elapsed)

    def draw(self, surf):
        # board
        self.board.draw(surf)
        # player
        self.player.draw(surf)
        # HUD
        self.hud.draw(surf)
