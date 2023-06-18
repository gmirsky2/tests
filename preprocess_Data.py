# Import necessary libraries
from utils import frame_dir, os, cv2, np

# Set the directory where the images are stored
frame_dir = "Temp\images"

# Get the list of image filenames
image_filenames = os.listdir(frame_dir)

# Preprocess the images
preprocessed_images = []
for image_filename in image_filenames:
    # Load the image
    image = cv2.imread(os.path.join(frame_dir, image_filename))

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize the image to a standard size
    resized_image = cv2.resize(gray_image, (224, 224))

    # Normalize the image
    normalized_image = resized_image / 255.0

    # Add the preprocessed image to the list
    preprocessed_images.append(normalized_image)

# Convert the list of images to a NumPy array
preprocessed_images = np.array(preprocessed_images)
