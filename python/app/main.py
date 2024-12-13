import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
from utils import predict_image, class_names
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

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    result = predict_image(contents, model, class_names)
    return {"result": result}