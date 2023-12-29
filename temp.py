import dearpygui.dearpygui as dpg
import cv2 as cv
import numpy as np

WIDTH, HEIGHT = 800, 600

config_main_window = {
    'autosize': False,
    'no_resize': True,
    'no_title_bar': True,
    'no_move': True,
    'no_scrollbar': True,
    'no_collapse': True,
    'horizontal_scrollbar': False,
    'no_focus_on_appearing': True,
    'no_bring_to_front_on_focus': False,
    'no_close': True,
    'show': True,
    'width': WIDTH,
    'height': HEIGHT,
    'no_background': False,
    'min_size': (WIDTH, HEIGHT),
    'max_size': (WIDTH, HEIGHT),
    'pos': (0, 0)
}


dpg.create_context()
dpg.create_viewport(title='Custom Title', width=WIDTH, height=HEIGHT)
dpg.setup_dearpygui()

vid = cv.VideoCapture(0)
ret, frame = vid.read()

# image size or you can get this from image shape
frame_width = vid.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = vid.get(cv.CAP_PROP_FRAME_HEIGHT)
video_fps = vid.get(cv.CAP_PROP_FPS)
print(frame_width)
print(frame_height)
print(video_fps)

print("Frame Array:")
print("Array is of type: ", type(frame))
print("No. of dimensions: ", frame.ndim)
print("Shape of array: ", frame.shape)
print("Size of array: ", frame.size)
print("Array stores elements of type: ", frame.dtype)
data = np.flip(frame, 2)  # because the camera data comes in as BGR and we need RGB
data = data.ravel()  # flatten camera data to a 1 d stricture
data = np.asfarray(data, dtype='f')  # change data type to 32bit floats
texture_data = np.true_divide(data, 255.0)  # normalize image data to prepare for GPU

print("texture_data Array:")
print("Array is of type: ", type(texture_data))
print("No. of dimensions: ", texture_data.ndim)
print("Shape of array: ", texture_data.shape)
print("Size of array: ", texture_data.size)
print("Array stores elements of type: ", texture_data.dtype)

with dpg.texture_registry(show=False):
    dpg.add_raw_texture(frame.shape[1], frame.shape[0], texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb)

with dpg.window(label="Main", **config_main_window):
    dpg.add_image("texture_tag")

# dpg.show_metrics()
dpg.show_viewport()
while dpg.is_dearpygui_running():

    # updating the texture in a while loop the frame rate will be limited to the camera frame rate.
    # commenting out the "ret, frame = vid.read()" line will show the full speed that operations and updating a texture can run at
    
    ret, frame = vid.read()
    data = np.flip(frame, 2)
    data = data.ravel()
    data = np.asfarray(data, dtype='f')
    texture_data = np.true_divide(data, 255.0)
    dpg.set_value("texture_tag", texture_data)

    # to compare to the base example in the open cv tutorials uncomment below
    # cv.imshow('frame', frame)
    dpg.render_dearpygui_frame()

vid.release()
#cv.destroyAllWindows() # when using upen cv window "imshow" call this also
dpg.destroy_context()