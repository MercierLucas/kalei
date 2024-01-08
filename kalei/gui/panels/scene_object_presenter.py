from scipy.spatial.transform import Rotation
from typing import List

from kalei.events import event_manager, Events
from kalei.engine import Object

from .scene_object_ui import SceneObjectsPanel


class SceneObjectPresenter:
    def __init__(self, config:dict, pos_x:int, pos_y:int) -> None:
        self.panel = SceneObjectsPanel(config)
        self.panel.init_ui(pos_x, pos_y)

        event_manager.register(Events.ON_OBJECT_ADDED_TO_SCENE, self.objects_added_to_scene)
        event_manager.register(Events.ON_CAMERA_UPDATED, self.camera_update)


    def objects_added_to_scene(self, objects:List[Object]):
        self.panel.objects_added_to_scene([o.name for o in objects])


    def camera_update(self, transform_matrix):
        x, y, z = transform_matrix[:3, 3]
        rot = Rotation.from_matrix(transform_matrix[:3, :3])
        alpha, beta, gamma = rot.as_euler("xyz", degrees=True)
        self.panel.update_camera_transform(x, y, z, alpha, beta, gamma)