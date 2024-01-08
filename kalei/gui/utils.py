import numpy as np


def frame_to_dpg(frame):
    # frame = np.flip(frame, 2)  # BGR to RGB
    frame = frame.ravel()  # flatten camera data to a 1 d stricture
    frame = np.asfarray(frame, dtype='f')  # change data type to 32bit floats
    data = np.true_divide(frame, 255.0)  # normalize image data to prepare for GPU
    return data


def create_fixed_windows_parameters(height:int, width:int, pos=None) -> dict:
    fixed_windows_parameters = {
        'autosize': False,
        'no_resize': True,
        # 'no_title_bar': True,
        'no_move': True,
        'no_scrollbar': True,
        'no_collapse': True,
        'horizontal_scrollbar': False,
        'no_focus_on_appearing': True,
        'no_bring_to_front_on_focus': True,
        'no_close': True,
        'min_size': (width, height),
        'max_size': (width, height),
        'width': width,
        'height': height,
    }
    if pos is not None:
        fixed_windows_parameters["pos"] = pos
    return fixed_windows_parameters