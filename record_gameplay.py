# Import necessary libraries from the utils file
from utils import (
    cv2, keyboard, time, os,
    image_dir, video_dir, fourcc, video_width, video_height, video_fps,
    )

def record_gameplay(filename, key_presses_file):
    # Set the file name for the recorded video
    #filename = r"Zeepkist\Temp\videos\gameplay.avi"
    #key_presses_file = r"Zeepkist\Temp\key_presses.txt"


    print("Initialize the video capture object")
    # Initialize the video capture object
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, video_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height)

    # Create the video writer object using the properties from the utils file
    out = cv2.VideoWriter(filename, fourcc, video_fps, (video_width, video_height))

    # Initialize a list to store the key press data
    key_presses = []

    # Define a function to handle key press events
    def on_press(key):
        # Get the current time
        current_time = time.time()
        # Add the key press data to the list
        key_presses.append((key, 'down', current_time))

    # Define a function to handle key release events
    def on_release(key):
        # Get the current time
        current_time = time.time()
        # Add the key release data to the list
        key_presses.append((key, 'up', current_time))

    # Create a keyboard listener to capture the key events
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Record the video
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
            cv2.imshow('frame',frame)
            # Check if the 'q' key has been pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Stop the keyboard listener
    listener.stop()

    # Release the video capture and writer objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Print the key press data
    for key, state, timestamp in key_presses:
        print(key, state, timestamp)

    # Save the key press data and timestamps to a file
    with open(key_presses_file, 'w') as f:
        for key, state, timestamp in key_presses:
            f.write(str(key) + ' ' + state + ' ' + str(timestamp) + '\n')

