import cv2
import numpy as np
from scipy.spatial.transform import Rotation

from kalei.engine import Camera, Scene, Object
from kalei.engine.transforms import rotate_x, rotate_y
from kalei.events import event_manager, Events
from kalei.enums import Colors



def draw_point(frame, point, color= Colors.DARK_GREEN):
    cv2.circle(frame, (int(point[0]), int(point[1])), 4, color.value, -1)


def draw_line(frame, p1, p2, color= Colors.LIGHT_GREEN):
    x1, y1 = p1
    x2, y2 = p2
    cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), color.value, 2)



class OpenCVRenderer:

    def __init__(self, camera:Camera, scene:Scene) -> None:
        self.camera = camera
        self.scene = scene
        self.background_frame = np.ones((camera.height, camera.width, 3)) * Colors.LIGHT_GREY.value# black frame


    def after_init(self):
        event_manager.trigger(Events.ON_CAMERA_UPDATED, self.camera.lookat)
        event_manager.trigger(Events.ON_OBJECT_SELECTED, self.scene.objects[0])
        event_manager.trigger(Events.ON_OBJECT_ADDED_TO_SCENE, self.scene.objects)


    def rotate(self, points, ellapsed):
        transformed_points = np.array([rotate_x(p, ellapsed*np.pi/10) for p in points])
        transformed_points = np.array([rotate_y(p, ellapsed*np.pi/10) for p in transformed_points])
        return transformed_points
    

    def mock_transforms(self, obj:Object, ellapsed:float):
        rotmat = obj.transform_matrix[:3, :3]
        rotmat = Rotation.from_matrix(rotmat)
        x, y, z = rotmat.as_euler("xyz", degrees=False)
        # y = ellapsed * np.pi/10000
        rotmat = Rotation.from_euler("xyz", np.array([x, y, z]))
        obj.transform_matrix[:3, :3] = rotmat.as_matrix().T

        x, y, z = Rotation.from_matrix(rotmat.as_matrix()).as_euler("xyz", degrees=True)
        # print(np.rad2deg([x, y, z]))

        new_points = np.zeros_like(obj.vertices)
        for idx, p in enumerate(obj.vertices):
            p = obj.transform_matrix @ p
            new_points[idx] = p
        return new_points



    def render(self, ellapsed:float):
        frame = self.background_frame.copy()

        objects = {}

        for idx, obj in enumerate(self.scene.objects):
            obj_name = obj.name if obj.name else f"Unamed_object_{idx}"

            local_axis = np.eye(4)

            vertices, edges = obj.vertices, obj.edges

            points = self.mock_transforms(obj, ellapsed)

            # points = self.rotate(vertices, ellapsed)
            objects[obj_name] = vertices

            proj_points = self.camera.get_projection(points)
            local_axis = self.camera.get_projection(local_axis)

            # Draw axis
            p1, p2, p3, origin = local_axis
            draw_line(frame, origin, p1, Colors.RED)
            draw_line(frame, origin, p2, Colors.DARK_GREEN)
            draw_line(frame, origin, p3, Colors.DARK_BLUE)
        
            if edges:
                for p1, p2 in edges:
                    draw_line(frame, proj_points[p1], proj_points[p2])

            for x, y in proj_points:
                draw_point(frame, [x, y], Colors.CYAN)
        
        event_manager.trigger(Events.ON_OBJECTS_UPDATE, objects)

        return frame