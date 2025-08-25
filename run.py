import pygame as pg
from settings import WIDTH, HEIGHT, FPS, TITLE, BG_COLOR
from core.scene_manager import SceneManager
from scenes.menu import MenuScene
from scenes.input_name import InputNameScene
from scenes.play import PlayScene
from scenes.game_over import GameOverScene
from scenes.leaderboard import LeaderboardScene

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(TITLE)
    clock = pg.time.Clock()

    manager = SceneManager()
    manager.register('menu', MenuScene(manager))
    manager.register('input_name', InputNameScene(manager))
    manager.register('play', PlayScene(manager))
    manager.register('game_over', GameOverScene(manager))
    manager.register('leaderboard', LeaderboardScene(manager))
    manager.switch('menu')

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            else:
                manager.handle_event(event)
        manager.update(dt)
        screen.fill(BG_COLOR)
        manager.draw(screen)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
