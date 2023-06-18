1. ✅ record_gameplay.py: This script captures the game as you play and saves the resulting video and keystokes to a file.

2. ✅ extract_frames.py: This script extracts the individual frames from the video file and saves them as separate image files.
    a. ✅ use edge detection to identify the boundaries of the game screen
    b. contour detection to identify the position of the player character
    c. object recognition to identify obstacles in the game

3. ✅ label_images.py: This script labels the images with the correct actions for the model to take.


4. ✅ preprocess_data.py: This script preprocesses the data by converting the images to grayscale, resizing them, and normalizing them.




5. split_data.py: This script splits the labeled data into a training set and a testing set.

6. choose_model.py: This script chooses a machine learning model and designs the architecture.

7. train_model.py: This script compiles and trains the model using the labeled training data.