# Import necessary libraries
import os
import cv2
import pyautogui
import numpy as np
import time
from tqdm import tqdm
from pynput import keyboard


# Set the directory where the images are stored
contours_dir = "Temp/images/contours"
edges_dir = "Temp/images/edges"
frame_dir = "Temp/images/frames/"
image_dir = "Temp/images/"
video_dir = "Temp/videos/"

# Set the label for each image
labels = []

# Get the list of image filenames
image_filenames = os.listdir(frame_dir)

# Set the file names for the recorded video and key press data
video_filename = os.path.join(video_dir, "gameplay.avi")
key_presses_filename = os.path.join(image_dir, "key_presses.txt")

# Set the output video properties
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_width = 640
video_height = 480
video_fps = 30

# Orientation
left_count = 0
right_count = 0
other_count = 0