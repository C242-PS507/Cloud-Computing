# app/main.py
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
from utils import preprocess_image
import numpy as np
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="My SunSign API",
    description="An API for My SunSign Apps",
    version="1.0.0"
)

# Get the model path from the environment variable
MODEL_PATH = os.getenv('MODEL_PATH', 'default_model_path')

# Load the model once at startup
model = tf.keras.models.load_model(MODEL_PATH)

# Define class names globally
class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
               'del', 'nothing', 'space']

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = preprocess_image(contents)
    predictions = model.predict(np.expand_dims(image, axis=0))
    predicted_label = np.argmax(predictions, axis=1)[0]
    result = class_names[predicted_label]
    return {"result": result}