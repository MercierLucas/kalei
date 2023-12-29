import numpy as np
from typing import List

from src.object3d import Object
from src.events import event_manager, Events


def mock_data_cube():
    data =  np.array([
        [0, 0, 0, 1], # front-bottom-left
        [1, 0, 0, 1], # front-bottom-right
        [0, 1, 0, 1], # front-up-left
        [1, 1, 0, 1], # front-up-right

        [0, 0, 1, 1], # back-bottom-left
        [1, 0, 1, 1], # back-bottom-right
        [0, 1, 1, 1], # back-up-left
        [1, 1, 1, 1], # back-up-right
    ])
    connections = [
        (0, 1), (0, 2), (1, 3), (2, 3),
        (0, 4), (1, 5), (2, 6), (3, 7),
        (4, 6), (4, 5), (5, 7), (6, 7),
    ]
    return data, connections



class Scene:
    def __init__(self) -> None:
        self.objects:List[Object] = []
        # self.add_sample_object("cube")
        vertices, edges = mock_data_cube()
        obj = Object(vertices, edges, "Cube")
        self.objects.append(obj)
        event_manager.register(Events.ON_ADD_SAMPLE_OBJECT, self.add_sample_object)

    
    def add_sample_object(self, object_type:str):
        if object_type == "cube":
            vertices, edges = mock_data_cube()
            wp = np.random.random(3) > 1
            obj = Object(vertices, edges, "Cube")
            self.objects.append(obj)
            event_manager.trigger(Events.ON_OBJECT_ADDED_TO_SCENE, self.objects)


    


