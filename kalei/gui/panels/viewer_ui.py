import numpy as np
from typing import Callable
import dearpygui.dearpygui as dpg

from kalei.gui.utils import frame_to_dpg, create_fixed_windows_parameters



class ViewerPanel:
    def __init__(self, config:dict) -> None:
        self.config = config
        self.dummy_frame = np.zeros((config["height"], config["width"], 3))


    def render_frame(self, render_func: Callable):
        frame_data = render_func(0)
        frame_data = frame_to_dpg(frame_data)
        dpg.set_value("3dscene", frame_data)


    def init_ui(self, pos_x:int, pos_y:int):
        frame_data = frame_to_dpg(self.dummy_frame)
        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(self.dummy_frame.shape[1], self.dummy_frame.shape[0],
                                frame_data, tag="3dscene", format=dpg.mvFormat_Float_rgb)
            
        scene_parameters = create_fixed_windows_parameters(
            self.config["height"],self.config["width"],
            pos=(pos_x, pos_y)
        )
        
        with dpg.window(label="Scene", **scene_parameters):
            dpg.add_image("3dscene")