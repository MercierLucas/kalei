from typing import Callable

from kalei.events import event_manager, Events

from .viewer_ui import ViewerPanel


class ViewerPresenter:
    def __init__(self, config:dict, pos_x:int, pos_y:int) -> None:
        self.panel = ViewerPanel(config)
        self.panel.init_ui(pos_x, pos_y)

        event_manager.register(Events.ON_SCENE_READY_TO_DRAW, self.draw_scene)



    def draw_scene(self, render_func:Callable):
        self.panel.render_frame(render_func)


