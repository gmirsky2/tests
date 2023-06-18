# Import necessary libraries
# Import the functions and variables from the utils module
from utils import (
    os,
    cv2,
    pyautogui,
    np,
    tqdm,
    time,
    contours_dir,
    edges_dir,
    frame_dir,
    image_dir,
    video_dir,
    labels,
    fourcc,
    video_width,
    video_height,
    video_fps,
    left_count,
    right_count,
    other_count,
    video_filename,
    key_presses_filename
)

# Import the functions from the other scripts
from record_gameplay import record_gameplay
from label_Images import label_images
from calculate_Orientation import calculate_orientation

def play_game():
    # Record the game and extract the frames
    record_gameplay(video_filename, key_presses_filename)

    # Label the images
    label_images()

    # Calculate the orientation of the player character
    orientation = calculate_orientation()

    # Press the key based on the orientation
    if orientation == "left":
        pyautogui.press("up")
    elif orientation == "right":
        pyautogui.press("up")

    # Sleep for one second before repeating the process
    time.sleep(1)

# Start the game
while True:
    play_game()