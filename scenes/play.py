import pygame as pg
import random

from core.scene_manager import Scene
from core.ui import HUD
from game.board import Board
from game.player import Player
from game.task import TaskCard, Stage
from game.obstacle import ObstacleTag

from settings import *

class PlayScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.hud = None
        self.board = None
        self.player = None
        self.elapsed = 0.0
        self.task = None
        self.pulse_t = 0.0  # for target zone highlight pulse

        self.delivered_count = 0

        # pickup settings
        self.pickup_radius = 48  # px around ToDo center

        # Anti-instant-penalty helpers
        self.grace_time = 0.8     # seconds to ignore zone penalties after start
        self.grace_left = 0.0
        self.left_todo_once = False  # allow auto-pickup only after leaving TODO once

        # Distractors state
        self.obstacles = []
        self.spawn_timer = 0.0
        self.spawn_interval = DISTRACTOR_SPAWN_INTERVAL
        self.diff_timer = 0.0

        # Error/invulnerability
        self.errors = 0
        self.invuln = 0.0  # seconds of post-hit invulnerability

        # Delivery respawn flag
        self._respawn_requested = False

    def spawn_task_in_todo(self):
        # Spawn one task centered in ToDo zone
        todo_rect = self.board.rects["todo"]
        center = todo_rect.center
        self.task = TaskCard(center) 

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

        self.delivered_count = 0
        self.elapsed = 0.0
        self.manager.state["score"] = START_SCORE

        # Start player OUTSIDE the ToDo rect to avoid instant pickup/penalty
        todo_rect = self.board.rects["todo"]
        start_pos = (todo_rect.left - 40, todo_rect.centery)  # place slightly to the left
        # Clamp start inside playable area (in case left margin is too small)
        clamp = self.board.clamp_rect()
        if start_pos[0] < clamp.left:
            start_pos = (clamp.left + 10, start_pos[1])

        self.player = Player(self.board, start_pos)

        self.elapsed = 0.0
        self.spawn_task_in_todo()

        # Reset distractors and timers
        self.obstacles.clear()
        self.spawn_timer = 0.0
        self.spawn_interval = DISTRACTOR_SPAWN_INTERVAL
        self.diff_timer = 0.0
        self.errors = 0
        self.invuln = 0.0

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
                    self.task.carried = False
                    done_rect = self.board.rects["done"]
                    self.task.set_center(done_rect.center)
                    self.delivered_count += 1  # track delivered tasks
                    self._respawn_requested = True

        else:
            # Do NOT penalize if still in the origin zone for current stage.
            origin_zone = "todo" if self.task.stage == Stage.TODO else ("progress" if self.task.stage == Stage.IN_PROGRESS else None)
            if zone == origin_zone:
                return  # still at origin; allow the player to leave without penalty

            # Wrong zone order -> penalty and reset to TODO center
            todo_rect = self.board.rects["todo"]
            self.manager.state["score"] -= PENALTY_SKIP_STAGE
            # End the run if score dropped to zero or below
            if self.manager.state["score"] <= 0:
                self.manager.state["score"] = 0
                self.manager.switch('game_over', reason="score_depleted")
                return
            self.task.reset_to_todo(pos=todo_rect.center)

    def spawn_distractor(self):
        # Spawn within right band area, random x and start slightly below bottom to fly upward
        screen = pg.display.get_surface()
        screen_w = screen.get_width()
        screen_h = screen.get_height()
        x_min = int(screen_w * RIGHT_BAND_X_FRAC)
        x_max = screen_w - 20
        x = random.randint(x_min, x_max)
        y = random.randint(screen_h + 10, screen_h + 80)  # start off-screen below
        speed = random.randint(DISTRACTOR_MIN_SPEED, DISTRACTOR_MAX_SPEED)
        word = random.choice(DISTRACTOR_WORDS)
        ob = ObstacleTag(word, x, y, speed, color=DISTRACTOR_COLOR)
        self.obstacles.append(ob)

    def update_distractors(self, dt):
        # Spawn timer
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer -= self.spawn_interval
            self.spawn_distractor()

        # Difficulty bump
        self.diff_timer += dt
        if self.diff_timer >= DISTRACTOR_STEP_TIME:
            self.diff_timer -= DISTRACTOR_STEP_TIME
            # Tighten interval (up to min), could also raise speeds if desired
            self.spawn_interval = max(DISTRACTOR_MIN_INTERVAL, self.spawn_interval - DISTRACTOR_DIFFICULTY_STEP)

        # Update and cull
        for ob in self.obstacles:
            ob.update(dt)
        self.obstacles = [ob for ob in self.obstacles if ob.alive]

    def handle_distractor_collisions(self):
        # Short invulnerability window to avoid draining score too fast
        if self.invuln > 0.0:
            return
        player_rect = self.player.rect
        hit = None
        for ob in self.obstacles:
            if player_rect.colliderect(ob.rect):
                hit = ob
                break
        if not hit:
            return

        # Apply penalty
        self.manager.state["score"] -= PENALTY_HIT_DISTRACTOR
        self.errors += 1
        self.invuln = 0.8  # 800 ms invulnerability

        # Reset task to TODO center if exists
        if self.task:
            todo_rect = self.board.rects["todo"]
            self.task.reset_to_todo(pos=todo_rect.center)

        # Remove the obstacle hit (feedback)
        hit.alive = False

        if self.manager.state["score"] <= 0:
            # optional: clamp to zero for nicer display
            self.manager.state["score"] = 0
            self.manager.switch('game_over', reason="score_depleted")
        # maybe for futures
        # Too many errors -> game over 
        # if self.errors >= MAX_ERRORS:
        #     self.manager.switch('game_over', reason="too_many_errors")

    def finish_run(self, reason: str):
        # Pack results into shared state
        self.manager.state["time_spent"] = int(self.elapsed)
        self.manager.state["delivered"] = self.delivered_count
        self.manager.state["target"] = TARGET_N
        self.manager.state["reason"] = reason
        # score уже лежит в state
        self.manager.switch('game_over', reason=reason)
        
    def update(self, dt):
        self.elapsed += dt
        if self.grace_left > 0.0:
            self.grace_left = max(0.0, self.grace_left - dt)
        if self.invuln > 0.0:
            self.invuln = max(0.0, self.invuln - dt)

        keys = pg.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(dt)

        # Auto pickup near TODO card
        self.auto_pickup_if_near_todo()

        # Move carried card with player (visual)
        if self.task and self.task.carried:
            px, py = self.player.rect.centerx, self.player.rect.top - 10
            self.task.set_center((px, py))

        # Handle zone transitions and scoring
        self.handle_zone_transitions()

        # Update distractors (spawn/move/cull)
        self.update_distractors(dt)

        # Handle collisions with distractors
        self.handle_distractor_collisions()

        # Update HUD
        self.hud.set_score(self.manager.state.get("score", 0))
        self.hud.update_timer(self.elapsed)
        # expose delivered/target as string for HUD
        self.hud.delivered_str = f"{self.delivered_count}/{TARGET_N}"


        # Pulse for expected-zone highlight
        self.pulse_t += dt

        # Win condition: delivered enough before time runs out
        if self.delivered_count >= TARGET_N:
            self.finish_run("win")
            return

        # Lose condition: time limit exceeded without reaching target
        if self.elapsed >= TIME_LIMIT and self.delivered_count < TARGET_N:
            self.finish_run("time_up")
            return

        # Lose condition: score depleted (safety check in case other code hasn't switched yet)
        if self.manager.state["score"] <= 0:
            self.manager.state["score"] = 0
            self.finish_run("score_depleted")
            return


        # Respawn new task if previous delivered (next frame)
        if self._respawn_requested:
            self._respawn_requested = False
            self.spawn_task_in_todo()

    def draw(self, surf):
        self.board.draw(surf)

        # Expected-zone highlight
        if self.task:
            next_zone = self.expected_zone_for_stage(self.task.stage)
            if next_zone:
                import math
                intensity = 0.75 + 0.25 * math.sin(self.pulse_t * 4.0)
                self.board.highlight_zone(surf, next_zone, intensity=intensity)

        # Task
        if self.task:
            self.task.draw(surf)

        # Distractors
        for ob in self.obstacles:
            ob.draw(surf)

        # Player (flash if invulnerable)
        if self.invuln > 0.0:
            self.player.draw(surf)
            pr = self.player.rect
            glow = pg.Surface((pr.width, pr.height), pg.SRCALPHA)
            glow.fill((255, 255, 255, 60))
            surf.blit(glow, pr.topleft)
        else:
            self.player.draw(surf)

        self.hud.draw(surf)
