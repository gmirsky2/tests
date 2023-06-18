# Import the necessary libraries
from utils import image_filenames, frame_dir, os, cv2, np, contours_dir, edges_dir, video_fps, video_dir, video_width, video_height, fourcc, tqdm

# Define a function to apply Canny edge detection to an image and return the resulting edge image
def detect_edges(image):
    """Applies Canny edge detection to the input image and returns the resulting edge image."""
    # Convert the image to grayscale
    if image is None or image.size == 0:
        print("Error: Image file not found or invalid image data")
        return
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 100)

    # Dilate the edges to close small gaps
    kernel = np.ones((3,3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # Fill small holes in the edges
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Return the edge image
    return edges

# Create a VideoWriter object to write the contours and edges video
contours_video_path = os.path.join(video_dir, "contours.avi")
contours_video_writer = cv2.VideoWriter(contours_video_path, fourcc, video_fps, (video_width, video_height))

edges_video_path = os.path.join(video_dir, "edges.avi")
edges_video_writer = cv2.VideoWriter(edges_video_path, fourcc, video_fps, (video_width, video_height))

print("|   Make Contours/Edges    |")
for image_filename in tqdm(image_filenames):
    # Construct the full image path
    image_path = os.path.join(frame_dir, image_filename)

    # Check if the image file exists
    if not os.path.isfile(image_path):
        print("Error: Image file not found:", image_path)
        continue

    # Load the image and detect the edges
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not read image file:", image_path)
        continue
    edges = detect_edges(image)
    if edges is None:
        print("Error: Could not detect edges in image")
        continue

    # Extract the contours from the edge image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original image
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    
    # Save the edge image to a file
    cv2.imwrite(os.path.join(edges_dir, "edges_{}".format(image_filename)), edges)

    # Save the contours image to a file
    cv2.imwrite(os.path.join(contours_dir, "contours_{}".format(image_filename)), image)
    contours_video_writer.write(image)