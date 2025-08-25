import pygame as pg
from core.scene_manager import Scene
from core.ui import HUD
from game.board import Board
from game.player import Player
from game.task import TaskCard, Stage
from settings import SCORE_TO_PROGRESS, SCORE_TO_DONE, PENALTY_SKIP_STAGE, HUD_HEIGHT

class PlayScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.hud = None
        self.board = None
        self.player = None
        self.elapsed = 0.0
        self.task = None
        self.pulse_t = 0.0  # for target zone highlight pulse

        # pickup settings
        self.pickup_radius = 48  # px around ToDo center

        # Anti-instant-penalty helpers
        self.grace_time = 0.8     # seconds to ignore zone penalties after start
        self.grace_left = 0.0
        self.left_todo_once = False  # allow auto-pickup only after leaving TODO once

    def spawn_task_in_todo(self):
        # Spawn one task centered in ToDo zone
        todo_rect = self.board.rects["todo"]
        center = todo_rect.center
        self.task = TaskCard(center, title="Task")

    def expected_zone_for_stage(self, stage):
        # Map stage to zone name
        if stage == Stage.TODO:
            return "progress"
        if stage == Stage.IN_PROGRESS:
            return "done"
        return None  # DONE has no next zone

    def enter(self, **kwargs):
        self.hud = HUD()
        self.board = Board()
        self._respawn_requested = False

        # Start player OUTSIDE the ToDo rect to avoid instant pickup/penalty
        todo_rect = self.board.rects["todo"]
        start_pos = (todo_rect.left - 40, todo_rect.centery)  # place slightly to the left
        # Clamp start inside playable area (in case left margin is too small)
        clamp = self.board.clamp_rect()
        if start_pos[0] < clamp.left:
            start_pos = (clamp.left + 10, start_pos[1])

        self.player = Player(self.board, start_pos)

        self.elapsed = 0.0
        self.manager.state["score"] = 0
        self.spawn_task_in_todo()

        # Init grace period and flags
        self.grace_left = self.grace_time
        self.left_todo_once = False

    def handle_event(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            self.manager.switch('game_over', reason="quit")

    def auto_pickup_if_near_todo(self):
        # Only pickup when:
        # - there's a task in TODO
        # - not already carrying
        if not self.task or self.task.carried:
            return
        if self.task.stage != Stage.TODO:
            return

        # Track 'left TODO once' at any time
        current_zone = self.board.zone_at(self.player.rect.center)
        if not self.left_todo_once and current_zone != "todo":
            self.left_todo_once = True

        # Allow pickup if either:
        # - player left TODO at least once
        # - OR initial grace period is over
        if not self.left_todo_once and self.grace_left > 0.0:
            # Still in the initial phase and haven't left TODO yet
            return

        # Distance-based pickup (stick when close enough)
        p = pg.Vector2(self.player.rect.center)
        c = pg.Vector2(self.task.rect.center)
        if p.distance_to(c) <= self.pickup_radius:
            self.task.carried = True


    def handle_zone_transitions(self):
        # Skip transitions during initial grace period to avoid instant penalties
        if self.grace_left > 0.0:
            return

        if not self.task:
            return

        # DONE has no further transitions
        if self.task.stage == Stage.DONE:
            return

        # Only react when carrying the card
        if not self.task.carried:
            return

        # Where is the player right now?
        zone = self.board.zone_at(self.player.rect.center)
        if not zone:
            return

        expected_zone = self.expected_zone_for_stage(self.task.stage)

        if zone == expected_zone:
            # Correct progression
            advanced = self.task.advance()
            if advanced:
                if self.task.stage == Stage.IN_PROGRESS:
                    # Reached IN_PROGRESS from TODO
                    self.manager.state["score"] += SCORE_TO_PROGRESS
                elif self.task.stage == Stage.DONE:
                    # Reached DONE from IN_PROGRESS
                    self.manager.state["score"] += SCORE_TO_DONE
                    # 1) drop the card
                    self.task.carried = False
                    # 2) place the card into Done center (visual confirmation)
                    done_rect = self.board.rects["done"]
                    self.task.set_center(done_rect.center)
                    # 3) optional: schedule immediate respawn flag
                    self._respawn_requested = True

        else:
            # Do NOT penalize if still in the origin zone for current stage.
            origin_zone = "todo" if self.task.stage == Stage.TODO else ("progress" if self.task.stage == Stage.IN_PROGRESS else None)
            if zone == origin_zone:
                return  # still at origin; allow the player to leave without penalty

            # Wrong zone order -> penalty and reset to TODO center
            todo_rect = self.board.rects["todo"]
            self.manager.state["score"] -= PENALTY_SKIP_STAGE
            self.task.reset_to_todo(pos=todo_rect.center)


    def update(self, dt):
        self.elapsed += dt
        if self.grace_left > 0.0:
            self.grace_left = max(0.0, self.grace_left - dt)

        keys = pg.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(dt)

        # Auto pickup near TODO card (subject to left_todo_once)
        self.auto_pickup_if_near_todo()

        # Handle zone transitions and scoring
        self.handle_zone_transitions()

        # Update HUD
        self.hud.set_score(self.manager.state.get("score", 0))
        self.hud.update_timer(self.elapsed)

        # Pulse for expected-zone highlight
        self.pulse_t += dt

        # If task reached DONE and not carried -> respawn a new task
        if self.task and self.task.carried:
            px, py = self.player.rect.centerx, self.player.rect.top - 10
            self.task.set_center((px, py))

        if getattr(self, "_respawn_requested", False):
            self._respawn_requested = False
            self.spawn_task_in_todo()

    def draw(self, surf):
        # Board
        self.board.draw(surf)

        # Expected-zone highlight with soft pulse
        if self.task:
            next_zone = self.expected_zone_for_stage(self.task.stage)
            if next_zone:
                import math
                intensity = 0.75 + 0.25 * math.sin(self.pulse_t * 4.0)  # 0.5..1.0
                self.board.highlight_zone(surf, next_zone, intensity=intensity)

        # Task card
        if self.task:
            self.task.draw(surf)

        # Player
        self.player.draw(surf)

        # HUD on top
        self.hud.draw(surf)
