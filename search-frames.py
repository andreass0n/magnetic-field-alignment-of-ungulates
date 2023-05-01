import numpy as np
import cv2
import ipywidgets as widgets
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import display

postures = np.load('posture_data_utms/observation015-postures.npy')


# FRAME 1040 = 3:21:46 // 1040 frames = 34.6s // 3:21:46 - 34.6 // frame 0 = 2:46 // 015
# FRAME 190  = 2:53:63 // 190  frames = 6.3s  // 2:53:63 - 6.3s // frame 0 = 2:47 // 015

current_frame_index = 300
frame_jump = 10

def update_plot(frame_index):
    global current_frame_index
    current_frame_index = frame_index

    # Get the frame and corresponding animal positions
    frame = postures[:, frame_index]
    animal_positions = frame[:, :, :]

    # Clear the plot
    plt.clf()

    # Plot the animal positions
    for animal_index, positions in enumerate(animal_positions):
        x_coordinates = positions[:, 0]
        y_coordinates = positions[:, 1]
        plt.scatter(x_coordinates, y_coordinates, label=f"Animal {animal_index}", marker='o', s=4)

    # Display the current frame number
    plt.annotate(f"Frame: {frame_index}", xy=(0.02, 0.95), xycoords='axes fraction', fontsize=12)

    plt.legend(s=10)

def on_key(event):
    if event.key == 'right':
        step_forward(None)
    elif event.key == 'left':
        step_backward(None)

def step_forward(_):
    global frame_jump
    if current_frame_index < postures.shape[1] - 1:
        frame_slider.set_val(min(current_frame_index + frame_jump, postures.shape[1] - 1))

def step_backward(_):
    global frame_jump
    if current_frame_index > 0:
        frame_slider.set_val(max(current_frame_index - frame_jump, 0))

# Create a figure and axes for the plot
fig, ax = plt.subplots()

# Create the animation function
def animate(frame_index):
    update_plot(frame_index)
    plt.pause(0.001)

# Create a slider for manual frame navigation
frame_slider = plt.Slider(ax=plt.axes([0.2, 0.03, 0.6, 0.03]), label='Frame', valmin=0, valmax=postures.shape[1] - 1, valinit=0)
frame_slider.on_changed(animate)

# Connect keyboard events
fig.canvas.mpl_connect('key_press_event', on_key)

# Initialize the plot with the initial frame
update_plot(current_frame_index)

# Display the animation
plt.show()
