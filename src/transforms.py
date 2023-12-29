import numpy as np


# @timer
def translate(point, tx, ty, tz):
    mat = np.eye(4)
    mat[:3, 3] = np.array([tx, ty, tz])
    mat[3, 3] = 1
    return mat @ point

# @timer
def rotate_x(point, theta):
    rotmat = np.eye(4)
    rotmat[1, 1] = np.cos(theta)
    rotmat[1, 2] = - np.sin(theta)
    rotmat[2, 1] = np.sin(theta)
    rotmat[2, 2] = np.cos(theta)
    return rotmat @ point

# @timer
def rotate_y(point, theta):
    rotmat = np.eye(4)
    rotmat[0, 0] = np.cos(theta)
    rotmat[0, 2] = np.sin(theta)
    rotmat[2, 0] = -np.sin(theta)
    rotmat[2, 2] = np.cos(theta)
    return rotmat @ point

