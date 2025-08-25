import pygame as pg
from settings import *

class Board:
    """
    Tree areas
    - To Do: left area
    - In Progress: right-upper area
    - Done: bottom area
    """
    def __init__(self):
        w, h = WIDTH, HEIGHT
        pad = BOARD_MARGIN
        hud_h = HUD_HEIGHT  # use a single header height

        # Geometry of Areas (shift the top to hud_h)
        third = (w - pad*2) // 3
        usable_h = h - pad*2 - hud_h  # available height for zones
        top_y = pad + hud_h

        todo_rect = pg.Rect(pad, top_y, third - pad//2, usable_h - 120)
        progress_rect = pg.Rect(w - pad - third + pad//2, top_y, third - pad//2, usable_h - 120)
        done_rect = pg.Rect(pad, h - pad - 100, w - pad*2, 100)

        self.rects = {
            "todo": todo_rect,
            "progress": progress_rect,
            "done": done_rect,
        }
        self.font = pg.font.SysFont(None, 24)

    def draw(self, surf):
        fill_map = {
            "todo": ZONE_TODO_FILL,
            "progress": ZONE_PROGRESS_FILL,
            "done": ZONE_DONE_FILL,
        }
        border_map = {
            "todo": ZONE_TODO_BORDER,
            "progress": ZONE_PROGRESS_BORDER,
            "done": ZONE_DONE_BORDER,
        }
        label_map = {"todo": "To Do", "progress": "In Progress", "done": "Done"}

        for name, r in self.rects.items():
            pg.draw.rect(surf, fill_map[name], r, border_radius=10)
            pg.draw.rect(surf, border_map[name], r, width=2, border_radius=10)
            img = self.font.render(label_map[name], True, ZONE_TITLE)
            surf.blit(img, (r.x + 8, r.y + 6))

    def clamp_rect(self):
        # Inner area for player movement (entire screen with small protrusions on top under HUD)
        pad = BOARD_MARGIN
        hud_h = 100
        return pg.Rect(pad, pad + hud_h, WIDTH - pad*2, HEIGHT - pad*2 - hud_h)

    def zone_at(self, pos):
        # What is the zone under the position
        for name, r in self.rects.items():
            if r.collidepoint(pos):
                return name
        return None

    def highlight_zone(self, surf, zone_name, intensity=1.0):
        """
        Draw a subtle highlight overlay on the expected zone.
        intensity in [0..1] to modulate alpha.
        """
        r = self.rects.get(zone_name)
        if not r:
            return
        # soft white overlay with low alpha for 'comic pastel' feel
        overlay = pg.Surface((r.width, r.height), pg.SRCALPHA)
        alpha = int(40 * max(0.0, min(1.0, intensity)))  # 0..40
        overlay.fill((255, 255, 255, alpha))
        surf.blit(overlay, r.topleft)
