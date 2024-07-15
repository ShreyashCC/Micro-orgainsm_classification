from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
MODEL_PATH = "../models/My_model.keras"
CLASS_NAMES = ["Amoeba", "Euglena", "Hydra", "Paramecium", "Rod_bacteria", "Spherical_bacteria", "Spiral_bacteria", "Yeast"]

try:
    MODEL = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    logging.error(f"Error loading model: {e}")
    MODEL = None

def read_file_as_image(data) -> np.ndarray:
    try:
        image = np.array(Image.open(BytesIO(data)))
        return image
    except Exception as e:
        logging.error(f"Error reading image file: {e}")
        raise e

@app.get("/ping")
async def ping():
    return "hello I am alive"

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        data = await file.read()
        image = read_file_as_image(data)
        image = tf.image.resize(image, [256, 256])
        img_batch = np.expand_dims(image, 0)

        predictions = MODEL.predict(img_batch)
        index = np.argmax(predictions[0])
        predicted_class = CLASS_NAMES[index]

        confidence = np.max(predictions[0])

        return {
            'class': predicted_class,
            'confidence': float(confidence)
        }
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    try:
        with open("index.html") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        logging.error(f"Error serving frontend: {e}")
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000, log_level="debug")
