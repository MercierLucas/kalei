
from kalei.gui.panels import InspectorPresenter, SceneObjectPresenter, ViewerPresenter

from .main_window import MainWindow



class MainPresenter:

    panels = [
        InspectorPresenter,
        SceneObjectPresenter,
        ViewerPresenter
    ]

    def __init__(self, config:dict) -> None:
        self.window = MainWindow(config)
        self.config = config
        self.init_panels()


    def start_main_loop(self, func):
        self.window.setup_window()
        self.window.scene_loop(func)


    def init_panels(self):
        curr_x = 0
        p = SceneObjectPresenter(self.config, curr_x, 0)
        curr_x += self.config["left_panel_width"]

        p = ViewerPresenter(self.config, curr_x, 0)
        curr_x += self.config["width"]
        p = InspectorPresenter(self.config, curr_x, 0)




