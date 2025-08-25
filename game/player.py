import pygame as pg
from settings import PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED
from game.board import Board

class Player:
    def __init__(self, board: Board, start_pos=(100, 200)):
        self.board = board
        w, h = PLAYER_SIZE
        x,y = start_pos
        self.rect = pg.Rect(x, y, w, h)
        self.speed = PLAYER_SPEED
        self.color = PLAYER_COLOR
        self.vel = pg.Vector2(0, 0)

    def handle_input(self, keys):
        self.vel.update(0, 0)
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -1
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = 1
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -1
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = 1
        # normalize the diagonal
        if self.vel.length_squared() > 0:
            self.vel = self.vel.normalize()

    def update(self, dt):
        # movement
        self.rect.x += int(self.vel.x * self.speed * dt)
        self.rect.y += int(self.vel.y * self.speed * dt)
        # clamp inside board
        clamp_area = self.board.clamp_rect()
        if self.rect.left < clamp_area.left:
            self.rect.left = clamp_area.left
        if self.rect.right > clamp_area.right:
            self.rect.right = clamp_area.right
        if self.rect.top < clamp_area.top:
            self.rect.top = clamp_area.top
        if self.rect.bottom > clamp_area.bottom:
            self.rect.bottom = clamp_area.bottom

    def draw(self, surf):
        pg.draw.rect(surf, self.color, self.rect, border_radius=6)
