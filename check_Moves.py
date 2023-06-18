# Import necessary libraries
from utils import labels, image_dir, os, cv2, np
from edge_detection import detect_edges









def check_for_good_move(image):
    """Returns True if a good move is detected in the image, False otherwise."""
    # Detect edges in the image
    edges = detect_edges(image)

    # Calculate the average pixel value of the edges
    mean, _, _, _ = cv2.mean(edges)

    # Define a lower and upper threshold for the pixel values
    lower_threshold = 100
    upper_threshold = 200

    # Return True if the average pixel value is within the threshold range, False otherwise
    return lower_threshold <= mean <= upper_threshold














def check_for_bad_move(image):
    """Returns True if a bad move is detected in the image, False otherwise."""
    # Detect edges in the image
    edges = detect_edges(image)

    # Calculate the average pixel value of the edges
    mean, _, _, _ = cv2.mean(edges)

    # Define a lower and upper threshold for the pixel values
    lower_threshold = 0
    upper_threshold = 50

    # Return True if the average pixel value is outside of the threshold range, False otherwise
    return mean < lower_threshold or mean > upper_threshold












def check_for_win(image):
    """Returns True if a win is detected in the image, False otherwise."""
    # Detect edges in the image
    edges = detect_edges(image)
    
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper limits for the "green" color range
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])
    
    # Create a mask for the "green" color range
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Dilate the mask to increase the size of the green pixels
    kernel_size = 5
    mask = cv2.dilate(mask, np.ones((kernel_size, kernel_size), np.uint8))
    
    # Define the contour area threshold
    contour_area_threshold = 1000
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through the contours and check if the contour area is above the threshold
    for contour in contours:
        if cv2.contourArea(contour) > contour_area_threshold:
            return True
    
    # If no contour with area above the threshold was found, return False
    return False

    
    
    
    
    
    
    
    
    
def check_for_fail(image):
    """Returns True if a fail is detected in the image, False otherwise."""
    # Detect edges in the image
    edges = detect_edges(image)
    
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper limits for the "red" color range
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    
    # Create a mask for the "red" color range
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # Dilate the mask to increase the size of the red pixels
    kernel_size = 5
    mask = cv2.dilate(mask, np.ones((kernel_size, kernel_size), np.uint8))
    
    # Define the contour area threshold
    contour_area_threshold = 1000
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through the contours and check if the contour area is above the threshold
    for contour in contours:
        if cv2.contourArea(contour) > contour_area_threshold:
            return True
    
    # If no contour with area above the threshold was found, return False
    return False

