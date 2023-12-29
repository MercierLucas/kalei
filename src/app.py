import threading
import time

from src.gui.app import MainWindow
from src.utils import load_config
from src.camera import Camera
from src.scene import Scene
from src.renderer import OpenCVRenderer


class App:
    def __init__(self) -> None:
        self.config = load_config()
        self.main_window = MainWindow(self.config)
        camera = Camera(width=self.config["width"], height=self.config["height"])
        scene = Scene()
        self.renderer = OpenCVRenderer(camera, scene)
        self.main_window.setup_window(self.renderer.background_frame)
        self.pause_scene = False
        self.renderer.after_init()
        

    def get_renderer_frame(self, *args):
        return self.renderer.render(*args)

    
    # def main_thread(self):
    #     delay = int(1/self.config["fps"])

    #     while not self.pause_scene:
    #         print("tick")
    #         frame = self.renderer.render()
    #         self.main_window.update_scene(frame)
    #         time.sleep(delay)


    def run(self):
        self.main_window.scene_loop(self.get_renderer_frame)
        # thread = threading.Thread(target=self.main_thread)
        # thread.daemon = True
        # thread.start()
    

