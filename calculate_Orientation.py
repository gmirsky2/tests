def calculate_orientation():
    from utils import (
    os, cv2, tqdm,
    contours_dir, left_count, right_count, other_count
    )
    print("+" + "-" * 26 + "+")
    print("| Calculating Orientation  |")
    print("+" + "-" * 26 + "+")
    # Loop through all of the contour images in the directory
    for contours_filename in tqdm(os.listdir(contours_dir)):
        # Load the contours of the player character
        contours_image = cv2.imread(os.path.join(contours_dir, contours_filename))

        # Extract the contours of the player character
        gray = cv2.cvtColor(contours_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            # Increment the "other" count
            other_count += 1
        else:
            # Calculate the orientation of the player character using image moments
            moments = cv2.moments(contours[0])
            if moments['m00'] == 0:
                # Increment the "other" count
                other_count += 1
            else:
                cx = int(moments['m10']/moments['m00'])
                cy = int(moments['m01']/moments['m00'])
                orientation = moments['mu11'] / moments['mu02']

                # Determine the label based on the orientation of the player character
                if orientation < 0:
                    left_count += 1
                elif orientation > 0:
                    right_count += 1
                else:
                    other_count += 1

    # Print the totals for each label
    print("\n" + "+" + "-" * 26 + "+")
    print("|    Orientation Totals    |")
    print("+" + "-" * 26 + "+")
    print("+" + "-" * 26 + "+")
    print(f'| Left count: {left_count}          |')
    print(f'| Right count: {right_count}         |')
    print(f'| Other count: {other_count}         |')
    print("+" + "-" * 26 + "+")
