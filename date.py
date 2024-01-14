import cv2
import os
import time
import uuid

# Configuration
BASE_PATH = 'F:\hand-gesture-recognition-code/Tensorflow/workspace/images/collectedimages'
labels = ['Yo', 'Kachaw', 'Rocking', 'Kon', 'Aon']
interval_seconds = 5  # Set the interval for capturing images

# Create the base image directory if it doesn't exist
os.makedirs(BASE_PATH, exist_ok=True)
print(f"Base image directory created: {BASE_PATH}")

# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Webcam not found.")
    exit()

try:
    while True:
        # Prompt user to select a label
        print("Select a label:")
        for i, label in enumerate(labels, start=1):
            print(f"{i}. {label}")

        choice = input("Enter the number corresponding to the label: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(labels):
                selected_label = labels[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Create subdirectory for the selected label
    label_path = os.path.join(BASE_PATH, selected_label)
    os.makedirs(label_path, exist_ok=True)
    print(f"Image directory for {selected_label} created: {label_path}")

    image_number = 1

    while True:
        # Capture frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Generate a unique image name using label and image number
        image_name = os.path.join(label_path, '{}.jpg'.format(str(uuid.uuid1())))
        print(f"Saving image to: {image_name}")

        # Save the captured frame as an image
        cv2.imwrite(image_name, frame)

        # Display the captured frame
        cv2.imshow('frame', frame)

        # Increment image number
        image_number += 1

        # Wait for the specified interval in milliseconds
        key = cv2.waitKey(int(interval_seconds * 1000))

        # Break the loop if 'q' key is pressed
        if key & 0xFF == ord('q'):
            break

finally:
    # Release the webcam
    cap.release()
    # Destroy OpenCV window
    cv2.destroyAllWindows()
