import cv2
import time
import numpy as np
import glm
from src.enums import Colors
from data import mock_data, mock_data_cube2

from src.app import App

LOGTIME = False

# def timer(func):
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         res = func(*args, **kwargs)
#         total = time.time() - start
#         if LOGTIME:
#             print(f"{func.__name__} [{total*1000:.6f}ms]")
#         return res
#     return wrapper





# def show_fps(frame, fps):
#     cv2.putText(frame, f"{fps:.2f}fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
#         1, (0, 255, 0), 1, 1)


# def draw_point(frame, point, color= Colors.DARK_GREEN):
#     cv2.circle(frame, (int(point[0]), int(point[1])), 4, color.value, -1)


# def draw_line(frame, p1, p2, color= Colors.LIGHT_GREEN):
#     x1, y1 = p1
#     x2, y2 = p2
#     cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), color.value, 2)

# @timer
# def draw(frame, points, camera:Camera, connections = None):

#     proj_points = camera.get_projection(points)
   
#     if connections:
#         for p1, p2 in connections:
#             draw_line(frame, proj_points[p1], proj_points[p2])

#     for x, y in proj_points:
#         draw_point(frame, [x, y], Colors.CYAN)
    


# def get_fps(curr_time, last_time):
#     try:
#         fps = 1 / (curr_time - last_time)
#         return fps
#     except ZeroDivisionError:
#         return 0


# def main():
#     w, h = 800, 600
#     base_frame = np.zeros((h, w, 3))
#     show = True
#     key = None
#     last_time = time.time()
#     target_fps = 1000
#     delay = int(1/target_fps*1000)
#     points, connections = mock_data_cube2()
#     camera = Camera(width=w, height=h)

#     ellasped = 0

#     while show:
#         frame = base_frame.copy()
#         if key == ord("q"):
#             show = False
#         if key == ord("a"):
#             camera.zoom *= 1.1
#         if key == ord("e"):
#             camera.zoom /= 1.1
#         curr_time = time.time()
#         fps = get_fps(curr_time, last_time)
#         # print(fps)

#         ellasped += (curr_time - last_time)
#         # print(ellasped)
#         # Transforms
#         transformed_points = np.array([rotate_x(p, ellasped*np.pi/10) for p in points])
#         transformed_points = np.array([rotate_y(p, ellasped*np.pi/10) for p in transformed_points])

#         # Draw
#         draw(frame, transformed_points, camera, connections)
#         last_time = curr_time
#         show_fps(frame, fps)
#         cv2.imshow("3D Viewer", frame)
#         key = cv2.waitKey(delay)
#     cv2.destroyAllWindows()


def main():
    application = App()
    application.run()


if __name__ == "__main__":
    main()