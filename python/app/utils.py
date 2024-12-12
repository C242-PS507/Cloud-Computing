# app/utils.py
import numpy as np
import cv2
import mediapipe as mp
from PIL import Image
import io

# Initialize Mediapipe Hands once
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

def preprocess_image(image_data, padding=150):
    # Read image bytes and convert to NumPy array
    image = Image.open(io.BytesIO(image_data))
    image = np.array(image)

    # Convert image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if not results.multi_hand_landmarks:
        # If no hands are detected, return a blank image or raise an error
        resized_image = np.zeros((128, 128, 3))
    else:
        # Get hand landmarks and calculate bounding box
        landmarks = results.multi_hand_landmarks[0].landmark
        h, w, _ = image.shape
        x_min = min([lm.x for lm in landmarks]) * w - padding
        x_max = max([lm.x for lm in landmarks]) * w + padding
        y_min = min([lm.y for lm in landmarks]) * h - padding
        y_max = max([lm.y for lm in landmarks]) * h + padding

        # Ensure coordinates are within image bounds
        x_min = int(max(x_min, 0))
        x_max = int(min(x_max, w))
        y_min = int(max(y_min, 0))
        y_max = int(min(y_max, h))

        # Crop and resize the image
        cropped_image = image[y_min:y_max, x_min:x_max]
        resized_image = cv2.resize(cropped_image, (128, 128))
        resized_image = resized_image / 255.0  # Normalize

    return resized_image