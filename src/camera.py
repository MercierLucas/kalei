import numpy as np

from src.transforms import translate

from src.events import event_manager, Events


class Camera:
    TRANSLATION_SPEED = .1

    def __init__(self, target=None, width=800, height=600) -> None:
        self.zoom = 1
        self.position = np.array([0, 0, -30])
        self.height = height
        self.width = width
        self.lookat = self.create_lookat_matrix()
        self.proj = self.create_proj()
        self.screen_mat = self.create_screen_matrix()
        event_manager.register(Events.ON_MOVE_CAMERA, self.translate_camera)

    
    def translate_camera(self, direction):
        direction = np.array([0, 0, direction])
        self.position += direction# * self.TRANSLATION_SPEED
        self.lookat = self.create_lookat_matrix()
        event_manager.trigger(Events.ON_CAMERA_UPDATED, self.lookat)

    
    def create_lookat_matrix(self, target=None):
        if target is None:
            target = np.zeros(3) # origin
        z = (self.position - target) / np.linalg.norm(self.position - target)
        y_world = np.array([0, 1, 0])
        x = np.cross(y_world, z)
        y = np.cross(z, x)

        mat = np.eye(4)
        rot = np.array([x, y, z]).T
        mat[:3, :3] = rot
        mat[:3, 3] = - self.position #np.dot(rot, self.position)
        mat[3, 3] = 1
        return mat


    def create_screen_matrix(self):
        mat = np.eye(4)
        mat[0, 0] = self.width // 2
        mat[1, 1] = -self.height // 2
        mat[3, 0] = self.width // 2
        mat[3, 1] = self.height // 2
        return mat


    def create_proj(self, znear=0.1, zfar=1000, h_fov=90):
        mat = np.zeros((4, 4))
        ratio = self.height / self.width
        inv_fov = 1 / np.tan(np.deg2rad(h_fov) / 2)
        mat[0, 0] = ratio * inv_fov
        mat[1, 1] = inv_fov
        mat[2, 2] = zfar / (zfar - znear)
        mat[2, 3] = 1
        mat[3, 2] = (-zfar * znear) / (zfar-znear)
        return mat
    

    def viewport_transform(self, point):
        """Scale [-1, 1] normalized device coordinates (NDC) back
        to [0, width] and [0, height] (screen space)"""
        u, v = point[:2] + 1 # [-1, 1] -> [0, 2]
        u *= .5 * self.width
        v *= .5 * self.height
        return np.array([u, v])


    def get_projection(self, points):
        proj_points = np.zeros((points.shape[0], 2))
        for idx, p in enumerate(points):
            # p = translate(p, 0, 0, 15)
            p = self.lookat @ p
            p = self.proj @ p
            if p[-1] != 0:
                p /= p[-1] # x/w y/w z/w
            p = self.viewport_transform(p)
            # p[(p < -1 ) | (p > 1 )] = 0
            # p = self.screen_mat @ p
            proj_points[idx] = p
        # proj_points[:, 0] *= 800
        # print(proj_points)
        # proj_points[:, 1] *= 600
        return proj_points