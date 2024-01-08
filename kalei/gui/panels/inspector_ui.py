import dearpygui.dearpygui as dpg

from kalei.engine import Object
from ..utils import create_fixed_windows_parameters


class InspectorPanel:
    def __init__(self, config:dict) -> None:
        self.config = config
        

    def init_ui(self, pos_x:int, pos_y:int):
        inspector_parameters = create_fixed_windows_parameters(
                self.config["height"], self.config["right_panel_width"],
                pos=(pos_x, pos_y)
                )
        with dpg.window(label="Inspector", **inspector_parameters):
            dpg.add_text("Selected object", label="selected_object")
            
            dpg.add_text("[None]", label="selected_object_name", tag="selected_object_name")
            dpg.add_text("[None]", label="selected_object_num_vertices", tag="selected_object_num_vertices")
            dpg.add_text("[None]", label="selected_object_num_edges", tag="selected_object_num_edges")
            dpg.add_text("Position")
            dpg.add_text(f"X:{0.0:.2f}  Y:{0.0:.2f}  Z:{0.0:.2f}", label="selected_object_position", tag="selected_object_position")


    def object_selected(self, obj:Object):
        dpg.set_value("selected_object_name", f"Name: {obj.name}")
        dpg.set_value("selected_object_num_vertices", f"Num vertices: {len(obj.vertices)}")
        dpg.set_value("selected_object_num_edges", f"Num edges: {len(obj.edges)}")

        x, y, z, _ = obj.world_position
        dpg.set_value("selected_object_position", f"X:{x:.2f}  Y:{y:.2f}  Z:{z:.2f}")