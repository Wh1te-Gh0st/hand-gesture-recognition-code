# ... (existing imports and setup code)
# TechVidvan hand Gesture Recognizer

# import necessary packages

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import serial
import time
from tensorflow.keras.models import load_model

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)


# Initialize the webcam
cap = cv2.VideoCapture(0)

serial_port = serial.Serial('COM5', 115200, timeout=1)

def send_data(data):
    serial_port.write((data + '\n').encode())
    time.sleep(1)  # Allow time for ESP32 to process data
# Variable to track the current hand sign
current_hand_sign = None

while True:
    # Read each frame from the webcam
    _, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])
            classID = np.argmax(prediction)
            className = classNames[classID]

            # Check if the hand sign has changed
            if className != current_hand_sign:
            # Stop sending data when the hand sign changes
                print("Sent stop")

                current_hand_sign = className

                # Map hand signs to data to be sent
                sign_data_mapping = {
                    "rock": "A",
                    "ok": "B",
                    "peace": "C",
                    "thumbs up": "D",
                    "thumbs down": "E",
                    "stop": "F",
                    "fist": "G",
                    "smile": "H",
                # Add mappings for other signs
                }

                # Send data based on the current hand sign
                if current_hand_sign in sign_data_mapping:
                    send_data(sign_data_mapping[current_hand_sign])
                    time.sleep(1)
                    print(f"Sent data for {current_hand_sign}")


    # show the prediction on the frame
    cv2.putText(frame, current_hand_sign, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow("Output", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()

cv2.destroyAllWindows()