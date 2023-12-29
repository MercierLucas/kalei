from scipy.spatial.transform import Rotation

import dearpygui.dearpygui as dpg
import cv2 as cv
import numpy as np
from typing import List

from src.object3d import Object
from src.utils import load_config, FPSCounter
from src.events import event_manager, Events

WIDTH, HEIGHT = 800, 600


def create_fixed_windows_parameters(height:int, width:int, pos=None):
    fixed_windows_parameters = {
        'autosize': False,
        'no_resize': True,
        # 'no_title_bar': True,
        'no_move': True,
        'no_scrollbar': True,
        'no_collapse': True,
        'horizontal_scrollbar': False,
        'no_focus_on_appearing': True,
        'no_bring_to_front_on_focus': True,
        'no_close': True,
        'min_size': (width, height),
        'max_size': (width, height),
        'width': width,
        'height': height,
    }
    if pos is not None:
        fixed_windows_parameters["pos"] = pos
    return fixed_windows_parameters


def frame_to_dpg(frame):
    frame = np.flip(frame, 2)  # BGR to RGB
    frame = frame.ravel()  # flatten camera data to a 1 d stricture
    frame = np.asfarray(frame, dtype='f')  # change data type to 32bit floats
    data = np.true_divide(frame, 255.0)  # normalize image data to prepare for GPU
    return data


class MainWindow:
    def __init__(self, config:dict) -> None:
        h, w = config["height"], config["width"]  
        total_width = sum(config[w] for w in ["left_panel_width", "width", "right_panel_width"])
        self.config = config
        dpg.create_context()
        dpg.create_viewport(title='3D Viewer', width=total_width, height=h+50)
        dpg.setup_dearpygui()

        event_manager.register(Events.ON_OBJECTS_UPDATE, self.update_objects_infos)
        event_manager.register(Events.ON_CAMERA_UPDATED, self.camera_update)
        event_manager.register(Events.ON_OBJECT_SELECTED, self.object_selected)
        event_manager.register(Events.ON_OBJECT_ADDED_TO_SCENE, self.objects_added_to_scene)
        # self.config_main_window = main_window_parameters
        # self.set_window_size(h, w)

    def objects_added_to_scene(self, objects:List[Object]):
        dpg.configure_item("scene_objects", items=[o.name for o in objects])


    def camera_update(self, transform_matrix):
        x, y, z = transform_matrix[:3, 3]
        rot = Rotation.from_matrix(transform_matrix[:3, :3])
        alpha, beta, gamma = rot.as_euler("xyz", degrees=True)
        dpg.set_value("camera_transform_position", f"X:{x:.2f}  Y:{y:.2f}  Z:{z:.2f}")
        dpg.set_value("camera_transform_rotation", f"X:{alpha:.2f}  Y:{beta:.2f}  Z:{gamma:.2f}")


    def object_selected(self, obj:Object):
        dpg.set_value("selected_object_name", f"Name: {obj.name}")
        dpg.set_value("selected_object_num_vertices", f"Num vertices: {len(obj.vertices)}")
        dpg.set_value("selected_object_num_edges", f"Num edges: {len(obj.edges)}")
        # dpg.set_value("camera_transform", f"X:{x:.2f}  Y:{y:.2f}  Z:{z:.2f}")

    
    def update_objects_infos(self, objects:dict):
        # print(objects)
        pass
    

    def set_window_size(self, height:int, width:int):
        self.config_main_window["width"] = width
        self.config_main_window["height"] = height
        self.config_main_window["min_size"] = (width, height)
        self.config_main_window["max_size"] = (width, height)

    
    def setup_window(self, frame:np.ndarray):
        curr_x = 0
        frame_data = frame_to_dpg(frame)
        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(frame.shape[1], frame.shape[0],
                                frame_data, tag="3dscene", format=dpg.mvFormat_Float_rgb)
            
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open")    
            dpg.add_menu_item(label="Help", callback=lambda : print("Help"))

            with dpg.menu(label="Add object"):
                dpg.add_menu_item(
                    label="Sample cube",
                    callback=lambda : event_manager.trigger(Events.ON_ADD_SAMPLE_OBJECT, "cube")
                )    


        objects_list_parameters = create_fixed_windows_parameters(self.config["height"], self.config["left_panel_width"])
        curr_x += self.config["left_panel_width"]
        with dpg.window(label="Scene objects", **objects_list_parameters):
            # 
            dpg.add_text("Camera", label="Camera")
            dpg.add_text("Position", label="camera_position")
            dpg.add_text(f"X:{0.0:.2f}  Y:{0.0:.2f}  Z:{0.0:.2f}", label="camera_transform_position", tag="camera_transform_position")
            dpg.add_text("Rotation", label="camera_rotation")
            dpg.add_text(f"X:{0.0:.2f}  Y:{0.0:.2f}  Z:{0.0:.2f}", label="camera_transform_rotation", tag="camera_transform_rotation")

            dpg.add_text("Objects")
            dpg.add_listbox(items=[], tag="scene_objects")

        scene_parameters = create_fixed_windows_parameters(self.config["height"], self.config["width"], pos=(curr_x, 0))
        curr_x += self.config["width"]

        with dpg.window(label="Scene", **scene_parameters):
            dpg.add_image("3dscene")

        inspector_parameters = create_fixed_windows_parameters(
            self.config["height"], self.config["right_panel_width"],
            pos=(curr_x, 0)
            )
        with dpg.window(label="Inspector", **inspector_parameters):
            dpg.add_text("Selected object", label="selected_object")
            
            dpg.add_text("[None]", label="selected_object_name", tag="selected_object_name")
            dpg.add_text("[None]", label="selected_object_num_vertices", tag="selected_object_num_vertices")
            dpg.add_text("[None]", label="selected_object_num_edges", tag="selected_object_num_edges")
            dpg.add_text("Position")
            dpg.add_text(f"X:{0.0:.2f}  Y:{0.0:.2f}  Z:{0.0:.2f}", label="selected_object_position", tag="selected_object_position")

        dpg.show_viewport()

        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Z, callback=lambda: event_manager.trigger(Events.ON_MOVE_CAMERA, 1))
            dpg.add_key_press_handler(dpg.mvKey_S, callback=lambda: event_manager.trigger(Events.ON_MOVE_CAMERA, -1))

    
    def update_scene(self, frame:np.ndarray):
        frame_data = frame_to_dpg(frame)
        dpg.set_value("3dscene", frame_data)
        dpg.render_dearpygui_frame()
    

    def scene_loop(self, render_func):
        ellapsed = 0
        counter = FPSCounter()
        while dpg.is_dearpygui_running():
            frame_data = render_func(ellapsed)
            frame_data = frame_to_dpg(frame_data)
            dpg.set_value("3dscene", frame_data)
            dpg.render_dearpygui_frame()
            fps, eps = counter.tick()
            # print(f"{fps:.2f}")
            ellapsed += eps

        dpg.destroy_context()



if __name__ == "__main__":
    dummy_frame = np.zeros((400, 400, 3))
    win = MainWindow(load_config())
    win.setup_window(dummy_frame)
    win.run(dummy_frame)