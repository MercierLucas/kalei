from scipy.spatial.transform import Rotation
from typing import List

from kalei.gui.windows import MainPresenter
from kalei.utils import load_config
from kalei.engine import Camera, Scene, Object
from kalei.renderer import OpenCVRenderer
from kalei.events import Events, event_manager



class App:
    """Listen for changes in logic (the engine) and updates the UI,
    and listen for inputs in UI to notify the engine."""
    def __init__(self) -> None:
        self.config = load_config()
        self.main_window = MainPresenter(self.config)
        camera = Camera(width=self.config["width"], height=self.config["height"])
        self.scene = Scene()
        self.renderer = OpenCVRenderer(camera, self.scene)
        # self.init_events()
        self.pause_scene = False
        self.renderer.after_init()


    # def init_events(self):
    #     event_manager.register(Events.ON_ADD_SAMPLE_OBJECT, self.add_sample_object)
    #     event_manager.register(Events.ON_OBJECTS_UPDATE, self.update_scene_objects_list)
    #     event_manager.register(Events.ON_CAMERA_UPDATED, self.camera_update)
    #     event_manager.register(Events.ON_OBJECT_SELECTED, self.object_selected)
    #     event_manager.register(Events.ON_OBJECT_ADDED_TO_SCENE, self.objects_added_to_scene)


    # def add_sample_object(self, object_type:str):
    #     self.scene.add_sample_object(object_type)
    #     self.objects_added_to_scene(self.scene.objects)

    
    # def objects_added_to_scene(self, objects:List[Object]):
    #     self.main_window.scene_obj_panel.objects_added_to_scene([o.name for o in objects])


    # def object_selected(self, obj:Object):
    #     self.main_window.inspector_panel.object_selected(obj)


    # def update_scene_objects_list(self, object):
    #     pass
    #     # self.main_window.update_objects_infos({})

    
    # def camera_update(self, transform_matrix):
    #     x, y, z = transform_matrix[:3, 3]
    #     rot = Rotation.from_matrix(transform_matrix[:3, :3])
    #     alpha, beta, gamma = rot.as_euler("xyz", degrees=True)
    #     self.main_window.scene_obj_panel.update_camera_transform(x, y, z, alpha, beta, gamma)

    
        


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
        self.main_window.start_main_loop(self.get_renderer_frame)
        # thread = threading.Thread(target=self.main_thread)
        # thread.daemon = True
        # thread.start()
    

