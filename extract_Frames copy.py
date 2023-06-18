# Import necessary libraries
from utils import frame_dir, cv2, tqdm, image_filenames, video_dir
# Set the file name for the recorded video
filename = "gameplay.avi"

# Set the total number of iterations
total = len(image_filenames)
# Initialize the progress bar
progress_bar = tqdm(total=total)

# Open the video file
cap = cv2.VideoCapture(video_dir + filename)

# Set the frame counter and the output file prefix
frame_counter = 0
output_prefix = "frame_"

# Extract the frames from the video and save them as separate image files
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # Use the frame counter as the label for the image
        label = str(frame_counter)
        output_filename = frame_dir + output_prefix + label + ".jpg"
        cv2.imwrite(output_filename, frame)
        frame_counter += 1
        progress_bar.update(1)
    else:
        break
    
# Close the progress bar
progress_bar.close()
# Release the video capture object
cap.release()
