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
        # Use edge detection to identify the boundaries of the game screen
        edges = cv2.Canny(frame, 100, 200)
        
        # Use contour detection to identify the position of the player character
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        player_contour = max(contours, key=cv2.contourArea)
        
        # Use object recognition to identify obstacles in the game
        obstacle_classifier = cv2.CascadeClassifier('obstacle_classifier.xml')
        obstacles = obstacle_classifier.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
        
        # Use the frame counter as the label for the image
        label = str(frame_counter)
        output_filename = frame_dir + output_prefix + label + ".jpg"
        
        # Draw the player and obstacles on the frame
        for (x, y, w, h) in obstacles:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.drawContours(frame, [player_contour], -1, (0, 255, 0), 2)
        
        # Save the frame as an image file
        cv2.imwrite(output_filename, frame)
        frame_counter += 1
        progress_bar.update(1)
    else:
        break
    
# Close the progress bar
progress_bar.close()

# Release the video capture object
cap.release()
