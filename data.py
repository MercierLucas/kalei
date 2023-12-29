import numpy as np


def mock_data():
    return np.array([
        [0, 0, 0],
        [1, 1, 1],
        [20, 20, 20],
        [100, 100, 20],
    ])


def mock_data_cube2():
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


def mock_data_cube():
    return np.array([
        [0.5, 0.5, 0, 1],
        [0.5, -0.5, 0, 1],
        [-0.5, -0.5, 0, 1],
        [-0.5, 0.5, 0, 1],
    ])


def mock_data_skeleton() -> np.ndarray:
    return np.array([
        [-204.52339768, -501.50644147, 5338.20702051],
        [ -89.94705732, -520.16598099, 5382.00873327],
        [ -66.68852326,  -51.28206556, 5432.73565558],
        [ -22.06038522,  415.21045797, 5434.06356141],
        [-319.10005872, -482.84677178, 5294.40520373],
        [-333.42270017,  -12.49098762, 5333.48931062],
        [-322.93508027,  455.52108971, 5311.97088283]
    ])
