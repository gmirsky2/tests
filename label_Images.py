# Import necessary libraries
from utils import labels, frame_dir, os, cv2, image_filenames, tqdm, video_dir, video_width, video_height, video_fps

def label_images():
    # Create a dictionary to store the count for each label
    label_count = {
        1: 0,
        0: 0,
        2: 0,
        3: 0,
        -1: 0
    }

    # Set the total number of iterations
    total = len(image_filenames)
    print("+" + "-" * 26 + "+")
    print("|      Defining Moves      |")
    print("+" + "-" * 26 + "+")
    from check_Moves import check_for_good_move, check_for_bad_move, check_for_win, check_for_fail

    print("|       Label Images       |")
    # Initialize the progress bar
    progress_bar = tqdm(total=total)
    # Loop through the image filenames
    labels = []
    for image_filename in image_filenames:
        # Load the image file
        image = cv2.imread(os.path.join(frame_dir, image_filename))

        # Define the criteria for a good move
        good_move = check_for_good_move(image)

        # Define the criteria for a bad move
        bad_move = check_for_bad_move(image)

        # Define the criteria for a win
        win = check_for_win(image)

        # Define the criteria for a fail
        fail = check_for_fail(image)

        # Assign a label to the image based on the criteria
        if good_move:
            label = 1
        elif bad_move:
            label = 0
        elif win:
            label = 2
        elif fail:
            label = 3
        else:
            label = -1
        labels.append(label)
        # Increment the count for the label in the dictionary
        label_count[label] += 1
        # Update the progress bar
        progress_bar.update(1)
    # Close the progress bar
    progress_bar.close()
    print("+" + "-" * 26 + "+")

    #Print the count for each label
    print("\n" + "+" + "-" * 27 + "+")
    print("| Good move count: {:<8} |".format(label_count[1]))
    print("| Bad move count:  {:<8} |".format(label_count[0]))
    print("| Win count:       {:<8} |".format(label_count[2]))
    print("| Fail count:      {:<8} |".format(label_count[3]))
    print("| Other count:     {:<8} |".format(label_count[-1]))
    print("+" + "-" * 27 + "+")