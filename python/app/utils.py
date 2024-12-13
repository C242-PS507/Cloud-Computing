# app/utils.py

import numpy as np
import cv2
import mediapipe as mp
from PIL import Image
import io

# Initialize MediaPipe Hands once outside the loop for efficiency
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

class_names = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del',
    'nothing', 'space'
]

def crop_hand(image_data, padding=150):
    """Crop the hand region from an image using MediaPipe Hands."""
    # Read image data from bytes
    image = Image.open(io.BytesIO(image_data)).convert('RGB')
    image = np.array(image)
    image_rgb = image  # Image is already in RGB format

    # Process the image to detect hand landmarks
    results = hands.process(image_rgb)
    if not results.multi_hand_landmarks:
        # If no hands are detected, return None or handle accordingly
        return None

    # Extract landmarks and calculate bounding box
    landmarks = results.multi_hand_landmarks[0].landmark
    image_height, image_width, _ = image_rgb.shape
    x_min, x_max, y_min, y_max = image_width, 0, image_height, 0

    for landmark in landmarks:
        x, y = landmark.x, landmark.y
        x_pixel = int(x * image_width)
        y_pixel = int(y * image_height)
        x_min = min(x_min, x_pixel)
        x_max = max(x_max, x_pixel)
        y_min = min(y_min, y_pixel)
        y_max = max(y_max, y_pixel)

    x_min = max(0, x_min - padding)
    x_max = min(image_width, x_max + padding)
    y_min = max(0, y_min - padding)
    y_max = min(image_height, y_max + padding)

    # Crop the hand region
    cropped_image = image_rgb[y_min:y_max, x_min:x_max]
    return cropped_image

def preprocess_image(image_data, padding=150):
    """Preprocess image for model input."""
    hand_image = crop_hand(image_data, padding)
    if hand_image is None:
        # Handle the case where no hand is detected
        raise ValueError("No hand detected in the image.")

    # Resize and normalize the image
    resized_hand_image = cv2.resize(hand_image, (128, 128))
    resized_hand_image = resized_hand_image / 255.0  # Normalize to [0, 1]
    resized_hand_image = np.expand_dims(resized_hand_image, axis=0)  # Add batch dimension
    return resized_hand_image

def predict_image(image_data, model, class_names, padding=150):
    """Make a prediction on the image data."""
    images = preprocess_image(image_data, padding)

    # Make prediction
    predictions = model.predict(images)
    predicted_labels = np.argmax(predictions, axis=1)

    return class_names[predicted_labels[0]]