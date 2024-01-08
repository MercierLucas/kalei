import dearpygui.dearpygui as dpg
import numpy as np
from typing import List


from kalei.utils import load_config, FPSCounter
from kalei.events import event_manager, Events



class MainWindow:
    def __init__(self, config:dict) -> None:
        h, w = config["height"], config["width"]
        total_width = sum(config[w] for w in ["left_panel_width", "width", "right_panel_width"])
        self.config = config

        dpg.create_context()
        dpg.create_viewport(title='Kalei', width=total_width, height=h+50)
        dpg.setup_dearpygui()

    def setup_window(self):
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open")    
            dpg.add_menu_item(label="Help", callback=lambda : print("Help"))

            with dpg.menu(label="Add object"):
                dpg.add_menu_item(
                    label="Sample cube",
                    callback=lambda : event_manager.trigger(Events.ON_ADD_SAMPLE_OBJECT, "cube")
                )

        dpg.show_viewport()

        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Z, callback=lambda: event_manager.trigger(Events.ON_MOVE_CAMERA, 1))
            dpg.add_key_press_handler(dpg.mvKey_S, callback=lambda: event_manager.trigger(Events.ON_MOVE_CAMERA, -1))

    
    def scene_loop(self, render_func):
        ellapsed = 0
        counter = FPSCounter()
        while dpg.is_dearpygui_running():
            event_manager.trigger(Events.ON_SCENE_READY_TO_DRAW, render_func)
            dpg.render_dearpygui_frame()
            fps, eps = counter.tick()
            # print(f"{fps:.2f}")
            ellapsed += eps

        dpg.destroy_context()
