import pygame as pg
import random

class ObstacleTag:
    """
    Vertical moving text 'distractor'.
    Moves upward by default. Uses a text surface as its sprite.
    """
    def __init__(self, text, x, y, speed, color=(230, 90, 120)):
        self.text = text
        self.color = color
        self.font = pg.font.SysFont(None, 22)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed  # pixels per second
        self.alive = True

    def update(self, dt):
        # Move upward
        self.rect.y -= int(self.speed * dt)
        # Kill when off the top
        if self.rect.bottom < 0:
            self.alive = False

    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)
