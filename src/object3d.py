import numpy as np

class Object:
    def __init__(self, vertices:np.ndarray, edges, name:str=None, world_position=None) -> None:
        self.name = name
        self.vertices = vertices
        self.edges = edges
        self.position = None
        self.rotation = None
        if world_position is None:
            world_position = np.array([0, 0, 0, 1])
        self.world_position = world_position

        self.transform_matrix = np.eye(4)
        self.transform_matrix[:, 3] = world_position
    
    