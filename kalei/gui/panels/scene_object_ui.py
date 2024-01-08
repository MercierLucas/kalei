import dearpygui.dearpygui as dpg
from typing import List

from kalei.gui.utils import create_fixed_windows_parameters



class SceneObjectsPanel:
    def __init__(self, config:dict) -> None:
        self.config = config

    
    def init_ui(self, pos_x:int, pos_y:int):
        objects_list_parameters = create_fixed_windows_parameters(
            self.config["height"], self.config["left_panel_width"],
            (pos_x, pos_y)
        )
        with dpg.window(label="Scene objects", **objects_list_parameters):
            dpg.add_separator(label="Camera")
            dpg.add_text("Camera", label="Camera")
            dpg.add_text("Position", label="camera_position")
            dpg.add_text(f"X:{0.0:.2f}  Y:{0.0:.2f}  Z:{0.0:.2f}", label="camera_transform_position", tag="camera_transform_position")
            dpg.add_text("Rotation", label="camera_rotation")
            dpg.add_text(f"X:{0.0:.2f}  Y:{0.0:.2f}  Z:{0.0:.2f}", label="camera_transform_rotation", tag="camera_transform_rotation")

            dpg.add_separator()
            dpg.add_text("Objects")
            dpg.add_listbox(items=[], tag="scene_objects")


    def objects_added_to_scene(self, objects_name:List[str]):
        dpg.configure_item("scene_objects", items=objects_name)


    def update_camera_transform(self,  x, y, z, alpha, beta, gamma):
        dpg.set_value("camera_transform_position", f"X:{x:.2f}  Y:{y:.2f}  Z:{z:.2f}")
        dpg.set_value("camera_transform_rotation", f"X:{alpha:.2f}  Y:{beta:.2f}  Z:{gamma:.2f}")