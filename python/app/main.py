# app/main.py

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import FastAPI, File, UploadFile, HTTPException
import tensorflow as tf
from .utils import predict_image, class_names
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
# model = tf.keras.models.load_model(MODEL_PATH)

# @app.post("/predict/")
# async def predict(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         result = predict_image(contents, model, class_names)
#         return {"result": result}
#     except ValueError as ve:
#         # No hand detected
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         # General exception
#         raise HTTPException(status_code=500, detail="Internal Server Error")


from fastapi import FastAPI, File, UploadFile, HTTPException
from .database import ImageDatabase

image_db = ImageDatabase()


@app.get("/images/{title}")
async def get_image(title: str):
    image = image_db.get_image(title)
    if image:
        return image
    raise HTTPException(status_code=404, detail="Image not found")

@app.post("/images/")
async def add_image(title: str, image_url: str):
    image_db.add_image(title, image_url)
    return {"message": "Image added successfully"}

@app.delete("/images/{title}")
async def delete_image(title: str):
    image = image_db.get_image(title)
    if image:
        image_db.delete_image(title)
        return {"message": "Image deleted successfully"}
    raise HTTPException(status_code=404, detail="Image not found")

@app.get("/images/")
async def search_images(query: str = ""):
    results = image_db.search_images(query)
    return [doc.to_dict() for doc in results]

@app.post("/populate-database/")
async def populate_database():
    image_db.populate_database()
    return {"message": "Database populated successfully"}
