import numpy as np
import cv2
import mediapipe as mp
from PIL import Image
import io

# Initialize MediaPipe Hands once outside the loop for efficiency
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'space']

def crop_hand(image_data, padding=150):
    """Crop the hand region from an image using MediaPipe Hands."""
    image = Image.open(io.BytesIO(image_data))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(image)
    if not results.multi_hand_landmarks:
        return image  # Return the original image if no hands are detected

    landmarks = results.multi_hand_landmarks[0].landmark
    image_height, image_width, _ = image.shape
    x_min, x_max, y_min, y_max = image_width, 0, image_height, 0

    for landmark in landmarks:
        x, y = landmark.x, landmark.y
        x_pixel, y_pixel = int(x * image_width), int(y * image_height)
        x_min, x_max = min(x_min, x_pixel), max(x_max, x_pixel)
        y_min, y_max = min(y_min, y_pixel), max(y_max, y_pixel)

    x_min = max(0, x_min - padding)
    x_max = min(image_width, x_max + padding)
    y_min = max(0, y_min - padding)
    y_max = min(image_height, y_max + padding)

    return image[y_min:y_max, x_min:x_max]

def preprocess_image(image_data, padding=150):
    """Preprocess image for model input."""
    hand_image = crop_hand(image_data, padding)
    resized_hand_image = cv2.resize(hand_image, (128, 128))
    resized_hand_image = np.expand_dims(resized_hand_image, axis=0)  # Add batch dimension
    return resized_hand_image

def predict_image(image_data, model, class_names, padding=150):
    """Evaluate the model on a folder of images."""
    images = preprocess_image(image_data, padding)

    # Batch the data for better performance
    batch_size = 1
    images_tensor = tf.convert_to_tensor(images, dtype=tf.float32)

    # Make predictions in batches
    predictions = model.predict(images_tensor, batch_size=batch_size)
    predicted_labels = np.argmax(predictions, axis=1)

    return class_names[predicted_labels[0]]