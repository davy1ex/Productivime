class Scene:
    def __init__(self, manager):
        self.manager = manager
    def enter(self, **kwargs): pass
    def exit(self): pass
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self, surf): pass

class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current = None
        self.state = {
            "player_name": "",
            "score": 0,
            "last_result": {}
        }
    def register(self, key, scene):
        self.scenes[key] = scene
    def switch(self, key, **kwargs):
        if self.current:
            self.current.exit()
        self.current = self.scenes[key]
        self.current.enter(**kwargs)
    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)
    def update(self, dt):
        if self.current:
            self.current.update(dt)
    def draw(self, surf):
        if self.current:
            self.current.draw(surf)
