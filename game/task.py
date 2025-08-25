import pygame as pg
from enum import IntEnum
from settings import TASK_SIZE, TASK_COLOR, TASK_BORDER, TASK_TEXT

class Stage(IntEnum):
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2

class TaskCard:
    """
    Single task card with a current stage and simple visual.
    """
    def __init__(self, pos, title="Task"):
        w, h = TASK_SIZE
        x, y = pos
        self.rect = pg.Rect(x - w//2, y - h//2, w, h)  # center around pos
        self.stage = Stage.TODO
        self.title = title
        self.carried = False   # if player is currently carrying
        self.font = pg.font.SysFont(None, 20)

    def set_center(self, pos):
        # Place card center to given position
        self.rect.center = pos

    def advance(self):
        # Advance stage by one step if possible
        if self.stage == Stage.TODO:
            self.stage = Stage.IN_PROGRESS
            return True
        elif self.stage == Stage.IN_PROGRESS:
            self.stage = Stage.DONE
            return True
        return False

    def reset_to_todo(self, pos=None):
        # Reset card to TODO (optionally reposition)
        self.stage = Stage.TODO
        self.carried = False
        if pos:
            self.set_center(pos)

    def draw(self, surf):
        # Draw card body and title
        pg.draw.rect(surf, TASK_COLOR, self.rect, border_radius=8)
        pg.draw.rect(surf, TASK_BORDER, self.rect, width=2, border_radius=8)
        label = self.font.render(self.title, True, TASK_TEXT)
        surf.blit(label, label.get_rect(center=self.rect.center))
